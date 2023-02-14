import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from model import get_model
from modelbase.ode import Model, Simulator, _Simulate
from modelbase.typing import Array
from pages._sidebar import make_sidebar
from typing import Callable
from utils import get_localised_text


def make_simulation_data(slider_time: float, slider_light: int, slider_pings: float) -> tuple[Array, Array]:
    # Erstellen der passenden Liste
    n = round(slider_time * 60 / slider_pings)  # n: Pulsintervalle
    interval: list[float] = [1, 0.8, 30]  # definiere Listen mit den ersten beiden Impulsen
    light = [0, 5000, 0]

    for _ in range(n):
        interval.append(0.8)
        interval.append(slider_pings - 0.8)

    for _ in range(n):
        light.append(5000)
        light.append(slider_light)

    # light and interval for the model
    tprot = np.array(interval)
    ProtPFDs = np.array(light)
    return tprot, ProtPFDs


# Function for PAM experiment
def changingLight(
    model: Model,
    y0d: dict[str, float],
    lights: list[float],
    interval: list[float],
) -> _Simulate:
    s = Simulator(model)
    s.initialise(y0d)
    dt = 0.0
    for i in range(len(interval)):
        s.update_parameter("PFD", lights[i])
        dt += interval[i]
        s.simulate(
            dt,
            **{"rtol": 1e-16, "atol": 1e-8, "maxnef": 20, "maxncf": 10},
        )  # type: ignore
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
    npq = (Fm[0] - Fm) / Fm
    PhiPSII = (Fm - Fo) / Fm  # see Baker2000
    return Fm, npq, tm, Fo, to, PhiPSII


def simulate(updated_parameters, tprot, ProtPFDs):
    y0d = {"P": 0, "H": 6.32975752e-05, "E": 0, "A": 25.0, "Pr": 1, "V": 1}
    model = get_model()
    model.update_parameters(updated_parameters)
    PAM = changingLight(model, y0d, ProtPFDs, tprot)  # type: ignore
    F = PAM.get_variable(variable="Fluo")

    # FIXME: couple of variables are unused
    Fm, NPQ, tm, Fo, to, PhiPSII = get_NPQ(
        PAM.get_variable(variable="Fluo"),
        PAM.get_time(),
        PAM.get_variable(variable="L"),
        maxlight=5000,
    )

    return PAM, F, NPQ, tm, PhiPSII


def make_plot_meta_data(text: Callable[[str], str], slider_time: float):
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

    text = (
        alt.Chart(areas_data)  # type: ignore
        .mark_text(align="left", baseline="middle", dx=7, dy=-135, size=13)  # type: ignore
        .encode(x="start", x2="stop", text="Phasen", color=alt.value("#FAFAFA"))
    )

    return areas, text


def simple_plot(_, PAM, F, areas, text):
    chart_data = pd.DataFrame({"Fluoreszenz": F / max(F), "Zeit": PAM.get_time()})  # type: ignore

    chart = (
        alt.Chart(chart_data)  # type: ignore
        .mark_line(color="#FF4B4B")  # type: ignore
        .encode(
            x="Zeit",
            tooltip="Fluoreszenz",
            y=alt.Y("Fluoreszenz", axis=alt.Axis(title="Fluoreszenz [F´ₘ /Fₘ]")),  # type: ignore
        )
    )

    st.altair_chart(chart + text + areas, use_container_width=True)
    return areas, text


def expert_plot(NPQ, tm, PhiPSII, areas, text):
    left, right = st.columns(2)
    # second graph
    with left:
        chart_data1 = pd.DataFrame({"NPQ": NPQ, "Zeit": tm})

        chart1 = (
            alt.Chart(chart_data1)  # type: ignore
            .mark_line(color="#FF4B4B")  # type: ignore
            .encode(x=alt.X("Zeit"), tooltip="NPQ", y=alt.Y("NPQ", axis=alt.Axis(title="NPQ [a.u.]")))  # type: ignore
        )

        points1 = (
            alt.Chart(chart_data1)  # type: ignore
            .mark_point(filled=True, size=65, color="#FF4B4B")  # type: ignore
            .encode(x=alt.X("Zeit"), tooltip="NPQ", y=alt.Y("NPQ", axis=alt.Axis(title="NPQ [a.u.]")))  # type: ignore
        )

        st.altair_chart(chart1 + text + areas + points1, use_container_width=True)

        # third graph
    with right:
        chart_data2 = pd.DataFrame({"Phi": PhiPSII, "Zeit": tm})

        chart2 = (
            alt.Chart(chart_data2)  # type: ignore
            .mark_line(color="#FF4B4B")  # type: ignore
            .encode(x="Zeit", tooltip="Phi", y=alt.Y("Phi", axis=alt.Axis(title="Φ(PSII)")))  # type: ignore
        )

        points2 = (
            alt.Chart(chart_data2)  # type: ignore
            .mark_point(filled=True, size=65, color="#FF4B4B")  # type: ignore
            .encode(x=alt.X("Zeit"), tooltip="Phi", y=alt.Y("Phi", axis=alt.Axis(title="Φ(PSII)")))  # type: ignore
        )

        st.altair_chart(chart2 + text + areas + points2, use_container_width=True)


def make_page(text: Callable[[str], str]) -> None:
    # UI (Mainpage-Website)
    st.markdown(text("HEADLINE_ANALYSE"))
    st.markdown(text("INTRODUKTION"))

    # Assignments
    if version == "simple":
        with st.expander(text("TASK_1")):
            st.markdown(text("TASK_1_EXPLANATION"))
        with st.expander(text("TASK_2")):
            st.markdown(text("TASK_2_EXPLANATION"))
        with st.expander(text("TASK_3")):
            st.markdown(text("TASK_3_EXPLANATION"))
        with st.expander(text("TASK_4")):
            st.markdown(text("TASK_4_EXPLANATION"))
        with st.expander(text("TASK_5")):
            st.markdown(text("TASK_5_EXPLANATION"))

    st.markdown(text("HEADLINE_SLIDER"))
    st.markdown(text("EXPLANATNION"))
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

    if version == "expert":
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
            areas, text = make_plot_meta_data(text, slider_time)

            simple_plot(text, PAM, F, areas, text)

            if version == "expert":
                expert_plot(NPQ, tm, PhiPSII, areas, text)


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

    # if version == 'expert':
    #     with st.expander(text('RESULTS')):
    #         st.markdown(text('EXPLANATION_RESULTS'))


if __name__ == "__main__":
    version, language = make_sidebar()
    text = get_localised_text("b-Analyse", version, language)
    make_page(text)
    make_sliders(text)
    make_quiz(text)
