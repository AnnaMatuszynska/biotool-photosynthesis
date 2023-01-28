import altair as alt
import gettext
import numpy as np
import os.path
import pandas as pd
import streamlit as st
from model import M16model, Simulator
from modelbase.ode import Model, _Simulate

_ = gettext.gettext

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

# headline sidebar
st.sidebar.write("## Settings :gear:")

# decide which version and language
version_options = {"simple": "Simple", "expert": "Expert"}

version = st.sidebar.selectbox(
    "⚙ Version 👩‍🎓👩🏼‍🔬", version_options.keys(), format_func=lambda x: version_options[x]
)

language = st.sidebar.selectbox("⚙ Language 🌍💬", ["English", "German"])
try:
    localizator = gettext.translation(
        "b-Analyse", localedir=os.path.join("locales", version), languages=[language]
    )
    localizator.install()
    _ = localizator.gettext
except:
    pass

# UI (Mainpage-Website)
st.markdown(_("HEADLINE_ANALYSE"))

st.markdown(_("INTRODUKTION"))

# Assignments
if version == "simple":
    with st.expander(_("TASK_1")):
        st.markdown(_("TASK_1_EXPLANATION"))

    with st.expander(_("TASK_2")):
        st.markdown(_("TASK_2_EXPLANATION"))

    with st.expander(_("TASK_3")):
        st.markdown(_("TASK_3_EXPLANATION"))

    with st.expander(_("TASK_4")):
        st.markdown(_("TASK_4_EXPLANATION"))

    with st.expander(_("TASK_5")):
        st.markdown(_("TASK_5_EXPLANATION"))


st.markdown(_("HEADLINE_SLIDER"))

st.markdown(_("EXPLANATNION"))

st.markdown(_("TIPP1"))

st.markdown(_("TIPP2"))


# Function for PAM experiment
def changingLight(
    model: Model, y0d: dict[str, float], lights: list[float], interval: list[float]
) -> _Simulate:
    s = Simulator(model)
    s.initialise(y0d)
    dt = 0.0
    for i in range(len(interval)):
        s.update_parameter("PFD", lights[i])
        dt += interval[i]
        s.simulate(dt, **{"rtol": 1e-16, "atol": 1e-8, "maxnef": 20, "maxncf": 10})
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


# slider zum Einstellen in zwei Spalten angeordnet
slider_light = st.slider(
    _("SLIDER_LIGHT"),  # Exponenten können reinkopiert werden durch commands
    100,
    900,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
)

col1, col2 = st.columns(2)
with col1:
    slider_time = st.slider(
        _("SLIDER_TIME"),
        5,
        30,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
    )
with col2:
    slider_pings = st.slider(_("SLIDER_PULSES"), 20, 150, 85)

if version == "expert":
    col1, col2 = st.columns(2)
    with col1:
        slider_aktivation = st.slider(
            _("SLIDER_ACTIVATION"),
            -1000,
            +1000,
            0,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
        )
    with col2:
        slider_deaktivation = st.slider(
            _("SLIDER_DEACTIVATION"),
            -1000,
            +1000,
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

if st.button("Start", type="primary"):
    with st.spinner(_("SPINNER")):

        # Erstellen der passenden Liste
        n = round(slider_time * 60 / slider_pings)  # n: Pulsintervalle
        interval = [1, 0.8, 30]  # definiere Listen mit den ersten beiden Impulsen
        light = [0, 5000, 0]
        for i in range(n):
            interval.append(0.8)
            interval.append(slider_pings - 0.8)

        for i in range(n):
            light.append(5000)
            light.append(slider_light)

        # light and interval for the model
        tprot = np.array(interval)
        ProtPFDs = np.array(light)

        # plt the graph
        y0d = {"P": 0, "H": 6.32975752e-05, "E": 0, "A": 25.0, "Pr": 1, "V": 1}
        model_copy = M16model.copy()
        model_copy.update_parameters(updated_parameters)
        PAM = changingLight(model_copy, y0d, ProtPFDs, tprot)
        F = PAM.get_variable(variable="Fluo")
        Fm, NPQ, tm, Fo, to, PhiPSII = get_NPQ(
            PAM.get_variable(variable="Fluo"), PAM.get_time(), PAM.get_variable(variable="L"), maxlight=5000
        )

        # maingraph
        chart_data = pd.DataFrame({"Fluoreszenz": F / max(F), "Zeit": PAM.get_time()})

        chart = (
            alt.Chart(chart_data)
            .mark_line(color="#FF4B4B")
            .encode(
                x="Zeit",
                tooltip="Fluoreszenz",
                y=alt.Y("Fluoreszenz", axis=alt.Axis(title="Fluoreszenz [F´ₘ /Fₘ]")),
            )
        )

        # coloured areas
        areas_data = pd.DataFrame(
            {
                "Phasen": ["", _("MEASUREMENT_PHASE")],
                "start": [0, 0.53 * 60],
                "stop": [0.53 * 60, 0.53 * 60 + slider_time * 60],
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
                x=alt.X("start", axis=alt.Axis(title=_("TIME"))),
            )
        )

        # Einfügen der Phasenbeschriftung
        text = (
            alt.Chart(areas_data)
            .mark_text(align="left", baseline="middle", dx=7, dy=-135, size=13)
            .encode(x="start", x2="stop", text="Phasen", color=alt.value("#FAFAFA"))
        )

        st.altair_chart(chart + text + areas, use_container_width=True)

        left, right = st.columns(2)

        if version == "expert":
            # second graph
            with left:
                chart_data1 = pd.DataFrame({"NPQ": NPQ, "Zeit": tm})

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
                chart_data2 = pd.DataFrame({"Phi": PhiPSII, "Zeit": tm})

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

# QUIZ STARTS HERE
if version == "simple":
    with st.expander(_("KONTROLL")):
        st.markdown(_("INTRODUCTION_QUESTION"))
        option1 = st.radio(_("QUESTION_1"), ("None", _("AW1"), _("AW2")), index=0)
        if option1 == _("AW1"):
            st.markdown(_("RA1"))
        elif option1 == _("AW2"):
            st.markdown(_("RA2"))

        option2 = st.radio(_("QUESTION_2"), ("None", _("AW3"), _("AW4"), _("AW5")), index=0)
        if option2 == _("AW4"):
            st.markdown(_("RA3"))
        elif option2 == _("AW4") or option2 == _("AW5"):
            st.markdown(_("RA4"))

        option2 = st.radio(_("QUESTION_3"), ("None", _("AW6"), _("AW7")), index=0)
        if option2 == _("AW6"):
            st.markdown(_("RA5"))
        elif option2 == _("AW7"):
            st.markdown(_("RA6"))

# Text not yet written
# st.markdown(_('STOPP'))
# if version == 'simple':
#     with st.expander(_('RESULTS')):
#         st.markdown(_('EXPLANATION_RESULTS'))

# if version == 'expert':
#     with st.expander(_('RESULTS')):
#         st.markdown(_('EXPLANATION_RESULTS'))
