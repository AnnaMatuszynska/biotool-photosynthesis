import numpy as np
import matplotlib.pyplot as plt
from modelbase.ode import Model, Simulator
from cycler import cycler

def infection(S, I, N, beta):
    return beta * S * I / N


def turnover(I, gamma):
    return gamma * I


def total_population(S, I, R):
    return S + I + R


parameters = {
    "beta": 2,  # new infections caused by one infection
    "gamma": 0.5,  # turnover rate of infected (death or recovery)
}

m = Model()

m.add_parameters(parameters)

m.add_compounds(("S", "I", "R"))

m.add_algebraic_module(
    module_name="N",
    function=total_population,
    compounds=["S", "I", "R"],
    derived_compounds=["N"],
)
m.add_reaction(
    rate_name="infection",
    function=infection,
    stoichiometry={"S": -1, "I": 1},
    modifiers=["I", "N"],
    parameters=["beta"],
)
m.add_reaction(
    rate_name="turnover",
    function=turnover,
    stoichiometry={"I": -1, "R": 1},
    parameters=["gamma"],
)

s = Simulator(m)

s.initialise({"S": 900, "I": 100, "R": 0})
s.simulate(20)

with plt.rc_context(
    {
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.prop_cycle": cycler(color=["#70A288", "#D5896F", "#8E7DBE"]),
    }
):
# Create the Figure    
    s.plot(xlabel="Months",
           ylabel="Population size",
           grid = False,
           plot_kwargs = {'label': ['S', 'I', 'R']},
           label_kwargs = {'fontsize': 18},
           tick_kwargs = {'axis': 'both', 'labelsize': 12},
           figure_kwargs = {'figsize': (7, 4)}, 
          )

# Change the ticks
plt.xlim(0)
plt.ylim(0)

plt.legend(loc = 'center right', frameon = False)

# Uncomment to save
#plt.savefig('..\SIR.png', bbox_inches='tight', facecolor = 'white', edgecolor = 'white')

plt.show()