from typing import Callable

import streamlit as st

from utils import (
    get_localised_text,
    include_image,
    include_ytvideo,
    make_prev_next_button,
    markdown_click,
    resetting_click_detector_setup,
    track_page_visit,
)


def make_introduction(text: Callable[[str], str]) -> None:
    markdown_click("STR_HEADLINE_MAIN", text)
    markdown_click("STR_INTRO", text)

    # Introduction biotool
    st.markdown(text("STR_HEADLINE_USAGE"))
    col1, col2 = st.columns((0.4, 0.6))
    with col1:
        markdown_click("STR_USAGE", text)
    with col2:
        include_ytvideo("https://youtu.be/KvyjIWLD8rU", 0.9)

    if st.session_state["show_video_transcripts"]:
        with st.expander(text("EXPANDER_VIDEO_TRANSCRIPT")):
            st.write(text("STR_VIDEO_TRANSCRIPT_INTRODUCTION"))

    markdown_click("STR_SPECIFIC_USE", text)

    # Learning objectives
    st.markdown(text("STR_LEARNING_OBJECTIVES_HEADER"))
    st.info(text("STR_LEARNING_OBJECTIVES"))
    st.markdown(text("STR_LINK_PLANTS_AND_PYTHON"))


# FIXME: version and language should probably be replaced by text
def make_chapters(text: Callable[[str], str], version: str, language: str) -> None:
    markdown_click("STR_HEADLINE_PAGES", text)
    markdown_click("STR_INTRODUCTION_PAGES", text)
    markdown_click("STR_PHOTOSYNTHESIS", text)
    markdown_click("STR_METHOD", text)
    markdown_click("STR_MODEL", text)
    markdown_click("STR_EXPERIMENT", text)
    markdown_click("STR_MEMORY", text)

    # Explanation about "in vivo" etc
    if version == "4Math":
        st.divider()
        st.markdown(text("STR_DROP_BOX_INTRO"))
        with st.expander(text("STR_EXPANDER_IN")):
            st.markdown(text("STR_EXPLANATION_IN_VITRO"))
            st.markdown(text("STR_EXPLANATION_IN_VIVO"))
            st.markdown(text("STR_EXPLANATION_IN_SILICO"))
        st.divider()

    # Make About section
    with st.expander(text("STR_EXPANDER_ABOUT")):
        markdown_click("STR_EXPLANATION_ABOUT", text)
        st.markdown(text("PROGRAMS_USED"))


def make_literature(text: Callable[[str], str], language: str, version: str) -> None:
    with st.expander(text("LITERATURE")):
        st.markdown(text("LITERATURE_ONPAGE"))
        st.markdown(
            "- Matuszyńska, A., Heidari, S., Jahns, P., & Ebenhöh, O. (2016). "
            "A mathematical model of non-photochemical quenching to study short-term light memory in plants. "
            "Biochimica et Biophysica Acta (BBA) - Bioenergetics, 1857(12), 1860–1869. https://doi.org/10.1016/j.bbabio.2016.09.003"
        )
        st.markdown(text("LITERATURE_PLANTS_AND_PYTHON"))


if __name__ == "__main__":
    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version: str = st.session_state.setdefault("version", "4Bio")
    language: str = st.session_state.setdefault("language", "English")

    text = get_localised_text(version, language)

    resetting_click_detector_setup()
    track_page_visit("Start")
    make_introduction(text)
    make_chapters(text, version, language)

    with st.expander(text("APPEARANCES")):
        st.markdown(text("APPEARANCE_EXPLANATION"))
        st.markdown(text("EPS2_CONFERENCE_TITLE"), unsafe_allow_html=True)
        st.markdown(text("EPS2_CONFERENCE_1"), unsafe_allow_html=True)
        st.markdown(text("EPS2_CONFERENCE_2"), unsafe_allow_html=True)
        st.markdown(text("EPS2_CONFERENCE_3"), unsafe_allow_html=True)
        col1, col2 = st.columns((0.5, 0.5))
        with col1:
            include_image("pictures/Poster.png", img_width=0.6)
        with col2:
            include_image("pictures/Editable/Elouen_Poster.svg", img_width=0.6)

    make_literature(text, version, language)
    make_prev_next_button(
        text,
        None,
        "routes/photosynthesis.py",
        key="lower_nav_button",
    )
