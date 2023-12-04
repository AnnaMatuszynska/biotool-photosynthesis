import numpy as np
import streamlit as st
import time
from pages._sidebar import fill_sidebar, make_sidebar
from pages.assets.model._model_functions import calculate_results_to_plot, make_plot, sim_model
from pathlib import Path
from streamlit.components.v1 import html
from typing import Callable
from utils import (
    get_localised_text,
    include_image,
    include_ytvideo,
    make_prev_next_button,
    markdown_click,
    resetting_click_detector_setup,
    track_page_visit,
)


def make_page(text: Callable[[str], str]) -> bool:
    st.markdown(text("FAL_HEADLINE_EXPERIMENTS"))

    # Learning objectives
    st.info(text("FAL_LEARNING_OBJECTIVES"))

    st.markdown(text("FAL_HEADLINE_MODEL_CONSTRUCTION"))

    st.markdown(text("FAL_CONSTRUCTION_EXPLANATION_1"))

    include_image("pictures/NPQphotosynthesis.png", 0.8, text("FAL_CAPTION_MODEL_NPQ"), True)

    st.markdown(text("FAL_CONSTRUCTION_EXPLANATION_2"))
    st.markdown(text("FAL_RATES_1"), unsafe_allow_html=True)
    st.markdown(text("FAL_RATES_2"))
    st.markdown(text("FAL_RATES_3"))
    st.markdown(text("FAL_RATES_4"))
    st.markdown(text("FAL_RATES_5"))
    st.markdown(text("FAL_RATES_6"), unsafe_allow_html=True)

    if version == "4Math":
        st.markdown(text("FAL_HEADLINE_MODEL_EQUATIONS"))
        st.markdown(text("FAL_MODEL_EQUATIONS_INTRODUCTION"))
        st.latex(
            r"""
            \begin{aligned}
                \frac{\mathrm{dPQH_2}}{\mathrm{d}t} &= v_\mathrm{PSII} - v_\mathrm{PQ_{ox}} \\
                \frac{\mathrm{dATP}}{\mathrm{d}t} &= v_\mathrm{ATPsynthase} - v_\mathrm{ATPconsumption} \\
                \frac{\mathrm{dATPase^{*}}}{\mathrm{d}t} &= F k_\mathrm{actATPase} \cdot \mathrm{H}(\mathrm{PFD}) \cdot \mathrm{ATPase} - k_\mathrm{deactATPase} \cdot (1 - \mathrm{H}(\mathrm{PFD})) \cdot \mathrm{ATPase^{*}} \\
                b_\mathrm{H}\cdot\frac{\mathrm{dH}}{\mathrm{d}t} &= 2 v_\mathrm{PSII} + 4 v_\mathrm{PQ_{ox}} -\frac{14}{3} v_\mathrm{ATPsynthase} - v_\mathrm{leak} \\
                \frac{\mathrm{dPsbS}}{\mathrm{d}t} &= -v_\mathrm{Psbs^{p}} \\
                \frac{\mathrm{dVx}}{\mathrm{d}t} &= -v_\mathrm{Xcyc} \\
            \end{aligned}
        """
        )

        with st.expander(text("FAL_REACTION_RATES")):
            st.markdown(text("FAL_RATES_DYNAMIC"))
            st.latex(
                r"""
                \begin{aligned}
                    v_{\mathrm{PSII}} &= k_2 \cdot 0.5 \cdot B_1 \\
                    v_{PQ_{ox}} 7 &= \left(\frac{k_{Cyt_{b6f}} \cdot \mathrm{PFD} \cdot K_\mathrm{eq,cytb6f}(\mathrm{pH})}{K_\mathrm{eq,cytb6f}(\mathrm{pH}) + 1} + k_\mathrm{PTOX}\right) \cdot \mathrm{PQH_2} - \frac{k_\mathrm{PFD}}{K_\mathrm{eq,cytb6f}(\mathrm{pH}) + 1} \cdot \mathrm{PQ} \\
                    v_\mathrm{ATPsynthase} &= \mathrm{ATPase}^* \cdot k_\mathrm{ATPsynthase}\cdot \left(AP^{tot}-\mathrm{ATP} - \frac{\mathrm{ATP}}{K_\mathrm{eq,ATPsynthase}(H)} \right) \\
                    v_\mathrm{ATPactivity} &= k_\mathrm{actATPase} \cdot \mathrm{H}(\mathrm{PFD}) \cdot \mathrm{ATPase} - k_\mathrm{deactATPase} \cdot (1 - \mathrm{H}(\mathrm{PFD})) \cdot \mathrm{ATPase^{*}} \\
                    v_\mathrm{Leak} &= k_\mathrm{leak} \cdot (H - pH_{\mathrm{inv}}(\mathrm{pH_{stroma}})) \\
                    v_\mathrm{ATPconsumption} &= k_\mathrm{ATPconsumption} \cdot \mathrm{ATP} \\
                \end{aligned}
                """
            )

            st.markdown(text("FAL_RATE_QUENCHER"))
            st.latex(
                r"""
                \begin{aligned}
                    v_\mathrm{Xcyc} &= k_\mathrm{DeepoxV} \cdot \frac{H^\mathrm{nH_X}}{H^\mathrm{nH_X} + pH_{\mathrm{inv}}(K_\mathrm{phSat})^\mathrm{nH_X}} \cdot \mathrm{Vx} - k_\mathrm{EpoxZ} \cdot (\mathrm{X^{tot}} - \mathrm{Vx}) \\
                    v_\mathrm{Psbs^{p}} &= k_\mathrm{ProtonationL} \cdot \frac{H^\mathrm{nH_L}} {H^\mathrm{nH_L} + pH_{\mathrm{inv}}(K_\mathrm{phSatLHC})^\mathrm{nH_L}} \cdot \mathrm{PsbS} - k_\mathrm{Deprotonation} \cdot \mathrm{PsbS^p} \\
                    Q &= \gamma_0 \cdot (1-\frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}})\cdot\mathrm{PsbS}+ \gamma_1\cdot(1-\frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}})\cdot\mathrm{PsbS^p} + \gamma_2\cdot \frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}}\cdot\mathrm{PsbS^p} + \gamma_3\cdot \frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}}\cdot\mathrm{PsbS} \\
                \end{aligned}
                """
            )

    st.markdown(text("FAL_HEADLINE_IMPLEMENTATION"))

    st.markdown(text("FAL_IMPLEMENTATION_DESCRIPTION"))

    if version == "4Bio":
        markdown_click("FAL_IMPLEMENTATION_TO_EXPERT", text)

    if version == "4Math":
        with st.expander(text("FAL_MODEL_CODE_EXPANDER")):
            st.markdown(text("FAL_CONSTRUCTION_HEADER"))
            st.markdown(text("FAL_CONSTRUCTION_1"))

            with open(Path(__file__).parent / "assets" / "model" / "model_define.py") as fp:
                model_define = f"{fp.read()}"

            st.code(model_define, "python")

            st.markdown(text("FAL_CONSTRUCTION_2"))

            tab1, tab2 = st.tabs(["Parameters", "Compounds"])

            with tab1:
                with open(Path(__file__).parent / "assets" / "model" / "model_parameters.py") as fp:
                    model_parameters = f"{fp.read()}"

                st.code(model_parameters, "python")

            with tab2:
                with open(Path(__file__).parent / "assets" / "model" / "model_comps.py") as fp:
                    model_comps = f"{fp.read()}"

                st.code(model_comps, "python")

            st.markdown(text("FAL_CONSTRUCTION_3"))

            with open(Path(__file__).parent / "assets" / "model" / "model_addcompspars.py") as fp:
                model_addcompspars = f"{fp.read()}"

            st.code(model_addcompspars, "python")

            st.markdown(text("FAL_CONSTRUCTION_4"))

            tab1, tab2 = st.tabs(["Derived parameters", "Algebraic modules"])

            with tab1:
                with open(Path(__file__).parent / "assets" / "model" / "model_derivedparameters.py") as fp:
                    model_derivedparameters = f"{fp.read()}"

                st.code(model_derivedparameters, "python")

            with tab2:
                with open(Path(__file__).parent / "assets" / "model" / "model_algebraicmodules.py") as fp:
                    model_algebraicmodules = f"{fp.read()}"

                st.code(model_algebraicmodules, "python")

            st.markdown(text("FAL_CONSTRUCTION_5"))

            tab1, tab2 = st.tabs(["Rate reactions", "Other functions"])

            with tab1:
                with open(Path(__file__).parent / "assets" / "model" / "model_reactions.py") as fp:
                    model_reactions = f"{fp.read()}"

                st.code(model_reactions, "python")

            with tab2:
                with open(Path(__file__).parent / "assets" / "model" / "model_otherfunctions.py") as fp:
                    model_otherfunctions = f"{fp.read()}"

                st.code(model_otherfunctions, "python")

            st.markdown(text("FAL_CONSTRUCTION_6"))

            with open(Path(__file__).parent / "assets" / "model" / "model_addreactions.py") as fp:
                model_addreactions = f"{fp.read()}"

            st.code(model_addreactions, "python")

            st.markdown(text("FAL_CONSTRUCTION_7"))

            st.markdown(text("FAL_SIMULATION_HEADER"))

            st.markdown(text("FAL_SIMULATION_1"))

            with open(Path(__file__).parent / "assets" / "model" / "model_definesim.py") as fp:
                model_definesim = f"{fp.read()}"

            st.code(model_definesim, "python")

            st.markdown(text("FAL_SIMULATION_2"))

            with open(Path(__file__).parent / "assets" / "model" / "model_initialisesim.py") as fp:
                model_initialisesim = f"{fp.read()}"

            st.code(model_initialisesim, "python")

            st.markdown(text("FAL_SIMULATION_3"))

            col1, col2 = st.columns([1, 1])

            with col1:
                with open(Path(__file__).parent / "assets" / "model" / "model_basicplot.py") as fp:
                    model_basicplot = f"{fp.read()}"

                st.code(model_basicplot, "python")

                st.write(
                    """<style>
                    [data-testid="stHorizontalBlock"] {
                        align-items: center;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                include_image("pictures/basic_plot.png", 1)

            st.markdown(text("FAL_SIMULATION_4"))
            st.markdown(text("FAL_SIMULATION_FLOURESCENCE_HEADER"))
            st.markdown(text("FAL_SIMULATION_FLOURESCENCE_1"))

            col1, col2 = st.columns([1, 1])

            with col1:
                with open(Path(__file__).parent / "assets" / "model" / "model_onlyflou.py") as fp:
                    model_onlyflou = f"{fp.read()}"

                st.code(model_onlyflou, "python")

                st.write(
                    """<style>
                    [data-testid="stHorizontalBlock"] {
                        align-items: center;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                include_image("pictures/only_flou.png", 1)

            st.markdown(text("FAL_SIMULATION_FLOURESCENCE_2"))

            col1, col2 = st.columns([1, 1])

            with col1:
                with open(Path(__file__).parent / "assets" / "model" / "model_relativeflou.py") as fp:
                    model_relativeflou = f"{fp.read()}"

                st.code(model_relativeflou, "python")

                st.write(
                    """<style>
                    [data-testid="stHorizontalBlock"] {
                        align-items: center;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                include_image("pictures/relative_flou.png", 1)

            st.markdown(text("FAL_SIMULATION_PHASES_HEADER"))
            st.markdown(text("FAL_SIMULATION_PHASES_1"))

            col1, col2 = st.columns([1, 1])

            with col1:
                with open(Path(__file__).parent / "assets" / "model" / "model_phases.py") as fp:
                    model_phases = f"{fp.read()}"

                st.code(model_phases, "python")

                st.write(
                    """<style>
                    [data-testid="stHorizontalBlock"] {
                        align-items: center;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                include_image("pictures/phases.png", 1)

            st.markdown(text("FAL_SIMULATION_PRETTY_HEADER"))
            st.markdown(text("FAL_SIMULATION_PRETTY_1"))

            include_image("pictures/complete_mockup.png", 1)

            with open(Path(__file__).parent / "assets" / "model" / "model_complemockup.py") as fp:
                model_complemockup = f"{fp.read()}"

            st.code(model_complemockup, "python")

    st.markdown(text("FAL_HEADLINE_ANALYSE"))
    st.markdown(text("FAL_INTRODUKTION"))

    st.markdown(text("FAL_HEADLINE_SLIDER"))
    st.markdown(text("FAL_EXPLANATNION"))
    include_ytvideo("https://youtu.be/zxGZKeopEDw", 0.5)

    with st.expander(text("FAL_GRAPH_EXPLANATION_EXPANDER"), expanded=True):
        st.markdown(text("FAL_GRAPH_EXPLANATION_HEADER_SINGLE"))
        include_image(str(Path("pictures/explanation_graph_oneresult.png")), img_width=1)
        st.markdown(text("FAL_GRAPH_EXPLANATION_1"))
        st.latex(r"NPQ = \frac{F_m - F_m'}{F_m'}")
        st.markdown(text("FAL_GRAPH_EXPLANATION_2"))

        st.markdown(text("FAL_GRAPH_EXPLANATION_HEADER_DUO"))
        include_image(str(Path("pictures/explanation_graph_tworesults.png")), img_width=1)
        st.markdown(text("FAL_GRAPH_EXPLANATION_DUO"))

    # Add guiding questions:
    with st.expander(text("FAL_GUIDING_EXPANDER")):
        # The answers are hidden by default
        st.markdown(text("FAL_GUIDING_HEADER"))
        see_interpr = st.toggle(text("FAL_GUIDING_TOGGLE"))

        if not see_interpr:
            st.markdown(text("FAL_GUIDING_QUESTIONS"))
            if version == "4Bio":
                st.markdown(text("FAL_GUIDING_QUESTIONS_EXTEND"))
        else:  # If toggle is switched show possible interpretation
            st.markdown(text("FAL_GUIDING_ANSWERS"))
            if version == "4Bio":
                st.markdown(text("FAL_GUIDING_ANSWERS_EXTEND"))

    with st.form("simple_model"):
        slider_light = st.slider(
            label=text("SLIDER_LIGHT"),
            min_value=50,
            max_value=900,
            value=100,
        )
        col1, col2 = st.columns(2)

        with col1:
            slider_time = st.slider(
                label=text("FAL_SLIDER_TIME"),
                min_value=1,
                max_value=15,
                value=5,
            )
        with col2:
            slider_pings = st.slider(label=text("SLIDER_PULSES"), min_value=5, max_value=150, value=85)

        if version == "4Bio":
            col1, col2 = st.columns(2)
            with col1:
                slider_aktivation = st.select_slider(
                    text("SLIDER_ACTIVATION"),
                    options=np.round(np.logspace(0, 4, 21)).astype(int),
                    value=100,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
                )
                slider_darklength = st.slider(
                    text("FAL_SLIDER_DARKLENGTH"), min_value=0, max_value=slider_time * 60, value=30
                )
            with col2:
                slider_deaktivation = st.select_slider(
                    text("SLIDER_DEACTIVATION"),
                    options=np.round(np.logspace(0, 4, 21)).astype(int),
                    value=100,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
                )
                slider_saturate = st.slider(
                    label=text("FAL_SLIDER_SATURATE"), min_value=0, max_value=10000, value=5000
                )

            updated_parameters = {
                "kDeepoxV": 0.0024 * (slider_aktivation / 100),  # Aktivierung des Quenchings
                "kEpoxZ": 0.00024
                * (slider_deaktivation / 100),  # 6.e-4,  #converted to [1/s]   # Deaktivierung
            }
        else:
            updated_parameters = {
                "kDeepoxV": 0.0024,  # Aktivierung des Quenchings
                "kEpoxZ": 0.00024,  # 6.e-4,  #converted to [1/s]   # Deaktivierung
            }
            slider_darklength = 30
            slider_saturate = 5000

        if "model_variables" not in st.session_state:
            st.session_state["model_variables"] = {
                "New": {
                    "AL [μmol m⁻² s⁻¹]": slider_light,
                    "SP [μmol m⁻² s⁻¹]": slider_saturate,
                    "CtZ [s⁻¹]": round(updated_parameters["kDeepoxV"], 5),
                    "CtV [s⁻¹]": round(updated_parameters["kEpoxZ"], 6),
                }
            }
        else:
            st.session_state["model_variables"]["New"].update(
                {
                    "AL [μmol m⁻² s⁻¹]": slider_light,
                    "SP [μmol m⁻² s⁻¹]": slider_saturate,
                    "CtZ [s⁻¹]": round(updated_parameters["kDeepoxV"], 5),
                    "CtV [s⁻¹]": round(updated_parameters["kEpoxZ"], 6),
                }
            )

        col1_, col2_ = st.columns(2)

        with col2_:
            show_old = st.checkbox("Compare with the last simulation", value=True)

        with col1_:
            # if st.button("Start the simulation", type="primary", use_container_width=True):
            submitted = st.form_submit_button(
                "Start the simulation", type="primary", use_container_width=True
            )
        if submitted:
            with st.spinner(text("SPINNER")):
                time.sleep(0.1)
                sim_time, sim_results = sim_model(
                    updated_parameters,
                    slider_time,
                    slider_light,
                    slider_pings,
                    slider_saturate,
                    slider_darklength,
                )

                if "model_results" not in st.session_state:
                    st.session_state["model_results"] = calculate_results_to_plot(sim_time, sim_results)
                else:
                    st.session_state["model_results"].update(calculate_results_to_plot(sim_time, sim_results))

                if show_old:
                    plot_values = st.session_state["model_results"]
                    plot_variables = st.session_state["model_variables"]

                else:
                    plot_values = {
                        k: v
                        for k, v in st.session_state["model_results"].items()
                        if k in ["Fluo", "NPQ", "PhiPSII"]
                    }
                    plot_variables = {"New": st.session_state["model_variables"]["New"]}

                fig_4Bio = make_plot(
                    values=plot_values,
                    variables=plot_variables,
                    version="4Bio",
                    width=15,
                    height=6,
                    xlabel1=text("AXIS_TIME_S"),
                    xlabel2=text("AXIS_TIME_MIN"),
                    ylabel={
                        "Fluo": text("FLUO"),
                        "NPQ": text("AXIS_NPQ"),
                        "PhiPSII": text("AXIS_PHIPSII"),
                    },
                    dark_length=slider_darklength,
                    max_time=slider_time * 60,
                    new_label=text("NEW_LABEL"),
                    old_label=text("OLD_LABEL"),
                )

                fig_4Math = make_plot(
                    values=plot_values,
                    variables=plot_variables,
                    version="4Math",
                    width=15,
                    height=3,
                    xlabel1=text("AXIS_TIME_S"),
                    xlabel2=text("AXIS_TIME_MIN"),
                    ylabel={"Fluo": text("FLUO")},
                    dark_length=slider_darklength,
                    max_time=slider_time * 60,
                    new_label=text("NEW_LABEL"),
                    old_label=text("OLD_LABEL"),
                )

                st.session_state["fig_4Bio"] = fig_4Bio
                st.session_state["fig_4Math"] = fig_4Math

            old_results = {}
            for key, value in st.session_state["model_results"].items():
                old_results.update({f"old {key}": value})

            st.session_state["model_results"].update(old_results)

            st.session_state["model_variables"].update(
                {"Old": {k: v for k, v in st.session_state["model_variables"]["New"].items()}}
            )

        if "fig_4Bio" in st.session_state and "fig_4Math" in st.session_state:
            if version == "4Bio":
                showed_fig = st.session_state["fig_4Bio"]
            else:
                showed_fig = st.session_state["fig_4Math"]

            st.pyplot(showed_fig, transparent=True)

        return see_interpr


def make_literature(text: Callable[[str], str], language: str, version: str) -> None:
    with st.expander(text("LITERATURE")):
        st.markdown(text("LITERATURE_ONPAGE"))
        st.markdown(
            "- Matuszyńska, A., Heidari, S., Jahns, P., & Ebenhöh, O. (2016). A mathematical model of non-photochemical quenching to study short-term light memory in plants. Biochimica et Biophysica Acta (BBA) - Bioenergetics, 1857(12), 1860–1869. https://doi.org/10.1016/j.bbabio.2016.09.003"
        )


def style_guinding_questions(see_interpr: bool = False) -> None:
    # Remove the bullet point marker
    st.markdown(
        """<style>
        .st-emotion-cache-0.eqpbllx5 ul{
            list-style: none; /* Remove list bullets */
            padding: 0;
            margin: 0;
        }
        </style>""",
        unsafe_allow_html=True,
    )
    if see_interpr:
        # Replace the bullet point with a "A:"
        st.markdown(
            """<style>
            .st-emotion-cache-0.eqpbllx5 ul li:before{
                content: 'A:';
                padding-right: 10px;
                font-weight: bold;
                margin: 0 0 0 -25px;
            }
            </style>""",
            unsafe_allow_html=True,
        )
    else:
        # Replace the bullet point with a "Q:"
        st.markdown(
            """<style>
            .st-emotion-cache-0.eqpbllx5 ul li:before{
                content: 'Q:';
                padding-right: 10px;
                font-weight: bold;
                margin: 0 0 0 -27px;
            }
            </style>""",
            unsafe_allow_html=True,
        )
    return None


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version: str = st.session_state.setdefault("version", "4Bio")
    language: str = st.session_state.setdefault("language", "English")
    text = get_localised_text(version, language)
    placeholder_sidebar = make_sidebar()
    resetting_click_detector_setup()
    track_page_visit("first_analysis")
    see_interpr = make_page(text)
    make_literature(text, version, language)
    make_prev_next_button("computational models", "plant light memory")
    style_guinding_questions(see_interpr)
    fill_sidebar(placeholder_sidebar)
