import argparse, datetime, json, os, sys
from typing import Dict, Any
from personas import PERSONAS, classify_persona, TEMPLATES
from nlp import detect_intent
from data_loader import load_customer_profile
from strategy_engine import recommend_next_action

LOG_DIR = "chat_logs"
os.makedirs(LOG_DIR, exist_ok=True)

def render(template: str, data: Dict[str, Any]) -> str:
    # Provide safe defaults for formatting variables
    safe = dict(data)
    safe.setdefault("name", safe.get("Name") or safe.get("NameFallback") or "Customer")
    safe.setdefault("outstanding", safe.get("Outstanding") or safe.get("LoanAmount") or 0)
    safe.setdefault("date", (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d"))
    try:
        return template.format(**safe)
    except Exception:
        return template

class Chatbot:
    def __init__(self, customer_id: int | None = None):
        self.profile = load_customer_profile(customer_id)
        self.name = self.profile.get("Name") or self.profile.get("NameFallback") or "Customer"
        self.persona_key = classify_persona(self.profile)
        self.persona = PERSONAS[self.persona_key]
        self.session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(LOG_DIR, f"{self.profile.get('CustomerID','unknown')}_{self.session_id}.jsonl")
        self._log_event({"type": "meta", "persona": self.persona_key, "profile": self.profile})

    def _log_event(self, obj: Dict[str, Any]):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    def system_greet(self) -> str:
        t = TEMPLATES["greeting"][self.persona_key]
        return render(t, self.profile)

    def respond(self, user_text: str) -> Dict[str, str]:
        intent = detect_intent(user_text)
        template = TEMPLATES.get(intent, TEMPLATES["unknown"])[self.persona_key]
        reply = render(template, self.profile)
        nba = recommend_next_action(self.persona_key, self.profile, intent)
        # Log turn
        self._log_event({"type": "turn", "user": user_text, "intent": intent, "reply": reply, "nba": nba})
        return {"reply": reply, "intent": intent, "next_best_action": nba}

def run_cli(customer_id: int | None):
    bot = Chatbot(customer_id)
    print(f"Persona detected: {bot.persona_key} ({bot.persona.tone}).")
    print(bot.system_greet())
    while True:
        try:
            user = input("You: ").strip()
        except EOFError:
            break
        if user.lower() in {"quit","exit","q"}:
            goodbye = render(TEMPLATES["goodbye"][bot.persona_key], bot.profile)
            print("Bot:", goodbye)
            bot._log_event({"type":"end"})
            break
        out = bot.respond(user)
        print("Bot:", out["reply"])
        print("[Next-best action]:", out["next_best_action"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Persona-based Loan Chatbot (CLI)")
    parser.add_argument("--customer-id", type=str, default=None, help="CustomerID to load from CSV")
    args = parser.parse_args()
    run_cli(args.customer_id)
