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
        "b-model", localedir=os.path.join("locales", version), languages=[language]
    )
    localizator.install()
    _ = localizator.gettext
except:
    pass

st.markdown(_("HEADLINE_MODEL"))

st.markdown(_("INTRODUCTION_CLIMATE_CHANCE"))

if version == "expert":
    st.markdown(_("POINT_1"))
    st.markdown(_("POINT_2"))
    st.markdown(_("POINT_3"))
    st.markdown(_("END_OF_INTRODUCTION"))

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

with st.expander(_("LITERATURE")):
    st.markdown(_("LITERATURE_DECLARATION"))
    if version == "expert":
        """
        - Cook J, Oreskes N, Doran PT, Anderegg WR, Verheggen B, Maibach EW, Carlton JS, Lewandowsky S, Skuce AG, Green SA (2016) Consensus on consensus: a synthesis of consensus estimates on human-caused global warming. J Environmental Research Letters 11: 048002
        """