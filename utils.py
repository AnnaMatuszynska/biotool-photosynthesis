import gettext
import os
import streamlit as st
from logging import getLogger
from streamlit_extras.switch_page_button import switch_page
from typing import Callable


def get_localised_text(domain: str, version: str, language: str) -> Callable[[str], str]:
    try:
        localizator = gettext.translation(
            domain, localedir=os.path.join("locales", version), languages=[language]
        )
        localizator.install()
        getLogger().warning(f"Using locale {language} and version {version}")
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
