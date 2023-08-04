import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path
from model import get_model
from modelbase.ode import Model, Simulator, _Simulate
from modelbase.ode.integrators import Scipy
from pages._monkey_patch import _simulate
from pages._sidebar import make_sidebar
from PIL import Image
from typing import Any, Callable
from utils import get_localised_text, make_prev_next_button, include_ytvideo, include_image, resetting_click_detector_setup, markdown_click
from matplotlib import pyplot as plt, patches
from scipy.signal import find_peaks, peak_prominences

def make_matplotlib_plot_advanced(text: Callable[[str], str], xlabel1, xlabel2, ylabel, time, values, max_time, dark_length, width, height):
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
        "figure.figsize": (width,height)
    }
):
        fig, axs = plt.subplot_mosaic(
            mosaic=[
                ['A', 'A'],
                ['B', 'C']
            ],
            constrained_layout=True
        )
        axs['A'].plot(time['PAM'], values['PAM'], color='#FF4B4B')
        axs['B'].plot(time['NPQ'], values['NPQ'], color='#FF4B4B')
        axs['C'].plot(time['PhiPSII'], values['PhiPSII'], color='#FF4B4B')

    for j in range(len([axs['A'], axs['B'], axs['C']])):
        ax = [axs['A'], axs['B'], axs['C']][j]
        # Add the dark phase length to the xticks
        default_xticks = ax.get_xticks()
        new_xticks = []
        for i in range(len(default_xticks)):
            try:
                if default_xticks[i] > dark_length and default_xticks[i-1] < dark_length:
                    new_xticks.append(dark_length)
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
            xy=(ax.get_xlim()[0],ax.get_ylim()[0]),
            width = dark_length,
            height = ax.get_ylim()[1],
            facecolor = '#1c5bc7',
            alpha = 0.3
        )
        light_patch = patches.Rectangle(
            xy=(dark_length,ax.get_ylim()[0]),
            width = max_time-dark_length,
            height = ax.get_ylim()[1],
            facecolor = '#cf6d0c',
            alpha = 0.3
        )

        ax.add_patch(dark_patch)
        ax.add_patch(light_patch)

        #Create the top xaxis for the minutes
        ax_top = ax.secondary_xaxis('top', functions=(lambda x: x/60, lambda x: x*60))
        ax_top.set_color("#9296a4")

        

        #Add labels
        ax.set_xlabel(xlabel1)
        ax.set_ylabel(ylabel[j])
        ax_top.set_xlabel(xlabel2)

        for i in [ax, ax_top]:
            i.spines['bottom'].set_color("#9296a4")
            i.spines['left'].set_color("#9296a4")
            i.spines['top'].set_color("#9296a4")
            i.spines['right'].set_visible(False)

    return fig

def make_matplotlib_plot(text: Callable[[str], str], xlabel1, xlabel2, ylabel, time, values, max_time, dark_length, width, height):
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
        "figure.figsize": (width,height)
    }
):
        fig, ax = plt.subplots()
        ax.plot(time,
            values,
            color = '#FF4B4B'    
        )

    # Add the dark phase length to the xticks
    default_xticks = ax.get_xticks()
    new_xticks = []
    for i in range(len(default_xticks)):
        try:
            if default_xticks[i] > dark_length and default_xticks[i-1] < dark_length:
                new_xticks.append(dark_length)
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
        xy=(ax.get_xlim()[0],ax.get_ylim()[0]),
        width = dark_length,
        height = ax.get_ylim()[1],
        facecolor = '#1c5bc7',
        alpha = 0.3
    )
    light_patch = patches.Rectangle(
        xy=(dark_length,ax.get_ylim()[0]),
        width = max_time-dark_length,
        height = ax.get_ylim()[1],
        facecolor = '#cf6d0c',
        alpha = 0.3
    )

    ax.add_patch(dark_patch)
    ax.add_patch(light_patch)

    #Create the top xaxis for the minutes
    ax_top = ax.secondary_xaxis('top', functions=(lambda x: x/60, lambda x: x*60))
    ax_top.set_color("#9296a4")

    

    #Add labels
    ax.set_xlabel(xlabel1)
    ax.set_ylabel(ylabel)
    ax_top.set_xlabel(xlabel2)

    for i in [ax, ax_top]:
        i.spines['bottom'].set_color("#9296a4")
        i.spines['left'].set_color("#9296a4")
        i.spines['top'].set_color("#9296a4")
        i.spines['right'].set_visible(False)

    
    return fig

def sim_model(updated_parameters,slider_time, slider_light, slider_pings, slider_saturate, slider_darklength):
    m = get_model()
    m.update_parameters(updated_parameters)
    s = Simulator(m)

    y0 = {"P": 0, "H": 6.32975752e-05, "E": 0, "A": 25.0, "Pr": 1, "V": 1}
    s.initialise(y0)

    max_time = slider_time*60
    saturating_pulse = slider_saturate
    length_pulse = 0.8
    dark_length = slider_darklength
    dark_light = 0
    light_light = slider_light
    pulses_intervall = slider_pings

    for i in range(max_time):
        if i == 2:
            s.update_parameter("PFD", dark_light)
            s.simulate(i)
            s.update_parameter("PFD", saturating_pulse)
            s.simulate(i + length_pulse)
        elif i == dark_length:
            s.update_parameter("PFD", dark_light)
            s.simulate(i)
            s.update_parameter("PFD", saturating_pulse)
            s.simulate(i + length_pulse)
        elif i in [dark_length + (pulses_intervall * j) for j in range((max_time-dark_length)+1)]:
            s.update_parameter("PFD", light_light)
            s.simulate(i)
            s.update_parameter("PFD", saturating_pulse)
            s.simulate(i + length_pulse)
        elif i == max_time - 1:
            s.update_parameter("PFD", light_light)
            s.simulate(i)
            s.simulate(max_time)

    sim_time = s.get_time()
    sim_results = s.get_full_results_dict()
    return sim_time, sim_results

def make_sim_area(text: Callable[[str], str]) -> None:
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
        slider_pings = st.slider(
            label=text("SLIDER_PULSES"),
            min_value=20,
            max_value=150,
            value=85
        )

    if version == "Advanced":
        col1, col2 = st.columns(2)
        with col1:
            slider_aktivation = st.slider(
                text("SLIDER_ACTIVATION"),
                -1000,
                +1000,
                0,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
            )
            slider_darklength = st.slider(
                text("SLIDER_DARKLENGTH"),
                min_value=0,
                max_value=slider_time*60,
                value=30
            )
        with col2:
            slider_deaktivation = st.slider(
                text("SLIDER_DEACTIVATION"),
                -1000,
                +1000,
                0,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
            )
            slider_saturate = st.slider(
                label=text("SLIDER_SATURATE"),
                min_value=0,
                max_value=10000,
                value=5000
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
        slider_darklength = 30
        slider_saturate = 5000
        
    if st.button("Start", type="primary"):
        with st.spinner(text("SPINNER")):
            sim_time, sim_results = sim_model(updated_parameters,slider_time, slider_light, slider_pings, slider_saturate, slider_darklength)
            
            PAM_F = sim_results['Fluo']
            PAM_Fmax = max(sim_results['Fluo'])

            if version == 'Simple':
                fig_PAM = make_matplotlib_plot(
                    text=text,
                    xlabel1=text("AXIS_TIME_S"),
                    xlabel2=text("AXIS_TIME_MIN"),
                    ylabel=text("FLUO"),
                    time=sim_time,
                    values=PAM_F/PAM_Fmax,
                    max_time=slider_time*60,
                    dark_length=slider_darklength,
                    width = 15,
                    height = 3
                )

                st.pyplot(fig_PAM)

            if version == 'Advanced':
                peaks, _ = find_peaks((PAM_F/PAM_Fmax), height=0) # Find the Flourescence peaks (Fmaxs)
                NPQ = ((PAM_F[peaks][0] - PAM_F[peaks])) / PAM_F[peaks]

                prominences, prominences_left, prominences_right = peak_prominences((PAM_F/PAM_Fmax), peaks) # Find the minima around the peaks
                Fo = [(PAM_F/PAM_Fmax)[i] for i in prominences_left] # Fo is always the minima before the peak
                PhiPSII = (PAM_F[peaks] - Fo) / PAM_F[peaks]

                fig_advanced = make_matplotlib_plot_advanced(
                    text=text,
                    xlabel1=text("AXIS_TIME_S"),
                    xlabel2=text("AXIS_TIME_MIN"),
                    ylabel=[text("FLUO"), text("AXIS_NPQ"), text("AXIS_PHIPSII")],
                    time={'PAM': sim_time, 'NPQ': sim_time[peaks], 'PhiPSII': sim_time[peaks]},
                    values={'PAM': PAM_F/PAM_Fmax, 'NPQ': NPQ, 'PhiPSII': PhiPSII},
                    max_time=slider_time*60,
                    dark_length=slider_darklength,
                    width = 15,
                    height = 6
                )
                
                st.pyplot(fig_advanced)



def make_page(text: Callable[[str], str]) -> None:
    st.markdown(text("HEADLINE_EXPERIMENTS"))

    st.markdown(text("HEADLINE_MODEL_CONSTRUCTION"))

    st.markdown(text("CONSTRUCTION_EXPLANATION_1"))

    include_image("pictures/NPQphotosynthesis.png", 0.8, text("CAPTION_MODEL_NPQ"), True)

    st.markdown(text("CONSTRUCTION_EXPLANATION_2"))
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
        markdown_click("IMPLEMENTATION_TO_EXPERT", text)

    if version == "Advanced":
        with st.expander(text("MODEL_CODE_EXPANDER")):
            st.markdown(text("CONSTRUCTION_HEADER"))
            st.markdown(text("CONSTRUCTION_1"))

            with open(Path(__file__).parent / "assets" / "model" / "model_define.py") as fp:
                model_define = f"{fp.read()}"

            st.code(model_define, "python")

            st.markdown(text("CONSTRUCTION_2"))
            
            tab1, tab2 = st.tabs(['Parameters', 'Compounds'])

            with tab1:
                with open(Path(__file__).parent / "assets" / "model" / "model_parameters.py") as fp:
                    model_parameters = f"{fp.read()}"

                st.code(model_parameters, "python")

            with tab2:
                with open(Path(__file__).parent / "assets" / "model" / "model_comps.py") as fp:
                    model_comps = f"{fp.read()}"

                st.code(model_comps, "python")

            st.markdown(text("CONSTRUCTION_3"))

            with open(Path(__file__).parent / "assets" / "model" / "model_addcompspars.py") as fp:
                model_addcompspars = f"{fp.read()}"

            st.code(model_addcompspars, "python")

            st.markdown(text("CONSTRUCTION_4"))

            tab1, tab2 = st.tabs(["Derived parameters", "Algebraic modules"])

            with tab1:

                with open(Path(__file__).parent / "assets" / "model" / "model_derivedparameters.py") as fp:
                    model_derivedparameters = f"{fp.read()}"

                st.code(model_derivedparameters, "python")

            with tab2:

                with open(Path(__file__).parent / "assets" / "model" / "model_algebraicmodules.py") as fp:
                    model_algebraicmodules = f"{fp.read()}"

                st.code(model_algebraicmodules, "python")

            st.markdown(text("CONSTRUCTION_5"))

            tab1, tab2 = st.tabs(["Rate reactions", "Other functions"])

            with tab1:

                with open(Path(__file__).parent / "assets" / "model" / "model_reactions.py") as fp:
                    model_reactions = f"{fp.read()}"

                st.code(model_reactions, "python")

            with tab2:

                with open(Path(__file__).parent / "assets" / "model" / "model_otherfunctions.py") as fp:
                    model_otherfunctions = f"{fp.read()}"

                st.code(model_otherfunctions, "python")

            st.markdown(text("CONSTRUCTION_6"))

            with open(Path(__file__).parent / "assets" / "model" / "model_addreactions.py") as fp:
                model_addreactions = f"{fp.read()}"

            st.code(model_addreactions, "python")

            st.markdown(text("CONSTRUCTION_7"))

            st.markdown(text("SIMULATION_HEADER"))

            st.markdown(text("SIMULATION_1"))

            with open(Path(__file__).parent / "assets" / "model" / "model_definesim.py") as fp:
                model_definesim = f"{fp.read()}"
            
            st.code(model_definesim, "python")

            st.markdown(text("SIMULATION_2"))

            with open(Path(__file__).parent / "assets" / "model" / "model_initialisesim.py") as fp:
                model_initialisesim = f"{fp.read()}"
            
            st.code(model_initialisesim, "python")

            st.markdown(text("SIMULATION_3"))

            col1, col2 = st.columns([1,1])

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

            st.markdown(text("SIMULATION_4"))
            st.markdown(text("SIMULATION_FLOURESCENCE_HEADER"))
            st.markdown(text("SIMULATION_FLOURESCENCE_1"))

            col1, col2 = st.columns([1,1])

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

            st.markdown(text("SIMULATION_FLOURESCENCE_2"))

            col1, col2 = st.columns([1,1])

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

            st.markdown(text("SIMULATION_PHASES_HEADER"))
            st.markdown(text("SIMULATION_PHASES_1"))

            col1, col2 = st.columns([1,1])

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

            st.markdown(text("SIMULATION_PRETTY_HEADER"))
            st.markdown(text("SIMULATION_PRETTY_1"))

            include_image("pictures/complete_mockup.png", 1)

            with open(Path(__file__).parent / "assets" / "model" / "model_complemockup.py") as fp:
                model_complemockup = f"{fp.read()}"
            
            st.code(model_complemockup, "python")

    # UI (Mainpage-Website)
    st.markdown(text("HEADLINE_ANALYSE"))
    st.markdown(text("INTRODUKTION"))

    st.markdown(text("HEADLINE_SLIDER"))
    st.markdown(text("EXPLANATNION"))
    include_ytvideo("https://youtu.be/zxGZKeopEDw", 0.5)
    st.markdown(text("TIPP1"))
    st.markdown(text("TIPP2"))

    make_sim_area(text)

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

    version: str = st.session_state.setdefault("version", "Simple")
    language: str = st.session_state.setdefault("language", "English")
    text = get_localised_text(version, language)
    resetting_click_detector_setup()
    make_page(text)
    include_image("pictures/slider-default-value.png", 0.6, text("CAPTION_DEFAULT_SLIDERS"), center_caption=True)
    make_literature(text, version, language)
    make_prev_next_button("computational models", "plant light memory")
    make_sidebar()
