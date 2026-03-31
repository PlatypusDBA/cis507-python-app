# CIS507 Python App

Course project: a small **Streamlit** web app that calls the **OpenAI Responses API** with a user prompt and shows the model reply as markdown. The OpenAI API key is loaded from a **`.env`** file (never committed).

**Repository:** [github.com/PlatypusDBA/cis507-python-app](https://github.com/PlatypusDBA/cis507-python-app)

## Features

- Load `OPENAI_API_KEY` via `python-dotenv`
- Task-type presets (general, summarize, explain simply, study help)
- Input validation, loading state, markdown output
- Graceful errors (no stack traces in the UI)

## Requirements

- Python **3.9+**
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Setup

```bash
git clone https://github.com/PlatypusDBA/cis507-python-app.git
cd cis507-python-app
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and set OPENAI_API_KEY
```

Use the **same** Python for install and run (e.g. `python -m pip` and `python -m streamlit`).

## Run

```bash
streamlit run app.py
```

Open the local URL shown in the terminal (default [http://localhost:8501](http://localhost:8501)).

## Security

- Do not commit `.env` (it is gitignored).
- The app does not display or log the API key.

## Project layout

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI and OpenAI client |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for local secrets |
| `CHANGELOG.md` | Version history |

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md).
