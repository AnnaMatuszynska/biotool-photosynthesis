import streamlit as st
from typing import cast

# from utils import get_localised_text


def make_sidebar() -> tuple[str, str]:
    st.sidebar.write("## Settings :gear:")

    # Versions selectbox
    versions = ["Simple", "Advanced"]
    version_to_idx = dict(zip(versions, range(len(versions))))
    version = cast(
        str,
        st.sidebar.selectbox(
            label="⚙ Version 👩‍🎓👩🏼‍🔬",
            options=versions,
            index=version_to_idx[st.session_state["version"]],
        ),
    )

    # language selectbox
    languages = ["English", "German", "Polish", "French", "Spanish"]
    language_to_idx = dict(zip(languages, range(len(languages))))
    language = cast(
        str,
        st.sidebar.selectbox(
            label="⚙ Language 🌍💬",
            options=languages,
            index=language_to_idx[st.session_state["language"]],
            # label_visibility="visible",
        ),
    )
    return version, language


if __name__ == "__main__":
    make_sidebar()
