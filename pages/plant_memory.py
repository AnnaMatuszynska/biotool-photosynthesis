import datetime
import numpy as np
import streamlit as st
import time
from matplotlib import patches
from matplotlib import pyplot as plt
from model import get_model
from modelbase.ode import Simulator
from pages._sidebar import fill_sidebar, make_sidebar
from pages.assets.model._model_functions import calculate_results_to_plot, make_plot, sim_model_memory
from scipy.signal import find_peaks, peak_prominences
from typing import Any, Callable
from utils import (
    get_localised_text,
    make_prev_next_button,
    markdown_click,
    resetting_click_detector_setup,
    track_page_visit,
)


def make_page(text: Callable[[str], str], version: str) -> None:
    st.markdown(text("MEM_HEADLINE_BRAIN"))

    # Learning objectives
    st.info(text("MEM_LEARNING_OBJECTIVES"))

    col1, col2, _ = st.columns(3)
    with col2:
        st.image("pictures/Kurzvideo-Pflanzengedachtnis.gif")

    markdown_click("MEM_INTRODUCTION_BRAIN", text)

    col1, col2, _ = st.columns(3)
    with col2:
        st.image("pictures/memory_protocol.png")

    # Add guiding questions:
    see_interpr = False
    # with st.expander(text("MEM_GUIDING_EXPANDER")):
    #     # The answers are hidden by default
    #     st.markdown(text("MEM_GUIDING_HEADER"))
    #     see_interpr = st.toggle(text("MEM_GUIDING_TOGGLE"))

    #     if not see_interpr:
    #         st.markdown(text("MEM_GUIDING_QUESTIONS"))
    #     else:  # If toggle is switched show possible interpretation
    #         st.markdown(text("MEM_GUIDING_ANSWERS"))

    # slider zum Einstellen in zwei Spalten angeordnet
    with st.form("memory_model"):
        col1, col2 = st.columns(2)
        with col1:
            slider_light = st.slider(
                text("SLIDER_LIGHT"),  # Exponenten können reinkopiert werden durch commands
                100,
                900,
                key="light2",  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
            )
        with col2:
            slider_pings = st.slider(label=text("SLIDER_PULSES"), min_value=10, max_value=60, value=20)

        col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

        with col1:
            slider_training = st.slider(label=text("MEM_SLIDER_TRAINING"), min_value=0, max_value=5, value=2)
        with col2:
            slider_relaxation = st.slider(
                label=text("MEM_SLIDER_RELAXATION"), min_value=0, max_value=5, value=2
            )
        with col3:
            slider_memory = st.slider(label=text("MEM_SLIDER_MEMORY"), min_value=0, max_value=5, value=2)

        if version == "4Bio":
            slider_darklength = 60
            slider_saturate = 5000
            col1, col2 = st.columns(2)
            with col1:
                slider_aktivation = st.select_slider(
                    text("SLIDER_ACTIVATION"),
                    options=np.round(np.logspace(0, 4, 21)).astype(int),
                    value=100,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
                )
            with col2:
                slider_deaktivation = st.select_slider(
                    text("SLIDER_DEACTIVATION"),
                    options=np.round(np.logspace(0, 4, 21)).astype(int),
                    value=100,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
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
            slider_darklength = 60
            slider_saturate = 5000

        if "memory_model_variables" not in st.session_state:
            st.session_state["memory_model_variables"] = {
                "New": {
                    "AL [μmol m⁻² s⁻¹]": slider_light,
                    "SP [μmol m⁻² s⁻¹]": slider_saturate,
                    "CtZ [s⁻¹]": round(updated_parameters["kDeepoxV"], 5),
                    "CtV [s⁻¹]": round(updated_parameters["kEpoxZ"], 6),
                }
            }
        else:
            st.session_state["memory_model_variables"]["New"].update(
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
            submitted = st.form_submit_button(
                "Start the simulation", type="primary", use_container_width=True
            )

        if submitted:
            with st.spinner(text("SPINNER")):  #
                time.sleep(0.1)
                sim_time, sim_results = sim_model_memory(
                    updated_parameters=updated_parameters,
                    slider_light=slider_light,
                    slider_pings=slider_pings,
                    slider_saturate=slider_saturate,
                    slider_darklength=slider_darklength,
                    training_length=slider_training * 60,
                    relaxation_phase=slider_relaxation * 60,
                    memory_length=slider_memory * 60,
                )

                if "memory_model_results" not in st.session_state:
                    st.session_state["memory_model_results"] = calculate_results_to_plot(
                        sim_time, sim_results
                    )
                else:
                    st.session_state["memory_model_results"].update(
                        calculate_results_to_plot(sim_time, sim_results)
                    )

                if show_old:
                    plot_values = st.session_state["memory_model_results"]
                    plot_variables = st.session_state["memory_model_variables"]
                else:
                    plot_values = {
                        k: v
                        for k, v in st.session_state["memory_model_results"].items()
                        if k in ["Fluo", "NPQ", "PhiPSII"]
                    }
                    plot_variables = {"New": st.session_state["memory_model_variables"]["New"]}

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
                    new_label=text("NEW_LABEL"),
                    old_label=text("OLD_LABEL"),
                    memory_flag=True,
                    memory_length=slider_memory * 60,
                    training_length=slider_training * 60,
                    relaxation_length=slider_relaxation * 60,
                    annotation_labels={
                        "Training": text("MEM_ANNO_TRAINING"),
                        "Relaxation": text("MEM_ANNO_RELAXATION"),
                        "Memory": text("MEM_ANNO_MEMORY"),
                    },
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
                    new_label=text("NEW_LABEL"),
                    old_label=text("OLD_LABEL"),
                    memory_flag=True,
                    memory_length=slider_memory * 60,
                    training_length=slider_training * 60,
                    relaxation_length=slider_relaxation * 60,
                    annotation_labels={
                        "Training": text("MEM_ANNO_TRAINING"),
                        "Relaxation": text("MEM_ANNO_RELAXATION"),
                        "Memory": text("MEM_ANNO_MEMORY"),
                    },
                )

                st.session_state["memory_fig_4Bio"] = fig_4Bio
                st.session_state["memory_fig_4Math"] = fig_4Math

                old_results = {}
                for key, value in st.session_state["memory_model_results"].items():
                    old_results.update({f"old {key}": value})

                st.session_state["memory_model_results"].update(old_results)

                st.session_state["memory_model_variables"].update(
                    {"Old": {k: v for k, v in st.session_state["memory_model_variables"]["New"].items()}}
                )

        if "memory_fig_4Bio" in st.session_state and "memory_fig_4Math" in st.session_state:
            if version == "4Bio":
                showed_fig = st.session_state["memory_fig_4Bio"]
            else:
                showed_fig = st.session_state["memory_fig_4Math"]

            st.pyplot(showed_fig, transparent=True)
    return see_interpr


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


def make_literature(text: Callable[[str], str], language: str, version: str) -> None:
    with st.expander(text("LITERATURE")):
        st.markdown(text("LITERATURE_ONPAGE"))
        st.markdown(
            "- Matuszyńska, A., Heidari, S., Jahns, P., & Ebenhöh, O. (2016). A mathematical model of non-photochemical quenching to study short-term light memory in plants. Biochimica et Biophysica Acta (BBA) - Bioenergetics, 1857(12), 1860–1869. https://doi.org/10.1016/j.bbabio.2016.09.003"
        )


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version: str = st.session_state.setdefault("version", "4Bio")
    language: str = st.session_state.setdefault("language", "English")
    text = get_localised_text(version, language)
    placeholder_sidebar = make_sidebar()
    resetting_click_detector_setup()
    track_page_visit("plant_memory")
    see_interpr = make_page(text, version)
    make_literature(text, version, language)
    make_prev_next_button("experiments in silico", "take home messages")
    style_guinding_questions(see_interpr)
    fill_sidebar(placeholder_sidebar)
