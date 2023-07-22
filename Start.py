import streamlit as st
from pages._sidebar import make_sidebar
from PIL import Image
from st_pages import Page, show_pages
from typing import Callable
from utils import get_localised_text, make_prev_next_button, resetting_click_detector_setup, markdown_click
import re

def make_introduction(text: Callable[[str], str]) -> None:
    markdown_click("HEADLINE_MAIN", text)
    markdown_click("INTRO", text)

    with st.expander(text("EXPANDER_ABOUT")):
        markdown_click("EXPLANATION_ABOUT", text)

    # Introduction biotool
    st.video("https://youtu.be/KvyjIWLD8rU")
    markdown_click("HEADLINE_USAGE", text)
    markdown_click("USAGE", text)
    markdown_click("ADVANCED_USE", text)
    markdown_click("DROP_BOX_INTRO", text)


# FIXME: version and language should probably be replaced by text
def make_chapters(text: Callable[[str], str], version: str, language: str) -> None:
    with st.expander(text("EXPANDER_IN")):
        markdown_click("EXPLANATION_IN_VITRO", text)
        markdown_click("EXPLANATION_IN_VIVO", text)
        markdown_click("EXPLANATION_IN_SILICO", text)

    markdown_click("HEADLINE_PAGES", text)
    markdown_click("INTRODUCTION_PAGES", text)
    markdown_click("PHOTOSYNTHESIS", text)
    markdown_click("METHOD", text)
    markdown_click("MODEL", text)
    markdown_click("EXPERIMENT", text)
    markdown_click("MEMORY", text)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version: str = st.session_state.setdefault("version", "Simple")
    language: str = st.session_state.setdefault("language", "English")

    text = get_localised_text(version, language)

    # NOTE: this belongs with the sidebar, but works globally
    # so I'd prefer to put it here
    show_pages(
        [
            Page(
                "Start.py",
                "Start",
                ":house:",
            ),
            Page(
                "pages/photosynthesis.py",
                "Photosynthesis",
                ":leaves:",
            ),
            Page(
                "pages/method.py",
                "Measuring Method",
                ":books:",
            ),
            Page(
                "pages/model_explain.py",
                "Computational Models",
                ":computer:",
            ),
            Page(
                "pages/first_analysis.py",
                "Experiments in silico",
                ":bar_chart:",
            ),
            Page(
                "pages/plant_memory.py",
                "Plant Light Memory",
                ":chart_with_upwards_trend:",
            ),
            Page(
                "pages/conclusion.py",
                "Take Home Messages",
                ":heavy_check_mark:",
            ),
            Page(
                "pages/contact.py",
                "Contact",
                ":phone:",
            ),
        ]
    )
    resetting_click_detector_setup()
    make_introduction(text)
    make_chapters(text, version, language)
    make_prev_next_button(None, "photosynthesis")

    make_sidebar()
