import re
from typing import Literal

Intent = Literal["greeting","ask_due","ask_amount","promise_pay","need_extension","hardship","dispute","connect_agent","goodbye","unknown"]

KEYWORDS = {
    "greeting": [r"\b(hi|hello|hey|good (morning|evening|afternoon))\b"],
    "ask_due": [r"\b(due|deadline|date|when|pending)\b"],
    "ask_amount": [r"\b(amount|balance|how much|outstanding|due amount)\b"],
    "promise_pay": [r"\b(promise|will pay|pay (by|on)|settle on)\b"],
    "need_extension": [r"\b(extension|extra time|grace|postpone|defer|push)\b"],
    "hardship": [r"\b(hardship|lost job|medical|emergency|cannot pay|financial issue)\b"],
    "dispute": [r"\b(dispute|wrong|incorrect|not mine|error|chargeback)\b"],
    "connect_agent": [r"\b(agent|human|representative|call me|talk to someone)\b"],
    "goodbye": [r"\b(bye|goodbye|thanks|thank you|see you)\b"],
}

def detect_intent(text: str) -> Intent:
    if not text:
        return "unknown"
    t = text.lower().strip()
    for intent, patterns in KEYWORDS.items():
        for p in patterns:
            if re.search(p, t):
                return intent  # first match wins
    return "unknown"
