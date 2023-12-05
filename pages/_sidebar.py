import streamlit as st
import time
from typing import cast
from utils import get_localised_text


def keep(key):
    # Copy from temporary widget key to permanent key
    st.session_state[key] = st.session_state["_" + key]


def unkeep(key):
    # Copy from permanent key to temporary widget key
    st.session_state["_" + key] = st.session_state[key]


def make_sidebar() -> tuple[str, str]:
    version: str = st.session_state.version
    language: str = st.session_state.language
    text = get_localised_text(version, language)
    st.sidebar.write("## Settings :gear:")

    placeholder_sidebar = st.sidebar.empty()
    with placeholder_sidebar.container():
        st.selectbox(
            label="⚙ Version 👩‍🎓👩🏼‍🔬",
            options=["Loading page..."],
            index=0,
        )

        st.selectbox(
            label="⚙ Language 🌍💬",
            options=["Loading page..."],
            index=0,
        )

    st.session_state.setdefault("show_video_transcripts", False)
    unkeep("show_video_transcripts")
    st.sidebar.checkbox(
        label=text("VIDEO_TRANSCRIPT_SWITCH"),
        value=False,
        key="_show_video_transcripts",
        on_change=keep,
        args=["show_video_transcripts"],
    )
    return placeholder_sidebar


def fill_sidebar(placeholder_sidebar):
    version: str = st.session_state.version
    language: str = st.session_state.language
    text = get_localised_text(version, language)

    # Versions selectbox
    placeholder_sidebar.empty()
    with placeholder_sidebar.container():
        versions = ["4Bio", "4Math"]
        version_display = dict(zip(versions, [text("SDE_4BIO"), text("SDE_4MATH")]))
        version_to_idx = dict(zip(versions, range(len(versions))))

        # with st.session_state["placeholder_version"]:
        unkeep("version")
        version = cast(
            str,
            st.selectbox(
                label="⚙ Version 👩‍🎓👩🏼‍🔬",
                options=versions,
                format_func=lambda x: version_display[x],
                # index=version_to_idx[st.session_state["version"]],
                key="_version",
                on_change=keep,
                args=["version"],
            ),
        )
        # language selectbox
        languages = ["English", "German", "Polish"]  # , "French", "Spanish"]
        language_to_idx = dict(zip(languages, range(len(languages))))
        # with st.session_state["placeholder_languages"]:
        unkeep("language")
        language = cast(
            str,
            st.selectbox(
                label="⚙ Language 🌍💬",
                options=languages,
                # index=language_to_idx[st.session_state["language"]],
                key="_language",
                on_change=keep,
                args=["language"],
            ),
        )


if __name__ == "__main__":
    placeholder_sidebar = make_sidebar()
