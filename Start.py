import gettext
import os
import streamlit as st
from PIL import Image
from st_pages import Page, show_pages

_ = gettext.gettext

# wide mode on and change page name
st.set_page_config(layout="wide")

# headline sidebar
st.sidebar.write("## Settings :gear:")

# decide which version and language
version_options = {"simple": "Simple", "expert": "Expert"}

version = st.sidebar.selectbox(
    "⚙ Version 👩‍🎓👩🏼‍🔬", version_options.keys(), format_func=lambda x: version_options[x]
)

# language selectbox
language = st.sidebar.selectbox("⚙ Language 🌍💬", ["English", "German"], label_visibility="visible")
try:
    localizator = gettext.translation(
        "base", localedir=os.path.join("locales", version), languages=[language]
    )
    localizator.install()
    _ = localizator.gettext
except:
    pass

# Specify what pages should be shown in the sidebar, and what their titles
# and icons should be
show_pages(
    [
        Page("Start.py", _("Start"), ":house:"),
        Page("pages/method.py", _("Method"), ":books:"),
        Page("pages/analyse.py", _("First analyses"), ":chart_with_upwards_trend:"),
        Page("pages/brain.py", _("Plant memory"), ":chart_with_downwards_trend:"),
    ]
)

##############-Try-Zone-Begin-#############################


##############-Try-Zone-End-#############################

# ui
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

# -*- coding: cp852 -*-             # für Umlaute
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

st.markdown(_("CREDITS_ANNA"))

with st.expander(_("Literature")):
    st.markdown(_("INTRODUCTION_LITERATURE"))
    if version == "expert":
        st.markdown(
            "- Stirbet, A. et al (2020). Photosynthesis: basic, history and modelling."
            "Annals of botany vol 126,4: 511-537: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7489092/"
        )
        st.markdown(
            "- Holzner, Steven. Differential equations for dummies. John Wiley & Sons, 2008."
        )
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
            st.markdown(
                "- Holzner, Steven. Differential equations for dummies. John Wiley & Sons, 2008."
            )
            st.markdown(
                "- May, Elizabeth, and John Kidder. Climate Change for Dummies. John Wiley & Sons, 2022."
            )
