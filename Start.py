import streamlit as st
from pages._sidebar import make_sidebar
from PIL import Image
from st_pages import Page, show_pages
from typing import Callable
from utils import get_localised_text, make_prev_next_button, icons, resetting_click_detector_setup, markdown_click

def make_introduction(text: Callable[[str], str]) -> None:
    markdown_click("HEADLINE_MAIN", text)
    markdown_click("INTRO", text)

    with st.expander(text("EXPANDER_ABOUT")):
        markdown_click("EXPLANATION_ABOUT", text)
        st.markdown(text("PROGRAMS_USED"))

    # Introduction biotool
    st.video("https://youtu.be/KvyjIWLD8rU")
    st.markdown(text("HEADLINE_USAGE"))
    markdown_click("USAGE", text)
    markdown_click("FOR_MATH_USE", text)


# FIXME: version and language should probably be replaced by text
def make_chapters(text: Callable[[str], str], version: str, language: str) -> None:
    if version == "Simple":
        st.markdown(text("DROP_BOX_INTRO"))
        with st.expander(text("EXPANDER_IN")):
            st.markdown(text("EXPLANATION_IN_VITRO"))
            st.markdown(text("EXPLANATION_IN_VIVO"))
            st.markdown(text("EXPLANATION_IN_SILICO"))

    markdown_click("HEADLINE_PAGES", text)
    markdown_click("INTRODUCTION_PAGES", text)
    markdown_click("PHOTOSYNTHESIS", text)
    markdown_click("METHOD", text)
    markdown_click("MODEL", text)
    markdown_click("EXPERIMENT", text)
    markdown_click("MEMORY", text)

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
    resetting_click_detector_setup()
    make_introduction(text)
    make_chapters(text, version, language)
    make_literature(text, version, language)
    make_prev_next_button(None, "photosynthesis")
    make_sidebar()
