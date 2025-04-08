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