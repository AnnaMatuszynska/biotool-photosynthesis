import streamlit as st
from pages._sidebar import make_sidebar
from pathlib import Path
from PIL import Image
from typing import Callable
from utils import centered_image, get_localised_text, make_prev_next_button, include_image


def make_page(text: Callable[[str], str], language: str, version: str) -> None:
    st.markdown(text("HEADLINE_PHOTOSYNTHESIS_PAGE"))

    st.markdown(text("HEADLINE_CLIMATE"))
    st.markdown(text("INTRODUCTION_CLIMATE_CHANGE"))

    if version == "Advanced":
        st.markdown(text("POINT_1"))
        st.markdown(text("POINT_2"))
        st.markdown(text("POINT_3"))
        st.markdown(text("END_OF_INTRODUCTION"))

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

    st.markdown(text("HEADLINE_PHOTOSYNTHESIS"))
    st.markdown(text("PHOTOSYNTHESIS_EXPLANATION_1"))
    st.markdown(text("PHOTOSYNTHESIS_EXPLANATION_2"))

    if language == "German":
        include_image("pictures/Fotosynthese.jpg", 0.6, text("CAPTION_FOTOSYNTHESE_PICTURE"), True)
    else:
        include_image("pictures/Fotosynthese_eng.jpg", 0.6, text("CAPTION_FOTOSYNTHESE_PICTURE"), True)

    st.markdown(text("HEADLINE_PHOTOSYNTHESIS_LOCATION"))
    st.markdown(text("PHOTOSYNTHESIS_LOCATION_EXPLANATION"))

    if language == "German":
        include_image("pictures/Fotosynthese-Apparat.jpg", 0.6, text("CAPTION_FOTOSYNTHESE_APPARAT_PICTURE"), True)
    else:
        include_image("pictures/BioTool-photosynthesis.png", 0.6, text("CAPTION_FOTOSYNTHESE_APPARAT_PICTURE"), True)

    st.markdown(text("PHOTOSYNTHESIS_LOCATION_CONTINUE"))

    # Journey into leaf
    st.video("https://youtu.be/hMCA0bBVoxE")

    st.markdown(text("HEADLINE_NPQ"))
    st.markdown(text("NPQ_EXPLANATION"))

    st.markdown(text("HEADER_MODEL_ORGANISMEN"))
    st.markdown(text("MODEL_ORGANISMEN_EXPLANATION"))

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
    make_page(text, language, version)
    make_prev_next_button("start", "measuring method")
    make_sidebar()
