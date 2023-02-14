import streamlit as st
from typing import cast

# headline sidebar
st.sidebar.write("## Settings :gear:")

# decide which version and language
version_options = {"simple": "Simple", "expert": "Expert"}


version: str = cast(
    str,
    st.sidebar.selectbox(
        "⚙ Version 👩‍🎓👩🏼‍🔬",
        version_options.keys(),
        format_func=lambda x: version_options[x],
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
