import streamlit as st
from pages._sidebar import fill_sidebar, make_sidebar
from PIL import Image
from typing import Callable
from utils import (
    get_localised_text,
    include_image,
    include_ytvideo,
    make_prev_next_button,
    markdown_click,
    resetting_click_detector_setup,
    track_page_visit,
)


# FIXME: language and version probably should be put into text here
def make_page(text: Callable[[str], str], language: str, version: str) -> None:
    st.markdown(text("MTH_HEADLINE_ONE"))

    # Learning objectives
    st.info(text("MTH_LEARNING_OBJECTIVES"))
    make_prev_next_button(
        text,
        text("SDE_PAGENAMES_PHOTOSYNTHESIS"),
        text("SDE_PAGENAMES_COMPUTATIONALMODELS"),
        key="mth_learning_objectives",
    )

    _, col2, _ = st.columns(3)
    with col2:
        st.image("pictures/Kurzvideo-Messmethode.gif")

    st.markdown(text("MTH_INTRODUCTION_MEASUREMENT"), unsafe_allow_html=True)

    st.image(Image.open("pictures/Foto-Fluoreszierende_Pflanzen.jpg"))
    st.caption(text("MTH_CAPTION_ABB1"))

    with st.expander(text("MTH_GROWING_PLANTS_1"), expanded=True):
        st.markdown(text("MTH_INTRODUCTION_GLOWING"), unsafe_allow_html=True)
        st.markdown(text("MTH_PLANT_ARE_SHINING_RED"), unsafe_allow_html=True)
        st.markdown(text("MTH_INTRODUCTION_EXPERIMENT"), unsafe_allow_html=True)

        include_ytvideo("https://youtu.be/g3uTNWsDEdo", 0.9)

        st.markdown(text("MTH_EXPLANATION_VIDEO"), unsafe_allow_html=True)

    with st.expander(text("MTH_MEASURING_FLUORESZENZ"), expanded=True):
        markdown_click("MTH_EXPLANATION_MEASUREMENT_1", text)
        st.markdown(text("MTH_INTRODUCTION_PHI"), unsafe_allow_html=True)
        include_ytvideo("https://youtu.be/EwXkOlMBl3o", 0.9)

    if st.session_state["show_video_transcripts"]:
        with st.expander(text("EXPANDER_VIDEO_TRANSCRIPT")):
            st.write(text("MTH_VIDEO_TRANSCRIPT_PAM"))

    st.markdown(text("MTH_HEADLINE_PAM_MEASUREMENT"), unsafe_allow_html=True)
    st.markdown(text("MTH_INTRODUCTION_PAM_MEASUREMENT"), unsafe_allow_html=True)

    with st.expander(text("MTH_MEASURING_LIGHT_FLUORESCENCE"), expanded=True):
        st.markdown(text("MTH_EXPLANATION_INTRODUCTION_ATTEMPTS"))
        include_image(
            "pictures/PAMbasics.png", img_width=1, caption=text("MTH_CAPTION_ABB2"), center_caption=True
        )

    # if version == "4Bio":
    #     with st.expander(text("MTH_SATURATING_PULSES")):
    #         st.markdown(text("MTH_EXPLANATION_ATTEMPTS"), unsafe_allow_html=True)

    st.markdown(text("MTH_HEADLINE_ILLUSTRATION"), unsafe_allow_html=True)
    st.markdown(text("MTH_EXPLANATION_ILLUSTRATION_UNITS"), unsafe_allow_html=True)
    st.markdown(text("MTH_EXPLANATION_ILLUSTRATION"), unsafe_allow_html=True)

    if language == "German":
        include_image(
            "pictures/Beispielabbildung_de.png",
            img_width=1,
            caption=text("MTH_CAPTION_ABB2"),
            center_caption=True,
        )
    else:
        include_image(
            "pictures/Beispielabbildung_en.png",
            img_width=1,
            caption=text("MTH_CAPTION_ABB2"),
            center_caption=True,
        )


# FIXME: language and version probably should be put into text here
def make_literature(text: Callable[[str], str], language: str, version: str) -> None:
    with st.expander(text("LITERATURE")):
        st.markdown(text("MTH_LITERATURE_DECLARATION"), unsafe_allow_html=True)
        if version == "4Bio":
            """
            - Brooks, M. D., & Niyogi, K. K. (2011). Use of a pulse-amplitude modulated chlorophyll fluorometer to study the efficiency of photosynthesis in Arabidopsis plants. Chloroplast Research in Arabidopsis: Methods and Protocols, Volume II, 299-310. https://link.springer.com/protocol/10.1007/978-1-61779-237-3_16
            """
            """
            - Nies, T., Niu, Y., Ebenhöh, O., Matsubara, S., & Matuszyńska, A. (2021). Chlorophyll fluorescence: How the quality of information about PAM instrument parameters may affect our research (p. 2021.05.12.443801). bioRxiv. https://doi.org/10.1101/2021.05.12.443801

            """
        elif version == "4Math":
            if language == "German":
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
    st.set_page_config(layout="wide")
    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version: str = st.session_state.setdefault("version", "4Bio")
    language: str = st.session_state.setdefault("language", "English")
    text = get_localised_text(version, language)
    placeholder_sidebar = make_sidebar()
    resetting_click_detector_setup()
    track_page_visit("method")
    make_page(text, language, version)
    make_literature(text, language, version)
    make_prev_next_button(
        text,
        text("SDE_PAGENAMES_PHOTOSYNTHESIS"),
        text("SDE_PAGENAMES_COMPUTATIONALMODELS"),
    )
    fill_sidebar(placeholder_sidebar)
