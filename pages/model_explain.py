import streamlit as st
from pages._sidebar import make_sidebar
from pathlib import Path
from typing import Callable
from utils import get_localised_text


def make_page(text: Callable[[str], str], language: str, version: str) -> None:
    st.markdown(text("HEADLINE_MODEL"))

    st.markdown(text("HEADLINE_MODEL_CONSTRUCTION"))

    st.markdown(text("CONSTRUCTION_EXPLANATION"))
    st.markdown(text("RATES_1"))
    st.markdown(text("RATES_2"))
    st.markdown(text("RATES_3"))
    st.markdown(text("RATES_4"))
    st.markdown(text("RATES_5"))
    st.markdown(text("RATES_6"))

    if version == "expert":
        st.markdown(text("HEADLINE_MODEL_EQUATIONS"))
        st.markdown(text("MODEL_EQUATIONS_INTRODUCTION"))
        st.latex(
            r"""
        \frac{d\mathrm{PQH_2}}{dt} = v_\mathrm{PSII} - v_\mathrm{PQ_{ox}}
        """
        )
        st.latex(
            r"""
        \frac{d\mathrm{ATP}}{dt} = v_\mathrm{ATPsynthase} - v_\mathrm{ATPconsumption}
        """
        )
        st.latex(
            r"""
        \frac{d\mathrm{ATPase^{*}}}{dt} =F k_\mathrm{actATPase} \cdot \mathrm{H}(\mathrm{PFD}) \cdot \mathrm{ATPase} - k_\mathrm{deactATPase} \cdot (1 - \mathrm{H}(\mathrm{PFD})) \cdot \mathrm{ATPase^{*}}
        """
        )
        st.latex(
            r"""
        b_\mathrm{H}\cdot\frac{dH}{dt} = 2 v_\mathrm{PSII} + 4 v_\mathrm{PQ_{ox}} -\frac{14}{3} v_\mathrm{ATPsynthase} - v_\mathrm{leak}
        """
        )
        st.latex(
            r"""
        \frac{d\mathrm{PsbS}}{dt} = -v_\mathrm{Psbs^{p}}
        """
        )
        st.latex(
            r"""
        \frac{d\mathrm{Vx}}{dt} = -v_\mathrm{Xcyc}
        """
        )

        with st.expander(text("REACTION_RATES")):
            st.markdown(text("RATES_DYNAMIC"))
            st.latex(
                r"""
                    v_{\mathrm{PSII}} = k_2 \cdot 0.5 \cdot B_1,
                            """
            )
            st.latex(
                r"""
                    v_{PQ_{ox}} = \left(\frac{k_{Cyt_{b6f}} \cdot \mathrm{PFD} \cdot K_\mathrm{eq,cytb6f}(\mathrm{pH})}{K_\mathrm{eq,cytb6f}(\mathrm{pH}) + 1} + k_\mathrm{PTOX}\right) \cdot \mathrm{PQH_2} - \frac{k_\mathrm{PFD}}{K_\mathrm{eq,cytb6f}(\mathrm{pH}) + 1} \cdot \mathrm{PQ},
                    """
            )
            st.latex(
                r"""
                    v_\mathrm{ATPsynthase} = \mathrm{ATPase}^* \cdot k_\mathrm{ATPsynthase}\cdot \left(AP^{tot}-\mathrm{ATP} - \frac{\mathrm{ATP}}{K_\mathrm{eq,ATPsynthase}(H)} \right),
                            """
            )
            st.latex(
                r"""
                    v_\mathrm{ATPactivity} = k_\mathrm{actATPase} \cdot \mathrm{H}(\mathrm{PFD}) \cdot \mathrm{ATPase} - k_\mathrm{deactATPase} \cdot (1 - \mathrm{H}(\mathrm{PFD})) \cdot \mathrm{ATPase^{*}},
                            """
            )
            st.latex(
                r"""
                    v_\mathrm{Leak} = k_\mathrm{leak} \cdot (H - pH_{\mathrm{inv}}(\mathrm{pH_{stroma}})),
                            """
            )
            st.latex(
                r"""
                    v_\mathrm{ATP_{consumption}} = k_\mathrm{ATPconsumption} \cdot \mathrm{ATP},
                            """
            )

            st.markdown(text("RATE_QUENCHER"))
            st.latex(
                r"""
                    v_\mathrm{Xcyc} = k_\mathrm{DeepoxV} \cdot \frac{H^\mathrm{nH_X}}{H^\mathrm{nH_X} + pH_{\mathrm{inv}}(K_\mathrm{phSat})^\mathrm{nH_X}} \cdot \mathrm{Vx} - k_\mathrm{EpoxZ} \cdot (\mathrm{X^{tot}} - \mathrm{Vx}),
                            """
            )
            st.latex(
                r"""
                    v_\mathrm{Psbs^{p}}= k_\mathrm{ProtonationL} \cdot \frac{H^\mathrm{nH_L}} {H^\mathrm{nH_L} + pH_{\mathrm{inv}}(K_\mathrm{phSatLHC})^\mathrm{nH_L}} \cdot \mathrm{PsbS} - k_\mathrm{Deprotonation} \cdot \mathrm{PsbS^p},
                                    """
            )
            st.latex(
                r"""
                    Q = \gamma_0 \cdot (1-\frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}})\cdot\mathrm{PsbS}+ \gamma_1\cdot(1-\frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}})\cdot\mathrm{PsbS^p} + \gamma_2\cdot \frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}}\cdot\mathrm{PsbS^p} + \gamma_3\cdot \frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}}\cdot\mathrm{PsbS},
                                    """
            )

    st.markdown(text("HEADLINE_IMPLEMENTATION"))

    st.markdown(text("IMPLEMENTATION_DESCRIPTION"))

    if version == "Simple":
        st.markdown(text("IMPLEMENTATION_TO_EXPERT"))

    if version == "expert":
        with open(Path(__file__).parent / "assets" / "sir_v1.py") as fp:
            sir_v1 = f"\n```python\n{fp.read()}```\n\n"

        # with open(Path(__file__).parent / "assets" / "sir_v2.py") as fp:
        #     sir_v2 = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "sir_v2_rate_fns.py") as fp:
            sir_v2_rate_fns = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "sir_v2_model.py") as fp:
            sir_v2_model = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "sir_v2_reactions.py") as fp:
            sir_v2_reactions = f"\n```python\n{fp.read()}```\n\n"

        with open(Path(__file__).parent / "assets" / "sird.py") as fp:
            sird = f"\n```python\n{fp.read()}```\n\n"

        st.markdown(
            f"""
The model has been implemented using the modelbase package,
which allows for a modular construction of ODE models.
To see why this is beneficial, take a look at this manually
constructed SIR model.

{sir_v1}

Great care needs to be taken in order for the `y0` vector to align
with the unpacked variable names, as well as the respective differential
equations. The same holds true for the order of the parameters `beta` and
`gamma`.

Clearly this way of writing models is very error-prone and hard to modularise.
Let's improve on the situation using `modelbase`.

First, we are going to factor out the rate functions `infection` and `recovery` as
plain Python functions.

{sir_v2_rate_fns}

Next, we can build the model.
For this we supply all our system variables using `add_compounds`
and parameters as a dictionary using `add_parameters`.

{sir_v2_model}

Lastly, we add the transitions using `add_reaction_from_args`, supplying
- a name for the transition
- a reference to the rate function
- stoichiometries, encoding how the rate affects the system variables
- the arguments for the rate function

{sir_v2_reactions}

From this modelbase will automatically assemble a system of ODEs ready to be studied.
In order to help minimise minor oversights, modelbase will check for various common
inconsistencies during this process and will display appropriate warnings.

Now extending the SIR model to include an additional compartment for deceased individuals
(also refered to as a SIRD model) is as easy as adding a new variable, parameter and reaction:

{sird}

which would have been a lot more cumbersome with the manual approach.
            """
        )


def make_literature(text: Callable[[str], str], language: str, version: str) -> None:
    with st.expander(text("LITERATURE")):
        if version == "expert":
            """
            - Cook J, Oreskes N, Doran PT, Anderegg WR, Verheggen B, Maibach EW, Carlton JS, Lewandowsky S, Skuce AG, Green SA (2016) Consensus on consensus: a synthesis of consensus estimates on human-caused global warming. J Environmental Research Letters 11: 048002
            - van Aalst M, Ebenhöh O, and Matuszyńska A (2020). Constructing and analysing dynamic models with modelbase v1.2.3 - a software update. BioMed Central
            """


if __name__ == "__main__":
    version, language = make_sidebar()
    text = get_localised_text("b-model", version, language)
    make_page(text, language, version)
    make_literature(text, language, version)
