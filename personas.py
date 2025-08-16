from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Persona:
    name: str
    tone: str
    style_notes: str

# Persona library with fixed tones
PERSONAS: Dict[str, Persona] = {
    "cooperative": Persona(
        name="cooperative",
        tone="empathetic",
        style_notes="Use warm, polite language and acknowledge customer efforts."
    ),
    "evasive": Persona(
        name="evasive",
        tone="assertive",
        style_notes="Be concise, firm, and focus on accountability and specific timelines."
    ),
    "aggressive": Persona(
        name="aggressive",
        tone="empathetic",
        style_notes="Stay calm and professional, acknowledge frustration, de-escalate the situation."
    ),
    "confused": Persona(
        name="confused",
        tone="informative",
        style_notes="Be patient, explain things step-by-step, simplify terms."
    ),
}

def classify_persona(profile: Dict[str, Any]) -> str:
    """
    Rule-based persona detection using:
      - SentimentScore (-1..1, negative -> aggressive/confused)
      - Complaints (count)
      - ResponseTimeHours (higher -> evasive)
      - InteractionAttempts (higher -> evasive)
      - MissedPayments (context)
    """
    s = profile.get("SentimentScore", 0)
    complaints = profile.get("Complaints", 0)
    rth = profile.get("ResponseTimeHours", 24)
    attempts = profile.get("InteractionAttempts", 0)
    missed = profile.get("MissedPayments", 0)

    try:
        s = float(s)
    except Exception:
        s = 0.0
    try:
        complaints = int(complaints)
    except Exception:
        complaints = 0
    try:
        rth = float(rth)
    except Exception:
        rth = 24.0
    try:
        attempts = int(attempts)
    except Exception:
        attempts = 0
    try:
        missed = int(missed)
    except Exception:
        missed = 0

    # Primary signals
    if complaints >= 2 and s <= -0.2:
        return "aggressive"
    if rth >= 48 and attempts >= 3:
        return "evasive"
    if -0.2 <= s <= 0.1 and missed >= 1:
        return "confused"
    if s >= 0.2 and rth <= 24:
        return "cooperative"

    # Fallbacks
    if missed >= 2:
        return "evasive"
    return "cooperative"

# Persona-aware response templates by intent
TEMPLATES = {
    "greeting": {
        "cooperative": "Hi {name}! Thanks for staying in touch. How can I assist you with your loan today?",
        "evasive": "Hello {name}. Please confirm your plan for the pending payment.",
        "aggressive": "Hello {name}. I hear your concerns—let’s resolve this together calmly.",
        "confused": "Hi {name}! I can help clarify your loan details. What would you like to understand first?"
    },
    "ask_due": {
        "cooperative": "Your next payment is pending. Would you like me to set a reminder or share steps to pay now?",
        "evasive": "Your payment is pending. Please confirm when you will complete it.",
        "aggressive": "Your payment shows as pending. I understand this may be stressful—shall I outline next steps?",
        "confused": "Your payment is pending. I can guide you step by step to complete it—shall we proceed?"
    },
    "ask_amount": {
        "cooperative": "Your current outstanding balance is ₹{outstanding:,.0f}. Would you like a payment link?",
        "evasive": "Outstanding balance: ₹{outstanding:,.0f}. Please confirm your payment date.",
        "aggressive": "Your outstanding balance is ₹{outstanding:,.0f}. I can share clear options to help you complete this.",
        "confused": "You currently owe ₹{outstanding:,.0f}. I can explain how this was calculated if you'd like."
    },
    "promise_pay": {
        "cooperative": "Thanks for the update! I’ll note your promise to pay on {date}. Need a reminder set?",
        "evasive": "Noted. Please complete payment by {date} and reply 'DONE' once finished.",
        "aggressive": "Appreciate the confirmation. Completing payment by {date} will help avoid further issues.",
        "confused": "Got it. You plan to pay on {date}. Would you like me to share the steps now so it's easy later?"
    },
    "need_extension": {
        "cooperative": "We can explore an extension or a flexible plan. Would a short grace period help?",
        "evasive": "We can review an extension after a concrete date. What new date works for you?",
        "aggressive": "We can consider an extension. Let’s review options that reduce stress while keeping you on track.",
        "confused": "Extensions are possible. I can explain the options simply—shall we walk through them?"
    },
    "hardship": {
        "cooperative": "I’m sorry you’re going through this. We can look at temporary relief or restructuring options.",
        "evasive": "Understood. Please share a brief note on your situation so we can evaluate relief options.",
        "aggressive": "I’m sorry this is difficult. We can discuss relief options respectfully and privately.",
        "confused": "Thanks for sharing. I can explain relief programs in simple steps—shall we start?"
    },
    "dispute": {
        "cooperative": "Thanks for raising this. I can log your dispute and share a reference number.",
        "evasive": "I can log your dispute now. Please confirm the specific charge or date in question.",
        "aggressive": "I understand your concern. I’ll register the dispute right away and share the reference.",
        "confused": "No problem—let’s document your dispute clearly. I’ll ask a few simple questions."
    },
    "connect_agent": {
        "cooperative": "Sure, I’ll connect you with a specialist now. Please stay on this chat.",
        "evasive": "Connecting you to an agent. Please stay available to respond.",
        "aggressive": "I’ll connect you to a specialist who can help further. Thanks for your patience.",
        "confused": "I’ll bring in a human specialist to assist you step by step."
    },
    "goodbye": {
        "cooperative": "Happy to help! If you need anything else, I’m here.",
        "evasive": "Thanks. Please remember to complete the payment as discussed.",
        "aggressive": "Thank you for your time today. We’re here to help if you need support.",
        "confused": "Glad I could help. If anything is unclear later, just message me again."
    },
    "unknown": {
        "cooperative": "I’m here to help with payments, plans, or details. What would you like to do?",
        "evasive": "Please let me know your plan for the pending payment or how I can assist.",
        "aggressive": "I want to help resolve this. Tell me what you’d like to do next.",
        "confused": "Could you share that in another way? I can help with amount, due, or extensions."
    }
}
