import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from model import get_model
from modelbase.ode import Simulator, _Simulate
from modelbase.ode.integrators import Scipy
from modelbase.typing import Array
from pages._monkey_patch import _simulate
from pages._sidebar import make_sidebar
from typing import Callable
from utils import get_localised_text, make_prev_next_button


# Function for PAM experiment
def changingLight(model, y0d, lights, interval):  # type: ignore
    s: _Simulate = Simulator(model, integrator=Scipy)  # type: ignore
    s._integrator._simulate = _simulate  # type: ignore
    s.initialise(y0d)
    dt = 0
    for i in range(len(interval)):
        s.update_parameter("PFD", lights[i])
        dt += interval[i]
        s.simulate(dt)
    return s


def get_NPQ(F, t, lights, maxlight):  # type: ignore
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
    NPQ = (Fm[0] - Fm) / Fm
    PhiPSII = (Fm - Fo) / Fm  # see Baker2000
    return Fm, NPQ, tm, Fo, to, PhiPSII


def create_simulation_parameters(slider_time: float, slider_light: float) -> tuple[Array, Array]:
    tprot = np.array(
        [
            1.0,
            0.8,
            28,
            0.8,
            30,
            0.8,
            50,
            0.8,
            69,
            0.8,
            90,
            0.8,
            110,
            0.8,
            130,
            0.8,
            151,
            0.8,
            171,
            0.8,
            29,
            0.8,
            49,
            0.8,
            70,
            0.8,
            90,
            0.8,
            109,
            0.8,
            slider_time * 60,
            0.8,
            30,
            0.8,
            30,
            0.8,
            50,
            0.8,
            70,
            0.8,
            90,
            0.8,
            110,
            0.8,
        ]
    )

    ProtPFDs = np.array(
        [
            0.0,
            5000.0,
            0.0,
            5000.0,
            slider_light,
            5000.0,
            slider_light,
            5000.0,
            slider_light,
            5000.0,
            slider_light,
            5000.0,
            slider_light,
            5000.0,
            slider_light,
            5000.0,
            slider_light,
            5000.0,
            slider_light,
            5000.0,
            0.0,
            5000.0,
            0.0,
            5000.0,
            0.0,
            5000.0,
            0.0,
            5000.0,
            0.0,
            5000.0,
            0.0,
            5000.0,
            0.0,
            5000.0,
            slider_light,
            5000.0,
            slider_light,
            5000.0,
            slider_light,
            5000.0,
            slider_light,
            5000.0,
            slider_light,
            5000.0,
        ]
    )
    return tprot, ProtPFDs


def simulate(updated_parameters, tprot, ProtPFDs):
    y0d = {"P": 0, "H": 6.32975752e-05, "E": 0, "A": 25.0, "Pr": 1, "V": 1}
    model = get_model()
    model.update_parameters(updated_parameters)
    PAM = changingLight(model, y0d, ProtPFDs, tprot)
    F = PAM.get_variable(variable="Fluo")
    Fm, NPQ, tm, Fo, to, PhiPSII = get_NPQ(
        PAM.get_variable(variable="Fluo"),
        PAM.get_time(),
        PAM.get_variable(variable="L"),
        maxlight=5000,
    )

    return PAM, F, NPQ, tm, PhiPSII


def make_plot_meta(text: Callable[[str], str], slider_time: float):
    areas_data = pd.DataFrame(
        {
            "Phasen": ["Dunkelphase", "Trainingsphase", "Dunkelphase", "Gedächtnisphase"],
            "Phasen+1": [" ", text("PHASE1"), text("PHASE2"), text("PHASE3")],
            "start": [0, 0.53, 14, 20 + slider_time],
            "stop": [0.53, 14, 20 + slider_time, 30 + slider_time],
            "color": ["#1c5bc7", "#cf6d0c", "#1c5bc7", "#d10a0d"],
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
            x=alt.X("start", axis=alt.Axis(title=text("AXSIS_TIME"))),  # type: ignore
        )
    )

    # Einfügen der Phasenbeschriftung
    chart_labels = (
        alt.Chart(areas_data)  # type: ignore
        .mark_text(align="left", baseline="middle", dx=7, dy=-135, size=13)  # type: ignore
        .encode(x="start", x2="stop", text="Phasen+1", color=alt.value("#FAFAFA"))
    )

    return areas, chart_labels


def make_simple_plot(chart_data, areas, chart_labels):
    chart = (
        alt.Chart(chart_data)  # type: ignore
        .mark_line(color="#FF4B4B")  # type: ignore
        .encode(x="Zeit", y="Fluoreszenz", tooltip="Fluoreszenz")
    )

    # coloured areas

    st.altair_chart(areas + chart + chart_labels, use_container_width=True)


def make_expert_plot(NPQ, tm, PhiPSII, areas, chart_labels, left, right):
    left, right = st.columns(2)

    def create_chart_data(data, x, y):
        chart_data = pd.DataFrame({x: data[x], y: data[y]})
        return chart_data

    def create_chart(text: Callable[[str], str], chart_data, x, y, color):
        chart = (
            alt.Chart(chart_data)
            .mark_line(color=color)
            .encode(
                x=alt.X(x, axis=alt.Axis(title=text("TIME"))),
                y=alt.Y(y, axis=alt.Axis(title=text("FLUO"))),  # type: ignore
            )
        )
        return chart

    def create_points(text: Callable[[str], str], chart_data, x, y, color):
        points = (
            alt.Chart(chart_data)
            .mark_point(filled=True, size=65, color=color)
            .encode(
                x=alt.X(x, axis=alt.Axis(title=text("TIME"))),
                y=alt.Y(y, axis=alt.Axis(title=text("FLUO"))),
            )
        )
        return points

    chart_data1 = create_chart_data({"NPQ": NPQ, "Zeit": tm / 60}, "Zeit", "NPQ")
    chart_data2 = create_chart_data({"Phi": PhiPSII, "Zeit": tm / 60}, "Zeit", "Phi")

    chart1 = create_chart(chart_data1, "Zeit", "NPQ", "#FF4B4B")
    points1 = create_points(chart_data1, "Zeit", "NPQ", "#FF4B4B")

    chart2 = create_chart(chart_data2, "Zeit", "Phi", "#FF4B4B")
    points2 = create_points(chart_data2, "Zeit", "Phi", "#FF4B4B")

    with left:
        st.altair_chart(chart1 + chart_labels + areas + points1, use_container_width=True)
    with right:
        st.altair_chart(chart2 + chart_labels + areas + points2, use_container_width=True)


# FIXME: version here should probably be replaced by text
def make_page(text: Callable[[str], str], version: str) -> None:
    st.markdown(text("HEADLINE_BRAIN"))

    # FIXME: why is col3 unused?
    col1, col2, _ = st.columns(3)
    with col2:
        st.image("pictures/Kurzvideo-Pflanzengedachtnis.gif")

    st.markdown(text("INTRODUCTION_BRAIN"))

    if version == "simple":
        with st.expander(text("TASK_1")):
            st.markdown(text("TASK_1_EXPLANATION"))

        with st.expander(text("TASK_2")):
            st.markdown(text("TASK_2_EXPLANATION"))

    st.markdown(text("TIP1"))

    st.markdown(text("TIP2"))

    # slider zum Einstellen in zwei Spalten angeordnet
    col1, col2 = st.columns(2)
    with col1:
        slider_light = st.slider(
            text("SLIDER_LIGHT"),  # Exponenten können reincopiert werden durch commands
            100,
            900,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
        )
    with col2:
        slider_time = st.slider(text("SLIDER_TIME"), 5, 60)
    if version == "expert":
        col1, col2 = st.columns(2)
        with col1:
            slider_aktivation = st.slider(
                text("SLIDER_ACTIVATION"),
                -100,
                +100,
                0,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
            )
        with col2:
            slider_deaktivation = st.slider(
                text("SLIDER_DEACTIVATION"),
                -100,
                +100,
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

    # light and interval for the model
    tprot, ProtPFDs = create_simulation_parameters(slider_time, slider_light)

    # open everything behind
    if st.button("Start", type="primary"):
        with st.spinner(text("SPINNER")):  # loading indicator
            # plt the graph
            PAM, F, NPQ, tm, PhiPSII = simulate(updated_parameters, tprot, ProtPFDs)

            # maingraph
            chart_data = pd.DataFrame({"Fluoreszenz": F / max(F), "Zeit": PAM.get_time() / 60})
            areas, chart_labels = make_plot_meta(text, slider_time)

            make_simple_plot(chart_data, areas, chart_labels)

            left, right = st.columns(2)

            if version == "expert":
                # second Graph
                make_expert_plot(NPQ, tm, PhiPSII, areas, chart_labels, left, right)

    with st.expander(text("CONCLUSION")):
        st.markdown(text("BEGIN_OF_CONCLUTION"))

        st.markdown(text("CONCLUTION_POINT_1"))
        st.markdown(text("CONCLUTION_POINT_2"))
        st.markdown(text("CONCLUTION_POINT_3"))

        st.markdown(text("END_OF_CONCLUTION"))


if __name__ == "__main__":
    version, language = make_sidebar()
    _ = get_localised_text("b-brain", version, language)
    make_page(_, version)
    make_prev_next_button("experiments in silico", None)
