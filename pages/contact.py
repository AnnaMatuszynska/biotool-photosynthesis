import numpy as np
import streamlit as st
from pages._sidebar import fill_sidebar, make_sidebar
from pathlib import Path
from PIL import Image
from typing import Callable
from utils import centered_image, get_localised_text, make_prev_next_button, track_page_visit


def make_page(text: Callable[[str], str], language: str, version: str):
    # Make balloons appear the first time the final page is visited
    if st.session_state["visited_pages"].all() and "ballooned" not in st.session_state:
        st.balloons()
        st.toast(":blue[Thank you for finishing our Biotool!]", icon="🎉")
        st.session_state["ballooned"] = True

    st.header(":mailbox: Contact Us!")

    st.markdown(
        "We welcome your feedback and questions about our project! Here are the best ways to get in touch with our team members:"
    )

    st.markdown(
        "### Sarah Philipps\n"
        "- **Email:** sarah.philipps@rwth-aachen.de\n"
        "- **Topics:** education, motivation behind the platform, and general inquiries\n"
    )

    st.markdown(
        "### Tobias Pfennig\n"
        "- **Email:** tobias.pfennig@rwth-aachen.de\n"
        "- **Topics:** fluorescence measuring methods and modelling of photosynthesis\n"
        "- **Website:** [RWTH Aachen](https://www.cpbl.rwth-aachen.de/cms/CPBL/Die-Juniorprofessur/Unser/~wljpm/Tobias-Pfennig/)\n"
    )

    st.markdown(
        "### Elouën Corvest\n"
        "- **Email:** elouen.corvest@rwth-aachen.de\n"
        "- **Topics:** available computational models of photosynthesis"
        "- **Website:** [RWTH Aachen](https://www.cpbl.rwth-aachen.de/cms/CPBL/Die-Juniorprofessur/Unser/~wljuk/Elouen-Corvest/lidx/1/)\n"
    )

    st.markdown(
        "### Marvin van Aalst\n"
        "- **Email:** marvin.van.aalst@hhu.de\n"
        "- **Topics:** technical questions about the platform, programming and software development\n"
        "- **Website:** [Heinrich Heine University Duesseldorf](https://www.qtb.hhu.de/qtb-team/qtb-team-details?tt_address%5Bfunktion%5D=26702&tt_address%5Bperson%5D=21874&cHash=9ebb911fc0f89ce42ec1fd253420bca6)\n"
    )

    st.markdown(
        "### Lisa Fürtauer\n"
        "- **Email:** lisa.fuertauer@bio3.rwth-aachen.de\n"
        "- **Topics:** research on photosynthesis in the context of climat change\n"
        "- **Website:** [RWTH Aachen](https://www.bio3.rwth-aachen.de/cms/BIO3/Das-Institut/~tcejj/Juniorprofessur-Molekulare-Systembiologi/)\n"
    )

    st.markdown(
        "### Anna Matuszyńska\n"
        "- **Email:** anna.matuszynska@rwth-aachen.de\n"
        "- **Topics:** general project inquiries, computational modelling, photosynthesis\n"
        "- **Website:** [RWTH Aachen](https://www.cpbl.rwth-aachen.de/cms/CPBL/Die-Juniorprofessur/Unser/~ywkwc/Anna-Matuszy-324-ska/)\n"
    )

    st.markdown(
        "Please note that our team members may have different response times due to their schedules and \
                    responsibilities. We will do our best to respond to your messages as soon as possible."
    )

    st.markdown("Thank you for your interest in our project!")

    st.markdown("### Resources")
    st.markdown(text("PROGRAMS_USED"))


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version: str = st.session_state.setdefault("version", "4Bio")
    language: str = st.session_state.setdefault("language", "English")
    text = get_localised_text(version, language)
    placeholder_sidebar = make_sidebar()
    track_page_visit("contact")
    make_page(text, language, version)
    make_prev_next_button("take home messages", None)
    fill_sidebar(placeholder_sidebar)
