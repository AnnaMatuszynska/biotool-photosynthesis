import streamlit as st
from pages._sidebar import make_sidebar
from pathlib import Path
from PIL import Image
from typing import Callable
from utils import (
    get_localised_text,
    make_prev_next_button,
)

def make_page(text: Callable[[str], str], language: str, version: str) -> None:
    st.markdown(text("HEADLINE_CONCLUSION"))

    st.markdown(text("CONCLUSION_TEXT"))

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version, language = make_sidebar()
    text = get_localised_text(version, language)
    make_page(text, language, version)
    make_prev_next_button("measuring method", "experiments in silico")