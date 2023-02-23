import streamlit as st
from pages._sidebar import make_sidebar
from PIL import Image
from typing import Callable
from utils import get_localised_text


# FIXME: language and version probably should be put into text here
def make_page(text: Callable[[str], str], language: str, version: str) -> None:
    st.markdown(text("HEADLINE_ONE"))

    st.markdown(text("INTRODUCTION_MEASUREMENT"))
    with st.expander(text("GROWING_PLANTS_1")):
        st.markdown(text("INTRODUCTION_GLOWING"))
        st.markdown(text("PLANT_ARE_SHINING_RED"))

    with st.expander(text("GROWING_PLANTS_2")):
        st.markdown(text("INTRODUCTION_EXPERIMENT"))
        '''
        [VIDEO]
        '''

        st.markdown(text("EXPLANATION_VIDEO"))

    with st.expander(text("MEASURING_FLUORESZENZ")):
        if version == 'simple':
            st.markdown(text("EXPLANATION_MEASUREMENT_1"))
            st.markdown(text("INTRODUCTION_PHI"))

    # FIXME: unused columns, are you trying to center?
    _, col2, _ = st.columns(3)
    with col2:
        st.image("pictures/Kurzvideo-Messmethode.gif")

    st.markdown(text("INTRODUCTION_PAM_MEASUREMENT"))

    with st.expander(text("MEASURING_LIGHT_FLUORESCENCE")):
        st.markdown(text("EXPLANATION_INTRODUCTION_ATTEMPTS"))
        st.markdown(text("EXPLANATION_MEASUREMENT_2"))

    with st.expander(text("SATURATING_PULSES")):
        st.markdown(text("EXPLANATION_ATTEMPTS"))

    # FIXME: unused columns. Are you trying to center the picture?
    _, col2, _ = st.columns(3)
    with col2:
        st.image(
            "pictures/Arabidopsis.jpg", caption=text("CAPTION_THAIANA_PICTURE"), width=400
        )  # Add Caption

    with st.expander(text("EXPANDER_MODEL_ORGANISMEN")):
        st.markdown(text("EXPANDER_MODEL_ORGANISM_EXPLANATION_1"))
        st.markdown(text("EXPANDER_MODEL_ORGANISM_EXPLANATION_PONT1"))
        st.markdown(text("EXPANDER_MODEL_ORGANISM_EXPLANATION_PONT2"))
        st.markdown(text("EXPANDER_MODEL_ORGANISM_EXPLANATION_PONT3"))
        st.markdown(text("EXPANDER_MODEL_ORGANISM_EXPLANATION_PONT4"))
        st.markdown(text("EXPANDER_MODEL_ORGANISM_EXPLANATION_2"))

    st.markdown(text("HEADLINE_ILLUSTRATION"))
    st.markdown(text("EXPLANATION_ILLUSTRATION_UNITS"))
    st.markdown(text("EXPLANATION_ILLUSTRATION"))

    if language == "German":
        image1 = Image.open("pictures/Beispielabbildung_de.png")
        st.image(image1, caption=text("CAPTION_ABB1"))
    else:
        image1 = Image.open("pictures/Beispielabbildung_en.png")
        st.image(image1, caption=text("CAPTION_ABB1"))

# FIXME: language and version probably should be put into text here
def make_literature(text: Callable[[str], str], language: str, version: str) -> None:
    with st.expander(text("LITERATURE")):
        st.markdown(text("LITERATURE_DECLARATION"))
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
    text = get_localised_text("b-messmeth", version, language)
    make_page(text, language, version)
    make_literature(text, language, version)
