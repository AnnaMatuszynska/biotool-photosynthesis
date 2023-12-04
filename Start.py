import streamlit as st
from pages._sidebar import make_sidebar
from PIL import Image
from st_pages import Page, show_pages
from typing import Callable
from utils import (
    get_localised_text,
    icons,
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
    markdown_click("STR_SPECIFIC_USE", text)

    # Learning objectives
    st.markdown(text("STR_LEARNING_OBJECTIVES_HEADER"))
    st.info(text("STR_LEARNING_OBJECTIVES"))


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
        st.markdown(text("STR_PROGRAMS_USED"))


def make_literature(text: Callable[[str], str], language: str, version: str) -> None:
    with st.expander(text("LITERATURE")):
        st.markdown(text("LITERATURE_ONPAGE"))
        st.markdown(
            "- Matuszyńska, A., Heidari, S., Jahns, P., & Ebenhöh, O. (2016). A mathematical model of non-photochemical quenching to study short-term light memory in plants. Biochimica et Biophysica Acta (BBA) - Bioenergetics, 1857(12), 1860–1869. https://doi.org/10.1016/j.bbabio.2016.09.003"
        )


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version: str = st.session_state.setdefault("version", "4Bio")
    language: str = st.session_state.setdefault("language", "English")

    text = get_localised_text(version, language)

    # NOTE: this belongs with the sidebar, but works globally
    # so I'd prefer to put it here
    show_pages(
        [
            Page(
                "Start.py",
                "Start",
                icons["house"],
            ),
            Page(
                "pages/photosynthesis.py",
                "Photosynthesis",
                icons["leaves"],
            ),
            Page(
                "pages/method.py",
                "Measuring Method",
                icons["books"],
            ),
            Page(
                "pages/model_explain.py",
                "Computational Models",
                icons["computer"],
            ),
            Page(
                "pages/first_analysis.py",
                "Experiments in silico",
                icons["bar_chart"],
            ),
            Page(
                "pages/plant_memory.py",
                "Plant Light Memory",
                icons["chart_with_upwards_trend"],
            ),
            Page(
                "pages/conclusion.py",
                "Take Home Messages",
                icons["heavy_check_mark"],
            ),
            Page(
                "pages/contact.py",
                "Contact",
                icons["phone"],
            ),
        ]
    )
    make_sidebar()
    resetting_click_detector_setup()
    track_page_visit("Start")
    make_introduction(text)
    make_chapters(text, version, language)
    make_literature(text, version, language)
    make_prev_next_button(None, "photosynthesis")
