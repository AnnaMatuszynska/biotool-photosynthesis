from model import get_model
from modelbase.ode import Simulator
from scipy.signal import find_peaks, peak_prominences
import matplotlib.pyplot as plt
from matplotlib import patches
from typing import Callable

def sim_model(
    updated_parameters, slider_time, slider_light, slider_pings, slider_saturate, slider_darklength
):
    m = get_model()
    m.update_parameters(updated_parameters)
    s = Simulator(m)

    y0 = {"P": 0, "H": 6.32975752e-05, "E": 0, "A": 25.0, "Pr": 1, "V": 1}
    s.initialise(y0)

    max_time = slider_time * 60
    saturating_pulse = slider_saturate
    length_pulse = 0.8
    dark_length = slider_darklength
    dark_light = 0
    light_light = slider_light
    pulses_intervall = slider_pings

    for i in range(max_time):
        if i == 2:
            s.update_parameter("PFD", dark_light)
            s.simulate(i)
            s.update_parameter("PFD", saturating_pulse)
            s.simulate(i + length_pulse)
        elif i == dark_length:
            s.update_parameter("PFD", dark_light)
            s.simulate(i)
            s.update_parameter("PFD", saturating_pulse)
            s.simulate(i + length_pulse)
        elif i in [dark_length + (pulses_intervall * j) for j in range((max_time - dark_length) + 1)]:
            s.update_parameter("PFD", light_light)
            s.simulate(i)
            s.update_parameter("PFD", saturating_pulse)
            s.simulate(i + length_pulse)
        elif i == max_time - 1:
            s.update_parameter("PFD", light_light)
            s.simulate(i)
            s.simulate(max_time)

    sim_time = s.get_time()
    sim_results = s.get_full_results_dict()
    return sim_time, sim_results

def calculate_results_to_plot(time, sim_results):
    
    # Fluorescense Calculation
    fluo_results = sim_results['Fluo'] / max(sim_results['Fluo'])
    
    # Find the Flourescence peaks (Fmaxs)
    peaks, _ = find_peaks(fluo_results, height=0)  
    
    #Calculate NPQ
    NPQ = ((sim_results['Fluo'][peaks][0] - sim_results['Fluo'][peaks])) / sim_results['Fluo'][peaks]
    
    # Find the minima around the peaks
    prominences, prominences_left, prominences_right = peak_prominences(
                (fluo_results), peaks
            )  
    # Fo is always the minima before the peak
    Fo = [
                (fluo_results)[i] for i in prominences_left
            ]  
    #Calculate PhiPSII
    PhiPSII = (sim_results['Fluo'][peaks] - Fo) / sim_results['Fluo'][peaks]
    
    results_dict = {
        'Fluo': [time, fluo_results],
        'NPQ': [time[peaks], NPQ],
        'PhiPSII': [time[peaks], PhiPSII]
    }
    
    return results_dict

def plot_stylings():
    
    text_color = "#727682"
    
    stylings_dict = {
        "axes.spines.right": False,
        "axes.edgecolor": text_color,
        "font.size": 12.0,
        "text.color": text_color,
        "axes.labelcolor": text_color,
        "xtick.color": text_color,
        "ytick.color": text_color,
        "grid.color": text_color,
        "font.weight": 'bold',  
    }
    
    return stylings_dict

def make_4Bio_plot(text: Callable[[str], str], xlabel1, xlabel2, ylabel, values, max_time, dark_length, width, height):
    
    alpha_old = 0.5
    
    style_dict = {
        'Fluo': {
            'color': '#FF4B4B',
            'alpha': 1,
            'linestyle': 'solid',
            'label': 'New'
        },
        'old Fluo': {
            'color': '#FF4B4B',
            'alpha': alpha_old,
            'linestyle': 'dashdot',
            'label': 'Old'
        }
    }
    
    plot_style = plot_stylings()
    plot_style.update({"figure.figsize": (width, height)})
    
    with plt.rc_context(plot_style):
        fig, ax = plt.subplots()
        for i in ['old Fluo', 'Fluo']:
            if values.get(i):
                ax.plot(
                    values[i][0],
                    values[i][1],
                    color = style_dict[i]['color'],
                    linestyle = style_dict[i]['linestyle'],
                    alpha = style_dict[i]['alpha'],
                    label = style_dict[i]['label']
                )

            # Create the top xaxis for the minutes
            ax_top = ax.secondary_xaxis("top", functions=(lambda x: x / 60, lambda x: x * 60))
            
            # Add labels
            ax.set_xlabel(xlabel1, weight = 'bold', size = 12)
            ax.set_ylabel(ylabel, weight = 'bold', size = 12)
            ax_top.set_xlabel(xlabel2, weight = 'bold', size = 12)
            
    # Add the dark phase length to the xticks
    default_xticks = ax.get_xticks()
    new_xticks = []
    for i in range(len(default_xticks)):
        try:
            if default_xticks[i] > dark_length and default_xticks[i - 1] < dark_length:
                new_xticks.append(dark_length)
                new_xticks.append(default_xticks[i])
            else:
                new_xticks.append(default_xticks[i])
        except:
            pass

    ax.set_xticks(new_xticks)

    # Change the left and down limit
    ax.set_xlim(0, max_time)
    ax.set_ylim(0)

    # Highlight dark and light phase
    dark_patch = patches.Rectangle(
        xy=(ax.get_xlim()[0], ax.get_ylim()[0]),
        width=dark_length,
        height=ax.get_ylim()[1],
        facecolor="#1c5bc7",
        alpha=0.3,
    )
    light_patch = patches.Rectangle(
        xy=(dark_length, ax.get_ylim()[0]),
        width=max_time - dark_length,
        height=ax.get_ylim()[1],
        facecolor="#cf6d0c",
        alpha=0.3,
    )

    ax.add_patch(dark_patch)
    ax.add_patch(light_patch)

    # Create and center legend
    plt.legend(loc = 'best', ncols = 2, frameon = False, labelcolor = 'linecolor', fontsize = 12, prop = {'weight':'bold'})

    return fig

def make_4STEM_plot(text: Callable[[str], str], xlabel1, xlabel2, ylabel, values, max_time, dark_length, width, height):
    
    alpha_old = 0.5
    
    style_dict = {
        'Fluo': {
            'color': '#FF4B4B',
            'alpha': 1,
            'linestyle': 'solid',
            'label': 'New'
        },
        'old Fluo': {
            'color': '#FF4B4B',
            'alpha': alpha_old,
            'linestyle': 'dashdot',
            'label': 'Old'
        },
        'NPQ': {
            'color': '#FF4B4B',
            'alpha': 1,
            'linestyle': 'solid',
            'label': 'New'
        },
        'old NPQ': {
            'color': '#FF4B4B',
            'alpha': alpha_old,
            'linestyle': 'dashdot',
            'label': 'Old'
        },
        'PhiPSII': {
            'color': '#FF4B4B',
            'alpha': 1,
            'linestyle': 'solid',
            'label': 'New'
        },
        'old PhiPSII': {
            'color': '#FF4B4B',
            'alpha': alpha_old,
            'linestyle': 'dashdot',
            'label': 'Old'
        }
    }
    
    plot_style = plot_stylings()
    plot_style.update({"figure.figsize": (width, height)})
    
    with plt.rc_context(plot_style):
        fig, axs = plt.subplot_mosaic(mosaic=[["A", "A"], ["B", "C"]], constrained_layout=True)
        
        graph_belong = {
            'Fluo': 'A',
            'NPQ': 'B',
            'PhiPSII': 'C'
        }
        
        for i in {'Fluo', 'NPQ', 'PhiPSII'}:
            if values.get('old ' + i):
                axs[graph_belong[i]].plot(
                        values['old ' + i][0],
                        values['old ' + i][1],
                        color = style_dict['old ' + i]['color'],
                        linestyle = style_dict['old ' + i]['linestyle'],
                        alpha = style_dict['old ' + i]['alpha'],
                        label = style_dict['old ' + i]['label']
                    )
            axs[graph_belong[i]].plot(
                    values[i][0],
                    values[i][1],
                    color = style_dict[i]['color'],
                    linestyle = style_dict[i]['linestyle'],
                    alpha = style_dict[i]['alpha'],
                    label = style_dict[i]['label']
                )
            
            # Create the top xaxis for the minutes
            ax_top = axs[graph_belong[i]].secondary_xaxis("top", functions=(lambda x: x / 60, lambda x: x * 60))
            
            # Add labels
            axs[graph_belong[i]].set_xlabel(xlabel1, weight = 'bold', size = 12)
            axs[graph_belong[i]].set_ylabel(ylabel[i], weight = 'bold', size = 12)
            ax_top.set_xlabel(xlabel2, weight = 'bold', size = 12)
            
            axs[graph_belong[i]].legend(loc = 'best', ncols=2, frameon = False, labelcolor = 'linecolor', fontsize = 12, prop = {'weight':'bold'})
            
    for j in range(len([axs["A"], axs["B"], axs["C"]])):
        ax = [axs["A"], axs["B"], axs["C"]][j]
        # Add the dark phase length to the xticks
        default_xticks = ax.get_xticks()
        new_xticks = []
        for i in range(len(default_xticks)):
            try:
                if default_xticks[i] > dark_length and default_xticks[i - 1] < dark_length:
                    new_xticks.append(dark_length)
                    new_xticks.append(default_xticks[i])
                else:
                    new_xticks.append(default_xticks[i])
            except:
                pass

        ax.set_xticks(new_xticks)

        # Change the left and down limit
        ax.set_xlim(0, max_time)
        ax.set_ylim(0)

        # Highlight dark and light phase
        dark_patch = patches.Rectangle(
            xy=(ax.get_xlim()[0], ax.get_ylim()[0]),
            width=dark_length,
            height=ax.get_ylim()[1],
            facecolor="#1c5bc7",
            alpha=0.3,
        )
        light_patch = patches.Rectangle(
            xy=(dark_length, ax.get_ylim()[0]),
            width=max_time - dark_length,
            height=ax.get_ylim()[1],
            facecolor="#cf6d0c",
            alpha=0.3,
        )

        ax.add_patch(dark_patch)
        ax.add_patch(light_patch)


    return fig
    
    


