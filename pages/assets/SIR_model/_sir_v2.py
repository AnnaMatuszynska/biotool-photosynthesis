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

# To get the same design as us
text_color = "#727682"

with plt.rc_context(
    {
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.edgecolor": text_color,
        "font.size": 12.0,
        "text.color": text_color,
        "axes.labelcolor": text_color,
        "xtick.color": text_color,
        "ytick.color": text_color,
        "grid.color": text_color,
        "font.weight": 'bold',
        "axes.prop_cycle": cycler(color=["#f9a51b", "#d1232a", "#1062ef"]), 
    }
):
    s.plot(xlabel="Time [Months]",
           ylabel="Population size [a.u.]",
           grid = False,
           tight_layout=True,
           plot_kwargs = {
               'label': ['S', 'I', 'R'],
               'linewidth': 5,
           },
           figure_kwargs = {
               'figsize': (7, 4)
           }
          )

# Set Axis titles
plt.xlabel('Time [Months]', fontsize = 12, weight= 'bold')
plt.ylabel('Population size [a.u.]', fontsize = 12, weight= 'bold')

# Change the left and down limit
plt.xlim(0)
plt.ylim(0)

# Create and center legend
plt.legend(loc = 'center right', frameon = False, labelcolor = 'linecolor', fontsize = 12, prop = {'weight':'bold'})

# Uncomment to save the figure
#plt.savefig('./pictures/SIR_modelbase.png', transparent = True)

# Show the plot
#plt.show()
