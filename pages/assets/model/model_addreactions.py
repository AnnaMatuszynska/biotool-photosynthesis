model.add_reaction_from_args(
        rate_name="vps2",
        function=vps2,
        stoichiometry={"P": 1, "H": 2 / pars["bH"]},
        args=["B1", "PFD", "PQtot", "kPQred", "KeqQAPQ", "kH", "kF", "kP", "PSIItot"],
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