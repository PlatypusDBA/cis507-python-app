"""
OpenAI Prompt Demo — Streamlit UI using the OpenAI Responses API.
Loads secrets from .env only; never prints or displays the API key.
"""

# Forward-referenced type hints (e.g. str | None) on supported Python versions.
from __future__ import annotations

# Read process environment variables (OPENAI_API_KEY).
import os

# Streamlit: web UI in the browser.
import streamlit as st
# Read .env into os.environ (no hardcoded secrets).
from dotenv import load_dotenv
# Client and errors we turn into friendly UI messages.
from openai import (
    APIConnectionError,  # Network failure reaching OpenAI.
    APIStatusError,  # HTTP error from API (4xx/5xx).
    AuthenticationError,  # Bad or missing credentials.
    OpenAI,  # Client for the Responses API.
)

# Load .env from the working directory (project folder).
load_dotenv()

# System message for every request; tone for a beginner Python course.
SYSTEM_INSTRUCTIONS = (
    "You are a helpful study assistant for a beginner Python student. "
    "Give clear, accurate answers. Use markdown when it helps readability."
)

# Dropdown label -> text prepended to the user prompt (task presets).
TASK_PREFIXES = {
    "General Question": "",
    "Summarize": "Summarize the following in clear, concise language:\n\n",
    "Explain Simply": (
        "Explain the following in simple terms for a beginner:\n\n"
    ),
    "Study Help": (
        "Help me study this topic: break it into key ideas, "
        "define terms, and suggest one short practice question:\n\n"
    ),
}


def get_api_key() -> str | None:
    """API key from environment, or None if missing or blank."""
    key = os.environ.get("OPENAI_API_KEY")  # From .env, not source code.
    if key is None:
        return None
    stripped = key.strip()  # Trim spaces from .env value.
    return stripped if stripped else None  # All-blank counts as missing.


def build_user_input(task_type: str, prompt: str) -> str:
    """Prefix from task type plus user prompt."""
    prefix = TASK_PREFIXES.get(task_type, "")  # "" if label missing.
    return f"{prefix}{prompt}"


def friendly_error_message(exc: Exception) -> str:
    """SDK exception -> short UI message (no tracebacks)."""
    if isinstance(exc, AuthenticationError):
        return (
            "Authentication failed. Check that `OPENAI_API_KEY` in your "
            "`.env` file is correct and has not expired."
        )
    if isinstance(exc, APIConnectionError):
        return (
            "Could not reach the OpenAI API. Check your internet "
            "connection and try again."
        )
    if isinstance(exc, APIStatusError):
        code = exc.status_code  # HTTP status of the failed call.
        return (
            f"The API returned an error ({code}). "
            "Please try again later."
        )
    return "Something went wrong while calling the API. Please try again."


def main() -> None:
    # Tab title and page width.
    st.set_page_config(page_title="OpenAI Prompt Demo", layout="centered")

    st.title("OpenAI Prompt Demo")
    # Markdown allows **bold** in the intro.
    st.markdown(
        "Enter a prompt below. Your message is sent to **ChatGPT** via the "
        "**OpenAI Responses API**. Your API key stays in `.env` and is "
        "never shown here."
    )

    api_key = get_api_key()
    if not api_key:
        # Cannot call the API without a key.
        st.error(
            "**Missing API key.** Create a `.env` file in this folder "
            "with:\n\n`OPENAI_API_KEY=your_key_here`\n\n"
            "Then restart the app."
        )
        st.stop()  # Stop this run; user edits .env and reloads.

    client = OpenAI(api_key=api_key)  # Key not logged by our code.

    # Preset adds a prefix string to the prompt (or none).
    task_type = st.selectbox(
        "Task type",
        options=list(TASK_PREFIXES.keys()),
        help="Optional presets that adjust how your prompt is framed.",
    )

    # Streamlit: cannot set widget session keys after the widget is built.
    # Clear stores a flag; on rerun we clear before text_area is created.
    if st.session_state.pop("_clear_prompt_next", False):
        st.session_state["prompt_input"] = ""

    # Multiline input; key links value to session_state for resets.
    prompt = st.text_area(
        "Your prompt",
        height=160,
        placeholder="Ask a question or paste text to work with…",
        label_visibility="collapsed",
        key="prompt_input",
    )

    col_a, col_b = st.columns([1, 4])  # Submit | Clear layout.
    with col_a:
        # True only in the run where the user clicked Submit.
        submit = st.button("Submit", type="primary")
    with col_b:
        if st.button("Clear"):
            st.session_state.pop("last_response", None)  # Drop answer.
            # Next run clears the text box (see pop above).
            st.session_state["_clear_prompt_next"] = True
            st.rerun()  # Start script again from the top.

    trimmed = prompt.strip()  # For validation (reject whitespace-only).
    char_count = len(prompt)  # Hint text length.
    st.caption(f"Characters: {char_count}")

    if submit:
        if not trimmed:
            st.warning(
                "Please enter a non-empty prompt "
                "(spaces alone are not valid)."
            )
        else:
            user_payload = build_user_input(task_type, trimmed)
            with st.spinner("Waiting for the model…"):
                try:
                    response = client.responses.create(
                        model="gpt-4o-mini",
                        input=user_payload,
                        instructions=SYSTEM_INSTRUCTIONS,
                    )
                    # Combined assistant text from the response object.
                    text = response.output_text or ""
                    st.session_state["last_response"] = text
                except (
                    AuthenticationError,
                    APIConnectionError,
                    APIStatusError,
                ) as e:
                    st.error(friendly_error_message(e))
                except Exception:
                    st.error(
                        "An unexpected error occurred. "
                        "Check your setup and try again."
                    )

    # Keep showing the last model reply until Clear or new submit.
    if "last_response" in st.session_state:
        st.markdown("---")
        st.subheader("Response")
        # Model may return markdown; st.markdown renders it.
        st.markdown(st.session_state["last_response"])


# Optional entrypoint if you run `python app.py` (Streamlit loads this too).
if __name__ == "__main__":
    main()
