import matplotlib.pyplot as plt
from cycler import cycler
from modelbase.ode import Model, Simulator


def infection(alpha, s, i, r):
    return alpha * s * i / (s + i + r)


def recovery(beta, x):
    return beta * x


sir = Model()
sir.add_compounds(["S", "I", "R"])
sir.add_parameters({"alpha": 2, "beta": 0.5})
sir.add_reaction_from_args("infection", infection, {"S": -1, "I": 1}, ["alpha", "S", "I", "R"])
sir.add_reaction_from_args("recovery", recovery, {"I": -1, "R": 1}, ["beta", "I"])
s = Simulator(sir)
s.initialise({"S": 900, "I": 100, "R": 0})
res = s.simulate(t_end=20)

with plt.rc_context(
    {
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.prop_cycle": cycler(color=["#70A288", "#D5896F", "#8E7DBE"]),
    }
):
    s.plot(xlabel="Time / months", ylabel="Population size")
