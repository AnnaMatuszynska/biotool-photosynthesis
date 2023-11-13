import numpy as np
import streamlit as st
from matplotlib import patches
from matplotlib import pyplot as plt
from model import get_model
from modelbase.ode import Simulator
from pages._sidebar import make_sidebar
from scipy.signal import find_peaks, peak_prominences
from typing import Any, Callable
from utils import (
    get_localised_text,
    make_prev_next_button,
    markdown_click,
    resetting_click_detector_setup,
    simulate_period,
)


def make_matplotlib_plot_memory(
    text: Callable[[str], str],
    xlabel1,
    xlabel2,
    ylabel,
    time,
    values,
    dark_length,
    width,
    height,
    training_length,
    relaxation_length,
    memory_length,
):
    max_time = dark_length + training_length + relaxation_length + memory_length

    with plt.rc_context(
        {
            "axes.spines.right": False,
            "figure.frameon": True,
            "axes.facecolor": (0.0, 0.0, 0.0, 0),
            "figure.facecolor": (0.0, 0.0, 0.0, 0),
            "figure.edgecolor": (0.0, 0.0, 0.0, 0),
            "text.color": "#9296a4",
            "axes.labelcolor": "#9296a4",
            "xtick.color": "#9296a4",
            "ytick.color": "#9296a4",
            "figure.figsize": (width, height),
        }
    ):
        fig, ax = plt.subplots()
        ax.plot(time, values, color="#FF4B4B")

    # Add the dark phase length to the xticks
    default_xticks = ax.get_xticks()
    new_xticks = []
    for i in range(len(default_xticks)):
        try:
            if default_xticks[i] > dark_length and default_xticks[i - 1] < dark_length:
                new_xticks.append(dark_length)
                new_xticks.append(default_xticks[i])
            elif (
                default_xticks[i] > training_length + dark_length
                and default_xticks[i - 1] < training_length + dark_length
            ):
                new_xticks.append(training_length + dark_length)
                new_xticks.append(default_xticks[i])
            elif (
                default_xticks[i] > relaxation_length + training_length + dark_length
                and default_xticks[i - 1] < relaxation_length + training_length + dark_length
            ):
                new_xticks.append(relaxation_length + training_length + dark_length)
                new_xticks.append(default_xticks[i])
            else:
                new_xticks.append(default_xticks[i])
        except:
            pass

    ax.set_xticks(new_xticks)

    # Change the left and down limit
    ax.set_xlim(0, max_time)
    ax.set_ylim(0)

    # Highlight dark and light phase
    dark_patch = patches.Rectangle(
        xy=(ax.get_xlim()[0], ax.get_ylim()[0]),
        width=dark_length,
        height=ax.get_ylim()[1],
        facecolor="#1c5bc7",
        alpha=0.3,
    )
    training_patch = patches.Rectangle(
        xy=(dark_length, ax.get_ylim()[0]),
        width=training_length,
        height=ax.get_ylim()[1],
        facecolor="#cf6d0c",
        alpha=0.3,
    )
    relaxation_patch = patches.Rectangle(
        xy=(training_length + dark_length, ax.get_ylim()[0]),
        width=relaxation_length,
        height=ax.get_ylim()[1],
        facecolor="#1c5bc7",
        alpha=0.3,
    )
    memory_patch = patches.Rectangle(
        xy=(dark_length + training_length + relaxation_length, ax.get_ylim()[0]),
        width=memory_length,
        height=ax.get_ylim()[1],
        facecolor="#D10A0D",
        alpha=0.3,
    )
    patch_list = [dark_patch, training_patch, relaxation_patch, memory_patch]
    anno_list = [text("MEM_ANNO_TRAINING"), text("MEM_ANNO_RELAXATION"), text("MEM_ANNO_MEMORY")]

    for i in range(len(patch_list)):
        ax.add_patch(patch_list[i])
        if i != 0 and patch_list[i].get_width() != 0:
            rx, ry = patch_list[i].get_xy()
            cx = rx + patch_list[i].get_width() / 2
            cy = ry + patch_list[i].get_height() * 0.1
            ax.annotate(
                anno_list[i - 1],
                (cx, cy),
                ha="center",
                va="center",
                color="#323336",
                alpha=1,
                backgroundcolor="#9296a4",
            )

    # Create the top xaxis for the minutes
    ax_top = ax.secondary_xaxis("top", functions=(lambda x: x / 60, lambda x: x * 60))
    ax_top.set_color("#9296a4")

    # Add labels
    ax.set_xlabel(xlabel1)
    ax.set_ylabel(ylabel)
    ax_top.set_xlabel(xlabel2)

    for i in [ax, ax_top]:
        i.spines["bottom"].set_color("#9296a4")
        i.spines["left"].set_color("#9296a4")
        i.spines["top"].set_color("#9296a4")
        i.spines["right"].set_visible(False)

    ax.grid(visible=True, which="both", axis="both", color="#9296a4", alpha=0.5)
    return fig


def sim_model_memory(
    updated_parameters,
    slider_light,
    slider_pings,
    slider_saturate,
    slider_darklength,
    training_length,
    relaxation_phase,
    memory_length,
):
    m = get_model()
    m.update_parameters(updated_parameters)
    s = Simulator(m)

    y0 = {"P": 0, "H": 6.32975752e-05, "E": 0, "A": 25.0, "Pr": 1, "V": 1}
    s.initialise(y0)

    length_pulse = 0.8
    dark_light = 0
    training_length = int(training_length)
    relaxation_phase = int(relaxation_phase)

    # Dark Period
    if slider_darklength > 0:
        simulate_period(
            s=s,
            starting_time=2,
            length_phase=slider_darklength,
            pulse_intervall=slider_pings,
            starting_light=dark_light,
            saturating_pulse=slider_saturate,
            length_pulse=length_pulse,
            during_light=dark_light,
            dark_flag=True,
        )
    # Training
    if training_length > 0:
        simulate_period(
            s=s,
            starting_time=slider_darklength,
            length_phase=training_length,
            pulse_intervall=slider_pings,
            starting_light=dark_light,
            saturating_pulse=slider_saturate,
            length_pulse=length_pulse,
            during_light=slider_light,
        )
    # Relaxation phase 1
    if relaxation_phase > 0:
        simulate_period(
            s=s,
            starting_time=slider_darklength + training_length,
            length_phase=slider_darklength + training_length + relaxation_phase - slider_pings,
            pulse_intervall=slider_pings,
            starting_light=slider_light,
            saturating_pulse=slider_saturate,
            length_pulse=length_pulse,
            during_light=dark_light,
            dark_flag=True,
        )
    # Relaxation phase 2
    if relaxation_phase > 0:
        simulate_period(
            s=s,
            starting_time=slider_darklength + training_length + relaxation_phase - slider_pings,
            length_phase=slider_pings,
            pulse_intervall=slider_pings,
            starting_light=dark_light,
            saturating_pulse=slider_saturate,
            length_pulse=length_pulse,
            during_light=dark_light,
            dark_flag=True,
        )
    # Memory Phase
    if memory_length > 0:
        simulate_period(
            s=s,
            starting_time=slider_darklength + training_length + relaxation_phase,
            length_phase=memory_length,
            pulse_intervall=slider_pings,
            starting_light=dark_light,
            saturating_pulse=slider_saturate,
            length_pulse=length_pulse,
            during_light=slider_light,
        )
    # End
    s.update_parameter("PFD", slider_light)
    s.simulate(slider_darklength + training_length + relaxation_phase + memory_length)

    sim_time = s.get_time()
    sim_results = s.get_full_results_dict()
    return sim_time, sim_results


def make_sim_area_memory(text: Callable[[str], str]) -> None:
    # slider zum Einstellen in zwei Spalten angeordnet
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
        slider_relaxation = st.slider(label=text("MEM_SLIDER_RELAXATION"), min_value=0, max_value=5, value=2)
    with col3:
        slider_memory = st.slider(label=text("MEM_SLIDER_MEMORY"), min_value=0, max_value=5, value=2)

    if version == "4Bio":
        slider_darklength = 60
        slider_saturate = 5000
        col1, col2 = st.columns(2)
        with col1:
            slider_aktivation = st.select_slider(
                text("SLIDER_ACTIVATION"),
                options=np.round(np.logspace(1, 3, 21)),
                value=100,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
            )
        with col2:
            slider_deaktivation = st.select_slider(
                text("SLIDER_DEACTIVATION"),
                options=np.round(np.logspace(1, 3, 21)),
                value=100,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
            )

        updated_parameters = {
            "kDeepoxV": 0.0024 * (1 + slider_aktivation / 100),  # Aktivierung des Quenchings
            "kEpoxZ": 0.00024
            * (1 + slider_deaktivation / 100),  # 6.e-4,  #converted to [1/s]   # Deaktivierung
        }
    else:
        updated_parameters = {
            "kDeepoxV": 0.0024,  # Aktivierung des Quenchings
            "kEpoxZ": 0.00024,  # 6.e-4,  #converted to [1/s]   # Deaktivierung
        }
        slider_darklength = 60
        slider_saturate = 5000

    if st.button("Start", type="primary", key="button2"):
        with st.spinner(text("SPINNER")):
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

            PAM_F = sim_results["Fluo"]
            PAM_Fmax = max(sim_results["Fluo"])

            fig_PAM = make_matplotlib_plot_memory(
                text=text,
                xlabel1=text("AXIS_TIME_S"),
                xlabel2=text("AXIS_TIME_MIN"),
                ylabel=text("FLUO"),
                time=sim_time,
                values=PAM_F / PAM_Fmax,
                dark_length=slider_darklength,
                width=15,
                height=3,
                training_length=slider_training * 60,
                relaxation_length=slider_relaxation * 60,
                memory_length=slider_memory * 60,
            )

            st.pyplot(fig_PAM)

            if version == "4Bio":
                peaks, _ = find_peaks((PAM_F / PAM_Fmax), height=0)  # Find the Flourescence peaks (Fmaxs)
                NPQ = ((PAM_F[peaks][0] - PAM_F[peaks])) / PAM_F[peaks]

                prominences, prominences_left, prominences_right = peak_prominences(
                    (PAM_F / PAM_Fmax), peaks
                )  # Find the minima around the peaks
                Fo = [
                    (PAM_F / PAM_Fmax)[i] for i in prominences_left
                ]  # Fo is always the minima before the peak
                PhiPSII = (PAM_F[peaks] - Fo) / PAM_F[peaks]

                fig_NPQ = make_matplotlib_plot_memory(
                    text=text,
                    xlabel1=text("AXIS_TIME_S"),
                    xlabel2=text("AXIS_TIME_MIN"),
                    ylabel=text("AXIS_NPQ"),
                    time=sim_time[peaks],
                    values=NPQ,
                    dark_length=slider_darklength,
                    width=15 / 2,
                    height=6,
                    training_length=slider_training * 60,
                    relaxation_length=slider_relaxation * 60,
                    memory_length=slider_memory * 60,
                )

                fig_PhiPSII = make_matplotlib_plot_memory(
                    text=text,
                    xlabel1=text("AXIS_TIME_S"),
                    xlabel2=text("AXIS_TIME_MIN"),
                    ylabel=text("AXIS_PHIPSII"),
                    time=sim_time[peaks],
                    values=PhiPSII,
                    dark_length=slider_darklength,
                    width=15 / 2,
                    height=6,
                    training_length=slider_training * 60,
                    relaxation_length=slider_relaxation * 60,
                    memory_length=slider_memory * 60,
                )

                col1, col2 = st.columns([1, 1])
                with col1:
                    st.pyplot(fig_NPQ, use_container_width=True)
                with col2:
                    st.pyplot(fig_PhiPSII, use_container_width=True)


# FIXME: version here should probably be replaced by text
def make_page(text: Callable[[str], str], version: str) -> None:
    st.markdown(text("MEM_HEADLINE_BRAIN"))

    # FIXME: why is col3 unused?
    col1, col2, _ = st.columns(3)
    with col2:
        st.image("pictures/Kurzvideo-Pflanzengedachtnis.gif")

    markdown_click("MEM_INTRODUCTION_BRAIN", text)

    col1, col2, _ = st.columns(3)
    with col2:
        st.image("pictures/memory_protocol.png")

    st.markdown(text("MEM_TIP1"))

    st.markdown(text("MEM_TIP2"))

    make_sim_area_memory(text)


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
    resetting_click_detector_setup()
    make_page(text, version)
    make_literature(text, version, language)
    make_prev_next_button("experiments in silico", "take home messages")
    make_sidebar()
