import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from model import get_model
from modelbase.ode import Model, Simulator, _Simulate
from modelbase.ode.integrators import Scipy
from pages._monkey_patch import _simulate
from pages._sidebar import make_sidebar
from PIL import Image
from typing import Any, Callable
from utils import get_localised_text, make_prev_next_button


def make_simulation_data(slider_time: float, slider_light: int, slider_pings: float) -> tuple:
    # Calculate the number of pulse intervals
    n_intervals = round(slider_time * 60 / slider_pings)

    # Define the initial pulse intervals and light values
    intervals = [1, 0.8, 30]
    light_values = [0, 5000, 0]

    # Append additional pulse intervals and light values
    for _ in range(n_intervals):
        intervals.extend([0.8, slider_pings - 0.8])
        light_values.extend([5000, slider_light])

    # Convert lists to numpy arrays
    tprot = np.array(intervals)
    ProtPFDs = np.array(light_values)

    return tprot, ProtPFDs


# Function for PAM experiment
def changingLight(
    model: Model,
    y0d: dict[str, float],
    lights: list[float],
    interval: list[float],
) -> _Simulate:
    s: _Simulate = Simulator(model, integrator=Scipy)  # type: ignore
    s._integrator._simulate = _simulate  # type: ignore
    s.initialise(y0d)
    dt = 0.0
    for i in range(len(interval)):
        s.update_parameter("PFD", lights[i])
        dt += interval[i]
        s.simulate(dt)  # type: ignore
    return s


def get_NPQ(F: Any, t: Any, lights: Any, maxlight: Any) -> Any:
    z = []  # container for lists. Each list contains the positions of fluorescence values for one peak
    o = []  # container for position of Fo'
    cnt = 0
    while cnt < len(lights):
        if lights[cnt] == maxlight:
            h = []  # temporary container for all F==maxlight. For each peak it is renewed
            while cnt != len(lights) and lights[cnt] == maxlight:
                h.append(cnt)
                cnt += 1
            z.append(h)
            o.append(h[0] - 1)  # value directly at the bottom of peak is Fo
        else:
            cnt += 1
    peaks = [i[np.argmax(F[i])] for i in z]  # Fm is the maximal value for each peak sequence
    Fm = F[peaks]
    tm = t[peaks]
    Fo = F[o]
    to = t[o]
    npq = (Fm[0] - Fm) / Fm
    PhiPSII = (Fm - Fo) / Fm  # see Baker2000
    return Fm, npq, tm, Fo, to, PhiPSII


def simulate(updated_parameters: dict[str, float], tprot: Any, ProtPFDs: Any) -> Any:
    y0d = {"P": 0, "H": 6.32975752e-05, "E": 0, "A": 25.0, "Pr": 1, "V": 1}
    model = get_model()
    model.update_parameters(updated_parameters)
    PAM = changingLight(model, y0d, ProtPFDs, tprot)  # type: ignore
    F = PAM.get_variable(variable="Fluo")

    _, NPQ, tm, _, _, PhiPSII = get_NPQ(
        PAM.get_variable(variable="Fluo"),
        PAM.get_time(),
        PAM.get_variable(variable="L"),
        maxlight=5000,
    )

    return PAM, F, NPQ, tm, PhiPSII


def make_plot_meta_data(text: Callable[[str], str], slider_time: float) -> Any:
    areas_data = pd.DataFrame(
        {
            "Phasen": ["", text("MEASUREMENT_PHASE")],
            "start": [0, 0.53 * 60],
            "stop": [0.53 * 60, 0.53 * 60 + slider_time * 60],
            "color": ["#1c5bc7", "#cf6d0c"],
        }
    )

    areas = (
        alt.Chart(areas_data.reset_index())  # type: ignore
        .mark_rect(opacity=0.3)  # type: ignore
        .encode(
            x2="stop",
            y=alt.value(0),
            y2=alt.value(290),  # pixels from top
            color=alt.Color("color", scale=None, legend=None),  # type: ignore
            x=alt.X("start", axis=alt.Axis(title=text("TIME"))),  # type: ignore
        )
    )

    chart_labels = (
        alt.Chart(areas_data)  # type: ignore
        .mark_text(align="left", baseline="middle", dx=7, dy=-135, size=13)  # type: ignore
        .encode(x="start", x2="stop", text="Phasen", color=alt.value("#FAFAFA"))
    )

    return areas, chart_labels


def simple_plot(text: Callable[[str], str], PAM: Any, F: Any, areas: Any, chart_labels: Any) -> Any:
    chart_data = pd.DataFrame({"Fluoreszenz": F / max(F), "Zeit": PAM.get_time()})  # type: ignore

    chart = (
        alt.Chart(chart_data)  # type: ignore
        .mark_line(color="#FF4B4B")  # type: ignore
        .encode(
            x="Zeit",
            tooltip="Fluoreszenz",
            y=alt.Y("Fluoreszenz", axis=alt.Axis(title=text("FLUO"))),  # type: ignore
        )
    )

    st.altair_chart(chart + chart_labels + areas, use_container_width=True)
    return areas, chart_labels


def expert_plot(NPQ: Any, tm: Any, PhiPSII: Any, areas: Any, chart_labels: Any) -> Any:
    # Define the left and right chart columns
    left, right = st.columns(2)

    # Create the first chart
    chart_data1 = pd.DataFrame({"NPQ": NPQ, "Zeit": tm})
    chart1 = (
        alt.Chart(chart_data1)
        .mark_line(color="#FF4B4B")
        .encode(x=alt.X("Zeit"), y=alt.Y("NPQ", axis=alt.Axis(title="NPQ [a.u.]")), tooltip="NPQ")
    )
    points1 = chart1.mark_point(filled=True, size=65, color="#FF4B4B")

    # Create the second chart
    chart_data2 = pd.DataFrame({"Phi": PhiPSII, "Zeit": tm})
    chart2 = (
        alt.Chart(chart_data2)
        .mark_line(color="#FF4B4B")
        .encode(x="Zeit", y=alt.Y("Phi", axis=alt.Axis(title="Φ(PSII)")), tooltip="Phi")
    )
    points2 = chart2.mark_point(filled=True, size=65, color="#FF4B4B")

    # Add the areas and labels
    chart1 = chart1 + chart_labels + areas + points1
    chart2 = chart2 + chart_labels + areas + points2

    # Display the charts in their respective columns
    with left:
        st.altair_chart(chart1, use_container_width=True)
    with right:
        st.altair_chart(chart2, use_container_width=True)


def make_page(text: Callable[[str], str]) -> None:
    st.markdown(text("HEADLINE_MODEL_CONSTRUCTION"))

    st.markdown(text("CONSTRUCTION_EXPLANATION"))
    st.markdown(text("RATES_1"), unsafe_allow_html=True)
    st.markdown(text("RATES_2"))
    st.markdown(text("RATES_3"))
    st.markdown(text("RATES_4"))
    st.markdown(text("RATES_5"))
    st.markdown(text("RATES_6"), unsafe_allow_html=True)

    if version == "Advanced":
        st.markdown(text("HEADLINE_MODEL_EQUATIONS"))
        st.markdown(text("MODEL_EQUATIONS_INTRODUCTION"))
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

        with st.expander(text("REACTION_RATES")):
            st.markdown(text("RATES_DYNAMIC"))
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

            st.markdown(text("RATE_QUENCHER"))
            st.latex(
                r"""
                \begin{aligned}
                    v_\mathrm{Xcyc} &= k_\mathrm{DeepoxV} \cdot \frac{H^\mathrm{nH_X}}{H^\mathrm{nH_X} + pH_{\mathrm{inv}}(K_\mathrm{phSat})^\mathrm{nH_X}} \cdot \mathrm{Vx} - k_\mathrm{EpoxZ} \cdot (\mathrm{X^{tot}} - \mathrm{Vx}) \\
                    v_\mathrm{Psbs^{p}} &= k_\mathrm{ProtonationL} \cdot \frac{H^\mathrm{nH_L}} {H^\mathrm{nH_L} + pH_{\mathrm{inv}}(K_\mathrm{phSatLHC})^\mathrm{nH_L}} \cdot \mathrm{PsbS} - k_\mathrm{Deprotonation} \cdot \mathrm{PsbS^p} \\
                    Q &= \gamma_0 \cdot (1-\frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}})\cdot\mathrm{PsbS}+ \gamma_1\cdot(1-\frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}})\cdot\mathrm{PsbS^p} + \gamma_2\cdot \frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}}\cdot\mathrm{PsbS^p} + \gamma_3\cdot \frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}}\cdot\mathrm{PsbS} \\
                \end{aligned}
                """
            )

    st.markdown(text("HEADLINE_IMPLEMENTATION"))

    st.markdown(text("IMPLEMENTATION_DESCRIPTION"))

    if version == "Simple":
        st.markdown(text("IMPLEMENTATION_TO_EXPERT"))

    # UI (Mainpage-Website)
    st.markdown(text("HEADLINE_ANALYSE"))
    st.markdown(text("INTRODUKTION"))

    # Assignments
    if version == "simple":
        with st.expander(text("TASK_1")):
            st.markdown(text("TASK_ANALYSIS_1_EXPLANATION"))
        with st.expander(text("TASK_2")):
            st.markdown(text("TASK_ANALYSIS_2_EXPLANATION"))
        with st.expander(text("TASK_3")):
            st.markdown(text("TASK_ANALYSIS_3_EXPLANATION"))
        with st.expander(text("TASK_4")):
            st.markdown(text("TASK_ANALYSIS_4_EXPLANATION"))
        with st.expander(text("TASK_5")):
            st.markdown(text("TASK_ANALYSIS_5_EXPLANATION"))

    st.markdown(text("HEADLINE_SLIDER"))
    st.markdown(text("EXPLANATNION"))
    st.video("https://youtu.be/zxGZKeopEDw")
    st.markdown(text("TIPP1"))
    st.markdown(text("TIPP2"))


def make_sliders(text: Callable[[str], str]) -> None:
    # slider zum Einstellen in zwei Spalten angeordnet
    slider_light = st.slider(
        text("SLIDER_LIGHT"),  # Exponenten können reinkopiert werden durch commands
        100,
        900,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
    )

    col1, col2 = st.columns(2)
    with col1:
        slider_time = st.slider(
            text("SLIDER_TIME"),
            5,
            30,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
        )
    with col2:
        slider_pings = st.slider(text("SLIDER_PULSES"), 20, 150, 85)

    if version == "Advanced":
        col1, col2 = st.columns(2)
        with col1:
            slider_aktivation = st.slider(
                text("SLIDER_ACTIVATION"),
                -1000,
                +1000,
                0,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
            )
        with col2:
            slider_deaktivation = st.slider(
                text("SLIDER_DEACTIVATION"),
                -1000,
                +1000,
                0,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
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

    if st.button("Start", type="primary"):
        with st.spinner(text("SPINNER")):
            tprot, ProtPFDs = make_simulation_data(slider_time, slider_light, slider_pings)

            # Simulate
            PAM, F, NPQ, tm, PhiPSII = simulate(updated_parameters, tprot, ProtPFDs)

            # coloured areas
            areas, chart_labels = make_plot_meta_data(text, slider_time)

            simple_plot(text, PAM, F, areas, chart_labels)

            if version == "Advanced":
                expert_plot(NPQ, tm, PhiPSII, areas, chart_labels)


def make_quiz(text: Callable[[str], str]) -> None:
    # delete all first options in st.radio -> no preselected anymore
    st.markdown(
        """ <style>
                div[role="radiogroup"] >  :first-child{
                    display: none !important;
                }
            </style>
            """,
        unsafe_allow_html=True,
    )

    if version == "simple":
        with st.expander(text("KONTROLL")):
            st.markdown(text("INTRODUCTION_QUESTION"))
            option1 = st.radio(text("QUESTION_1"), ("None", text("AW1"), text("AW2")), index=0)
            if option1 == text("AW1"):
                st.markdown(text("RA1"))
            elif option1 == text("AW2"):
                st.markdown(text("RA2"))

            option2 = st.radio(text("QUESTION_2"), ("None", text("AW3"), text("AW4"), text("AW5")), index=0)
            if option2 == text("AW4"):
                st.markdown(text("RA3"))
            elif option2 == text("AW4") or option2 == text("AW5"):
                st.markdown(text("RA4"))

            option2 = st.radio(text("QUESTION_3"), ("None", text("AW6"), text("AW7")), index=0)
            if option2 == text("AW6"):
                st.markdown(text("RA5"))
            elif option2 == text("AW7"):
                st.markdown(text("RA6"))

    # Text not yet written
    # st.markdown(text('STOPP'))
    # if version == 'simple':
    #     with st.expander(text('RESULTS')):
    #         st.markdown(text('EXPLANATION_RESULTS'))

    # if version == 'Advanced':
    #     with st.expander(text('RESULTS')):
    #         st.markdown(text('EXPLANATION_RESULTS'))


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    with open("./.streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    version, language = make_sidebar()
    text = get_localised_text(version, language)
    make_page(text)
    include_image("pictures/slider-default-value.png", 0.6, text("CAPTION_DEFAULT_SLIDERS"))
    make_sliders(text)
    make_quiz(text)
    make_prev_next_button("computational models", "plant light memory")
