import numpy as np
import streamlit as st
import time
from pages._sidebar import make_sidebar
from pages.assets.model._model_functions import calculate_results_to_plot, make_both_plots, sim_model
from pathlib import Path
from typing import Callable
from utils import (
    get_localised_text,
    include_image,
    include_ytvideo,
    make_prev_next_button,
    markdown_click,
    resetting_click_detector_setup,
)


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

    st.markdown(text("FAL_HEADLINE_ANALYSE"))
    st.markdown(text("FAL_INTRODUKTION"))

    st.markdown(text("FAL_HEADLINE_SLIDER"))
    st.markdown(text("FAL_EXPLANATNION"))
    include_ytvideo("https://youtu.be/zxGZKeopEDw", 0.5)
    st.markdown(text("FAL_TIPP1"))
    st.markdown(text("FAL_TIPP2"))

    with st.expander("See how to interpret your modelling results", expanded=True):
        st.markdown("### Graphs with one result")
        include_image(str(Path("pictures/explanation_graph_oneresult.png")), img_width=1)
        st.markdown(
            "We can look at the graph in three phases:\n"
            "1. The first phase happens in darkness and, therefore, our initial modelled fluorescence is 'F₀'. We then simulate a saturating light pulse which rapidly inceases the fluorescence up to the peak value 'Fₘ'. Fₘ should be the overall maximal fluorescence the plant can produce so we usually compare the other fluorescence signals to it. 'Fₜ', the fluorescence simulated outside of saturating pulses, shows the photosystems behaviour under the actinic light. We see that Fₜ decreases back to the F₀-level afterwards, meaning that the plant recovers from having its photosystems saturated.\n"
            "2. We initiate the following phase with another saturating pulse. Since this peak fluorescence level (Fₘ') is the same as Fₘ, the plant doesn't seem to have activated any light protection yet. However, now, instead of returning to dark, we turn on the (actinic) light to 100 μmol m⁻² s⁻¹. This leads to the fluorescence decreasing much more quickly after the saturating pulse and to a slightly higher level than F₀ which persists until the end of the experiment. The increased fluorescence yield shows us that the plant loses a larger amount of excitation energy to fluorescence now, implying that it is more stressed than it was in the dark.\n"
            "3. Indeed, when we proceed to give another saturating pulse, we see that the new maximum fluorescence Fₘ' is noticeably lower than Fₘ, showing us that non-photochemical quenching has been activated and is funnelling excitation energy away from both fluorescence and photosynthesis. You can find this observation directly reflected in the formula to estimate NPQ:"
        )
        st.latex(r"NPQ = \frac{F_m - F_m'}{F_m'}")
        st.markdown(
            "The same way you can analyse simulation graphs with changed parameters and even more light phases. In general, observe how  Fₜ and Fₘ' behave over time, especially when the light condition is changed. Then, connect your oversations with your knowledge on NPQ. If you are interested, you could also use the calculated estimated of NPQ and and PSII efficiency in the <a href='#' id='4Bio'>4Bio</a> version."
        )

        st.markdown("### Graphs with old and new results")
        include_image(str(Path("pictures/explanation_graph_tworesults.png")), img_width=1)
        st.markdown(
            "When changing the model parameters and doing another simulation, the old simulation graph will be displayed as a dashed line in the background of the new plot. This way, you can easily compare the two and investigate the effects of your change.\n\nIn the case shown, we increased the actinic light intensity from 100 (old) to 500 μmol m⁻² s⁻¹ (new). Because the dark phase is the same in all simulations, there is no difference in phase one. After the saturating pulse in phase two, the higher light intensity's fluorescence (Fₜ₋₅₀₀) is strongly raised takes much longer to decrease. This behaviour implies that the photosystem is under much more light stress and  requires more time to sufficiently activate the NPQ. Phase three validates this hypothesis, as we simulate strongly reduced Fₘ's, resulting in increased estimated NPQ according to the previous formula. Lastly, we see that the plant reaches a similar final fluorescence as with the weaker actinic light, implying that by the strong NPQ activation a similarly low stress level is reached."
        )

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
                "    - **Q:** When the light is being turned on, how does the reaction differ to when you used 100 μmol m⁻² s⁻¹? What does that mean to the plant?\n"
                "    - **Q:** How do the saturation pulse signals differ between the lower and higher intensity?\n"
                "2. :blue[On a hot and sunny day, higher intensities of over 900 μmol m⁻² s⁻¹ actinic light can be reached. Try this in a simulation and see if you previous observations also hold here.]\n"
                "    - **Q:** Compare the fluorescence at the very end of the simulation between default and high light - is there a difference?\n"
                "3. :blue[At this intensity, we can see much better how the fluorescence peaks during the saturation pulses lower over time. But a lot seems to happen in the first two miutes that we cannot see.]\n"
                "    - **Q:** Lower the time between the saturation pulses. What can you see?\n"
                "    - **Q:** Does it seem like the saturation pulses affect the plant's photosynthesis?\n"
                "4. :blue[The longer an experiment takes, the more work it is for the experimenter. Try lowering the measuring time to 1 min, then increase it to 10 min.]\n"
                "    - **Q:** Would it be useful to reduce the measuring time in our case? Why or why not?\n"
                "    - **Q:** Does this depend on the other settings?\n"
            )
            if version == "4Bio":
                st.markdown(
                    "5. :blue[The conversion rates to Zeaxanthin and Violaxanthin represent the activation and deactivation rates of NPQ respectively.]\n"
                    "    - **Q:** How does the simulated NPQ graph behave when you increase the Zeaxanthin conversion rate? And the Violaxanthin rate?\n"
                    "    - **Q:** Are changes in the two rates additive?\n"
                    "6. :blue[In the dark phase the plant's NPQ system relaxes.]\n"
                    "    - **Q:** What happens if you strongly reduce the adaption time?\n"
                    "7. :blue[It is very important, that the saturating pulses are actually saturating to get meaninful results.]\n"
                    "    - **Q:** Increase the saturating pulse intensity to maximum. Does something change?"
                    "    - **Q:** Gradually reduce the saturating pulse intensity. When do they not seem to saturate anymore? What happens to our measurements?"
                )
        else:  # If toggle is switched show possible interpretation
            st.markdown(
                "With the default values, the following simulation shows you a typical PAM experiment. When testing out the sliders you could try the following:\n"
                "1. :blue[You will find a light intensity of 100 μmol m⁻² s⁻¹ in the early morning or on a cloudy day, so it is quite low. On a mild day, the sun might shine with 500 μmol m⁻² s⁻¹ of photons - try that instead:]\n"
                "    - **A:** The fluorescence signal after turning on the light, shortly after the peak, is a lot higher. This is because chlorophyll receives much more energy which puts the plant under light stress.\n"
                "    - **A:** The later saturation pulses, after ca. 2 minutes, are shorter than those under low light. Therefore the plant has increased the heat quenching, aka NPQ, as a light protection mechanism.\n"
                "2. :blue[On a hot and sunny day, higher intensities of over 900 μmol m⁻² s⁻¹ actinic light can be reached. Try this in a simulation and see if you previous observations also hold here.]\n"
                "    - **A:** For this higher light intensity we can see as well the increased fluorescence after light-on and the further decreasing fluorescence during the pulses.\n"
                "    - **A:** The fluorescence at the very end of the very high light phase is increased compared to the low light simulation. Therefore, even after full acctivation of it's NPQ mechanism, the plant is still more stressed. Likely, the quenching potential of the plant's NPQ process is exhaused and higher light might damage the plant.\n"
                "3. :blue[At this intensity, we can see much better how the fluorescence peaks during the saturation pulses lower over time. But a lot seems to happen in the first two miutes that we cannot see.]\n"
                "    - **A:** With more fequent pulses, we can see the dropping peak fluorescence more clearly. Therefore, we see the NPQ activation in a higher resolution and could try to fit a function to estimate the activation rate.\n"
                "    - **A:** Normally we assume that the pulses don't affect the photosynthesis. After a pulse the signal returns to the previous level and the peak height seems to decrease always the same.\n"
                "    - **A:** However, if we give pulses in rapid succession under low light, the saturation pulses can have an effect like actinic light. You can see this if you try a light intensity of 50 μmol m⁻² s⁻¹ with pulses every 5 s. There, the peak height decreases more than with fewer pulses. \n"
                "4. :blue[The longer an experiment takes, the more work it is for the experimenter. Try lowering the measuring time to 1 min, then increase it to 10 min.]\n"
                "    - **A:** With a light intensity of 500 to 900 μmol m⁻² s⁻¹ the NPQ adaption seems to be finished after three to four seconds. We should measure at least this long to capture the whole process.\n"
                "    - **A:** With lower light intensities this adaption process takes less time. So a shorter measurement might be feasible.\n"
            )
            if version == "4Bio":
                st.markdown(
                    "5. :blue[The conversion rates to Zeaxanthin and Violaxanthin represent the activation and deactivation rates of NPQ respectively.]\n"
                    "    - **A:** If we increase the Zeaxanthin conversion rate, the maximal NPQ activity increases up to a factor of about two.\n"
                    "    - **A:** With a high frequency of saturation pulses we can also see that this maximal activity is reached faster.\n"
                    "    - **A:** If we increase the Zeaxanthin conversion rate, the maximal NPQ activity also increases up to a factor of about two.\n"
                    "    - **A:** Are changes in the two rates additive?\n"
                    "6. :blue[In the dark phase the plant's NPQ system relaxes.]\n"
                    "    - **A:** What happens if you strongly reduce the adaption time?\n"
                    "7. :blue[It is very important, that the saturating pulses are actually saturating to get meaninful results.]\n"
                    "    - **A:** Increase the saturating pulse intensity to maximum. Does something change?"
                    "    - **A:** Gradually reduce the saturating pulse intensity. When do they not seem to saturate anymore? What happens to our measurements?"
                )

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

    col1_, col2_ = st.columns(2)

    with col1_:
        if st.button("Start the simulation", type="primary", use_container_width=True):
            with st.spinner(text("SPINNER")):
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

                fig_4Bio, fig_4STEM = make_both_plots(
                    text=text,
                    xlabel1=text("AXIS_TIME_S"),
                    xlabel2=text("AXIS_TIME_MIN"),
                    ylabel_4STEM=text("FLUO"),
                    ylabel_4Bio={
                        "Fluo": text("FLUO"),
                        "NPQ": text("AXIS_NPQ"),
                        "PhiPSII": text("AXIS_PHIPSII"),
                    },
                    session_state_values=st.session_state["model_results"],
                    slider_time=slider_time,
                    slider_darklength=slider_darklength,
                )

                st.session_state["fig_4Bio"] = fig_4Bio
                st.session_state["fig_4STEM"] = fig_4STEM

                old_results = {}
                for key, value in st.session_state["model_results"].items():
                    old_results.update({f"old {key}": value})

                st.session_state["model_results"].update(old_results)
    with col2_:
        if st.button(label="Reset Graph", use_container_width=True):
            if "fig_4Bio" in st.session_state and "fig_4STEM" in st.session_state:
                for i in ["old Fluo", "old NPQ", "old PhiPSII"]:
                    if st.session_state["model_results"].get(i):
                        st.session_state["model_results"].pop(i)
                    else:
                        alert = st.warning("Nothing to reset")
                        time.sleep(1.5)
                        alert.empty()
                        break

                fig_4Bio, fig_4STEM = make_both_plots(
                    text=text,
                    xlabel1=text("AXIS_TIME_S"),
                    xlabel2=text("AXIS_TIME_MIN"),
                    ylabel_4STEM=text("FLUO"),
                    ylabel_4Bio={
                        "Fluo": text("FLUO"),
                        "NPQ": text("AXIS_NPQ"),
                        "PhiPSII": text("AXIS_PHIPSII"),
                    },
                    session_state_values=st.session_state["model_results"],
                    slider_time=slider_time,
                    slider_darklength=slider_darklength,
                )

                st.session_state["fig_4Bio"] = fig_4Bio
                st.session_state["fig_4STEM"] = fig_4STEM

                old_results = {}
                for key, value in st.session_state["model_results"].items():
                    old_results.update({f"old {key}": value})

                st.session_state["model_results"].update(old_results)

    if "fig_4Bio" in st.session_state and "fig_4STEM" in st.session_state:
        if version == "4Bio":
            showed_fig = st.session_state["fig_4Bio"]
        else:
            showed_fig = st.session_state["fig_4STEM"]

        st.pyplot(showed_fig, transparent=True)


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
