from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from cycler import cycler


def sir(t, y, alpha, beta):
    s, i, r = y
    infection = alpha * s * i / (s + i + r)
    recovery = beta * i
    return (
        -infection,  # ds/dt
        infection - recovery,  # di/dt
        recovery,  # dr/dt
    )


res = solve_ivp(
    sir,
    t_span=(0, 20),
    y0=(900, 100, 0),  # needs to match s, i, r unpacking order
    args=(2, 0.5),  # needs to match fn argument order
)

with plt.rc_context(
    {
        "font.size": 12,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "lines.linewidth": 3 ,
        "axes.labelsize": 12,
        "axes.prop_cycle": cycler(color=["#70A288", "#D5896F", "#8E7DBE"]),
    }
):
    fig, ax = plt.subplots(figsize = (7, 4))

    for i in ['S', 'I', 'R']:
        ax.plot(res['t'], res['y'][['S', 'I', 'R'].index(i)], label = i)

# Set Axis titles
plt.xlabel('Months', fontsize = 18)
plt.ylabel('Population size', fontsize = 18)

# Change the left and down limit
plt.xlim(0)
plt.ylim(0)

# Create and center legend
plt.legend(loc = 'center right', frameon = False)

# Save the figure
#plt.savefig('./pictures/SIR_manual.png', bbox_inches='tight', facecolor = 'white', edgecolor = 'white')

# Show the plot
plt.show()
