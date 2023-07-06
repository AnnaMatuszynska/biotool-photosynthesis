import streamlit as st
from typing import cast

# FIXME: this should probably be external data?
VERSION_OPTIONS = {"simple": "Simple", "expert": "Advanced"}


def make_sidebar() -> tuple[str, str]:
    st.sidebar.write("## Settings :gear:")

    version: str = cast(
        str,
        st.sidebar.selectbox(
            "⚙ Version 👩‍🎓👩🏼‍🔬",
            VERSION_OPTIONS.keys(),
            format_func=lambda x: VERSION_OPTIONS[x],
        ),
    )

    # language selectbox
    language: str = cast(
        str,
        st.sidebar.selectbox(
            "⚙ Language 🌍💬",
            ["English", "German"],
            label_visibility="visible",
        ),
    )
    return version, language


if __name__ == "__main__":
    make_sidebar()
