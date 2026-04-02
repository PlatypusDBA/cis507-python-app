# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-03-31

### Changed

- **`app.py`**: Added inline and block comments explaining imports, helpers, Streamlit UI flow, Responses API call, error handling, and the Clear-button session-state pattern.

## [1.0.0] - 2026-03-31

### Added

- Streamlit UI for prompting ChatGPT via the **OpenAI Responses API** (`gpt-4o-mini`).
- API key loading from `.env` with `python-dotenv`; no key in source or UI.
- Task-type dropdown (general, summarize, explain simply, study help).
- Submit / Clear, character count, markdown response display.
- Error handling for missing key, auth, connection, and API errors.
- Documentation: `README.md`, `.env.example`, `.gitignore`, `requirements.txt`.
