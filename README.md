# Loan Collection Persona Chatbot

A fully self-contained Python CLI chatbot that adapts tone and messaging to customer personas
(cooperative, evasive, aggressive, confused) and responds to common intents (due date/amount,
promise to pay, extension request, hardship, dispute, connect to agent, etc.).

## Features
- **Persona detection** from customer profile (rule-based, using sentiment, complaints, response time, etc.).
- **Intent detection** via lightweight keyword patterns (no external APIs).
- **Persona-aware responses** with templated, compliant language.
- **Transcript logging** to JSONL in `chat_logs/`.
- **CSV integration**: Can look up a customer's row by `CustomerID` from your uploaded dataset:
  `/mnt/data/Analytics_loan_collection_dataset.csv`.

## Quick Start
```bash
python chatbot.py --customer-id 1001
```
(Use any valid `CustomerID` present in your CSV. If not found, a demo profile is used.)

## Files
- `personas.py` – persona definitions, messaging templates, and rule-based classifier
- `nlp.py` – simple intent detection rules
- `chatbot.py` – main chatbot engine (CLI), transcript logging
- `data_loader.py` – loads CSV and resolves customer profile
- `strategy_engine.py` – simple mapping from persona+context to next best action (stub to extend)
- `README.md` – this file

## Notes
- This is a template you can extend with your predictive model and UI.
- The rules are transparent and easy to tweak in `personas.py` and `nlp.py`.
