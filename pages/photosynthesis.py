import streamlit as st
from pages._sidebar import make_sidebar
from pathlib import Path
from PIL import Image
from typing import Callable
from utils import get_localised_text, make_prev_next_button


def make_page(text: Callable[[str], str], version: str, language: str) -> None:
    st.markdown(text("HEADLINE_CLIMATE"))
    st.markdown(text("INTRODUCTION_CLIMATE_CHANGE"))

    if version == "expert":
        st.markdown(text("POINT_1"))
        st.markdown(text("POINT_2"))
        st.markdown(text("POINT_3"))
        st.markdown(text("END_OF_INTRODUCTION"))

    else:
        col1, col2 = st.columns(2)
        with col1:
            if language == "German":
                st.image("pictures/pflanzen_grundlagen.jpeg")
            if language == "English":
                st.image("pictures/plants_basics.jpeg")
        with col2:
            if language == "German":
                st.image("pictures/pflanzen_stress.jpeg")
            if language == "English":
                st.image("pictures/plants_stress.jpeg")

    st.markdown(text("HEADLINE_PHOTOSYNTHESIS"))
    st.markdown(text("PHOTOSYNTHESIS_EXPLANATION_1"))

    st.markdown(text("PHOTOSYNTHESIS_EXPLANATION_2"))
    if language == "German":
        image = Image.open("pictures/Fotosynthese.jpg")
        st.image(image, caption=text("CAPTION_FOTOSYNTHESE_PICTURE"))
    else:
        image = Image.open("pictures/Fotosynthese_eng.jpg")
        st.image(image, caption=text("CAPTION_FOTOSYNTHESE_PICTURE"))

    st.markdown(text("NUTRIENTS_EXPLANATION"))
    image = Image.open("pictures/Stomata1.jpg")
    st.image(image, caption=text("CAPTION_STOMATA_PICTURE"), width=400)  # make a caption

    st.markdown(text("HEADLINE_PHOTOSYNTHESIS_LOCATION"))
    st.markdown(text("PHOTOSYNTHESIS_LOCATION_EXPLANATION"))
    if language == "German":
        image = Image.open("pictures/Fotosynthese-Apparat.jpg")
        st.image(image, caption=text("CAPTION_FOTOSYNTHESE_APPARAT_PICTURE"), width=600)
    else:
        image = Image.open("pictures/Fotosynthese-Apparat_eng.jpg")
        st.image(image, caption=text("CAPTION_FOTOSYNTHESE_APPARAT_PICTURE"), width=600)

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
                "pictures/Arabidopsis.jpg", caption=text("CAPTION_THAIANA_PICTURE"), width=400
            )  # Add Caption
        st.markdown(text("EXPANDER_MODEL_ORGANISM_EXPLANATION_1"), unsafe_allow_html=True)
        st.markdown(text("EXPANDER_MODEL_ORGANISM_EXPLANATION_PONT1"), unsafe_allow_html=True)
        st.markdown(text("EXPANDER_MODEL_ORGANISM_EXPLANATION_PONT2"), unsafe_allow_html=True)
        st.markdown(text("EXPANDER_MODEL_ORGANISM_EXPLANATION_PONT3"), unsafe_allow_html=True)
        st.markdown(text("EXPANDER_MODEL_ORGANISM_EXPLANATION_PONT4"), unsafe_allow_html=True)
        st.markdown(text("EXPANDER_MODEL_ORGANISM_EXPLANATION_2"), unsafe_allow_html=True)


if __name__ == "__main__":
    version, language = make_sidebar()
    text = get_localised_text("main", version, language)
    make_page(text, language, version)
    make_prev_next_button("start", "measuring method")
