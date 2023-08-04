import streamlit as st
from pages._sidebar import make_sidebar
from pathlib import Path
from PIL import Image
from typing import Callable
from utils import (
    centered_image,
    get_localised_text,
    include_image,
    include_ytvideo,
    make_prev_next_button,
    resetting_click_detector_setup,
    markdown_click
)


def make_page(text: Callable[[str], str], language: str, version: str) -> None:
    st.markdown(text("HEADLINE_COMPUTATIONAL_MODELS"))

    st.markdown(text("HEADLINE_MODEL"))

    st.markdown(text("MATHEMATICAL_MODELLING_EXPLANATION_1"))

    include_image(
        path="pictures/Modeling_scheme_eng.png", img_width=0.8, caption=text("CAPTION_MODELLING_PICTURE")
    )

    st.markdown(text("MATHEMATICAL_MODELLING_EXPLANATION_1b"))

    # Making a model
    include_ytvideo("https://youtu.be/oVME5KIHrO8")

    st.markdown(text("EXAMPLE_MATHEMATICAL_MODEL"))

    if version == "Simple":
        tab1, tab2 = st.tabs([text("TAB_SIR"), " "])

    if version == "Advanced":
        tab1, tab2, tab3 = st.tabs([text("TAB_SIR"), text("TAB_MANUAL"), text("TAB_MODELBASE")])

    with tab1:
        st.markdown(text("HEADLINE_SIR"))

        st.markdown(text("MATHEMATICAL_MODELLING_EXAMPLE"), unsafe_allow_html=True)
        st.latex(
            r"""
            \mathrm{S} \xrightarrow{\textit{v}_1} \mathrm{I} \xrightarrow{\textit{v}_2} \mathrm{R}
            """
        )
        st.latex(
            r"""
            \begin{aligned}
                v_1 &= \beta \cdot \frac{\mathrm{S}\cdot \mathrm{I}}{\mathrm{N}} \\
                v_2 &= \gamma \cdot \mathrm{I} \\
            \end{aligned}
            """
        )
        st.markdown(text("MATHEMATICAL_MODELLING_EXAMPLE_2"))
        st.latex(
            r"""
            \mathrm{S} \xrightarrow{\textit{v}_1} \mathrm{I} \xrightarrow{\textit{v}_2} \mathrm{R}
            """
        )
        st.latex(
            r"""
            \begin{aligned}
                \frac{\mathrm{d}\mathrm{S}}{\mathrm{d}t} &= - v_1 \\
                \frac{\mathrm{d}\mathrm{I}}{\mathrm{d}t} &= v_1 - v_2 \\
                \frac{\mathrm{d}\mathrm{R}}{\mathrm{d}t} &=  v_2
            \end{aligned}
            """
        )
        st.markdown(text("MATHEMATICAL_MODELLING_EXAMPLE_3"))

        include_image(
            "pictures/SIR_modelbase.png", img_width=0.6, caption=text("CAPTION_SIR_RESULTS_PICTURE")
        )

        if version == "Simple":
            markdown_click("MATHEMATICAL_MODELLING_EXAMPLE_SIMPLE", text)

        if version == "Advanced":
            st.markdown(text("MATHEMATICAL_MODELLING_EXAMPLE_EXPERT"))

    if version == "Advanced":
        with open(Path(__file__).parent / "assets" / "sir_v1_integ.py") as fp:
            sir_v1_integ = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "sir_v1_plot.py") as fp:
            sir_v1_plot = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "sir_v2_rate_fns.py") as fp:
            sir_v2_rate_fns = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "sir_v2_model.py") as fp:
            sir_v2_model = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "sir_v2_reactions.py") as fp:
            sir_v2_reactions = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "sir_v2_simulation.py") as fp:
            sir_v2_simulation = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "sird.py") as fp:
            sird = f"\n```python\n{fp.read()}```\n\n"

        with tab2:
            st.markdown(text("HEADLINE_MANUAL"))
            st.markdown(f"{sir_v1_integ}")

            st.markdown(text("SIR_IMPLEMENTATION_MANUAL_1"))

            col1, col2 = st.columns(spec=2, gap="small")

            with col1:
                st.markdown(f"{sir_v1_plot}")

            with col2:
                include_image("pictures/SIR_manual.png", 1)

                st.write(
                    """<style>
                    [data-testid="stHorizontalBlock"] {
                        align-items: center;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown(text("SIR_IMPLEMENTATION_MANUAL_2"))

        with tab3:
            st.markdown(text("HEADLINE_MODELBASE"))

            st.markdown(text("SIR_IMPLEMENTATION_MODELBASE_1"))

            st.markdown(f"{sir_v2_rate_fns}")

            st.markdown(text("SIR_IMPLEMENTATION_MODELBASE_2"))

            st.markdown(f"{sir_v2_model}")

            st.markdown(text("SIR_IMPLEMENTATION_MODELBASE_3"))

            st.markdown(f"{sir_v2_reactions}")

            st.markdown(text("SIR_IMPLEMENTATION_MODELBASE_4"))

            col1, col2 = st.columns(spec=2, gap="small")

            with col1:
                st.markdown(f"{sir_v2_simulation}")

            with col2:
                include_image("pictures/SIR_modelbase.png", 1)

                st.write(
                    """<style>
                    [data-testid="stHorizontalBlock"] {
                        align-items: center;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown(text("SIR_IMPLEMENTATION_MODELBASE_5"))

            st.markdown(f"{sird}")

            st.markdown(text("SIR_IMPLEMENTATION_MODELBASE_6"))

    st.markdown(text("HEADLINE_MODEL_PHOTOSYNTHESIS"))

    tab1, tab2, tab3 = st.tabs(["FvCB", "e-photosynthesis", "Bellassio"])

    with tab1:
        st.markdown(text("HEADLINE_FVCB"))

        markdown_click("FVCB_1",text)

        if version == "Advanced":
            st.latex(
                r"""
                \newcommand{\indexni}[2]{#1 _{\mathrm{#2}}}
                \newcommand{\indexnig}[2]{\mathit{#1} _{\mathrm{#2}}}
                \begin{aligned}
                    \indexni{A}{c} &= \frac{(\indexni{C}{c} - \indexnig{\Gamma}{*}) \cdot \indexni{V}{cmax}}{\indexni{C}{c} + \indexni{K}{c} \cdot \left (1+ \dfrac{O}{\indexni{K}{o}}\right )} - \indexni{R}{d}\\
                    \indexni{A}{j} &= \dfrac{\left (\indexni{C}{c} - \indexnig{\Gamma}{*}\right )\cdot J}{4 \cdot \indexni{C}{c} + 8\cdot\indexnig{\Gamma}{*}} - \indexni{R}{d}\\
                    \indexni{A}{p} &= 3\cdot \indexni{T}{p} - \indexni{R}{d}\\
                    A &= \mathrm{min}\left(\indexni{A}{c},\ \indexni{A}{j},\ \indexni{A}{p}\right)
                \end{aligned}
                """
            )

        st.markdown(text("FVCB_2"), unsafe_allow_html=True)

    with tab2:
        st.markdown(text("HEADLINE_E_PHOTOSYNTHESIS"))

        markdown_click("E_PHOTOSYNTHESIS_1", text)

        if version == "Advanced":
            st.latex(
                r"""
                \newcommand{\indexni}[2]{#1 _{\mathrm{#2}}}
                A = \indexni{V}{c}-\indexni{v}{131}
                """
            )

        st.markdown(text("E_PHOTOSYNTHESIS_2"))

    with tab3:
        st.markdown(text("HEADLINE_BELLASIO"))

        markdown_click("BELLASIO_1", text)

        if version == "Advanced":
            st.latex(
                r"""
                \newcommand{\indexni}[2]{#1 _{\mathrm{#2}}}
                A = \indexni{V}{c} - 0.5 \cdot \indexni{V}{o} - \indexni{R}{d}
                """
            )

        st.markdown(text("BELLASIO_2"))

    with st.expander(text("EXPANDER_C3C4CAM")):
        st.markdown(text("HEADLINE_C3"), unsafe_allow_html=True)
        st.markdown(text("C3_1"), unsafe_allow_html=True)

        st.markdown(text("HEADLINE_C4"), unsafe_allow_html=True)
        st.markdown(text("C4_1"), unsafe_allow_html=True)

        st.markdown(text("HEADLINE_CAM"), unsafe_allow_html=True)
        st.markdown(text("CAM_1"), unsafe_allow_html=True)


def make_literature(text: Callable[[str], str], language: str, version: str) -> None:
    with st.expander(text("LITERATURE")):
        st.markdown(text("LITERATURE_ONPAGE"))
        if version == "Simple":
            """
            - Bellasio, C. (2019). A generalised dynamic model of leaf-level C3 photosynthesis combining light and dark reactions with stomatal behaviour. Photosynthesis Research, 141(1), 99–118. https://doi.org/10.1007/s11120-018-0601-1
            - Farquhar, G. D., von Caemmerer, S., & Berry, J. A. (1980). A biochemical model of photosynthetic CO2 assimilation in leaves of C3 species. Planta, 149(1), 78–90. https://doi.org/10.1007/BF00386231
            - Taiz, L., Zeiger, E., Møller, I. M., & Murphy, A. S. (2018). Fundamentals of plant physiology (First edition). Published in the United States of America by Oxford University Press.
            - Von Caemmerer, S. (2013). Steady-state models of photosynthesis. Plant, Cell & Environment, 36(9), 1617–1630. https://doi.org/10.1111/pce.12098
            - Zhu, X.-G., Wang, Y., Ort, D. R., & Long, S. P. (2013). e-photosynthesis: A comprehensive dynamic mechanistic model of C3 photosynthesis: from light capture to sucrose synthesis. Plant, Cell & Environment, 36(9), 1711–1727. https://doi.org/10.1111/pce.12025

            """

        if version == "Advanced":
            """
            - Bellasio, C. (2019). A generalised dynamic model of leaf-level C3 photosynthesis combining light and dark reactions with stomatal behaviour. Photosynthesis Research, 141(1), 99–118. https://doi.org/10.1007/s11120-018-0601-1
            - Bellasio, C., Quirk, J., Buckley, T. N., & Beerling, D. J. (2017). A Dynamic Hydro-Mechanical and Biochemical Model of Stomatal Conductance for C4 Photosynthesis. Plant Physiology, 175(1), 104–119. https://doi.org/10.1104/pp.17.00666
            - Farquhar, G. D., von Caemmerer, S., & Berry, J. A. (1980). A biochemical model of photosynthetic CO2 assimilation in leaves of C3 species. Planta, 149(1), 78–90. https://doi.org/10.1007/BF00386231
            - Taiz, L., Zeiger, E., Møller, I. M., & Murphy, A. S. (2018). Fundamentals of plant physiology (First edition). Published in the United States of America by Oxford University Press.
            - van Aalst, M., Ebenhöh, O., & Matuszyńska, A. (2021). Constructing and analysing dynamic models with modelbase v1.2.3: A software update. BMC Bioinformatics, 22(1), 1–15. https://doi.org/10.1186/s12859-021-04122-7
            - Von Caemmerer, S. (2013). Steady-state models of photosynthesis. Plant, Cell & Environment, 36(9), 1617–1630. https://doi.org/10.1111/pce.12098
            - Yin, X., Van Oijen, M., & Schapendonk, A. H. C. M. (2004). Extension of a biochemical model for the generalized stoichiometry of electron transport limited C3 photosynthesis. Plant, Cell & Environment, 27(10), 1211–1222. https://doi.org/10.1111/j.1365-3040.2004.01224.x
            - Zhu, X.-G., De Sturler, E., & Long, S. P. (2007). Optimizing the Distribution of Resources between Enzymes of Carbon Metabolism Can Dramatically Increase Photosynthetic Rate: A Numerical Simulation Using an Evolutionary Algorithm. Plant Physiology, 145(2), 513–526. https://doi.org/10.1104/pp.107.103713
            - Zhu, X.-G., Govindjee, Baker, N. R., deSturler, E., Ort, D. R., & Long, S. P. (2005). Chlorophyll a fluorescence induction kinetics in leaves predicted from a model describing each discrete step of excitation energy and electron transfer associated with Photosystem II. Planta, 223(1), 114–133. https://doi.org/10.1007/s00425-005-0064-4
            - Zhu, X.-G., Wang, Y., Ort, D. R., & Long, S. P. (2013). e-photosynthesis: A comprehensive dynamic mechanistic model of C3 photosynthesis: from light capture to sucrose synthesis. Plant, Cell & Environment, 36(9), 1711–1727. https://doi.org/10.1111/pce.12025
            """


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version: str = st.session_state.setdefault("version", "Simple")
    language: str = st.session_state.setdefault("language", "English")
    text = get_localised_text(version, language)
    resetting_click_detector_setup()
    make_page(text, language, version)
    make_literature(text, language, version)
    make_prev_next_button("measuring method", "experiments in silico")
    make_sidebar()
