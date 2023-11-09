import streamlit as st
from typing import cast
from utils import get_localised_text


def make_sidebar() -> tuple[str, str]:
    st.sidebar.write("## Settings :gear:")

    version: str = st.session_state.version
    language: str = st.session_state.language
    text = get_localised_text(version, language)
    # Versions selectbox
    versions = ["4Bio", "4STEM"]
    version_display = dict(zip(versions, [text("4BIO"), text("4STEM")]))
    version_to_idx = dict(zip(versions, range(len(versions))))

    version = cast(
        str,
        st.sidebar.selectbox(
            label="⚙ Version 👩‍🎓👩🏼‍🔬",
            options=versions,
            format_func=lambda x: version_display[x],
            index=version_to_idx[st.session_state["version"]],
            key="version",
        ),
    )
    # language selectbox
    languages = ["English", "German", "Polish"] #, "French", "Spanish"]
    language_to_idx = dict(zip(languages, range(len(languages))))
    language = cast(
        str,
        st.sidebar.selectbox(
            label="⚙ Language 🌍💬",
            options=languages,
            index=language_to_idx[st.session_state["language"]],
            key="language",
        ),
    )
    # return version, language


if __name__ == "__main__":
    make_sidebar()
