from typing import Dict, Any

def recommend_next_action(persona: str, profile: Dict[str, Any], intent: str) -> str:
    """
    Returns a lightweight recommendation string.
    Extend this to integrate with your business logic.
    """
    missed = int(profile.get("MissedPayments", 0) or 0)
    complaints = int(profile.get("Complaints", 0) or 0)

    if intent == "need_extension" or intent == "hardship":
        return "Offer short-term extension or restructuring evaluation."
    if intent == "dispute":
        return "Create dispute ticket and share reference number."
    if persona == "evasive" and missed >= 2:
        return "Send firm reminder and schedule confirmation call."
    if persona == "aggressive" and complaints >= 1:
        return "Escalate to senior agent with de-escalation training."
    if persona == "confused":
        return "Send simplified explainer with step-by-step payment guide."

    return "Share payment link and set follow-up reminder."
