import streamlit as st
from personas import classify_persona, TEMPLATES, PERSONAS
from nlp import detect_intent
from data_loader import load_customer_profile
from strategy_engine import recommend_next_action
import datetime

st.set_page_config(page_title="Loan Collection Chatbot", page_icon="💬")

st.title("💬 Loan Collection Chatbot")
st.subheader("📌 Available Commands")
st.markdown("""
- **👋 Greeting** → say `hi`, `hello`, `good morning`
- **📅 Ask Due Date** → ask `when is my payment due?`, `deadline?`
- **💰 Ask Amount** → ask `how much do I owe?`, `balance`
- **🤝 Promise to Pay** → say `I will pay on Friday`, `promise to pay tomorrow`
- **⏳ Request Extension** → say `I need extra time`, `can I get an extension?`
- **⚠️ Report Hardship** → say `I lost my job`, `financial issue`, `medical emergency`
- **❗ Raise Dispute** → say `this is wrong`, `not my loan`, `error`
- **🧑 Connect to Agent** → say `I want to talk to an agent`, `call me`
- **👋 Goodbye** → say `bye`, `thanks`, `see you`
""")


# Input as text (string) instead of number
customer_id = st.text_input("Enter CustomerID (e.g., CUST0001):", "CUST0001")

# Load profile (string-safe lookup inside data_loader)
profile = load_customer_profile(customer_id)

# Classify persona
persona_key = classify_persona(profile)
persona = PERSONAS[persona_key]
st.write(f"**Detected Persona:** {persona_key} ({persona.tone})")

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("You:", "")

if user_input:
    intent = detect_intent(user_input)
    template = TEMPLATES.get(intent, TEMPLATES["unknown"])[persona_key]
    reply = template.format(
        name=profile.get("Name", "Customer"),
        outstanding=profile.get("Outstanding", profile.get("LoanAmount", 0)),
        date=(datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
    )
    nba = recommend_next_action(persona_key, profile, intent)

    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", reply + f"\n\n👉 Next Best Action: {nba}"))

# Show chat history
for speaker, msg in st.session_state.history:
    if speaker == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")

