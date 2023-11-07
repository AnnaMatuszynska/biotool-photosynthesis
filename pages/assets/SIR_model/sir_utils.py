import matplotlib.pyplot as plt
from cycler import cycler
from modelbase.ode import Model, Simulator

def infection(beta, s, i, r):
    return beta * s * i / (s + i + r)


def recovery(gamma, x):
    return gamma * x

def get_results_dict_SIRModel(beta_param, gamma_param, S_initial, I_initial, R_initial, time_end):
    
    sir = Model()
    sir.add_compounds(["S", "I", "R"])
    sir.add_parameters({"beta": beta_param, "gamma": gamma_param})

    sir.add_reaction_from_args("infection", infection, {"S": -1, "I": 1}, ["beta", "S", "I", "R"])
    sir.add_reaction_from_args("recovery", recovery, {"I": -1, "R": 1}, ["gamma", "I"])

    s = Simulator(sir)
    s.initialise({"S": S_initial, "I": I_initial, "R": R_initial})
    s.simulate(t_end=time_end)
    
    sim_time = s.get_time()
    sim_results = s.get_full_results_dict()
    
    return sim_time, sim_results

def get_plot_SIRModel(values_dict):
    
    text_color = "#727682"
    alpha_old = 0.5
    
    style_dict = {
        'old S': {
            'color': '#f9a51b',
            'alpha': alpha_old,
            'linestyle': 'dashdot',
        },
        'old I': {
            'color': '#d1232a',
            'alpha': alpha_old,
            'linestyle': 'dashdot',
        },
        'old R': {
            'color': '#1062ef',
            'alpha': alpha_old,
            'linestyle': 'dashdot',
        },
        'S': {
            'color': '#f9a51b',
            'alpha': 1,
            'linestyle': 'solid',
        },
        'I': {
            'color': '#d1232a',
            'alpha': 1,
            'linestyle': 'solid',
        },
        'R': {
            'color': '#1062ef',
            'alpha': 1,
            'linestyle': 'solid',
        },
    }
    
    with plt.rc_context(
    {
        "axes.spines.right": False,
        "axes.edgecolor": text_color,
        "axes.spines.top": False,
        "font.size": 12.0,
        "text.color": text_color,
        "axes.labelcolor": text_color,
        "xtick.color": text_color,
        "ytick.color": text_color,
        "grid.color": text_color,
        "font.weight": 'bold',
    }
        ):
        
        fig, ax = plt.subplots()
        
        for key in ['old S', 'old I', 'old R', 'S', 'I', 'R']:
            if values_dict.get(key):
                ax.plot(
                    values_dict[key][0],
                    values_dict[key][1],
                    color = style_dict[key]['color'],
                    linestyle = style_dict[key]['linestyle'],
                    alpha = style_dict[key]['alpha'],
                    linewidth = 5,
                    label = key
                )

        
# Change the left and down limit
    plt.xlim(0)
    plt.xlabel('Time [Months]', weight= 'bold', size=12)
    plt.ylim(0, 1000)
    plt.ylabel('Population size [a.u.]', weight= 'bold', size=12)

# Create and center legend
    plt.legend(loc = 'center right', frameon = False, labelcolor = 'linecolor', fontsize = 12, prop = {'weight':'bold'})

# Show the plot

    plt.tight_layout()
    
    return fig

    