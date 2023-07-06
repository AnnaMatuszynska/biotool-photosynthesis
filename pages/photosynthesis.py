import streamlit as st
from pages._sidebar import make_sidebar
from pathlib import Path
from typing import Callable
from utils import get_localised_text


def make_page(text: Callable[[str], str], language: str, version: str) -> None:
    st.markdown("# Hello there")


if __name__ == "__main__":
    version, language = make_sidebar()
    text = get_localised_text("b-model", version, language)
    make_page(text, language, version)
