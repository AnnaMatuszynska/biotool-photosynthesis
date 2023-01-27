import altair as alt
import gettext
import numpy as np
import os
import pandas as pd
import streamlit as st
from model import M16model, Simulator

_ = gettext.gettext

# headline sidebar
st.sidebar.write("## Settings :gear:")

# decide which version and language
version_options = {"simple": "Simple", "expert": "Expert"}

version = st.sidebar.selectbox(
    "⚙ Version 👩‍🎓👩🏼‍🔬", version_options.keys(), format_func=lambda x: version_options[x]
)

language = st.sidebar.selectbox("⚙ Language 🌍💬", ["English", "German"], label_visibility="visible")
try:
    localizator = gettext.translation(
        "b-brain", localedir=os.path.join("locales", version), languages=[language]
    )
    localizator.install()
    _ = localizator.gettext
except:
    pass


# Function for PAM experiment
def changingLight(model, y0d, lights, interval):
    s = Simulator(model)
    s.initialise(y0d)
    dt = 0
    for i in range(len(interval)):
        s.update_parameter("PFD", lights[i])
        dt += interval[i]
        s.simulate(dt, **{"rtol": 1e-16, "atol": 1e-8}) # "maxnef": 20, "maxncf": 10})
    return s


def get_NPQ(F, t, lights, maxlight):
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


# UI (Mainpage-Website)

st.markdown(_("HEADLINE_BRAIN"))

col1, col2, col3 = st.columns(3)
with col2:
    st.image("pictures/Kurzvideo-Pflanzengedachtnis.gif")

st.markdown(_("INTRODUCTION_BRAIN"))

if version == "simple":
    with st.expander(_("TASK_1")):
        st.markdown(_("TASK_1_EXPLANATION"))

    with st.expander(_("TASK_2")):
        st.markdown(_("TASK_2_EXPLANATION"))

st.markdown(_("TIP1"))

st.markdown(_("TIP2"))

# slider zum Einstellen in zwei Spalten angeordnet
col1, col2 = st.columns(2)
with col1:
    slider_light = st.slider(
        _("SLIDER_LIGHT"),  # Exponenten können reincopiert werden durch commands
        100,
        900,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
    )
with col2:
    slider_time = st.slider(_("SLIDER_TIME"), 5, 60)
if version == "expert":
    col1, col2 = st.columns(2)
    with col1:
        slider_aktivation = st.slider(
            _("SLIDER_ACTIVATION"),
            -100,
            +100,
            0,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
        )
    with col2:
        slider_deaktivation = st.slider(
            _("SLIDER_DEACTIVATION"),
            -100,
            +100,
            0,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
        )

    updated_parameters = {
        "kDeepoxV": 0.0024 * (1 + slider_aktivation / 100),  # Aktivierung des Quenchings
        "kEpoxZ": 0.00024 * (1 + slider_deaktivation / 100),  # 6.e-4,  #converted to [1/s]   # Deaktivierung
    }

else:
    updated_parameters = {
        "kDeepoxV": 0.0024,  # Aktivierung des Quenchings
        "kEpoxZ": 0.00024,  # 6.e-4,  #converted to [1/s]   # Deaktivierung
    }

# light and interval for the model
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

# open everything behind
if st.button("Start", type="primary"):
    with st.spinner(_("SPINNER")):  # loading indicator
        # plt the graph
        y0d = {"P": 0, "H": 6.32975752e-05, "E": 0, "A": 25.0, "Pr": 1, "V": 1}
        model_copy = M16model.copy()
        model_copy.update_parameters(updated_parameters)
        PAM = changingLight(model_copy, y0d, ProtPFDs, tprot)
        PAM = changingLight(M16model, y0d, ProtPFDs, tprot)
        F = PAM.get_variable(variable="Fluo")
        Fm, NPQ, tm, Fo, to, PhiPSII = get_NPQ(
            PAM.get_variable(variable="Fluo"), PAM.get_time(), PAM.get_variable(variable="L"), maxlight=5000
        )

        # maingraph
        chart_data = pd.DataFrame({"Fluoreszenz": F / max(F), "Zeit": PAM.get_time() / 60})

        chart = (
            alt.Chart(chart_data)
            .mark_line(color="#FF4B4B")
            .encode(x="Zeit", y="Fluoreszenz", tooltip="Fluoreszenz")
        )

        # coloured areas
        areas_data = pd.DataFrame(
            {
                "Phasen": ["Dunkelphase", "Trainingsphase", "Dunkelphase", "Gedächtnisphase"],
                "Phasen+1": [" ", _("PHASE1"), _("PHASE2"), _("PHASE3")],
                "start": [0, 0.53, 14, 20 + slider_time],
                "stop": [0.53, 14, 20 + slider_time, 30 + slider_time],
            }
        )

        areas = (
            alt.Chart(areas_data.reset_index())
            .mark_rect(opacity=0.3)  # Durchsichtigkeits
            .encode(
                x2="stop",
                y=alt.value(0),
                y2=alt.value(290),  # pixels from top
                color=alt.Color("Phasen", legend=None),
                x=alt.X("start", axis=alt.Axis(title=_("AXSIS_TIME"))),
            )
        )

        # Einfügen der Phasenbeschriftung
        text = (
            alt.Chart(areas_data)
            .mark_text(align="left", baseline="middle", dx=7, dy=-135, size=13)
            .encode(x="start", x2="stop", text="Phasen+1", color=alt.value("#FAFAFA"))
        )

        st.altair_chart(areas + chart + text, use_container_width=True)

        left, right = st.columns(2)

        if version == "expert":
            # secound Graph
            with left:
                chart_data1 = pd.DataFrame({"NPQ": NPQ, "Zeit": tm / 60})

                chart1 = (
                    alt.Chart(chart_data1)
                    .mark_line(color="#FF4B4B")
                    .encode(x=alt.X("Zeit"), tooltip="NPQ", y=alt.Y("NPQ", axis=alt.Axis(title="NPQ [a.u.]")))
                )

                points1 = (
                    alt.Chart(chart_data1)
                    .mark_point(filled=True, size=65, color="#FF4B4B")
                    .encode(x=alt.X("Zeit"), tooltip="NPQ", y=alt.Y("NPQ", axis=alt.Axis(title="NPQ [a.u.]")))
                )

                st.altair_chart(chart1 + text + areas + points1, use_container_width=True)

            # third graph
            with right:
                chart_data2 = pd.DataFrame({"Phi": PhiPSII, "Zeit": tm / 60})

                chart2 = (
                    alt.Chart(chart_data2)
                    .mark_line(color="#FF4B4B")
                    .encode(x="Zeit", tooltip="Phi", y=alt.Y("Phi", axis=alt.Axis(title="Φ(PSII)")))
                )

                points2 = (
                    alt.Chart(chart_data2)
                    .mark_point(filled=True, size=65, color="#FF4B4B")
                    .encode(x=alt.X("Zeit"), tooltip="Phi", y=alt.Y("Phi", axis=alt.Axis(title="Φ(PSII)")))
                )

                st.altair_chart(chart2 + text + areas + points2, use_container_width=True)
