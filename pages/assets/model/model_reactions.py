
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