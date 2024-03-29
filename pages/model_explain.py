import numpy as np
import pandas as pd
import streamlit as st
from pages._sidebar import fill_sidebar, make_sidebar
from pages.assets.FCvB.FCvB_functions import make_FvCB_plot, steady_state_photosynthesis
from pages.assets.SIR_model.sir_utils import *
from pathlib import Path
from PIL import Image
from typing import Callable
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
    st.markdown(text("MDL_HEADLINE_COMPUTATIONAL_MODELS"))

    # Learning objectives
    st.info(text("MDL_LEARNING_OBJECTIVES"))
    make_prev_next_button(
        text,
        text("SDE_PAGENAMES_MEASURINGMETHOD"),
        text("SDE_PAGENAMES_EXPERIMENTSINSILICO"),
        key="mdl_learning_objectives",
    )

    st.markdown(text("MDL_HEADLINE_MODEL"))

    st.markdown(text("MDL_MATHEMATICAL_MODELLING_EXPLANATION_1"))

    include_image(
        path="pictures/Modeling_scheme_eng.png", img_width=0.8, caption=text("MDL_CAPTION_MODELLING_PICTURE")
    )

    st.markdown(text("MDL_MATHEMATICAL_MODELLING_EXPLANATION_1b"))

    # Making a model
    include_ytvideo("https://youtu.be/oVME5KIHrO8", 0.9)
    if st.session_state["show_video_transcripts"]:
        with st.expander(text("EXPANDER_VIDEO_TRANSCRIPT")):
            st.write(text("MDL_VIDEO_TRANSCRIPT_MODELS"))

    st.markdown(text("MDL_EXAMPLE_MATHEMATICAL_MODEL"))

    if version == "4Bio":
        tab1, tab2 = st.tabs([text("MDL_TAB_SIR"), " "])

    if version == "4Math":
        tab1, tab2, tab3 = st.tabs([text("MDL_TAB_SIR"), text("MDL_TAB_MANUAL"), text("MDL_TAB_MODELBASE")])

    with tab1:
        st.markdown(text("MDL_HEADLINE_SIR"))

        st.markdown(text("MDL_MATHEMATICAL_MODELLING_EXAMPLE"), unsafe_allow_html=True)

        if version == "4Bio":
            include_image("pictures/SIR_Aliens.png", 0.5)
        else:
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

        st.markdown(text("MDL_MATHEMATICAL_MODELLING_EXAMPLE_1"), unsafe_allow_html=True)

        if version == "4Bio":
            include_image("pictures/SIR_AliensScheme.png", 0.5)
        else:
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

        st.markdown(text("MDL_MATHEMATICAL_MODELLING_EXAMPLE_2"), unsafe_allow_html=True)

        if version == "4Bio":
            st.latex(
                r"""
                \begin{aligned}
                    \mathrm{Infecting\ rate:}\ v_1 &= \beta \cdot \frac{\mathrm{S}\cdot \mathrm{I}}{\mathrm{N}} \\
                    \mathrm{Recovery\ rate:}\ v_{2} &= \gamma \cdot \mathrm{I} \\
                \end{aligned}
                """
            )

        if version == "4Bio":
            st.markdown(text("MDL_MATHEMATICAL_MODELLING_EXAMPLE_3"), unsafe_allow_html=True)

            st.latex(
                r"""
                \begin{aligned}
                    \mathrm{dS} &= -v_1 \cdot \mathrm{d}t \\
                    \mathrm{dI} &= \left( v_1 - v_2 \right) \cdot \mathrm{d}t \\
                    \mathrm{dR} &= v_2 \cdot \mathrm{d}t
                \end{aligned}
                """
            )

            st.markdown(text("MDL_MATHEMATICAL_MODELLING_EXAMPLE_4"), unsafe_allow_html=True)

        # SIR Model
        def s_slider_callback():
            remain = 1000 - st.session_state.s_slider
            sum = st.session_state.i_slider + st.session_state.r_slider
            if sum == 0:
                st.session_state.i_slider = remain/2
                st.session_state.r_slider = remain/2
            else:
                st.session_state.i_slider = int(st.session_state.i_slider / sum * remain)
                st.session_state.r_slider = int(st.session_state.r_slider / sum * remain)

        def i_slider_callback():
            remain = 1000 - st.session_state.i_slider
            sum = st.session_state.s_slider + st.session_state.r_slider
            if sum == 0:
                st.session_state.s_slider = remain/2
                st.session_state.r_slider = remain/2
            else:
                st.session_state.s_slider = int(st.session_state.s_slider / sum * remain)
                st.session_state.r_slider = int(st.session_state.r_slider / sum * remain)

        def r_slider_callback():
            remain = 1000 - st.session_state.r_slider
            sum = st.session_state.s_slider + st.session_state.i_slider
            if sum == 0:
                st.session_state.s_slider = remain/2
                st.session_state.i_slider = remain/2
            else:
                st.session_state.i_slider = int(st.session_state.i_slider / sum * remain)
                st.session_state.s_slider = int(st.session_state.s_slider / sum * remain)

        if "s_slider" not in st.session_state:
            st.session_state["s_slider"] = 900

        if "i_slider" not in st.session_state:
            st.session_state["i_slider"] = 100

        if "r_slider" not in st.session_state:
            st.session_state["r_slider"] = 0

        col1_______, col2_______, col3_______ = st.columns(3)

        with col1_______:
            st.markdown(
                f"""
                <div style="background-color: rgb(249,165,27); padding: 2px; border: 5px solid rgb(253,207,140); border-radius: 0px; text-align: center; color: black">
                    {text("MDL_MATHEMATICAL_MODELLING_EXAMPLE_SUSCEPTIBLE")} (S)
                </div>
                """,
                unsafe_allow_html=True,
            )

            s_slider = st.slider(
                label="S",
                min_value=0,
                max_value=1000,
                on_change=s_slider_callback,
                key="s_slider",
                label_visibility="collapsed",
            )
        with col2_______:
            st.markdown(
                f"""
                <div style="background-color: rgb(209,35,42); padding: 2px; border: 5px solid rgb(229,146,121); border-radius: 0px; text-align: center; color: black">
                    {text("MDL_MATHEMATICAL_MODELLING_EXAMPLE_INFECTED")} (I)
                </div>
                """,
                unsafe_allow_html=True,
            )

            i_slider = st.slider(
                label="I",
                min_value=0,
                max_value=1000,
                on_change=i_slider_callback,
                key="i_slider",
                label_visibility="collapsed",
            )
        with col3_______:
            st.markdown(
                f"""
                <div style="background-color: #1062ef; padding: 2px; border: 5px solid #87b0f7; border-radius: 0px; text-align: center; color: black">
                    {text("MDL_MATHEMATICAL_MODELLING_EXAMPLE_RECOVERED")} (R)
                </div>
                """,
                unsafe_allow_html=True,
            )

            r_slider = st.slider(
                label="R",
                min_value=0,
                max_value=1000,
                on_change=r_slider_callback,
                key="r_slider",
                label_visibility="collapsed",
            )

        col1_, col2_, col3_ = st.columns([1.5, 1, 1])

        with col1_:
            sir_time_slider = st.slider(
                label=text("MDL_MATHEMATICAL_MODELLING_EXAMPLE_SIR_TIMESLIDER"),
                min_value=5,
                max_value=36,
                value=20,
                key="SIR_TIME_SLIDER",
            )

        with col2_:
            sir_beta_slider = st.slider(
                label=text("MDL_MATHEMATICAL_MODELLING_EXAMPLE_SIR_BETASLIDER"),
                min_value=0.0,
                max_value=5.0,
                value=2.0,
                key="SIR_BETA_SLIDER",
            )

        with col3_:
            sir_gamma_slider = st.slider(
                label=text("MDL_MATHEMATICAL_MODELLING_EXAMPLE_SIR_GAMMASLIDER"),
                min_value=0.0,
                max_value=2.0,
                value=0.2,
                key="SIR_GAMMA_SLIDER",
            )

        def reset_graph():
            st.session_state["SIR_model"] = {}

        st.button(label="Reset Graph", use_container_width=True, on_click=reset_graph)

        sir_time, sir_results = get_results_dict_SIRModel(
            beta_param=sir_beta_slider,
            gamma_param=sir_gamma_slider,
            S_initial=s_slider,
            I_initial=i_slider,
            R_initial=r_slider,
            time_end=sir_time_slider,
        )

        if "SIR_model" not in st.session_state:
            st.session_state["SIR_model"] = {
                "S": [sir_time, sir_results["S"]],
                "I": [sir_time, sir_results["I"]],
                "R": [sir_time, sir_results["R"]],
            }

        else:
            st.session_state["SIR_model"].update(
                {
                    "S": [sir_time, sir_results["S"]],
                    "I": [sir_time, sir_results["I"]],
                    "R": [sir_time, sir_results["R"]],
                }
            )

        sir_fig = get_plot_SIRModel(st.session_state["SIR_model"])

        col1______, col2______, col3______ = st.columns([0.2, 0.6, 0.2])

        with col2______:
            st.pyplot(sir_fig, transparent=True)

        st.session_state["SIR_model"].update(
            {
                "old S": [sir_time, sir_results["S"]],
                "old I": [sir_time, sir_results["I"]],
                "old R": [sir_time, sir_results["R"]],
            }
        )

        markdown_click("MDL_MATHEMATICAL_MODELLING_EXAMPLE_SIMPLE", text)

    if version == "4Math":
        with open(Path(__file__).parent / "assets" / "SIR_model" / "sir_v1_integ.py") as fp:
            sir_v1_integ = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "SIR_model" / "sir_v1_plot.py") as fp:
            sir_v1_plot = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "SIR_model" / "sir_v2_rate_fns.py") as fp:
            sir_v2_rate_fns = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "SIR_model" / "sir_v2_model.py") as fp:
            sir_v2_model = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "SIR_model" / "sir_v2_reactions.py") as fp:
            sir_v2_reactions = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "SIR_model" / "sir_v2_simulation.py") as fp:
            sir_v2_simulation = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "SIR_model" / "sird.py") as fp:
            sird = f"\n```python\n{fp.read()}```\n\n"

        with tab2:
            st.markdown(text("MDL_HEADLINE_MANUAL"))
            st.markdown(f"{sir_v1_integ}")

            st.markdown(text("MDL_SIR_IMPLEMENTATION_MANUAL_1"))

            include_image("pictures/SIR_manual.png", 0.5)

            st.markdown(f"{sir_v1_plot}")

            st.markdown(text("MDL_SIR_IMPLEMENTATION_MANUAL_2"))

        with tab3:
            st.markdown(text("MDL_HEADLINE_MODELBASE"))

            st.markdown(text("MDL_SIR_IMPLEMENTATION_MODELBASE_1"))

            st.markdown(f"{sir_v2_rate_fns}")

            st.markdown(text("MDL_SIR_IMPLEMENTATION_MODELBASE_2"))

            st.markdown(f"{sir_v2_model}")

            st.markdown(text("MDL_SIR_IMPLEMENTATION_MODELBASE_3"))

            st.markdown(f"{sir_v2_reactions}")

            st.markdown(text("MDL_SIR_IMPLEMENTATION_MODELBASE_4"))

            include_image("pictures/SIR_modelbase.png", 0.5)

            st.markdown(f"{sir_v2_simulation}")

            st.markdown(text("MDL_SIR_IMPLEMENTATION_MODELBASE_5"))

            st.markdown(f"{sird}")

            st.markdown(text("MDL_SIR_IMPLEMENTATION_MODELBASE_6"))

    st.markdown(text("MDL_LINK_PLANTS_AND_PYTHON"))

    st.markdown(text("MDL_HEADLINE_MODEL_PHOTOSYNTHESIS"))

    st.markdown(text("MDL_MODELS_OVERVIEW"))

    tab1, tab2, tab3 = st.tabs(["FvCB", "e-photosynthesis", "Bellassio"])

    with tab1:
        st.markdown(text("MDL_HEADLINE_FVCB"))

        st.markdown(text("MDL_FVCB_1"), unsafe_allow_html=True)

        st.markdown(text("MDL_FVCB_2"), unsafe_allow_html=True)

        if version == "4Math":
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

        st.markdown(text("MDL_FVCB_3"), unsafe_allow_html=True)

        markdown_click("MDL_FVCB_4", text, unsafe_allow_html=True)

        if version == "4Math":
            st.markdown(text("MDL_FVCB_5"), unsafe_allow_html=True)

        fcvb_sliders = st.container()

        col1__, col2__, col3__, col4__ = st.columns([0.08, 0.3, 0.3, 0.32])

        with col1__:
            st.markdown(text("MDL_FVCB_SLIDERS_PRECISION"))

        with col2__:
            precise_O = st.number_input(
                label="Precise O", min_value=100, max_value=500, value=210, label_visibility="collapsed"
            )
        with col3__:
            precise_J = st.number_input(
                label="Precise J", min_value=50, max_value=300, value=124, label_visibility="collapsed"
            )
        with col4__:
            precise_Tp = st.number_input(
                label="Precise Tp", min_value=100, max_value=500, value=300, label_visibility="collapsed"
            )

        with fcvb_sliders:
            col1___, col2___, col3___, col4___ = st.columns([0.08, 0.3, 0.3, 0.32])

            with col1___:
                st.markdown(text("MDL_FVCB_SLIDERS_TEXT"))
            with col2___:
                slider_O = st.slider(
                    label=text("MDL_FVCB_SLIDERS_O"), min_value=100, max_value=500, value=precise_O
                )
            with col3___:
                slider_J = st.slider(
                    label=text("MDL_FVCB_SLIDERS_J"), min_value=50, max_value=300, value=precise_J
                )
            with col4___:
                slider_Tp = st.slider(
                    label=text("MDL_FVCB_SLIDERS_Tp"), min_value=100, max_value=500, value=precise_Tp
                )

        (
            col1____,
            col2____,
        ) = st.columns([0.3, 0.7])

        with col1____:
            st.markdown(
                f"""
                <div align="center"><strong>{text("MDL_FVCB_DEFAULT_PARAMETERS")}</strong></div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                |  | {text("MDL_FVCB_DEFAULT_PARAMETERS_VALUES")} | {text("MDL_FVCB_DEFAULT_PARAMETERS_UNITS")} |
                | --- | --- | --- |
                | V<sub>cmax</sub> | 80 | µmol m⁻² s⁻¹ |
                | K<sub>c</sub> | 259 | µbar |
                | K<sub>o</sub> | 179 | mbar |
                | Γ<sub>*</sub> | 38.6 | µbar |
                | R<sub>d</sub> | 1 | µmol m⁻² s⁻¹ |
                """,
                unsafe_allow_html=True,
            )

        with col2____:
            col1_____, col2_____, col3_____, col4_____ = st.columns(4)

            with col1_____:
                toggle_A = st.toggle(
                    label=f'{text("MDL_FVCB_TOGGLE")} A?',
                    value=True,
                )
            with col2_____:
                toggle_Ac = st.toggle(
                    label=f'{text("MDL_FVCB_TOGGLE")} Ac?',
                    value=False,
                )
            with col3_____:
                toggle_Aj = st.toggle(
                    label=f'{text("MDL_FVCB_TOGGLE")} Aj?',
                    value=False,
                )
            with col4_____:
                toggle_Ap = st.toggle(
                    label=f'{text("MDL_FVCB_TOGGLE")} Ap?',
                    value=False,
                )

            fcvb_results = steady_state_photosynthesis(
                Ci=np.linspace(0, 700, num=7000),
                O=slider_O,
                J=slider_J,
                Tp=slider_Tp,
                rm=0,
                Kc=259,
                Ko=179,
                gamma_star=38.6,
                Rd=1,
            )

            fcvb_fig = make_FvCB_plot(
                Ci=np.linspace(0, 700, num=7000),
                results=fcvb_results,
                display_bools={
                    "Ac": toggle_Ac,
                    "Aj": toggle_Aj,
                    "Ap": toggle_Ap,
                    "A": toggle_A,
                },
                xlabel=text("MDL_FVCB_XLABEL"),
                ylabel=text("MDL_FVCB_YLABEL"),
                empty_label=text("MDL_FVCB_EMPTY"),
            )

            st.pyplot(fcvb_fig, transparent=True)

    with tab2:
        st.markdown(text("MDL_HEADLINE_E_PHOTOSYNTHESIS"))

        st.markdown(text("MDL_E_PHOTOSYNTHESIS_1"), unsafe_allow_html=True)

        st.markdown(text("MDL_E_PHOTOSYNTHESIS_2"), unsafe_allow_html=True)

        st.markdown(text("MDL_E_PHOTOSYNTHESIS_3"), unsafe_allow_html=True)

    with tab3:
        st.markdown(text("MDL_HEADLINE_BELLASIO"))

        st.markdown(text("MDL_BELLASIO_1"))

        st.markdown(text("MDL_BELLASIO_2"))

        st.markdown(text("MDL_BELLASIO_3"))

        st.markdown(text("MDL_BELLASIO_4"), unsafe_allow_html=True)

    with st.expander(text("MDL_EXPANDER_C3C4CAM")):
        st.markdown(text("MDL_HEADLINE_C3"), unsafe_allow_html=True)
        st.markdown(text("MDL_C3_1"), unsafe_allow_html=True)

        st.markdown(text("MDL_HEADLINE_C4"), unsafe_allow_html=True)
        st.markdown(text("MDL_C4_1"), unsafe_allow_html=True)

        st.markdown(text("MDL_HEADLINE_CAM"), unsafe_allow_html=True)
        st.markdown(text("MDL_CAM_1"), unsafe_allow_html=True)


def style_page():
    # Stop the table from overflowing
    st.markdown(
        "<style>table{width: 100%} .st-emotion-cache-nahz7x.e1nzilvr5:has(table){overflow-x: scroll}</style>",
        unsafe_allow_html=True,
    )


def make_literature(text: Callable[[str], str], language: str, version: str) -> None:
    with st.expander(text("LITERATURE")):
        st.markdown(text("LITERATURE_ONPAGE"))
        if version == "4Bio":
            """
            1. Farquhar, G. D., von Caemmerer, S., & Berry, J. A. (1980). A biochemical model of photosynthetic CO₂ assimilation in leaves of C3 species. Planta, 149(1), 78–90. https://doi.org/10.1007/BF00386231
            2. Evans, J., &amp; Von Caemmerer, S. (2012). Temperature response of carbon isotope discrimination and mesophyll conductance in tobacco. Plant, Cell &amp;amp; Environment, 36(4), 745–756. https://doi.org/10.1111/j.1365-3040.2012.02591.x
            3. Price, G. D., Badger, M. R., & Von Caemmerer, S. (2010). The prospect of using cyanobacterial bicarbonate transporters to improve leaf photosynthesis in C3 crop plants. Plant Physiology, 155(1), 20–26. https://doi.org/10.1104/pp.110.164681
            4. Von Caemmerer, S. (2013). Steady-state models of photosynthesis. Plant, Cell & Environment, 36(9), 1617–1630. https://doi.org/10.1111/pce.12098
            5. Zhu, X.-G., Wang, Y., Ort, D. R., & Long, S. P. (2013). e-photosynthesis: A comprehensive dynamic mechanistic model of C3 photosynthesis: from light capture to sucrose synthesis. Plant, Cell & Environment, 36(9), 1711–1727. https://doi.org/10.1111/pce.12025
            6. Zhu, X.-G., Govindjee, Baker, N. R., deSturler, E., Ort, D. R., & Long, S. P. (2005). Chlorophyll a fluorescence induction kinetics in leaves predicted from a model describing each discrete step of excitation energy and electron transfer associated with Photosystem II. Planta, 223(1), 114–133. https://doi.org/10.1007/s00425-005-0064-4
            7. Zhu, X.-G., De Sturler, E., & Long, S. P. (2007). Optimizing the Distribution of Resources between Enzymes of Carbon Metabolism Can Dramatically Increase Photosynthetic Rate: A Numerical Simulation Using an Evolutionary Algorithm. Plant Physiology, 145(2), 513–526. https://doi.org/10.1104/pp.107.103713
            8. Bellasio, C. (2019). A generalised dynamic model of leaf-level C3 photosynthesis combining light and dark reactions with stomatal behaviour. Photosynthesis Research, 141(1), 99–118. https://doi.org/10.1007/s11120-018-0601-1
            9. Yin, X., Van Oijen, M., & Schapendonk, A. H. C. M. (2004). Extension of a biochemical model for the generalized stoichiometry of electron transport limited C3 photosynthesis. Plant, Cell & Environment, 27(10), 1211–1222. https://doi.org/10.1111/j.1365-3040.2004.01224.x
            10. Bellasio, C., Quirk, J., Buckley, T. N., & Beerling, D. J. (2017). A Dynamic Hydro-Mechanical and Biochemical Model of Stomatal Conductance for C4 Photosynthesis. Plant Physiology, 175(1), 104–119. https://doi.org/10.1104/pp.17.00666
            11. Taiz, L., Zeiger, E., Møller, I. M., & Murphy, A. S. (2018). Fundamentals of plant physiology (First edition). Published in the United States of America by Oxford University Press.
            """

        if version == "4Math":
            """
            1. van Aalst, M., Ebenhöh, O., & Matuszyńska, A. (2021). Constructing and analysing dynamic models with modelbase v1.2.3: A software update. BMC Bioinformatics, 22(1), 1–15. https://doi.org/10.1186/s12859-021-04122-7
            2. Farquhar, G. D., von Caemmerer, S., & Berry, J. A. (1980). A biochemical model of photosynthetic CO2 assimilation in leaves of C3 species. Planta, 149(1), 78–90. https://doi.org/10.1007/BF00386231
            3. Evans, J., &amp; Von Caemmerer, S. (2012). Temperature response of carbon isotope discrimination and mesophyll conductance in tobacco. Plant, Cell &amp;amp; Environment, 36(4), 745–756. https://doi.org/10.1111/j.1365-3040.2012.02591.x
            4. Price, G. D., Badger, M. R., & Von Caemmerer, S. (2010). The prospect of using cyanobacterial bicarbonate transporters to improve leaf photosynthesis in C3 crop plants. Plant Physiology, 155(1), 20–26. https://doi.org/10.1104/pp.110.164681
            5. Von Caemmerer, S. (2013). Steady-state models of photosynthesis. Plant, Cell & Environment, 36(9), 1617–1630. https://doi.org/10.1111/pce.12098
            6. Zhu, X.-G., Wang, Y., Ort, D. R., & Long, S. P. (2013). e-photosynthesis: A comprehensive dynamic mechanistic model of C3 photosynthesis: from light capture to sucrose synthesis. Plant, Cell & Environment, 36(9), 1711–1727. https://doi.org/10.1111/pce.12025
            7. Zhu, X.-G., Govindjee, Baker, N. R., deSturler, E., Ort, D. R., & Long, S. P. (2005). Chlorophyll a fluorescence induction kinetics in leaves predicted from a model describing each discrete step of excitation energy and electron transfer associated with Photosystem II. Planta, 223(1), 114–133. https://doi.org/10.1007/s00425-005-0064-4
            8. Zhu, X.-G., De Sturler, E., & Long, S. P. (2007). Optimizing the Distribution of Resources between Enzymes of Carbon Metabolism Can Dramatically Increase Photosynthetic Rate: A Numerical Simulation Using an Evolutionary Algorithm. Plant Physiology, 145(2), 513–526. https://doi.org/10.1104/pp.107.103713
            9. Bellasio, C. (2019). A generalised dynamic model of leaf-level C3 photosynthesis combining light and dark reactions with stomatal behaviour. Photosynthesis Research, 141(1), 99–118. https://doi.org/10.1007/s11120-018-0601-1
            10. Yin, X., Van Oijen, M., & Schapendonk, A. H. C. M. (2004). Extension of a biochemical model for the generalized stoichiometry of electron transport limited C3 photosynthesis. Plant, Cell & Environment, 27(10), 1211–1222. https://doi.org/10.1111/j.1365-3040.2004.01224.x
            11. Bellasio, C., Quirk, J., Buckley, T. N., & Beerling, D. J. (2017). A Dynamic Hydro-Mechanical and Biochemical Model of Stomatal Conductance for C4 Photosynthesis. Plant Physiology, 175(1), 104–119. https://doi.org/10.1104/pp.17.00666
            12. Taiz, L., Zeiger, E., Møller, I. M., & Murphy, A. S. (2018). Fundamentals of plant physiology (First edition). Published in the United States of America by Oxford University Press.
            """
        st.markdown(text("LITERATURE_PLANTS_AND_PYTHON"))


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version: str = st.session_state.setdefault("version", "4Bio")
    language: str = st.session_state.setdefault("language", "English")
    text = get_localised_text(version, language)
    placeholder_sidebar = make_sidebar()
    resetting_click_detector_setup()
    track_page_visit("model_explain")
    make_page(text, language, version)
    make_literature(text, language, version)
    make_prev_next_button(
        text,
        text("SDE_PAGENAMES_MEASURINGMETHOD"),
        text("SDE_PAGENAMES_EXPERIMENTSINSILICO"),
    )
    style_page()
    fill_sidebar(placeholder_sidebar)
