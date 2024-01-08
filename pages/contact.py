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

    st.header(":mailbox: " + text("CONT_HEADER"))

    st.markdown(text("CONT_SUBHEADER"))

    st.markdown(
        "### Sarah Philipps\n"
        f"- **{text('CONT_EMAIL')}** sarah.philipps@rwth-aachen.de\n"
        f"- **{text('CONT_TOPICS')}** {text('CONT_TOPICS_SARAH')}\n"
    )

    st.markdown(
        "### Tobias Pfennig\n"
        f"- **{text('CONT_EMAIL')}** tobias.pfennig@rwth-aachen.de\n"
        f"- **{text('CONT_TOPICS')}** {text('CONT_TOPICS_TOBIAS')}\n"
        f"- **{text('CONT_WEBSITE')}** [RWTH Aachen](https://www.cpbl.rwth-aachen.de/cms/CPBL/Die-Juniorprofessur/Unser/~wljpm/Tobias-Pfennig/)\n"
    )

    st.markdown(
        "### Elouen Corvest\n"
        f"- **{text('CONT_EMAIL')}** elouen.corvest@rwth-aachen.de\n"
        f"- **{text('CONT_TOPICS')}** {text('CONT_TOPICS_ELOUEN')}\n"
        f"- **{text('CONT_WEBSITE')}** [RWTH Aachen](https://www.cpbl.rwth-aachen.de/cms/CPBL/Die-Juniorprofessur/Unser/~wljuk/Elouen-Corvest/lidx/1/)\n"
    )

    st.markdown(
        "### Marvin van Aalst\n"
        f"- **{text('CONT_EMAIL')}** marvin.van.aalst@hhu.de\n"
        f"- **{text('CONT_TOPICS')}** {text('CONT_TOPICS_MARVIN')}\n"
        f"- **{text('CONT_WEBSITE')}** [Heinrich Heine University Duesseldorf](https://www.qtb.hhu.de/qtb-team/qtb-team-details?tt_address%5Bfunktion%5D=26702&tt_address%5Bperson%5D=21874&cHash=9ebb911fc0f89ce42ec1fd253420bca6)\n"
    )

    st.markdown(
        "### Lisa Fürtauer\n"
        f"- **{text('CONT_EMAIL')}** lisa.fuertauer@bio3.rwth-aachen.de\n"
        f"- **{text('CONT_TOPICS')}** {text('CONT_TOPICS_LISA')}\n"
        f"- **{text('CONT_WEBSITE')}** [RWTH Aachen](https://www.bio3.rwth-aachen.de/cms/BIO3/Das-Institut/~tcejj/Juniorprofessur-Molekulare-Systembiologi/)\n"
    )

    st.markdown(
        "### Anna Matuszyńska\n"
        f"- **{text('CONT_EMAIL')}** anna.matuszynska@rwth-aachen.de\n"
        f"- **{text('CONT_TOPICS')}** {text('CONT_TOPICS_ANNA')}\n"
        f"- **{text('CONT_WEBSITE')}** [RWTH Aachen](https://www.cpbl.rwth-aachen.de/cms/CPBL/Die-Juniorprofessur/Unser/~ywkwc/Anna-Matuszy-324-ska/)\n"
    )

    st.markdown(text("CONT_HOURS"))

    st.markdown(text("CONT_THANKS"))
    
    with st.expander(label=text("CONT_CITE")):
        st.markdown('Computational Photosynthesis (ComPhot): Simulation-Based Learning Platform to Study Photosynthesis, The Plant Cell, 2024')
        style_select = st.selectbox(
            label=text("CONT_STYLE"),
            options = ['BibTeX', 'RIS', 'EndNote'],
            index=None
        )
        
        if style_select == 'BibTeX':
            with open("cite_files/ComPhot.bib", "r") as file:
                start_flag = False
                data = ''''''
                for line in file:
                    data += line
                download_cite = st.download_button(
                        label="Download BibTeX",
                        data=file,
                        file_name="ComPhot.bib"
                    )
                st.code(data)
        
        elif style_select == 'RIS':
            with open("cite_files/ComPhot.ris", "r") as file:
                data = ''''''
                for line in file:
                    data += line
                download_cite = st.download_button(
                        label="Download RIS",
                        data=file,
                        file_name="ComPhot.ris"
                    )
                st.code(data)
                
        elif style_select == 'EndNote':
            with open("cite_files/ComPhot.enw", "r") as file:
                data = ''''''
                for line in file:
                    data += line
                download_cite = st.download_button(
                        label="Download EndNote Format",
                        data=file,
                        file_name="ComPhot.enw"
                    )
                st.code(data)

    st.markdown(text("CONT_RESOURCES"))
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
    make_prev_next_button(text, text("SDE_PAGENAMES_CONCLUSION"), None)
    fill_sidebar(placeholder_sidebar)
