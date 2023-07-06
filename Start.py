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
    st.video("https://youtu.be/pqFOIhzmGuk")
    st.markdown(text("HEADLINE_USAGE"))
    st.markdown(text("MOTIVATION"))
    st.markdown(text("PROCESS"))
    st.markdown(text("CONTINUING_TASK"))
    st.markdown(text("MOTIVATION_2.0"))
    st.markdown(text("DECLARATION"))


# FIXME: version and language should probably be replaced by text
def make_chapters(text: Callable[[str], str], version: str, language: str) -> None:
    with st.expander(text("EXPANDER_CLIMATE")):
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

        st.video("https://youtu.be/BU-R724Jyng")

    #    with st.expander(text("EXPANDER_NPQ")):
    #        st.markdown(text("EXPANDER_NPQ_EXPLANATION"))
    #        if version == "expert":
    #            st.markdown(text("EXPANDER_NPQ_VIOLAXIN_EXPLANATION"))

    with st.expander(text("EXPANDER_MATHEMATICAL_MODELLING")):
        st.markdown(text("EXPANDER_MATHEMATICAL_MODELLING_EXPLANATION_1"))
        st.markdown(text("EXPANDER_MATHEMATICAL_MODELLING_EXPLANATION_2"))
        st.video("https://youtu.be/WU5pUy2wtrk")

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

    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version, language = make_sidebar()
    text = get_localised_text("base", version, language)

    # NOTE: this belongs with the sidebar, but works globally
    # so I'd prefer to put it here
    show_pages(
        [
            Page(
                "Start.py",
                text("START"),
                ":house:",
            ),
            Page(
                "pages/photosynthesis.py",
                text("PHOTOSYNTHESIS"),
                ":potted_plant:",
            ),
            Page(
                "pages/method.py",
                text("METHOD"),
                ":books:",
            ),
            Page(
                "pages/model_explain.py",
                text("MODELS"),
                ":computer:",
            ),
            Page(
                "pages/first_analysis.py",
                text("EXPERIMENTS"),
                ":bar_chart:",
            ),
            Page(
                "pages/plant_memory.py",
                text("MEMORY"),
                ":chart_with_upwards_trend:",
            ),
            Page(
                "pages/contact.py",
                text("CONTACT"),
                ":phone:",
            ),
        ]
    )
    make_introduction(text)
    make_chapters(text, version, language)
    make_credits(text, version, language)
