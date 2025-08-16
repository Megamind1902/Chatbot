import streamlit as st
from personas import classify_persona, TEMPLATES, PERSONAS
from nlp import detect_intent
from data_loader import load_customer_profile
from strategy_engine import recommend_next_action
import datetime

st.set_page_config(page_title="Loan Collection Chatbot", page_icon="💬")

st.title("💬 Loan Collection Chatbot")

customer_id = st.number_input("Enter CustomerID:", min_value=1, step=1, value=1001)
profile = load_customer_profile(customer_id)
persona_key = classify_persona(profile)
st.write(f"**Detected Persona:** {persona_key} ({PERSONAS[persona_key].tone})")

if "history" not in st.session_state:
    st.session_state.history = []

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

for speaker, msg in st.session_state.history:
    if speaker == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")
