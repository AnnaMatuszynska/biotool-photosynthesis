import streamlit as st
from pages._sidebar import make_sidebar
from PIL import Image
from typing import Callable
from utils import get_localised_text

def make_page(text: Callable[[str], str], language: str, version: str) -> None:
    st.markdown(text("HEADLINE_MODEL"))

    st.markdown(text("INTRODUCTION_CLIMATE_CHANCE"))

    if version == "expert":
        st.markdown(text("POINT_1"))
        st.markdown(text("POINT_2"))
        st.markdown(text("POINT_3"))
        st.markdown(text("END_OF_INTRODUCTION"))

    else:
        col1, col2 = st.columns(2)
        with col1:
            if language == "German":
                st.image("pictures/pflanzen_grundlagen.jpeg")
            if language == "English":
                st.image("pictures/plants_basics.jpeg")
        with col2:
            if language == "German":
                st.image("pictures/pflanzen_stress.jpeg")
            if language == "English":
                st.image("pictures/plants_stress.jpeg")

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

        st.markdown("###### The quasi-steady state approximation used to calculate the rate of photosystem II")
        st.latex(r"""
        - \left(\mathrm{PFD} + \frac{k_\mathrm{PQred}}{K_\mathrm{eq,QAPQ}}(PQ^{tot}-P) \right) B_0 + (k_H Q+k_F) B_1 + k_\mathrm{PQred} P B_3 = 0, 
        """)
        st.latex(r"""
                {PFD} B_0 - (k_H Q + k_F + k_P) B_1 = 0,
                        """)
        st.latex(r"""
                {PFD} B_2 - (k_H Q + k_F) B_3 = 0,
                        """)
        st.latex(r"""
                B_0 + B_1 + B_2 + B_3 = PSII^{tot}.
                        """)


        st.markdown("###### Reaction rates used in the dynamic description of the system")
        st.latex(r"""
                v_{\mathrm{PSII}} = k_2 \cdot 0.5 \cdot B_1,
                        """)
        st.latex(r"""
                v_{PQ_{ox}} = \left(\frac{k_{Cyt_{b6f}} \cdot \mathrm{PFD} \cdot K_\mathrm{eq,cytb6f}(\mathrm{pH})}{K_\mathrm{eq,cytb6f}(\mathrm{pH}) + 1} + k_\mathrm{PTOX}\right) \cdot \mathrm{PQH_2} - \frac{k_\mathrm{PFD}}{K_\mathrm{eq,cytb6f}(\mathrm{pH}) + 1} \cdot \mathrm{PQ},
                """)
        st.latex(r"""
                v_\mathrm{ATPsynthase} = \mathrm{ATPase}^* \cdot k_\mathrm{ATPsynthase}\cdot \left(AP^{tot}-\mathrm{ATP} - \frac{\mathrm{ATP}}{K_\mathrm{eq,ATPsynthase}(H)} \right),
                        """)
        st.latex(r"""
                v_\mathrm{ATPactivity} = k_\mathrm{actATPase} \cdot \mathrm{H}(\mathrm{PFD}) \cdot \mathrm{ATPase} - k_\mathrm{deactATPase} \cdot (1 - \mathrm{H}(\mathrm{PFD})) \cdot \mathrm{ATPase^{*}},
                        """)
        st.latex(r"""
                v_\mathrm{Leak} = k_\mathrm{leak} \cdot (H - pH_{\mathrm{inv}}(\mathrm{pH_{stroma}})),
                        """)
        st.latex(r"""
                v_\mathrm{ATP_{consumption}} = k_\mathrm{ATPconsumption} \cdot \mathrm{ATP},
                        """)


        st.markdown("###### Reaction rates to calculate the quencher activity and the overall rate")
        st.latex(r"""
                v_\mathrm{Xcyc} = k_\mathrm{DeepoxV} \cdot \frac{H^\mathrm{nH_X}}{H^\mathrm{nH_X} + pH_{\mathrm{inv}}(K_\mathrm{phSat})^\mathrm{nH_X}} \cdot \mathrm{Vx} - k_\mathrm{EpoxZ} \cdot (\mathrm{X^{tot}} - \mathrm{Vx}),
                        """)
        st.latex(r"""
                v_\mathrm{Psbs^{p}}= k_\mathrm{ProtonationL} \cdot \frac{H^\mathrm{nH_L}} {H^\mathrm{nH_L} + pH_{\mathrm{inv}}(K_\mathrm{phSatLHC})^\mathrm{nH_L}} \cdot \mathrm{PsbS} - k_\mathrm{Deprotonation} \cdot \mathrm{PsbS^p},
                                """)
        st.latex(r"""
                Q = \gamma_0 \cdot (1-\frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}})\cdot\mathrm{PsbS}+ \gamma_1\cdot(1-\frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}})\cdot\mathrm{PsbS^p} + \gamma_2\cdot \frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}}\cdot\mathrm{PsbS^p} + \gamma_3\cdot \frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}}\cdot\mathrm{PsbS},
                                """)

        st.markdown("###### Equilibrium")
        st.latex(r"""
                K_\mathrm{eq,ATPsynthase}(\mathrm{pH}) = \mathrm{Pi_{mol}} \cdot e^{\frac{-\Delta G_{0_{ATP}} - log(10)\cdot RT \cdot \mathrm{HPR} \cdot (\mathrm{pH_{stroma}} - \mathrm{pH})}{RT}},
                        """)
        st.latex(r"""
                K_\mathrm{eq,cytb6f}(\mathrm{pH}) = e^{\frac{-\left(\left(2F\cdot E^0(\mathrm{PQ/PQH_2}) - 2 \cdot \mathrm{log}(10)\cdot RT \cdot \mathrm{pH}\right) - 2 \cdot F\cdot E^0(\mathrm{PC/PC^-}) + 2 \cdot \mathrm{log}(10)\cdot RT \cdot(\mathrm{pH_{stroma}} - \mathrm{pH})\right)} {RT}},
                                """)
        st.latex(r"""
                K_\mathrm{eq,QAPQ} = e^{\frac{-\left(-2\cdot E^0(\mathrm{QA/QA^-})\cdot F -2 \cdot E^0(\mathrm{PQ/PQH_2})\cdot F + 2\mathrm{pH_{stroma}} \cdot \mathrm{log}(10)\cdot RT  \right)}{RT}},
                                """)

        st.markdown("###### Method to calculate the fluorescence signal")
        st.latex(r"""
                \Phi = \frac{k_\mathrm{F}}{k_\mathrm{H}\cdot Q+k_\mathrm{F}+k_\mathrm{P}}B_0 + \frac{k_\mathrm{F}}{k_\mathrm{H}\cdot Q+k_\mathrm{F}}B_2,
                        """)



    st.markdown(text("HEADLINE_IMPLEMENTATION"))

    st.markdown(text("IMPLEMENTATION_DESCRIPTION"))

def make_literature(text: Callable[[str], str], language: str, version: str) -> None:
    with st.expander(text("LITERATURE")):
        if version == "expert":
            """
            - Cook J, Oreskes N, Doran PT, Anderegg WR, Verheggen B, Maibach EW, Carlton JS, Lewandowsky S, Skuce AG, Green SA (2016) Consensus on consensus: a synthesis of consensus estimates on human-caused global warming. J Environmental Research Letters 11: 048002
            """

if __name__ == "__main__":
    version, language = make_sidebar()
    text = get_localised_text("b-model", version, language)
    make_page(text, language, version)
    make_literature(text, language, version)
