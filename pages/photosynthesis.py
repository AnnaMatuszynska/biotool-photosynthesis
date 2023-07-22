import streamlit as st
from pages._sidebar import make_sidebar
from pathlib import Path
from PIL import Image
from typing import Callable
from utils import centered_image, get_localised_text, make_prev_next_button, include_image, resetting_click_detector_setup, markdown_click


def make_page(text: Callable[[str], str], language: str, version: str) -> None:
    markdown_click("HEADLINE_PHOTOSYNTHESIS_PAGE", text)

    markdown_click("HEADLINE_CLIMATE", text)
    markdown_click("INTRODUCTION_CLIMATE_CHANGE", text)

    if version == "Advanced":
        markdown_click("POINT_1", text)
        markdown_click("POINT_2", text)
        markdown_click("POINT_3", text)
        markdown_click("END_OF_INTRODUCTION", text)

    else:
        col1, col2 = st.columns(2)
        with col1:
            if language == "German":
                centered_image("pictures/pflanzen_grundlagen.jpeg")
            if language == "English":
                centered_image("pictures/plants_basics.jpeg")
        with col2:
            if language == "German":
                centered_image("pictures/pflanzen_stress.jpeg")
            if language == "English":
                centered_image("pictures/plants_stress.jpeg")

    markdown_click("HEADLINE_PHOTOSYNTHESIS", text)
    markdown_click("PHOTOSYNTHESIS_EXPLANATION_1", text)
    markdown_click("PHOTOSYNTHESIS_EXPLANATION_2", text)

    if language == "German":
        include_image("pictures/Fotosynthese.jpg", 0.6, text("CAPTION_FOTOSYNTHESE_PICTURE"), True)
    else:
        include_image("pictures/Fotosynthese_eng.jpg", 0.6, text("CAPTION_FOTOSYNTHESE_PICTURE"), True)

    markdown_click("HEADLINE_PHOTOSYNTHESIS_LOCATION", text)
    markdown_click("PHOTOSYNTHESIS_LOCATION_EXPLANATION", text)

    if language == "German":
        include_image("pictures/Fotosynthese-Apparat.jpg", 0.6, text("CAPTION_FOTOSYNTHESE_APPARAT_PICTURE"), True)
    else:
        include_image("pictures/BioTool-photosynthesis.png", 0.6, text("CAPTION_FOTOSYNTHESE_APPARAT_PICTURE"), True)

    markdown_click("PHOTOSYNTHESIS_LOCATION_CONTINUE", text)

    # Journey into leaf
    st.video("https://youtu.be/hMCA0bBVoxE")

    markdown_click("HEADLINE_NPQ", text)
    markdown_click("NPQ_EXPLANATION", text)

    markdown_click("HEADER_MODEL_ORGANISMEN", text)
    markdown_click("MODEL_ORGANISMEN_EXPLANATION", text)

    with st.expander(text("EXPANDER_MODEL_ORGANISMEN")):
        _, col2, _ = st.columns(3)
        with col2:
            st.image(
                "pictures/Arabidopsis.jpg", width=400
            )  # Add Caption
            st.caption(text("CAPTION_THAIANA_PICTURE"))
        st.markdown(text("EXPANDER_MODEL_ORGANISM_EXPLANATION"), unsafe_allow_html=True)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version: str = st.session_state.setdefault("version", "Simple")
    language: str = st.session_state.setdefault("language", "English")

    text = get_localised_text(version, language)
    resetting_click_detector_setup()
    make_page(text, language, version)
    make_prev_next_button("start", "measuring method")
    make_sidebar()
