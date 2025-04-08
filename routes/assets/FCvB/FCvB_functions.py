from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches

from routes.assets.model._model_functions import plot_stylings


def quadratic(a, b, c):
    """
    Calculates the quadratic solutions of a * x**2 + b * x + c
    """
    sol1 = (-b + np.sqrt((b**2) - (4 * (a * c)))) / (2 * a)
    sol2 = (-b - np.sqrt((b**2) - (4 * (a * c)))) / (2 * a)

    return np.array(sol1), np.array(sol2)


def temp_scaling(TK, R_gas, parameter25, Ea):
    """
    Calculates temperature dependencies of several Rubisco kinetics (Bernacchi et al. 2002)

    Parameters:
    -----
    TC: Temperature [°C]
    R_gas: Ideal gas constant [J mol⁻¹ K⁻¹]
    parameter25: The wished parameter at 25°C [universal]
    Ea: Activation energy of parameter [J mol⁻¹]
    """

    return parameter25 * np.exp((TC - 25) * Ea / (298 * R_gas * (273 + TC)))


def potential_electron_rate(Jmax, I2, theta):
    """
    Calculates the potential electron rate J [µmol m^-2 s^-1] (von Caemmerer 2013)

    Parameters:
    -----
    Jmax: The upper limit of the potential chloroplast electron transport [µmol m^-2 s^-1]
    I2: Useful light absorbed by PSII []
    theta: Empricial curvature factor []
    """
    return (I2 + Jmax - np.sqrt((I2 + Jmax) ** 2 - 4 * theta * I2 * Jmax)) / (2 * theta)


def useful_light(I, alpha, f):
    """
    Calculates the useful light absorbed by PSII I2 (von Caemmerer 2013)

    Parameters:
    -----
    I: Incident irradiance []
    absorptance: absorptance of leaves []
    f: Correction for specral quality []
    """
    return I * alpha * (1 - f) / 2


def steady_state_photosynthesis(
    Ci=300,
    Kc=259,
    Vcmax=80,
    gamma_star=None,
    Sco=114,
    O=210,
    Ko=179,
    J=None,
    I=1000,
    alpha=0.8,
    f=0.15,
    theta=0.7,
    Jmax=135.5,
    Tp=300,
    Rd=1,
    gm=1,
    rm=None,
    TC=25,
    R_gas=8.31,
):
    """
    Calculates the CO2 assimilation at an RuBP saturated rate (Ac), an electron transport limited rate (Aj),
    a phosphate limited rate (Ap) and the overall assimilation (A). To return the specific assimilation, set
    the bool to True. Only one is possible.

    Temperature dependencies:
    -----
    Kc, Ko, gamma_star, gm: Using the function temp_scaling from Bernacchi et al. 2002 and Sharkey et al. 2007

    Parameters:
    -----
    Ci -> Intercellular chloroplast pCO2 [µbar] !!Needed!!
    Kc -> Michaelis Menten constant for CO2 [µbar] !!Needed!!
    Vcmax -> Maximum Rubisco activity [µmol m⁻² s⁻¹] !!Needed!!

    gamma_star -> Chloroplast pCO2 where A = -Rd [µbar] !!Needed, but can be replaced by Sco!!
    Sco -> Relative specificity of Rubisco []

    O -> pO2 [mbar] !!Needed!!
    Ko -> Michaelis Menten constant for O2 [mbar] !!Needed!!

    J -> Electron transport rate [µmol m⁻² s⁻¹] !!Needed, but can be replaced by the params underneath!!
    I -> Incidient radiation []
    alpha -> Absorptance of leaves []
    f -> Correct for spectral quality []
    theta -> Empirical curvature factor []
    Jmax -> Maximal electron transport rate [µmol m⁻² s⁻¹]

    rm -> Mesophyll resistance to CO2 diffusion [] !!Needed, but can be calculated by gm!!
    gm -> Mesophyll conductance []
    """
    # Check for required params
    if (
        [rm, gm] == [None, None]
        or [gamma_star, Sco] == [None, None]
        or [J, Jmax, I, alpha, f, theta] == [None, None, None, None, None, None]
    ):
        print("Check your parameters again please")
        return

    # Calculation of gamma_star if not given
    if gamma_star is None and Sco is not None:
        gamma_star = 0.5 * O * 1e3 / Sco

    # Calculation of rm if not given
    if rm is None and gm is not None:
        rm = 1 / gm

    # Calculation of J if not given:
    if (
        J is None
        and Jmax is not None
        and I is not None
        and alpha is not None
        and f is not None
        and theta is not None
    ):
        I2 = useful_light(I=I, alpha=alpha, f=f)
        J = potential_electron_rate(Jmax=Jmax, I2=I2, theta=theta)
    # Temperature dependance

    # RuBP saturated rate of CO2 assimilation
    if rm != 0:
        Ac1, Ac2 = quadratic(
            a=1,
            b=-((Ci + Kc * (1 + O / Ko)) / rm + Vcmax - Rd),
            c=(Vcmax * (Ci - gamma_star) - Rd * (Ci + Kc * (1 + O / Ko))) / rm,
        )
        Ac = np.min([Ac1, Ac2], axis=0)

        # Electron transport limited rate of CO2 assimilation
        Aj1, Aj2 = quadratic(
            a=1,
            b=-((Ci + 2 * gamma_star) / rm + J / 4 - Rd),
            c=((Ci - gamma_star) * J / 4 - Rd * (Ci + 2 * gamma_star)) / rm,
        )
        Aj = np.min([Aj1, Aj2], axis=0)

    else:
        Ac = (Ci - gamma_star) * Vcmax / (Ci + Kc * (1 + O / Ko)) - Rd
        Aj = (Ci - gamma_star) * J / (4 * Ci + 8 * gamma_star) - Rd

    # Phosphate limited rate of CO2 assimilation
    Ap = 3 * Tp - Rd

    # Make every assimilation into an array, if not already
    if type(Ac) != type(np.array([1])):
        Ac = np.array([Ac])
    if type(Aj) != type(np.array([1])):
        Aj = np.array([Aj])
    if type(Ap) != type(np.array([1])):
        Ap = np.array([Ap])

    # Make every assimilation into an array of same length
    len_lst = [len(Ac), len(Aj), len(Ap)]

    Ac = np.array([Ac[0] if len(Ac) < max(len_lst) else Ac[i] for i in range(max(len_lst))])
    Aj = np.array([Aj[0] if len(Aj) < max(len_lst) else Aj[i] for i in range(max(len_lst))])
    Ap = np.array([Ap[0] if len(Ap) < max(len_lst) else Ap[i] for i in range(max(len_lst))])

    # The overal CO2 assimilation
    A = np.min([Ac, Aj, Ap], axis=0)

    return {"Ac": Ac, "Aj": Aj, "Ap": Ap, "A": A}


def make_FvCB_plot(Ci, results, display_bools, xlabel, ylabel, empty_label):
    style_dict = {
        "A": {"color": "#45D689", "alpha": 1, "linestyle": "solid", "label": "A"},
        "Ac": {"color": "#3740FA", "alpha": 1, "linestyle": "solid", "label": r"$\mathbf{A}_{\mathbf{c}}$"},
        "Aj": {"color": "#FAD64A", "alpha": 1, "linestyle": "solid", "label": r"${\mathbf{A}_{\mathbf{j}}}$"},
        "Ap": {"color": "#FA433E", "alpha": 1, "linestyle": "solid", "label": r"$\mathbf{A}_{\mathbf{p}}$"},
    }

    style_plot: dict[str, Any] = plot_stylings()
    style_plot.update(
        {
            "axes.spines.top": False,
            "figure.figsize": (7, 3),
            "font.size": 10.0,
        }
    )

    with plt.rc_context(style_plot):
        fig, ax = plt.subplots()

        for key, value in display_bools.items():
            if value:
                ax.plot(
                    Ci,
                    results[key],
                    color=style_dict[key]["color"],
                    linestyle=style_dict[key]["linestyle"],
                    alpha=style_dict[key]["alpha"],
                    label=style_dict[key]["label"],
                    linewidth=3,
                )

        if True not in display_bools.values():
            ax.annotate(empty_label, (ax.get_xlim()[1] / 2, ax.get_ylim()[1] / 2), ha="center", va="center")

    plt.xlim(0)
    plt.ylim(0)

    plt.xlabel(xlabel + " CO$\mathbf{_2}$ [µbar]", weight="bold", size=8)
    plt.ylabel("CO$\mathbf{_2}$ " + ylabel, weight="bold", size=8)

    if True in display_bools.values():
        plt.legend(loc="best", frameon=False, labelcolor="linecolor", fontsize=10, prop={"weight": "bold"})

    plt.tight_layout()
    return fig
