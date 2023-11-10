import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from matplotlib import patches
from matplotlib import pyplot as plt
from model import get_model
from modelbase.ode import Model, Simulator, _Simulate
from modelbase.ode.integrators import Scipy
from pages._monkey_patch import _simulate
from pages._sidebar import make_sidebar
from pathlib import Path
from PIL import Image
from scipy.signal import find_peaks, peak_prominences
from typing import Any, Callable
from utils import (
    get_localised_text,
    include_image,
    include_ytvideo,
    make_prev_next_button,
    markdown_click,
    resetting_click_detector_setup,
)


def make_matplotlib_plot_advanced(
    text: Callable[[str], str], xlabel1, xlabel2, ylabel, values, max_time, dark_length, width, height
):
    text_color = "#727682"
    alpha_old = 0.5
    
    style_dict = {
        'Fluo': {
            'color': '#FF4B4B',
            'alpha': 1,
            'linestyle': 'solid',
            'label': 'New'
        },
        'old Fluo': {
            'color': '#FF4B4B',
            'alpha': alpha_old,
            'linestyle': 'dashdot',
            'label': 'Old'
        },
        'NPQ': {
            'color': '#FF4B4B',
            'alpha': 1,
            'linestyle': 'solid',
            'label': 'New'
        },
        'old NPQ': {
            'color': '#FF4B4B',
            'alpha': alpha_old,
            'linestyle': 'dashdot',
            'label': 'Old'
        },
        'PhiPSII': {
            'color': '#FF4B4B',
            'alpha': 1,
            'linestyle': 'solid',
            'label': 'New'
        },
        'old PhiPSII': {
            'color': '#FF4B4B',
            'alpha': alpha_old,
            'linestyle': 'dashdot',
            'label': 'Old'
        }
    }
    
    with plt.rc_context(
    {
        "axes.spines.right": False,
        "axes.edgecolor": text_color,
        "font.size": 12.0,
        "text.color": text_color,
        "axes.labelcolor": text_color,
        "xtick.color": text_color,
        "ytick.color": text_color,
        "grid.color": text_color,
        "font.weight": 'bold',
        "figure.figsize": (width, height),
        
    }
        ):
        
        fig, axs = plt.subplot_mosaic(mosaic=[["A", "A"], ["B", "C"]], constrained_layout=True)
        
        graph_belong = {
            'Fluo': 'A',
            'NPQ': 'B',
            'PhiPSII': 'C'
        }
        
        for i in {'Fluo', 'NPQ', 'PhiPSII'}:
            if values.get('old ' + i):
                axs[graph_belong[i]].plot(
                        values['old ' + i][0],
                        values['old ' + i][1],
                        color = style_dict['old ' + i]['color'],
                        linestyle = style_dict['old ' + i]['linestyle'],
                        alpha = style_dict['old ' + i]['alpha'],
                        label = style_dict['old ' + i]['label']
                    )
            axs[graph_belong[i]].plot(
                    values[i][0],
                    values[i][1],
                    color = style_dict[i]['color'],
                    linestyle = style_dict[i]['linestyle'],
                    alpha = style_dict[i]['alpha'],
                    label = style_dict[i]['label']
                )
            
            # Create the top xaxis for the minutes
            ax_top = axs[graph_belong[i]].secondary_xaxis("top", functions=(lambda x: x / 60, lambda x: x * 60))
            
            # Add labels
            axs[graph_belong[i]].set_xlabel(xlabel1, weight = 'bold', size = 12)
            axs[graph_belong[i]].set_ylabel(ylabel[i], weight = 'bold', size = 12)
            ax_top.set_xlabel(xlabel2, weight = 'bold', size = 12)
            
            axs[graph_belong[i]].legend(loc = 'best', ncols=2, frameon = False, labelcolor = 'linecolor', fontsize = 12, prop = {'weight':'bold'})
        

    for j in range(len([axs["A"], axs["B"], axs["C"]])):
        ax = [axs["A"], axs["B"], axs["C"]][j]
        # Add the dark phase length to the xticks
        default_xticks = ax.get_xticks()
        new_xticks = []
        for i in range(len(default_xticks)):
            try:
                if default_xticks[i] > dark_length and default_xticks[i - 1] < dark_length:
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
            xy=(ax.get_xlim()[0], ax.get_ylim()[0]),
            width=dark_length,
            height=ax.get_ylim()[1],
            facecolor="#1c5bc7",
            alpha=0.3,
        )
        light_patch = patches.Rectangle(
            xy=(dark_length, ax.get_ylim()[0]),
            width=max_time - dark_length,
            height=ax.get_ylim()[1],
            facecolor="#cf6d0c",
            alpha=0.3,
        )

        ax.add_patch(dark_patch)
        ax.add_patch(light_patch)


    return fig


def make_matplotlib_plot(
    text: Callable[[str], str], xlabel1, xlabel2, ylabel, values, max_time, dark_length, width, height
):
    
    text_color = "#727682"
    alpha_old = 0.5
    
    style_dict = {
        'Fluo': {
            'color': '#FF4B4B',
            'alpha': 1,
            'linestyle': 'solid',
            'label': 'New'
        },
        'old Fluo': {
            'color': '#FF4B4B',
            'alpha': alpha_old,
            'linestyle': 'dashdot',
            'label': 'Old'
        }
    }
    
    with plt.rc_context(
    {
        "axes.spines.right": False,
        "axes.edgecolor": text_color,
        "font.size": 12.0,
        "text.color": text_color,
        "axes.labelcolor": text_color,
        "xtick.color": text_color,
        "ytick.color": text_color,
        "grid.color": text_color,
        "font.weight": 'bold',
        "figure.figsize": (width, height),
        
    }
        ):
        
        fig, ax = plt.subplots()
        for i in ['old Fluo', 'Fluo']:
            if values.get(i):
                ax.plot(
                    values[i][0],
                    values[i][1],
                    color = style_dict[i]['color'],
                    linestyle = style_dict[i]['linestyle'],
                    alpha = style_dict[i]['alpha'],
                    label = style_dict[i]['label']
                )
        
        # Create the top xaxis for the minutes
        ax_top = ax.secondary_xaxis("top", functions=(lambda x: x / 60, lambda x: x * 60))
        
        # Add labels
        ax.set_xlabel(xlabel1, weight = 'bold', size = 12)
        ax.set_ylabel(ylabel, weight = 'bold', size = 12)
        ax_top.set_xlabel(xlabel2, weight = 'bold', size = 12)

    # Add the dark phase length to the xticks
    default_xticks = ax.get_xticks()
    new_xticks = []
    for i in range(len(default_xticks)):
        try:
            if default_xticks[i] > dark_length and default_xticks[i - 1] < dark_length:
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
        xy=(ax.get_xlim()[0], ax.get_ylim()[0]),
        width=dark_length,
        height=ax.get_ylim()[1],
        facecolor="#1c5bc7",
        alpha=0.3,
    )
    light_patch = patches.Rectangle(
        xy=(dark_length, ax.get_ylim()[0]),
        width=max_time - dark_length,
        height=ax.get_ylim()[1],
        facecolor="#cf6d0c",
        alpha=0.3,
    )

    ax.add_patch(dark_patch)
    ax.add_patch(light_patch)

    # Create and center legend
    plt.legend(loc = 'best', ncols = 2, frameon = False, labelcolor = 'linecolor', fontsize = 12, prop = {'weight':'bold'})

    return fig


def sim_model(
    updated_parameters, slider_time, slider_light, slider_pings, slider_saturate, slider_darklength
):
    m = get_model()
    m.update_parameters(updated_parameters)
    s = Simulator(m)

    y0 = {"P": 0, "H": 6.32975752e-05, "E": 0, "A": 25.0, "Pr": 1, "V": 1}
    s.initialise(y0)

    max_time = slider_time * 60
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
        elif i in [dark_length + (pulses_intervall * j) for j in range((max_time - dark_length) + 1)]:
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
        50,
        900,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
        value=100,
    )
    col1, col2 = st.columns(2)
    with col1:
        slider_time = st.slider(
            text("FAL_SLIDER_TIME"),
            1,
            15,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
            value=5,
        )
    with col2:
        slider_pings = st.slider(label=text("SLIDER_PULSES"), min_value=5, max_value=150, value=85)

    if version == "4STEM":
        col1, col2 = st.columns(2)
        with col1:
            slider_aktivation = st.select_slider(
                text("SLIDER_ACTIVATION"),
                options=np.round(np.logspace(1, 3, 21)),
                value=100,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
            )
            slider_darklength = st.slider(
                text("FAL_SLIDER_DARKLENGTH"), min_value=0, max_value=slider_time * 60, value=30
            )
        with col2:
            slider_deaktivation = st.select_slider(
                text("SLIDER_DEACTIVATION"),
                options=np.round(np.logspace(1, 3, 21)),
                value=100,  # Zwischenschritte können durch folgendes angegeben werden: (x,y,z)
            )
            slider_saturate = st.slider(
                label=text("FAL_SLIDER_SATURATE"), min_value=0, max_value=10000, value=5000
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
        with st.spinner(text("FAL_SPINNER")):
            sim_time, sim_results = sim_model(
                updated_parameters,
                slider_time,
                slider_light,
                slider_pings,
                slider_saturate,
                slider_darklength,
            )
            
            st.session_state['simple_model_results'] = {
                'time': sim_time,
                'results': sim_results,
                'slider_time': slider_time,
                'slider_darklength': slider_darklength 
            }
                
    try:
        
        sim_time = st.session_state['simple_model_results']['time']
        sim_results = st.session_state['simple_model_results']['results']
        
        PAM_F = sim_results["Fluo"]
        PAM_Fmax = max(sim_results["Fluo"])

        if 'simple_model' not in st.session_state:
            st.session_state['simple_model'] = {
                'Fluo': [sim_time, PAM_F / PAM_Fmax]
            }
        else:
            st.session_state['simple_model'].update({
                'Fluo': [sim_time, PAM_F / PAM_Fmax]
            })
        
        if version == "4Bio":
            fig_PAM = make_matplotlib_plot(
                text=text,
                xlabel1=text("FAL_AXIS_TIME_S"),
                xlabel2=text("FAL_AXIS_TIME_MIN"),
                ylabel=text("FAL_FLUO"),
                values=st.session_state['simple_model'],
                max_time=st.session_state['simple_model_results']['slider_time'] * 60,
                dark_length=st.session_state['simple_model_results']['slider_darklength'],
                width=15,
                height=3,
            )

            st.pyplot(fig_PAM, transparent=True)
            
            st.session_state['simple_model'].update({
                'old Fluo': [sim_time, PAM_F / PAM_Fmax]
            })

        if version == "4STEM":
            peaks, _ = find_peaks((PAM_F / PAM_Fmax), height=0)  # Find the Flourescence peaks (Fmaxs)
            NPQ = ((PAM_F[peaks][0] - PAM_F[peaks])) / PAM_F[peaks]

            prominences, prominences_left, prominences_right = peak_prominences(
                (PAM_F / PAM_Fmax), peaks
            )  # Find the minima around the peaks
            Fo = [
                (PAM_F / PAM_Fmax)[i] for i in prominences_left
            ]  # Fo is always the minima before the peak
            PhiPSII = (PAM_F[peaks] - Fo) / PAM_F[peaks]
            
            st.session_state['simple_model'].update({
                'NPQ': [sim_time[peaks], NPQ],
                'PhiPSII': [sim_time[peaks], PhiPSII]
            })

            fig_advanced = make_matplotlib_plot_advanced(
                text=text,
                xlabel1=text("FAL_AXIS_TIME_S"),
                xlabel2=text("FAL_AXIS_TIME_MIN"),
                ylabel={'Fluo': text("FAL_FLUO"), 'NPQ': text("FAL_AXIS_NPQ"),'PhiPSII': text("FAL_AXIS_PHIPSII")},
                values=st.session_state['simple_model'],
                max_time=st.session_state['simple_model_results']['slider_time'] * 60,
                dark_length=st.session_state['simple_model_results']['slider_darklength'],
                width=15,
                height=6,
            )

            st.pyplot(fig_advanced, transparent = True)
            
            st.session_state['simple_model'].update({
                'old Fluo': st.session_state['simple_model']['Fluo'],
                'old NPQ': st.session_state['simple_model']['NPQ'],
                'old PhiPSII': st.session_state['simple_model']['PhiPSII'],
            })
    except:
        pass


def make_page(text: Callable[[str], str]) -> None:
    st.markdown(text("FAL_HEADLINE_EXPERIMENTS"))

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

    if version == "4STEM":
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

    if version == "4STEM":
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

    # UI (Mainpage-Website)
    st.markdown(text("FAL_HEADLINE_ANALYSE"))
    st.markdown(text("FAL_INTRODUKTION"))

    st.markdown(text("FAL_HEADLINE_SLIDER"))
    st.markdown(text("FAL_EXPLANATNION"))
    include_ytvideo("https://youtu.be/zxGZKeopEDw", 0.5)
    st.markdown(text("FAL_TIPP1"))
    st.markdown(text("FAL_TIPP2"))

    # Add guiding questions:
    with st.expander(
        "Having trouble connecting the simulation results to biology? Try our **guiding questions**"
    ):
        # The guide questionns are shown by default
        st.markdown("### Guiding Questions")
        see_interpr = st.toggle("See our interpretation")
        if not see_interpr:
            st.markdown(
                "With the default values, the following simulation shows you a typical PAM experiment. When testing out the sliders you could try the following:\n"
                "1. :blue[You will find a light intensity of 100 μmol m⁻² s⁻¹ in the early morning or on a cloudy day, so it is quite low. On a mild day, the sun might shine with 500 μmol m⁻² s⁻¹ of photons - try that instead:]\n"
                "    - When the light is being turned on, how does the reaction differ to when you used 100 μmol m⁻² s⁻¹? What does that mean to the plant?\n"
                "    - How do the saturation pulse signals differ between the lower and higher intensity?\n"
                "2. :blue[On a hot and sunny day, higher intensities of over 900 μmol m⁻² s⁻¹ actinic light can be reached. Try this in a simulation and see if you previous observations also hold here.]\n"
                "    - Compare the fluorescence at the very end of the simulation between default and high light - is there a difference?\n"
                "3. :blue[At this intensity, we can see much better how the fluorescence peaks during the saturation pulses lower over time. But a lot seems to happen in the first two miutes that we cannot see.]\n"
                "    - Lower the time between the saturation pulses. What can you see?\n"
                "    - Does it seem like the saturation pulses affect the plant's photosynthesis?\n"
                "4. :blue[The longer an experiment takes, the more work it is for the experimenter. Try lowering the measuring time to 1 min, then increase it to 10 min.]\n"
                "    - Would it be useful to reduce the measuring time in our case? Why or why not?\n"
                "    - Does this depend on the other settings?\n"
            )
            if version == "4STEM":
                st.markdown(
                    "5. :blue[The conversion rates to Zeaxanthin and Violaxanthin represent the activation and deactivation rates of NPQ respectively.]\n"
                    "    - How does the simulated NPQ graph behave when you increase the Zeaxanthin conversion rate? And the Violaxanthin rate?\n"
                    "    - Are changes in the two rates additive?\n"
                    "6. :blue[In the dark phase the plant's NPQ system relaxes.]\n"
                    "    - What happens if you strongly reduce the adaption time?\n"
                    "7. :blue[It is very important, that the saturating pulses are actually saturating to get meaninful results.]\n"
                    "    - Increase the saturating pulse intensity to maximum. Does something change?"
                    "    - Gradually reduce the saturating pulse intensity. When do they not seem to saturate anymore? What happens to our measurements?"
                )
        else:  # If toggle is switched show possible iterpretation
            st.markdown(
                "With the default values, the following simulation shows you a typical PAM experiment. When testing out the sliders you could try the following:\n"
                "1. :blue[You will find a light intensity of 100 μmol m⁻² s⁻¹ in the early morning or on a cloudy day, so it is quite low. On a mild day, the sun might shine with 500 μmol m⁻² s⁻¹ of photons - try that instead:]\n"
                "    - The fluorescence signal after turning on the light, shortly after the peak, is a lot higher. This is because chlorophyll receives much more energy which puts the plant under light stress.\n"
                "    - The later saturation pulses, after ca. 2 minutes, are shorter than those under low light. Therefore the plant has increased the heat quenching, aka NPQ, as a light protection mechanism.\n"
                "2. :blue[On a hot and sunny day, higher intensities of over 900 μmol m⁻² s⁻¹ actinic light can be reached. Try this in a simulation and see if you previous observations also hold here.]\n"
                "    - For this higher light intensity we can see as well the increased fluorescence after light-on and the further decreasing fluorescence during the pulses.\n"
                "    - The fluorescence at the very end of the very high light phase is increased compared to the low light simulation. Therefore, even after full acctivation of it's NPQ mechanism, the plant is still more stressed. Likely, the quenching potential of the plant's NPQ process is exhaused and higher light might damage the plant.\n"
                "3. :blue[At this intensity, we can see much better how the fluorescence peaks during the saturation pulses lower over time. But a lot seems to happen in the first two miutes that we cannot see.]\n"
                "    - With more fequent pulses, we can see the dropping peak fluorescence more clearly. Therefore, we see the NPQ activation in a higher resolution and could try to fit a function to estimate the activation rate.\n"
                "    - Normally we assume that the pulses don't affect the photosynthesis. After a pulse the signal returns to the previous level and the peak height seems to decrease always the same.\n" 
                "    - However, if we give pulses in rapid succession under low light, the saturation pulses can have an effect like actinic light. You can see this if you try a light intensity of 50 μmol m⁻² s⁻¹ with pulses every 5 s. There, the peak height decreases more than with fewer pulses. \n"
                "4. :blue[The longer an experiment takes, the more work it is for the experimenter. Try lowering the measuring time to 1 min, then increase it to 10 min.]\n"
                "    - With a light intensity of 500 to 900 μmol m⁻² s⁻¹ the NPQ adaption seems to be finished after three to four seconds. We should measure at least this long to capture the whole process.\n"
                "    - With lower light intensities this adaption process takes less time. So a shorter measurement might be feasible.\n"
            )
            if version == "4STEM":
                st.markdown(
                    "5. :blue[The conversion rates to Zeaxanthin and Violaxanthin represent the activation and deactivation rates of NPQ respectively.]\n"
                    "    - If we increase the Zeaxanthin conversion rate, the maximal NPQ activity increases up to a factor of about two.\n"
                    "    - With a high frequency of saturation pulses we can also see that this maximal activity is reached faster.\n"
                    "    - If we increase the Zeaxanthin conversion rate, the maximal NPQ activity also increases up to a factor of about two.\n" 
                    "    - Are changes in the two rates additive?\n"
                    "6. :blue[In the dark phase the plant's NPQ system relaxes.]\n"
                    "    - What happens if you strongly reduce the adaption time?\n"
                    "7. :blue[It is very important, that the saturating pulses are actually saturating to get meaninful results.]\n"
                    "    - Increase the saturating pulse intensity to maximum. Does something change?"
                    "    - Gradually reduce the saturating pulse intensity. When do they not seem to saturate anymore? What happens to our measurements?"
                )

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

    version: str = st.session_state.setdefault("version", "4Bio")
    language: str = st.session_state.setdefault("language", "English")
    text = get_localised_text(version, language)
    resetting_click_detector_setup()
    make_page(text)
    make_literature(text, version, language)
    make_prev_next_button("computational models", "plant light memory")
    make_sidebar()
