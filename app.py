"""
OpenAI Prompt Demo — Streamlit UI using the OpenAI Responses API.
Loads secrets from .env only; never prints or displays the API key.
"""

from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    OpenAI,
)

# Load variables from .env in the project directory (or cwd)
load_dotenv()

SYSTEM_INSTRUCTIONS = (
    "You are a helpful study assistant for a beginner Python student. "
    "Give clear, accurate answers. Use markdown when it helps readability."
)

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
    key = os.environ.get("OPENAI_API_KEY")
    if key is None:
        return None
    stripped = key.strip()
    return stripped if stripped else None


def build_user_input(task_type: str, prompt: str) -> str:
    prefix = TASK_PREFIXES.get(task_type, "")
    return f"{prefix}{prompt}"


def friendly_error_message(exc: Exception) -> str:
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
        code = exc.status_code
        return (
            f"The API returned an error ({code}). "
            "Please try again later."
        )
    return "Something went wrong while calling the API. Please try again."


def main() -> None:
    st.set_page_config(page_title="OpenAI Prompt Demo", layout="centered")

    st.title("OpenAI Prompt Demo")
    st.markdown(
        "Enter a prompt below. Your message is sent to **ChatGPT** via the "
        "**OpenAI Responses API**. Your API key stays in `.env` and is "
        "never shown here."
    )

    api_key = get_api_key()
    if not api_key:
        st.error(
            "**Missing API key.** Create a `.env` file in this folder "
            "with:\n\n`OPENAI_API_KEY=your_key_here`\n\n"
            "Then restart the app."
        )
        st.stop()

    client = OpenAI(api_key=api_key)

    task_type = st.selectbox(
        "Task type",
        options=list(TASK_PREFIXES.keys()),
        help="Optional presets that adjust how your prompt is framed.",
    )

    # Clear must reset widget state *before* the text_area is drawn (Streamlit rule).
    if st.session_state.pop("_clear_prompt_next", False):
        st.session_state["prompt_input"] = ""

    prompt = st.text_area(
        "Your prompt",
        height=160,
        placeholder="Ask a question or paste text to work with…",
        label_visibility="collapsed",
        key="prompt_input",
    )

    col_a, col_b = st.columns([1, 4])
    with col_a:
        submit = st.button("Submit", type="primary")
    with col_b:
        if st.button("Clear"):
            st.session_state.pop("last_response", None)
            st.session_state["_clear_prompt_next"] = True
            st.rerun()

    trimmed = prompt.strip()
    char_count = len(prompt)
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

    if "last_response" in st.session_state:
        st.markdown("---")
        st.subheader("Response")
        st.markdown(st.session_state["last_response"])


if __name__ == "__main__":
    main()
