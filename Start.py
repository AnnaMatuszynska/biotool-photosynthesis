import streamlit as st
from pages._sidebar import make_sidebar
from PIL import Image
from st_pages import Page, show_pages
from typing import Callable
from utils import get_localised_text


def make_introduction(_: Callable[[str], str]) -> None:
    st.markdown(_("HEADLINE_MAIN"))
    st.markdown(_("AUTHOR"))
    st.markdown(_("INTRO"))  # added by Anna
    image1 = Image.open("pictures/Foto-Fluoreszierende_Pflanzen.jpg")
    st.image(image1, caption=_("CAPTION_ABB1"))
    st.markdown(_("MOTIVATION"))
    st.markdown(_("PROCESS"))
    st.markdown(_("CONTINUING_TASK"))
    st.markdown(_("MOTIVATION_2.0"))
    st.markdown(_("DECLARATION"))


# FIXME: version and language should probably be replaced by _
def make_chapters(_: Callable[[str], str], version: str, language: str) -> None:
    with st.expander(_("EXPANDER_PRODUCENTEN")):
        st.markdown(_("EXPANDER_PRODUCENTEN_EXPLANATION"))

    with st.expander(_("EXPANDER_NUTRIENTS")):
        st.markdown(_("EXPANDER_NUTRIENTS_EXPLANATION"))
        image = Image.open("pictures/Stomata1.jpg")
        st.image(image, caption=_("CAPTION_STOMATA_PICTURE"), width=400)  # make a caption

    with st.expander(_("EXPANDER_PHOTOSYNTHESIS")):
        st.markdown(_("EXPANDER_PHOTOSYNTHESIS_EXPLANATION_1"))
        st.markdown(_("EXPANDER_PHOTOSYNTHESIS_EXPLANATION_2"))
        if language == "German":
            image = Image.open("pictures/Fotosynthese.jpg")
            st.image(image, caption=_("CAPTION_FOTOSYNTHESE_PICTURE"))
        else:
            image = Image.open("pictures/Fotosynthese_eng.jpg")
            st.image(image, caption=_("CAPTION_FOTOSYNTHESE_PICTURE"))

    with st.expander(_("EXPANDER_PHOTOSYNTHESIS_LOCATION")):
        st.markdown(_("EXPANDER_PHOTOSYNTHESIS_LOCATION_EXPLANATION"))
        if language == "German":
            image = Image.open("pictures/Fotosynthese-Apparat.jpg")
            st.image(image, caption=_("CAPTION_FOTOSYNTHESE_APPARAT_PICTURE"), width=600)
        else:
            image = Image.open("pictures/Fotosynthese-Apparat_eng.jpg")
            st.image(image, caption=_("CAPTION_FOTOSYNTHESE_APPARAT_PICTURE"), width=600)

    with st.expander(_("EXPANDER_NPQ")):
        st.markdown(_("EXPANDER_NPQ_EXPLANATION"))
        if version == "expert":
            st.markdown(_("EXPANDER_NPQ_VIOLAXIN_EXPLANATION"))

    with st.expander(_("EXPANDER_MATHEMATICAL_MODELLING")):
        st.markdown(_("EXPANDER_MATHEMATICAL_MODELLING_EXPLANATION_1"))
        st.markdown(_("EXPANDER_MATHEMATICAL_MODELLING_EXPLANATION_2"))

    with st.expander(_("EXPANDER_DIFFERENTIAL_EQUATIONS")):
        st.markdown(_("EXPANDER_DIFFERENTIAL_EQUATIONS_EXPLANATION_1"))
        st.markdown(_("EXPANDER_DIFFERENTIAL_EQUATIONS_EXPLANATION_2"))
        st.markdown(_("EXPANDER_DIFFERENTIAL_EQUATIONS_EXPLANATION_3"))


# FIXME: version & language should probably be replaced by _
def make_credits(_: Callable[[str], str], version: str, language: str) -> None:
    st.markdown(_("CREDITS_ANNA"))

    with st.expander(_("Literature")):
        st.markdown(_("INTRODUCTION_LITERATURE"))
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
    _ = get_localised_text("base", version, language)

    # NOTE: this belongs with the sidebar, but works globally
    # so I'd prefer to put it here
    show_pages(
        [
            Page("Start.py", _("Start"), ":house:"),
            Page("pages/method.py", _("Method"), ":books:"),
            Page("pages/first_analysis.py", _("First analyses"), ":chart_with_upwards_trend:"),
            Page("pages/plant_memory.py", _("Plant memory"), ":chart_with_downwards_trend:"),
        ]
    )
    make_introduction(_)
    make_chapters(_, version, language)
    make_credits(_, version, language)
