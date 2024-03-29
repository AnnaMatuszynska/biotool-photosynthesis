import numpy as np
from modelbase.ode import Model

model = Model()

pars = {
        # Pool sizes
        "PSIItot": 2.5,  # [mmol/molChl] total concentration of PSII
        "PQtot": 20,  # [mmol/molChl]
        "APtot": 50,  # [mmol/molChl] Bionumbers ~2.55mM (=81mmol/molChl)
        "PsbStot": 1,  # [relative] LHCs that get phosphorylated and protonated
        "Xtot": 1,  # [relative] xanthophylls
        "O2ex": 8,  # external oxygen, kept constant, corresponds to 250 microM, corr. to 20%
        "Pi": 0.01,
        # Rate constants and key parameters
        "kCytb6f": 0.104,  # a rough estimate of the transfer from PQ to cyt that is equal to ~ 10ms
        # [1/s*(mmol/(s*m^2))] - gets multiplied by light to determine rate
        "kActATPase": 0.01,  # paramter relating the rate constant of activation of the ATPase in the light
        "kDeactATPase": 0.002,  # paramter relating the deactivation of the ATPase at night
        "kATPsynthase": 20.0,
        "kATPconsumption": 10.0,
        "kPQred": 250.0,  # [1/(s*(mmol/molChl))]
        "kH": 5e9,  # Heatdisipation (rates)
        "kF": 6.25e8,  # fluorescence 16ns
        "kP": 5e9,  # original 5e9 (charge separation limiting step ~ 200ps) - made this faster for higher Fs fluorescence (express in unites of time
        "kPTOX": 0.01,  # ~ 5 electrons / seconds. This gives a bit more (~20)
        "pHstroma": 7.8,  # [1/s] leakage rate
        "kleak": 1000,
        "bH": 100,  # proton buffer: ratio total / free protons
        "HPR": 14.0 / 3.0,
        # Parameter associated with xanthophyll cycle
        "kDeepoxV": 0.0024,  # Aktivierung des Quenchings
        "kEpoxZ": 0.00024,  # 6.e-4,  #converted to [1/s]   # Deaktivierung
        "KphSatZ": 5.8,  # [-] half-saturation pH value for activity de-epoxidase, highest activity at ~pH 5.8
        "nHX": 5.0,  # [-] hill-coefficient for activity of de-epoxidase
        "Kzsat": 0.12,  # [-], half-saturation constant (relative conc. of Z) for quenching of Z
        # Parameter associated with PsbS protonation
        "nHL": 3,
        "kDeprot": 0.0096,
        "kProt": 0.0096,
        "KphSatLHC": 5.8,
        # Fitted quencher contribution factors
        "gamma0": 0.1,  # slow quenching of Vx present despite lack of protonation
        "gamma1": 0.25,  # fast quenching present due to the protonation
        "gamma2": 0.6,  # slow quenching of Zx present despite lack of protonation
        "gamma3": 0.15,  # fastest possible quenching
        # Physical constants
        "F": 96.485,  # Faraday constant
        "R": 8.3e-3,  # universal gas constant
        "T": 298,  # Temperature in K - for now assumed to be constant at 25 C
        # Standard potentials and DG0ATP
        "E0QAQAm": -0.140,
        "E0PQPQH2": 0.354,
        "E0PCPCm": 0.380,
        "DG0ATP": 30.6,  # 30.6kJ/mol / RT
        # PFD
        "PFD": 100,
    }

comps = [

            "P",  # reduced Plastoquinone
            "H",  # luminal Protons
            "E",  # ATPactivity
            "A",  # ATP
            "Pr",  # fraction of non-protonated PsbS (notation from doctoral thesis Matuszynska 2016)
            "V",  # fraction of Violaxanthin
    ]

model.add_parameters(pars)

model.add_compounds(comps)

# create functions for derived parameters
def proportional(x: float, y: float) -> float:
    return x * y

def _KeqQAPQ(F: float, E0QAQAm: float, E0PQPQH2: float, pHstroma: float, RT: float) -> float:
    DG1 = -F * E0QAQAm
    DG2 = -2 * F * E0PQPQH2 + 2 * pHstroma * np.log(10) * RT
    DG0 = -2 * DG1 + DG2
    Keq = np.exp(-DG0 / RT)
    return Keq  # type: ignore

# add derived parameters
model.add_derived_parameter(
    parameter_name="RT",
    function=proportional,
    parameters=["R", "T"],
)

model.add_derived_parameter(
    parameter_name="KeqQAPQ", function=_KeqQAPQ, parameters=["F", "E0QAQAm", "E0PQPQH2", "pHstroma", "RT"]
)

# create the functions for the algebraic modules

## Conserved quantities
def pqmoiety(P: float, PQtot: float) -> float:
    return PQtot - P


def atpmoiety(A: float, APtot: float) -> float:
    return APtot - A


def psbsmoiety(Pr: float, PsbStot: float) -> float:
    return PsbStot - Pr


def xcycmoiety(V: float, Xtot: float) -> float:
    return Xtot - V

## Auxiliary functions
def Quencher(Pr: float, V: float, Xtot: float, PsbStot: float, Kzsat: float, gamma0: float, gamma1: float, gamma2: float, gamma3: float) -> float:
    """Quencher mechanism

    accepts:
    Pr: fraction of non-protonated PsbS protein
    V: fraction of Violaxanthin
    """
    Z = Xtot - V
    P = PsbStot - Pr
    Zs = Z / (Z + Kzsat)

    Q = gamma0 * (1 - Zs) * Pr + gamma1 * (1 - Zs) * P + gamma2 * Zs * P + gamma3 * Zs * Pr
    return Q

def ps2states(P: float, Q: float, light: float, PQtot: float, kPQred: float, KeqQAPQ: float, kH: float, kF: float, kP: float, PSIItot: float) -> float:
    """Calculates the states of photosystem II

    accepts:
    P: reduced fraction of PQ pool (PQH2)
    Q: Quencher

    returns:
    B: array of PSII states
    """

    Bs = []
    Pox = PQtot - P
    b0 = light + kPQred * P / KeqQAPQ
    b1 = kH * Q + kF
    b2 = kH * Q + kF + kP

    for Pox, b0, b1, b2 in zip(Pox, b0, b1, b2):  # type: ignore
        A = np.array(
            [
                [-b0, b1, kPQred * Pox, 0],  # B0
                [light, -b2, 0, 0],  # B1
                [0, 0, light, -b1],  # B3
                [1, 1, 1, 1],
            ]
        )

        b = np.array([0, 0, 0, PSIItot])
        B0, B1, B2, B3 = np.linalg.solve(A, b)
        Bs.append([B0, B1, B2, B3])
    return np.array(Bs).T  # type: ignore

def Fluorescence(Q: float, B0: float, B2: float, kH: float, kF: float, kP: float) -> float:
    """Fluorescence function"""
    Fluo = kF / (kH * Q + kF + kP) * B0 + kF / (kH * Q + kF) * B2
    return Fluo

def constant(x: float) -> float:
    return x

# add algebraic modules
model.add_algebraic_module_from_args(
    module_name="P_am",
    function=pqmoiety,
    derived_compounds=["Pox"],
    args=["P", "PQtot"],
)

model.add_algebraic_module_from_args(
    module_name="A_am",
    function=atpmoiety,
    derived_compounds=["ADP"],
    args=["A", "APtot"],
)

model.add_algebraic_module_from_args(
    module_name="PsbS_am",
    function=psbsmoiety,
    derived_compounds=["Pnr"],
    args=["Pr", "PsbStot"],
)

model.add_algebraic_module_from_args(
    module_name="X_am",
    function=xcycmoiety,
    derived_compounds=["Z"],
    args=["V", "Xtot"],
)

model.add_algebraic_module_from_args(
    module_name="Quencher",
    function=Quencher,
    derived_compounds=["Q"],
    args=["Pr", "V", "Xtot", "PsbStot", "Kzsat", "gamma0", "gamma1", "gamma2", "gamma3"],
)

model.add_algebraic_module_from_args(
    module_name="PSIIstates",
    function=ps2states,
    derived_compounds=["B0", "B1", "B2", "B3"],
    args=["P", "Q", "PFD", "PQtot", "kPQred", "KeqQAPQ", "kH", "kF", "kP", "PSIItot"],
)

model.add_algebraic_module_from_args(
    module_name="Fluorescence",
    function=Fluorescence,
    derived_compounds=["Fluo"],
    args=["Q", "B0", "B2","kH", "kF", "kP"],
)

## Mock module to get Light vector over all simulated time points
model.add_algebraic_module_from_args(
    module_name="L",
    function=constant,
    derived_compounds=["L"],
    args=["PFD"],
)

def vps2(B1: float, kP: float) -> float:
    """Reduction of PQ due to ps2"""
    v = kP * 0.5 * B1
    return v

def vPQox(P: float, H: float, light: float, kCytb6f: float, kPTOX: float, O2ex: float, PQtot: float, F: float, E0PQPQH2: float, RT: float, E0PCPCm: float, pHstroma: float) -> float:
    """Oxidation of the PQ pool through cytochrome and PTOX"""
    kPFD = kCytb6f * light
    kPTOX = kPTOX * O2ex
    Keq = Keqcytb6f(H, F, E0PQPQH2, RT, E0PCPCm, pHstroma)
    a1 = kPFD * Keq / (Keq + 1)
    a2 = kPFD / (Keq + 1)
    v = (a1 + kPTOX) * P - a2 * (PQtot - P)
    return v

def vATPsynthase(A: float, H: float, E: float, kATPsynthase: float, DG0ATP: float, pHstroma: float, RT: float, Pi: float, APtot: float) -> float:
    """Production of ATP by ATPsynthase"""
    v = E * kATPsynthase * (APtot - A - A / KeqATPsyn(H, DG0ATP, pHstroma, RT, Pi))
    return v

def vATPactivity(E: float, light: float, kActATPase: float, kDeactATPase: float) -> float:
    """Activation of ATPsynthase by light"""
    switch = light > 0
    v = kActATPase * switch * (1 - E) - kDeactATPase * (1 - switch) * E
    return v

def vLeak(H: float, kleak: float, pHstroma: float) -> float:
    """Transmembrane proton leak"""
    v = kleak * (H - pHinv(pHstroma))
    return v

def vATPcons(A: float, kATPconsumption: float) -> float:
    """ATP consuming reaction"""
    v = kATPconsumption * A
    return v

def vXcyc(V: float, H: float, nHX: float, KphSatZ: float, kDeepoxV: float, kEpoxZ: float, Xtot: float) -> float:
    """Xanthophyll cycle"""
    a = H**nHX / (H**nHX + pHinv(KphSatZ) ** nHX)
    v = kDeepoxV * a * V - kEpoxZ * (Xtot - V)
    return v  # type: ignore

def vPsbSP(Pr: float, H: float, nHL: float, KphSatLHC: float, kProt: float, kDeprot: float, PsbStot: float) -> float:
    """Protonation of PsbS protein"""
    a = H**nHL / (H**nHL + pHinv(KphSatLHC) ** nHL)
    v = kProt * a * Pr - kDeprot * (PsbStot - Pr)
    return v  # type: ignore

def Keqcytb6f(H: float, F: float, E0PQPQH2: float, RT: float, E0PCPCm: float, pHstroma: float) -> float:
    """Equilibrium constant of Cytochrome b6f"""
    DG1 = -2 * F * E0PQPQH2 + 2 * RT * np.log(10) * pH(H)
    DG2 = -F * E0PCPCm
    DG3 = RT * np.log(10) * (pHstroma - pH(H))
    DG = -DG1 + 2 * DG2 + 2 * DG3
    Keq = np.exp(-DG / RT)
    return Keq  # type: ignore

def KeqATPsyn(H: float, DG0ATP: float, pHstroma: float, RT: float, Pi: float) -> float:
    """Equilibrium constant of ATP synthase. For more
    information see Matuszynska et al 2016 or Ebenhöh et al. 2011,2014
    """
    DG = DG0ATP - np.log(10) * (pHstroma - pH(H)) * (14 / 3) * RT
    Keq = Pi * np.exp(-DG / RT)
    return Keq  # type: ignore

def pH(H: float) -> float:
    value = H * 2.5e-4
    return -np.log10(value)  # type: ignore

def pHinv(pH: float) -> float:
    return 4e3 * 10**-pH

#Add reactions
model.add_reaction_from_args(
        rate_name="vps2",
        function=vps2,
        stoichiometry={"P": 1, "H": 2 / pars["bH"]},
        args=["B1", "kP"],
)

model.add_reaction_from_args(
    rate_name="vPQox",
    function=vPQox,
    stoichiometry={"P": -1, "H": 4 / pars["bH"]},
    args=["P", "H", "PFD", "kCytb6f", "kPTOX", "O2ex", "PQtot", "F", "E0PQPQH2", "RT", "E0PCPCm", "pHstroma"],
)

model.add_reaction_from_args(
    rate_name="vATPsynthase",
    function=vATPsynthase,
    stoichiometry={"A": 1, "H": (-14 / 3) / pars["bH"]},
    args=["A", "H", "E", "kATPsynthase", "DG0ATP", "pHstroma", "RT", "Pi", "APtot"],
)

model.add_reaction_from_args(
    rate_name="vATPactivity",
    function=vATPactivity,
    stoichiometry={"E": 1},
    args=["E", "PFD", "kActATPase", "kDeactATPase"],
)

model.add_reaction_from_args(
    rate_name="vLeak",
    function=vLeak,
    stoichiometry={"H": -1 / pars["bH"]},
    args=["H", "kleak", "pHstroma"],
)

model.add_reaction_from_args(
    rate_name="vATPcons",
    function=vATPcons,
    stoichiometry={"A": -1},
    args=["A", "kATPconsumption"],
)

model.add_reaction_from_args(
    rate_name="vXcyc",
    function=vXcyc,
    stoichiometry={"V": -1},
    args=["V", "H", "nHX", "KphSatZ", "kDeepoxV", "kEpoxZ", "Xtot"],
)

model.add_reaction_from_args(
    rate_name="vPsbSP",
    function=vPsbSP,
    stoichiometry={"Pr": -1},
    args=["Pr", "H", "nHL", "KphSatLHC", "kProt", "kDeprot", "PsbStot"],
)

### Define sim

from modelbase.ode import Simulator

simulator = Simulator(model)

# Initialise sim

y0 = {"P": 0, "H": 6.32975752e-05, "E": 0, "A": 25.0, "Pr": 1, "V": 1}
simulator.initialise(y0)

from matplotlib import pyplot as plt, patches

max_time = 600
saturating_pulse = 5000
length_pulse = 0.8
dark_length = 30
dark_light = 0
light_light= 100
number_pulses = 10

for i in range(max_time):
    if i == 1:
        simulator.update_parameter("PFD", dark_light)
        simulator.simulate(i)
        simulator.update_parameter("PFD", saturating_pulse)
        simulator.simulate(i + length_pulse)
    elif i == dark_length:
        simulator.update_parameter("PFD", dark_light)
        simulator.simulate(i)
        simulator.update_parameter("PFD", saturating_pulse)
        simulator.simulate(i + length_pulse)
    elif i % round(max_time/number_pulses) == 0:
        simulator.update_parameter("PFD", light_light)
        simulator.simulate(i)
        simulator.update_parameter("PFD", saturating_pulse)
        simulator.simulate(i + length_pulse)
    elif i == max_time - 1:
        simulator.update_parameter("PFD", light_light)
        simulator.simulate(i)
        simulator.simulate(max_time)

sim_results = simulator.get_full_results_dict() #Store the Results fo the sim

with plt.rc_context(
    {
        "axes.spines.right": False,
        "axes.spines.top": False,
        "figure.frameon": True,
        "figure.figsize": (10, 5),
        "axes.facecolor": "None",
        "figure.edgecolor": "None",
        "text.color": "#9296a4",
        "axes.labelcolor": "#9296a4",
        "xtick.color": "#9296a4",
        "ytick.color": "#9296a4"
    }
):
    fig, ax = plt.subplots()
    ax.plot(simulator.get_time(),
            sim_results['Fluo']/max(sim_results['Fluo']),
            color = '#FF4B4B'    
        )

# Change the left and down limit
plt.xlim(0, max_time)
plt.ylim(0, 1)

# Set the tick values
plt.xticks([i for i in range(0, max_time + 1, 50)])

# Highlight dark and light phase
dark_patch = patches.Rectangle((0,0), dark_length, 1, facecolor = '#1c5bc7', alpha = 0.3)
light_patch = patches.Rectangle((dark_length,0), max_time - dark_length, 1, facecolor = '#cf6d0c', alpha = 0.3)

ax.add_patch(dark_patch)
ax.add_patch(light_patch)

#Change color of axis
ax.spines['bottom'].set_color("#9296a4")
ax.spines['left'].set_color("#9296a4")

#Add labels
ax.set_xlabel("Time [s]")
ax.set_ylabel("Fluorescence [F´ₘ /Fₘ]")

#plt.savefig('./pictures/complete_mockup.png', bbox_inches='tight', dpi = 300, facecolor="None")

#plt.show()


