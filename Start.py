import streamlit as st
from pages._sidebar import make_sidebar
from PIL import Image
from st_pages import Page, show_pages
from typing import Callable
from utils import get_localised_text


def make_introduction(text: Callable[[str], str]) -> None:
    st.markdown(text("HEADLINE_MAIN"))
    st.markdown(text("AUTHOR"))
    st.markdown(text("INTRO"))  # added by Anna
    image1 = Image.open("pictures/Foto-Fluoreszierende_Pflanzen.jpg")
    st.image(image1, caption=text("CAPTION_ABB1"))
    st.markdown(text("MOTIVATION"))
    st.markdown(text("PROCESS"))
    st.markdown(text("CONTINUING_TASK"))
    st.markdown(text("MOTIVATION_2.0"))
    st.markdown(text("DECLARATION"))


# FIXME: version and language should probably be replaced by text
def make_chapters(text: Callable[[str], str], version: str, language: str) -> None:
    with st.expander(text("EXPANDER_PRODUCENTEN")):
        st.markdown(text("EXPANDER_PRODUCENTEN_EXPLANATION"))

    with st.expander(text("EXPANDER_NUTRIENTS")):
        st.markdown(text("EXPANDER_NUTRIENTS_EXPLANATION"))
        image = Image.open("pictures/Stomata1.jpg")
        st.image(image, caption=text("CAPTION_STOMATA_PICTURE"), width=400)  # make a caption

    with st.expander(text("EXPANDER_PHOTOSYNTHESIS")):
        st.markdown(text("EXPANDER_PHOTOSYNTHESIS_EXPLANATION_1"))
        st.markdown(text("EXPANDER_PHOTOSYNTHESIS_EXPLANATION_2"))
        if language == "German":
            image = Image.open("pictures/Fotosynthese.jpg")
            st.image(image, caption=text("CAPTION_FOTOSYNTHESE_PICTURE"))
        else:
            image = Image.open("pictures/Fotosynthese_eng.jpg")
            st.image(image, caption=text("CAPTION_FOTOSYNTHESE_PICTURE"))

    with st.expander(text("EXPANDER_PHOTOSYNTHESIS_LOCATION")):
        st.markdown(text("EXPANDER_PHOTOSYNTHESIS_LOCATION_EXPLANATION"))
        if language == "German":
            image = Image.open("pictures/Fotosynthese-Apparat.jpg")
            st.image(image, caption=text("CAPTION_FOTOSYNTHESE_APPARAT_PICTURE"), width=600)
        else:
            image = Image.open("pictures/Fotosynthese-Apparat_eng.jpg")
            st.image(image, caption=text("CAPTION_FOTOSYNTHESE_APPARAT_PICTURE"), width=600)

    with st.expander(text("EXPANDER_NPQ")):
        st.markdown(text("EXPANDER_NPQ_EXPLANATION"))
        if version == "expert":
            st.markdown(text("EXPANDER_NPQ_VIOLAXIN_EXPLANATION"))

    with st.expander(text("EXPANDER_MATHEMATICAL_MODELLING")):
        st.markdown(text("EXPANDER_MATHEMATICAL_MODELLING_EXPLANATION_1"))
        st.markdown(text("EXPANDER_MATHEMATICAL_MODELLING_EXPLANATION_2"))

    with st.expander(text("EXPANDER_DIFFERENTIAL_EQUATIONS")):
        st.markdown(text("EXPANDER_DIFFERENTIAL_EQUATIONS_EXPLANATION_1"))
        st.markdown(text("EXPANDER_DIFFERENTIAL_EQUATIONS_EXPLANATION_2"))
        st.markdown(text("EXPANDER_DIFFERENTIAL_EQUATIONS_EXPLANATION_3"))


# FIXME: version & language should probably be replaced by text
def make_credits(text: Callable[[str], str], version: str, language: str) -> None:
    st.markdown(text("CREDITS_ANNA"))

    with st.expander(text("Literature")):
        st.markdown(text("INTRODUCTION_LITERATURE"))
        if version == "expert":
            st.markdown(
                "- Stirbet, A. et al (2020). Photosynthesis: basic, history and modelling."
                "Annals of botany vol 126,4: 511-537: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7489092/"
            )
            st.markdown("- Holzner, Steven. Differential equations for dummies. John Wiley & Sons, 2008.")
        elif version == "simple":
            if language == "German":
                st.markdown(
                    "- https://simpleclub.com/lessons/biologie-fotosynthese#:~:text="
                    "Bei%20der%20Fotosynthese%20erzeugen%20gr%C3%BCne,als%20Energiequelle%20f%C3%BCr%20die%20Pflanze."
                )
            else:
                st.markdown(
                    "- Fromme, Petra, and Ingo Grotjohann. Overview of photosynthesis. Photosynthetic Protein Complexes: A \
                    Structural Approach (2008): 1-22."
                )
                st.markdown("- Holzner, Steven. Differential equations for dummies. John Wiley & Sons, 2008.")
                st.markdown(
                    "- May, Elizabeth, and John Kidder. Climate Change for Dummies. John Wiley & Sons, 2022."
                )


if __name__ == "__main__":
    st.set_page_config(layout="wide")

    version, language = make_sidebar()
    text = get_localised_text("base", version, language)

    # NOTE: this belongs with the sidebar, but works globally
    # so I'd prefer to put it here
    show_pages(
        [
            Page("Start.py", text("Start"), ":house:"),
            Page("pages/method.py", text("Method"), ":books:"),
            Page("pages/model_explain.py", text("Model"), ":computer:"),
            Page("pages/first_analysis.py", text("First analyses"), ":bar_chart:"),
            Page("pages/plant_memory.py", text("Plant memory"), ":chart_with_upwards_trend:"),
        ]
    )
    make_introduction(text)
    make_chapters(text, version, language)
    make_credits(text, version, language)


