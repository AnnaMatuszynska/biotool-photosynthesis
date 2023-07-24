import base64
import gettext
import os
import streamlit as st
from logging import getLogger
from pathlib import Path
from streamlit_extras.switch_page_button import switch_page
from typing import Callable
import json


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