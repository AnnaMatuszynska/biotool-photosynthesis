import base64
import gettext
import os
import streamlit as st
from logging import getLogger
from pathlib import Path
from streamlit_extras.switch_page_button import switch_page
from typing import Callable
import json
from st_click_detector import click_detector
import re
import warnings

def get_localised_text(version: str, language: str) -> Callable[[str], str]:
    version = version.lower()
    try:
        localizator = gettext.translation(
            "main", localedir=os.path.join("locales", version), languages=[language]
        )
        localizator.install()
        return localizator.gettext
    except:
        getLogger().warning(f"Could not find locale for language {language} and version {version}")
        return gettext.gettext


def make_prev_next_button(prev: str | None, next: str | None) -> None:
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button(
            "Previous",
            disabled=True if prev is None else False,
            use_container_width=True,
        ):
            if prev is not None:
                switch_page(prev)
    with col2:
        if st.button(
            "Next",
            disabled=True if next is None else False,
            use_container_width=True,
        ):
            if next is not None:
                switch_page(next)


def centered_image(img_path: str) -> None:
    st.markdown(
        f"""
        <p style='text-align: center'>
            <img
                src='data:image/png;base64,{base64.b64encode(Path(img_path).read_bytes()).decode()}'
                class='img-fluid'
                style='max-width: 100%'
            />
        </p>
        """,
        unsafe_allow_html=True,
    )


def include_ytvideo(yt_url: str, vid_width: float = 0.5) -> None:
    if vid_width > 1 or vid_width < 0:
        raise Exception("vid_width has to be between 0 and 1")

    if vid_width != 1:
        nonvid_width = (1 - vid_width) / 2
        _, col2, _ = st.columns([nonvid_width, vid_width, nonvid_width])

        with col2:
            st.video(yt_url)

    else:
        st.video(yt_url)


def include_image(path: str, img_width: float = 0.5, caption: str = None, center_caption: bool=False) -> None:
    """Function to include image in streamlit page with specific width and caption

    Args:
        path (str): Path to the image
        img_width (float, optional): Value between 0 and 1 for the percentage the img takes. Defaults to 0.5.
        caption (str, optional): Text for the caption in format text("EXAMPLE"). Defaults to None.
    """
    if img_width > 1 or img_width < 0:
        raise Exception("img_width has to be between 0 and 1")

    if img_width != 1:
        nonimg_width = (1 - img_width) / 2
        _, col2, _ = st.columns([nonimg_width, img_width, nonimg_width])

        with col2:
            st.image(path, use_column_width=True)

            if caption is not None:
                if center_caption == True:
                    st.caption(
                        f"""
                        <p style='text-align: center'>
                            {caption}
                        </p>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.caption(caption, unsafe_allow_html=True)

    else:
        st.image(path, use_column_width=True)

        if caption is not None:
                if center_caption == True:
                    st.caption(
                        f"""
                        <p style='text-align: center'>
                            {caption}
                        </p>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.caption(caption, unsafe_allow_html=True)

def js_r(filename: str):
    with open(filename, encoding='utf8') as f_in:
        return json.load(f_in)
icons = js_r("assets/emoji.json")

def resetting_click_detector_setup():
    # Implement a counter for the runs
    st.session_state.setdefault("_rcd#", 0)
    st.session_state["_rcd#"] += 1
    del_keys = [x for x in st.session_state.keys() if x.startswith("_rcd_") and re.search('[0-9]+$', x) and int(re.search('([0-9]+)$', x).group(1)) < st.session_state["_rcd#"]-1]
    if len(del_keys) > 0:
        for key in del_keys:
            del st.session_state[key]

def resetting_click_detector(content, key="_"):
    old_key = f"_rcd_{key}_{st.session_state['_rcd#']-1}"
    new_key = f"_rcd_{key}_{st.session_state['_rcd#']}"
    clicked = st.session_state.setdefault(old_key, "")
    del st.session_state[old_key]
    _ = click_detector(content, key=new_key)
    return clicked

def markdown_click(placeholder, text_obj, detector_key=None, unsafe_allow_html=False):
    """Automatically a click detector and set the version if applicable.

    Args:
        text (str): text to be displayed and possibly click-checked
        detector_key (Any, optional): key for the detector in session state. Defaults to None and sets it with the text's hash.
        allow_unsafe_html (Any): argument for st.markdown

    Returns:
        None or str: id of the clicked text otherwise None
    """
    text = text_obj(placeholder)
    if re.search("<a href='#'",text):
        clicked = resetting_click_detector(text, placeholder if detector_key is None else detector_key)
        if re.search("<a href='#' id='4STEM'|<a href='#' id='4Bio'", text) and clicked in ["4STEM","4Bio"]:
            st.session_state.version = clicked
            st.experimental_rerun()
        return clicked
    else:
        st.markdown(text, unsafe_allow_html=unsafe_allow_html)
        return None

def simulate_period(s, starting_time, length_phase, pulse_intervall, starting_light, saturating_pulse, length_pulse, during_light, dark_flag = False):
    warnings.filterwarnings("error", category= RuntimeWarning)
    error_flag = True
    
    while error_flag == True:
        try:
            s.update_parameter("PFD", starting_light)
            s.simulate(starting_time)
            s.update_parameter("PFD", saturating_pulse)
            s.simulate(starting_time + length_pulse)
            
            warnings.filterwarnings("default", category= RuntimeWarning)
            error_flag = False
        except RuntimeWarning:
            starting_light += 0.001
            
    
    num_pulses = int(length_phase/pulse_intervall)
            
    if dark_flag == False:
        for i in range(num_pulses):
            if i > 0:
                new_timepoint = starting_time + pulse_intervall * i
                s.update_parameter("PFD", during_light)
                s.simulate(new_timepoint)
                s.update_parameter("PFD", saturating_pulse)
                s.simulate(new_timepoint + length_pulse)
            
    return