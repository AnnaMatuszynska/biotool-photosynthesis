import gettext
import os
import streamlit as st
from PIL import Image

_ = gettext.gettext

# headline sidebar
st.sidebar.write("## Settings :gear:")

# decide which version and language
version_options = {"simple": "Simple", "expert": "Expert"}

version = st.sidebar.selectbox(
    "⚙ Version 👩‍🎓👩🏼‍🔬", version_options.keys(), format_func=lambda x: version_options[x]
)

# language selectbox
language = st.sidebar.selectbox(_("⚙ Language 🌍💬"), ["English", "German"], label_visibility="visible")
try:
    localizator = gettext.translation(
        "b-messmeth", localedir=os.path.join("locales", version), languages=[language]
    )
    localizator.install()
    _ = localizator.gettext
except:
    pass

st.markdown(_("HEADLINE_ONE"))

col1, col2, col3 = st.columns(3)
with col2:
    st.image("pictures/Kurzvideo-Messmethode.gif")

st.markdown(_("INTRODUCTION_MEASUREMENT"))  # (siehe Abbildung)

st.markdown(_("EXPLANATION_INTRODUCTION_ATTEMPTS"))

st.markdown(_("EXPLANATION_MEASUREMENT"))

st.markdown(_("EXPLANATION_ATTEMPTS"))

col1, col2, col3 = st.columns(3)
with col2:
    st.image("pictures/Arabidopsis.jpg", caption=_("CAPTION_THAIANA_PICTURE"), width=400)  # Add Caption

st.markdown(_("HEADLINE_ILLUSTRATION"))

st.markdown(_("EXPLANATION_ILLUSTRATION_UNITS"))

st.markdown(_("EXPLANATION_ILLUSTRATION"))

if language == "German":
    image1 = Image.open("pictures/Beispielabbildung_de.png")
    st.image(image1, caption=_("CAPTION_ABB1"))
else:
    image1 = Image.open("pictures/Beispielabbildung_en.png")
    st.image(image1, caption=_("CAPTION_ABB1"))

if version == "expert":
    with st.expander(_("EXPANDER_MODEL_EQUATIONS")):
        st.markdown(_("EXPANDER_MODEL_EQUATIONS_EXPLANATION"))
        st.markdown(_("EQUATION_LIST_1"))
        st.markdown(_("EQUATION_LIST_2"))
        st.markdown(_("EQUATION_LIST_3"))
        st.markdown(_("EQUATION_LIST_4"))
        st.markdown(_("EQUATION_LIST_5"))
        st.markdown(_("EQUATION_LIST_6"))

with st.expander(_("LITERATURE")):
    st.markdown(_("LITERATURE_DECLARATION"))
    if version == "expert":
        """
        - Nies, T. et al (2021). Chlorophyll fluorescence: How the quality of information about PAM instrument parameters may affect our research. https://www.biorxiv.org/content/10.1101/2021.05.12.443801v1.full
        """
    elif version == "simple":
        """
        - https://link.springer.com/referenceworkentry/10.1007/978-3-662-53493-9_13-1
        """
