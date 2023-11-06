s = Simulator(sir)
s.initialise({"S": 900, "I": 100, "R": 0})
res = s.simulate(t_end=20)

# Create the same figure as above
with plt.rc_context(
    {
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.prop_cycle": cycler(color=["#70A288", "#D5896F", "#8E7DBE"]),
    }
):
    s.plot(xlabel="Months",
           ylabel="Population size",
           grid = False,
           plot_kwargs = {'label': ['S', 'I', 'R']},
           label_kwargs = {'fontsize': 18},
           tick_kwargs = {'axis': 'both', 'labelsize': 12},
           figure_kwargs = {'figsize': (7, 4)}, 
          )

# Change the left and down limit
plt.xlim(0)
plt.ylim(0)

# Create and center legend
plt.legend(loc = 'center right', frameon = False)

# Show the plot
plt.show()

