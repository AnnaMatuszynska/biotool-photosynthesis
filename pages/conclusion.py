import streamlit as st
from pages._sidebar import make_sidebar
from pathlib import Path
from PIL import Image
from typing import Callable
from utils import (
    get_localised_text,
    make_prev_next_button,
    include_image
)

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
    make_page(text, language, version)
    make_prev_next_button("plant light memory", "contact")
    make_sidebar()
