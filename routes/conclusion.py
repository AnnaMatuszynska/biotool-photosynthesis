from typing import Callable

import streamlit as st

from utils import get_localised_text, include_image, make_prev_next_button, track_page_visit


def make_page(text: Callable[[str], str], language: str, version: str) -> None:
    st.markdown(text("CON_HEADLINE_CONCLUSION"))

    make_prev_next_button(
        text,
        "routes/plant_memory.py",
        "routes/contact.py",
        key="upper_nav_button",
    )

    st.markdown(text("CON_CONCLUSION_TEXT_ONE"))

    include_image("pictures/photosynthesis_productivity.gif", 0.7)

    st.markdown(text("CON_CONCLUSION_TEXT_TWO"))


if __name__ == "__main__":
    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version: str = st.session_state.setdefault("version", "4Bio")
    language: str = st.session_state.setdefault("language", "English")
    text = get_localised_text(version, language)
    track_page_visit("conclusion")

    make_page(text, language, version)
    make_prev_next_button(
        text,
        "routes/plant_memory.py",
        "routes/contact.py",
        key="lower_nav_button",
    )
