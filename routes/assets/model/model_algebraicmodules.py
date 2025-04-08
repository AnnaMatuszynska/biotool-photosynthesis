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