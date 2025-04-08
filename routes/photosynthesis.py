from typing import Callable

import streamlit as st

from utils import (
    centered_image,
    get_localised_text,
    include_image,
    include_ytvideo,
    make_prev_next_button,
    markdown_click,
    resetting_click_detector_setup,
    track_page_visit,
)


def make_page(text: Callable[[str], str], language: str, version: str) -> None:
    markdown_click("PHO_HEADLINE_PHOTOSYNTHESIS_PAGE", text)

    # Learning objectives
    st.info(text("PHO_LEARNING_OBJECTIVES"))
    make_prev_next_button(
        text,
        "routes/home.py",
        "routes/method.py",
        key="upper_nav_button",
    )

    markdown_click("PHO_HEADLINE_CLIMATE", text)
    markdown_click("PHO_INTRODUCTION_CLIMATE_CHANGE", text)

    if version == "4Math":
        col1, col2 = st.columns(2)
        with col1:
            if language == "German":
                centered_image("pictures/pflanzen_grundlagen.jpeg")
            if language == "English":
                centered_image("pictures/plants_basics.jpeg")
        with col2:
            if language == "German":
                centered_image("pictures/pflanzen_stress.jpeg")
            if language == "English":
                centered_image("pictures/plants_stress.jpeg")

    else:
        markdown_click("PHO_POINT_1", text)
        markdown_click("PHO_POINT_2", text)
        markdown_click("PHO_POINT_3", text)
        markdown_click("PHO_END_OF_INTRODUCTION", text)

    markdown_click("PHO_HEADLINE_PHOTOSYNTHESIS", text)
    markdown_click("PHO_PHOTOSYNTHESIS_EXPLANATION_1", text)
    markdown_click("PHO_PHOTOSYNTHESIS_EXPLANATION_2", text, unsafe_allow_html=True)

    if language == "German":
        include_image("pictures/Fotosynthese.jpg", 0.6, text("PHO_CAPTION_FOTOSYNTHESE_PICTURE"), True)
    else:
        include_image("pictures/Fotosynthese_eng.jpg", 0.8, text("PHO_CAPTION_FOTOSYNTHESE_PICTURE"), True)

    markdown_click("PHO_HEADLINE_PHOTOSYNTHESIS_LOCATION", text)
    markdown_click("PHO_PHOTOSYNTHESIS_LOCATION_EXPLANATION", text)
    include_image("pictures/phot_place_upper.PNG", 0.8, text("PHO_CAPTION_FOTOSYNTHESE_LEAF_ZOOM"), True)

    if language == "German":
        include_image(
            "pictures/Fotosynthese-Apparat.jpg", 0.6, text("PHO_CAPTION_FOTOSYNTHESE_APPARAT_PICTURE"), True
        )
    else:
        include_image(
            "pictures/NPQphotosynthesis.png", 0.6, text("PHO_CAPTION_FOTOSYNTHESE_APPARAT_PICTURE"), True
        )

    markdown_click("PHO_PHOTOSYNTHESIS_LOCATION_CONTINUE", text)

    # Journey into leaf
    include_ytvideo("https://youtu.be/hMCA0bBVoxE", 0.9)
    if st.session_state["show_video_transcripts"]:
        with st.expander(text("EXPANDER_VIDEO_TRANSCRIPT")):
            st.write(text("PHO_VIDEO_TRANSCRIPT_JOURNEY"))

    markdown_click("PHO_HEADLINE_NPQ", text)
    markdown_click("PHO_NPQ_EXPLANATION", text)

    # Explanation of NPQ
    st.info(text("PHO_NPQ_EXPLANATION_DETAILED"))

    markdown_click("PHO_NPQ_EXPLANATION_CONTINUED", text)

    include_image("pictures/Violaxanthin Scheme-4.png", 0.8, text("PHO_CAPTION_NPQ"))

    markdown_click("PHO_HEADER_MODEL_ORGANISMEN", text)
    markdown_click("PHO_MODEL_ORGANISMEN_EXPLANATION", text)

    with st.expander(text("PHO_EXPANDER_MODEL_ORGANISMEN")):
        _, col2, _ = st.columns(3)
        with col2:
            st.image("pictures/Arabidopsis.jpg", width=400)  # Add Caption
            st.caption(text("PHO_CAPTION_THAIANA_PICTURE"))
        st.markdown(text("PHO_EXPANDER_MODEL_ORGANISM_EXPLANATION"), unsafe_allow_html=True)


def make_literature(text: Callable[[str], str], language: str, version: str) -> None:
    if version == "4Bio":
        with st.expander(text("LITERATURE")):
            st.markdown(text("LITERATURE_ONPAGE"))
            st.markdown(
                "- Cook, J., Oreskes, N., Doran, P. T., Anderegg, W. R. L., Verheggen, B., Maibach, E. W., Carlton, J. S., Lewandowsky, S., Skuce, A. G., Green, S. A., Nuccitelli, D., Jacobs, P., Richardson, M., Winkler, B., Painting, R., & Rice, K. (2016). Consensus on consensus: A synthesis of consensus estimates on human-caused global warming. Environmental Research Letters, 11(4), 048002. https://doi.org/10.1088/1748-9326/11/4/048002"
            )


if __name__ == "__main__":
    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version: str = st.session_state.setdefault("version", "4Bio")
    language: str = st.session_state.setdefault("language", "English")

    text = get_localised_text(version, language)

    resetting_click_detector_setup()
    track_page_visit("photosynthesis")
    make_page(text, language, version)
    make_literature(text, language, version)
    make_prev_next_button(
        text,
        "routes/home.py",
        "routes/method.py",
        key="lower_nav_button",
    )
