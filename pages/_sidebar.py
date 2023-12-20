import streamlit as st
from st_pages import Page, show_pages
from streamlit.delta_generator import DeltaGenerator
from typing import Callable, cast
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
    st.session_state.setdefault("show_video_transcripts", False)

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

    return st.sidebar.container()


def rename_pages(text: Callable[[str], str]):
    from streamlit.source_util import _cached_pages, _on_pages_changed, _pages_cache_lock, get_pages

    # FIXME: this depends on the order of the dict
    # and list being the same, which isn't guaranteed

    new_names = [
        text("SDE_PAGENAMES_START"),
        text("SDE_PAGENAMES_PHOTOSYNTHESIS"),
        text("SDE_PAGENAMES_MEASURINGMETHOD"),
        text("SDE_PAGENAMES_COMPUTATIONALMODELS"),
        text("SDE_PAGENAMES_EXPERIMENTSINSILICO"),
        text("SDE_PAGENAMES_PLANTLIGHTMEMORY"),
        text("SDE_PAGENAMES_CONCLUSION"),
        text("SDE_PAGENAMES_CONTACT"),
    ]

    pages = get_pages("")
    for page, new_name in zip(pages.values(), new_names):
        page["page_name"] = new_name

    with _pages_cache_lock:
        _cached_pages.update(pages)


def fill_sidebar(placeholder_sidebar: DeltaGenerator) -> None:
    version: str = st.session_state.version
    language: str = st.session_state.language
    text = get_localised_text(version, language)

    # Pages
    rename_pages(text)

    # Versions selectbox
    with placeholder_sidebar.container():
        versions = ["4Bio", "4Math"]
        version_display = dict(zip(versions, [text("SDE_4BIO"), text("SDE_4MATH")]))

        st.write(f"## {text('SDE_SIDEBAR_SETTINGS')} :gear:")

        unkeep("version")
        version = cast(
            str,
            st.selectbox(
                label=f"⚙ {text('SDE_SIDEBAR_VERSION')} 👩‍🎓👩🏼‍🔬",
                options=versions,
                format_func=lambda x: version_display[x],
                key="_version",
                on_change=keep,
                args=["version"],
            ),
        )
        # language selectbox
        languages = {
            "English": "🇬🇧 " + text("SDE_LANGUAGE_EN"),
            "German": "🇩🇪 " + text("SDE_LANGUAGE_DE"),
            "Polish": "🇵🇱 " + text("SDE_LANGUAGE_PL"),
            "French": "🇫🇷 " + text("SDE_LANGUAGE_FR"),
        }

        unkeep("language")
        language = cast(
            str,
            st.selectbox(
                label=f"⚙ {text('SDE_SIDEBAR_LANGUAGE')} 🌍💬",
                options=[i for i in languages.keys()],
                format_func=lambda x: languages.get(x),
                key="_language",
                on_change=keep,
                args=["language"],
            ),
        )

        unkeep("show_video_transcripts")
        st.checkbox(
            label=text("VIDEO_TRANSCRIPT_SWITCH"),
            value=False,
            key="_show_video_transcripts",
            on_change=keep,
            args=["show_video_transcripts"],
        )


if __name__ == "__main__":
    make_sidebar()
