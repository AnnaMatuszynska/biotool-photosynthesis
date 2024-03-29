import streamlit as st
from pages._sidebar import fill_sidebar, make_sidebar
from pathlib import Path
from PIL import Image
from typing import Callable
from utils import get_localised_text, include_image, make_prev_next_button, track_page_visit


def make_page(text: Callable[[str], str], language: str, version: str) -> None:
    st.markdown(text("CON_HEADLINE_CONCLUSION"))

    st.markdown(text("CON_CONCLUSION_TEXT_ONE"))

    include_image("pictures/photosynthesis_productivity.gif", 0.7)

    st.markdown(text("CON_CONCLUSION_TEXT_TWO"))


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version: str = st.session_state.setdefault("version", "4Bio")
    language: str = st.session_state.setdefault("language", "English")
    text = get_localised_text(version, language)
    placeholder_sidebar = make_sidebar()
    track_page_visit("conclusion")
    make_page(text, language, version)
    make_prev_next_button(
        text,
        text("SDE_PAGENAMES_PLANTLIGHTMEMORY"),
        text("SDE_PAGENAMES_CONTACT"),
    )
    fill_sidebar(placeholder_sidebar)
