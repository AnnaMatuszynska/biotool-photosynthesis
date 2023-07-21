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