import streamlit as st
from pages._sidebar import make_sidebar
from PIL import Image
from typing import Callable
from utils import get_localised_text, make_prev_next_button


# FIXME: language and version probably should be put into text here
def make_page(text: Callable[[str], str], language: str, version: str) -> None:
    st.markdown(text("HEADLINE_ONE"))
    _, col2, _ = st.columns(3)
    with col2:
        st.image("pictures/Kurzvideo-Messmethode.gif")

    st.markdown(text("INTRODUCTION_MEASUREMENT"), unsafe_allow_html=True)

    image1 = Image.open("pictures/Foto-Fluoreszierende_Pflanzen.jpg")
    st.image(image1)
    st.caption(text("CAPTION_ABB1"))

    with st.expander(text("GROWING_PLANTS_1"), expanded=True):
        st.markdown(text("INTRODUCTION_GLOWING"), unsafe_allow_html=True)
        st.markdown(text("PLANT_ARE_SHINING_RED"), unsafe_allow_html=True)
        st.markdown(text("INTRODUCTION_EXPERIMENT"), unsafe_allow_html=True)
        _, col2, _ = st.columns(3)
        with col2:
            st.video("https://youtube.com/g3uTNWsDEdo")

        st.markdown(text("EXPLANATION_VIDEO"), unsafe_allow_html=True)

    with st.expander(text("MEASURING_FLUORESZENZ"), expanded=True):
        st.markdown(text("EXPLANATION_MEASUREMENT_1"), unsafe_allow_html=True)
        st.markdown(text("INTRODUCTION_PHI"), unsafe_allow_html=True)
        st.video("https://youtu.be/EwXkOlMBl3o")

    with st.expander(text("MEASURING_LIGHT_FLUORESCENCE"), expanded=True):
        st.markdown(text("EXPLANATION_INTRODUCTION_ATTEMPTS"))
        imageAnna = Image.open("pictures/PAMbasics.png")
        st.image(imageAnna, caption=text("CAPTION_ABB2"))

    with st.expander(text("SATURATING_PULSES")):
        st.markdown(text("EXPLANATION_ATTEMPTS"))
    st.markdown(text("INTRODUCTION_PAM_MEASUREMENT"), unsafe_allow_html=True)

    if version == "Expert":
        with st.expander(text("SATURATING_PULSES")):
            st.markdown(text("EXPLANATION_ATTEMPTS"), unsafe_allow_html=True)

    st.markdown(text("HEADLINE_ILLUSTRATION"), unsafe_allow_html=True)
    st.markdown(text("EXPLANATION_ILLUSTRATION_UNITS"), unsafe_allow_html=True)
    st.markdown(text("EXPLANATION_ILLUSTRATION"), unsafe_allow_html=True)

    if language == "German":
        image1 = Image.open("pictures/Beispielabbildung_de.png")
        st.image(image1, caption=text("CAPTION_ABB2"))
    else:
        image1 = Image.open("pictures/Beispielabbildung_en.png")
        st.image(image1, caption=text("CAPTION_ABB2"))


# FIXME: language and version probably should be put into text here
def make_literature(text: Callable[[str], str], language: str, version: str) -> None:
    with st.expander(text("LITERATURE")):
        st.markdown(text("LITERATURE_DECLARATION"), unsafe_allow_html=True)
        if version == "expert":
            """
            - Brooks, M. D., & Niyogi, K. K. (2011). Use of a pulse-amplitude modulated chlorophyll fluorometer to study the efficiency of photosynthesis in Arabidopsis plants. Chloroplast Research in Arabidopsis: Methods and Protocols, Volume II, 299-310. https://link.springer.com/protocol/10.1007/978-1-61779-237-3_16
            """
            """
            - Nies, T. et al (2021). Chlorophyll fluorescence: How the quality of information about PAM instrument parameters may affect our research. https://www.biorxiv.org/content/10.1101/2021.05.12.443801v1.full
            """
        elif version == "simple":
            if language == "german":
                """
                - https://link.springer.com/referenceworkentry/10.1007/978-3-662-53493-9_13-1
                """
            else:
                """
                - https://link.springer.com/protocol/10.1007/978-1-61779-237-3_16
                """
                """
                - https://link.springer.com/chapter/10.1007/978-1-4020-3218-9_11
                """


if __name__ == "__main__":
    version, language = make_sidebar()
    text = get_localised_text("main", version, language)
    make_page(text, language, version)
    make_literature(text, language, version)
    make_prev_next_button("photosynthesis", "computational models")
