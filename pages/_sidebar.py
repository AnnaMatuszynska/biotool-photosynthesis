import streamlit as st
from st_pages import Page, show_pages
from streamlit.delta_generator import DeltaGenerator
from typing import cast
from utils import get_localised_text, icons


def keep(key):
    # Copy from temporary widget key to permanent key
    st.session_state[key] = st.session_state["_" + key]


def unkeep(key):
    # Copy from permanent key to temporary widget key
    st.session_state["_" + key] = st.session_state[key]


def make_sidebar() -> DeltaGenerator:
    version: str = st.session_state.version
    language: str = st.session_state.language
    text = get_localised_text(version, language)

    placeholder_sidebar = st.sidebar.container()

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

        show_pages(
            [
                Page(
                    "Start.py",
                    text("SDE_PAGENAMES_START"),
                    icons["house"],
                ),
                Page(
                    "pages/photosynthesis.py",
                    text("SDE_PAGENAMES_PHOTOSYNTHESIS"),
                    icons["leaves"],
                ),
                Page(
                    "pages/method.py",
                    text("SDE_PAGENAMES_MEASURINGMETHOD"),
                    icons["books"],
                ),
                Page(
                    "pages/model_explain.py",
                    text("SDE_PAGENAMES_COMPUTATIONALMODELS"),
                    icons["computer"],
                ),
                Page(
                    "pages/first_analysis.py",
                    text("SDE_PAGENAMES_EXPERIMENTSINSILICO"),
                    icons["bar_chart"],
                ),
                Page(
                    "pages/plant_memory.py",
                    text("SDE_PAGENAMES_PLANTLIGHTMEMORY"),
                    icons["chart_with_upwards_trend"],
                ),
                Page(
                    "pages/conclusion.py",
                    text("SDE_PAGENAMES_CONCLUSION"),
                    icons["heavy_check_mark"],
                ),
                Page(
                    "pages/contact.py",
                    text("SDE_PAGENAMES_CONTACT"),
                    icons["phone"],
                ),
            ]
        )
        
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
        languages = {
            'English': '🇬🇧 ' + text('SDE_LANGUAGE_EN'),
            'German': '🇩🇪 ' + text('SDE_LANGUAGE_DE'),
            'Polish': '🇵🇱 ' + text('SDE_LANGUAGE_PL'),
            'French': '🇫🇷 ' + text('SDE_LANGUAGE_FR'),
        }

        unkeep("language")
        language = cast(
            str,
            st.selectbox(
                label="⚙ Language 🌍💬",
                options=[i for i in languages.keys()],
                format_func=lambda x: languages.get(x),
                key="_language",
                on_change=keep,
                args=["language"],
            ),
        )


if __name__ == "__main__":
    placeholder_sidebar = make_sidebar()
