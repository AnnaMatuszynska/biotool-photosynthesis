import streamlit as st
from typing import cast
from utils import get_localised_text


def make_sidebar() -> tuple[str, str]:
    st.sidebar.write("## Settings :gear:")

    version: str = st.session_state.setdefault("version", "Simple")
    language: str = st.session_state.setdefault("language", "English")
    text = get_localised_text(version, language)

    # Versions selectbox
    versions = ["Simple", "Advanced"]
    version_display = dict(zip(versions, [text("SIMPLE"), text("ADVANCED")]))
    version_to_idx = dict(zip(versions, range(len(versions))))
    version = cast(
        str,
        st.sidebar.selectbox(
            label="⚙ Version 👩‍🎓👩🏼‍🔬",
            options=versions,
            format_func=lambda x: version_display[x],
            index=version_to_idx[st.session_state["version"]],
        ),
    )

    # language selectbox
    languages = ["English", "German", "Polish", "French", "Spanish"]
    language_to_idx = dict(zip(languages, range(len(languages))))
    language = cast(
        str,
        st.sidebar.selectbox(
            label="⚙ Language 🌍💬",
            options=languages,
            index=language_to_idx[st.session_state["language"]],
        ),
    )
    return version, language


if __name__ == "__main__":
    make_sidebar()
