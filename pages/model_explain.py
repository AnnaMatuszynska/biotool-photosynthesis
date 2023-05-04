import streamlit as st
from pages._sidebar import make_sidebar
from PIL import Image
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
        st.latex(r"""
        \frac{d\mathrm{PQH_2}}{dt} = v_\mathrm{PSII} - v_\mathrm{PQ_{ox}}
        """)
        st.latex(r"""
        \frac{d\mathrm{ATP}}{dt} = v_\mathrm{ATPsynthase} - v_\mathrm{ATPconsumption}
        """)
        st.latex(r"""
        \frac{d\mathrm{ATPase^{*}}}{dt} =F k_\mathrm{actATPase} \cdot \mathrm{H}(\mathrm{PFD}) \cdot \mathrm{ATPase} - k_\mathrm{deactATPase} \cdot (1 - \mathrm{H}(\mathrm{PFD})) \cdot \mathrm{ATPase^{*}}
        """)
        st.latex(r"""
        b_\mathrm{H}\cdot\frac{dH}{dt} = 2 v_\mathrm{PSII} + 4 v_\mathrm{PQ_{ox}} -\frac{14}{3} v_\mathrm{ATPsynthase} - v_\mathrm{leak}
        """)
        st.latex(r"""
        \frac{d\mathrm{PsbS}}{dt} = -v_\mathrm{Psbs^{p}}
        """)
        st.latex(r"""
        \frac{d\mathrm{Vx}}{dt} = -v_\mathrm{Xcyc}
        """)


        with st.expander(text("REACTION_RATES")):
            st.markdown(text("RATES_DYNAMIC"))
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


            st.markdown(text("RATE_QUENCHER"))
            st.latex(r"""
                    v_\mathrm{Xcyc} = k_\mathrm{DeepoxV} \cdot \frac{H^\mathrm{nH_X}}{H^\mathrm{nH_X} + pH_{\mathrm{inv}}(K_\mathrm{phSat})^\mathrm{nH_X}} \cdot \mathrm{Vx} - k_\mathrm{EpoxZ} \cdot (\mathrm{X^{tot}} - \mathrm{Vx}),
                            """)
            st.latex(r"""
                    v_\mathrm{Psbs^{p}}= k_\mathrm{ProtonationL} \cdot \frac{H^\mathrm{nH_L}} {H^\mathrm{nH_L} + pH_{\mathrm{inv}}(K_\mathrm{phSatLHC})^\mathrm{nH_L}} \cdot \mathrm{PsbS} - k_\mathrm{Deprotonation} \cdot \mathrm{PsbS^p},
                                    """)
            st.latex(r"""
                    Q = \gamma_0 \cdot (1-\frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}})\cdot\mathrm{PsbS}+ \gamma_1\cdot(1-\frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}})\cdot\mathrm{PsbS^p} + \gamma_2\cdot \frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}}\cdot\mathrm{PsbS^p} + \gamma_3\cdot \frac{\mathrm{Zx}}{\mathrm{Zx}+K_\mathrm{{ZSat}}}\cdot\mathrm{PsbS},
                                    """)


    st.markdown(text("HEADLINE_IMPLEMENTATION"))

    st.markdown(text("IMPLEMENTATION_DESCRIPTION"))

    if version == "Simple":
        st.markdown(text("IMPLEMENTATION_TO_EXPERT"))

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
