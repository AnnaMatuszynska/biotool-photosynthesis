from model import get_model
from modelbase.ode import Simulator
from scipy.signal import find_peaks, peak_prominences
import matplotlib.pyplot as plt
from matplotlib import patches
from typing import Callable
import warnings
from matplotlib.lines import Line2D

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
    
    text_color = "black"
    
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

def sim_model_memory(
    updated_parameters,
    slider_light,
    slider_pings,
    slider_saturate,
    slider_darklength,
    training_length,
    relaxation_phase,
    memory_length,
):
    m = get_model()
    m.update_parameters(updated_parameters)
    s = Simulator(m)

    y0 = {"P": 0, "H": 6.32975752e-05, "E": 0, "A": 25.0, "Pr": 1, "V": 1}
    s.initialise(y0)

    length_pulse = 0.8
    dark_light = 0
    training_length = int(training_length)
    relaxation_phase = int(relaxation_phase)

    # Dark Period
    if slider_darklength > 0:
        simulate_period(
            s=s,
            starting_time=2,
            length_phase=slider_darklength,
            pulse_intervall=slider_pings,
            starting_light=dark_light,
            saturating_pulse=slider_saturate,
            length_pulse=length_pulse,
            during_light=dark_light,
            dark_flag=True,
        )
    # Training
    if training_length > 0:
        simulate_period(
            s=s,
            starting_time=slider_darklength,
            length_phase=training_length,
            pulse_intervall=slider_pings,
            starting_light=dark_light,
            saturating_pulse=slider_saturate,
            length_pulse=length_pulse,
            during_light=slider_light,
        )
    # Relaxation phase 1
    if relaxation_phase > 0:
        simulate_period(
            s=s,
            starting_time=slider_darklength + training_length,
            length_phase=slider_darklength + training_length + relaxation_phase - slider_pings,
            pulse_intervall=slider_pings,
            starting_light=slider_light,
            saturating_pulse=slider_saturate,
            length_pulse=length_pulse,
            during_light=dark_light,
            dark_flag=True,
        )
    # Relaxation phase 2
    if relaxation_phase > 0:
        simulate_period(
            s=s,
            starting_time=slider_darklength + training_length + relaxation_phase - slider_pings,
            length_phase=slider_pings,
            pulse_intervall=slider_pings,
            starting_light=dark_light,
            saturating_pulse=slider_saturate,
            length_pulse=length_pulse,
            during_light=dark_light,
            dark_flag=True,
        )
    # Memory Phase
    if memory_length > 0:
        simulate_period(
            s=s,
            starting_time=slider_darklength + training_length + relaxation_phase,
            length_phase=memory_length,
            pulse_intervall=slider_pings,
            starting_light=dark_light,
            saturating_pulse=slider_saturate,
            length_pulse=length_pulse,
            during_light=slider_light,
        )
    # End
    s.update_parameter("PFD", slider_light)
    s.simulate(slider_darklength + training_length + relaxation_phase + memory_length)

    sim_time = s.get_time()
    sim_results = s.get_full_results_dict()
    return sim_time, sim_results

def simulate_period(s, starting_time, length_phase, pulse_intervall, starting_light, saturating_pulse, length_pulse, during_light, dark_flag = False):
    warnings.filterwarnings("error", category= RuntimeWarning)
    error_flag = True
    
    while error_flag == True:
        try:
            s.update_parameter("PFD", starting_light)
            s.simulate(starting_time)
            s.update_parameter("PFD", saturating_pulse)
            s.simulate(starting_time + length_pulse)
            
            warnings.filterwarnings("default", category= RuntimeWarning)
            error_flag = False
        except RuntimeWarning:
            starting_light += 0.001
            
    
    num_pulses = int(length_phase/pulse_intervall)
            
    if dark_flag == False:
        for i in range(num_pulses):
            if i > 0:
                new_timepoint = starting_time + pulse_intervall * i
                s.update_parameter("PFD", during_light)
                s.simulate(new_timepoint)
                s.update_parameter("PFD", saturating_pulse)
                s.simulate(new_timepoint + length_pulse)
            
    return

def make_plot(
    values,
    variables,
    version,
    width,
    height,
    xlabel1,
    xlabel2,
    ylabel,
    dark_length,
    new_label,
    old_label,
    memory_flag  = False,
    max_time = None,
    training_length = None,
    relaxation_length = None,
    memory_length = None,
    annotation_labels = None
):
    if memory_flag:
        max_time = dark_length + training_length + relaxation_length + memory_length
    
    plot_style = plot_stylings()
    
    alpha_old = 0.5
    
    style_dict = {
        'Old': {
            'color': '#2D3047',
            'alpha': alpha_old,
            'linestyle': 'dashdot',
            'label': old_label
        },
        'New': {
            'color': '#2D3047',
            'alpha': 1,
            'linestyle': 'solid',
            'label': new_label
        }
    }
    
    plot_style.update({"figure.figsize": (width, height)})
    
    plot_mosaic = [['A' if i < 7 else 'D' for i in range(0, 10)]]
    
    if version == '4Bio':
        plot_mosaic.append(['B' if i < 5 else 'C' for i in range(0, 10)])
    
    with plt.rc_context(plot_style):
        fig, axs = plt.subplot_mosaic(mosaic=plot_mosaic, constrained_layout=True, figsize = (15,15/2.3))
        
        #Create fake legend
        axs['D'].set_axis_off()
        
        new_line = Line2D([0], [0], color = style_dict['New']['color'], linestyle = style_dict['New']['linestyle'], alpha = style_dict['New']['alpha'])
        old_line = Line2D([0], [0], color = style_dict['Old']['color'], linestyle = style_dict['Old']['linestyle'], alpha = style_dict['Old']['alpha'])
        
        new_legend = axs['D'].legend(
            [new_line],
            [new_label],
            frameon = False,
            labelcolor = 'linecolor',
            loc = 'center',
            bbox_to_anchor = (0.5, 1)
        )
        
        variable_text = ""
        variable_numbers_new = ''
        variable_numbers_old = ''
        
        for data_version, data_dict in variables.items():
            for variable_name, variable in data_dict.items():
                if data_version == 'New':
                    variable_text += f"{variable_name}\n"
                    variable_numbers_new += f"{variable}\n"
                else:
                    variable_numbers_old += f"{variable}\n"
        
        axs['D'].text(-0.15, 0.9, variable_text, linespacing=2, verticalalignment = 'top', ha='left')
        
        axs['D'].text(0.5, 0.9, variable_numbers_new, linespacing=2, verticalalignment = 'top', horizontalalignment = 'center')
        
        if values.get('old Fluo'):
            old_legend = axs['D'].legend(
                [old_line],
                [old_label],
                frameon = False,
                labelcolor = 'linecolor',
                loc = 'center',
                bbox_to_anchor = (0.85, 1)
            )
            axs['D'].text(0.85, 0.9, variable_numbers_old, linespacing=2, verticalalignment = 'top', horizontalalignment = 'center')
        
        axs['D'].add_artist(new_legend)

        # Plot the graphs
        graph_belong = {'Fluo': 'A'}
        
        if version == '4Bio':
            graph_belong.update({
                'NPQ': 'B',
                'PhiPSII': 'C'
            })
        
        for graph, letter in graph_belong.items():
            if values.get('old ' + graph):
                axs[letter].plot(
                    values['old ' + graph][0],
                    values['old ' + graph][1],
                    color = style_dict['Old']['color'],
                    linestyle = style_dict['Old']['linestyle'],
                    alpha = style_dict['Old']['alpha'],
                )
            axs[letter].plot(
                values[graph][0],
                values[graph][1],
                color = style_dict['New']['color'],
                linestyle = style_dict['New']['linestyle'],
                alpha = style_dict['New']['alpha'],
            )
            
            # Create the top xaxis for the minutes
            ax_top = axs[letter].secondary_xaxis("top", functions=(lambda x: x / 60, lambda x: x * 60))
            
            # Add labels
            axs[letter].set_xlabel(xlabel1, weight = 'bold', size = 14)
            axs[letter].set_ylabel(ylabel[graph], weight = 'bold', size = 14)
            ax_top.set_xlabel(xlabel2, weight = 'bold', size = 14)

            default_xticks = axs[letter].get_xticks()
            new_xticks = []
            if memory_flag:
                try:
                    if default_xticks[i] > dark_length and default_xticks[i - 1] < dark_length:
                        new_xticks.append(dark_length)
                        new_xticks.append(default_xticks[i])
                    elif (
                        default_xticks[i] > training_length + dark_length
                        and default_xticks[i - 1] < training_length + dark_length
                    ):
                        new_xticks.append(training_length + dark_length)
                        new_xticks.append(default_xticks[i])
                    elif (
                        default_xticks[i] > relaxation_length + training_length + dark_length
                        and default_xticks[i - 1] < relaxation_length + training_length + dark_length
                    ):
                        new_xticks.append(relaxation_length + training_length + dark_length)
                        new_xticks.append(default_xticks[i])
                    else:
                        new_xticks.append(default_xticks[i])
                except:
                    pass
            else:
                for i in range(len(default_xticks)):
                    try:
                        if default_xticks[i] > dark_length and default_xticks[i - 1] < dark_length:
                            new_xticks.append(dark_length)
                            new_xticks.append(default_xticks[i])
                        else:
                            new_xticks.append(default_xticks[i])
                    except:
                        pass

            axs[letter].set_xticks(new_xticks)

            # Change the left and down limit
            axs[letter].set_xlim(0, max_time)
            axs[letter].set_ylim(0)
            
            # Highlight dark and light phase
            dark_patch = patches.Rectangle(
                xy=(axs[letter].get_xlim()[0], axs[letter].get_ylim()[0]),
                width=dark_length,
                height=axs[letter].get_ylim()[1],
                facecolor="#1c5bc7",
                alpha=0.3,
            )
            
            axs[letter].add_patch(dark_patch)
            
            if memory_flag:
                training_patch = patches.Rectangle(
                    xy=(dark_length, axs[letter].get_ylim()[0]),
                    width=training_length,
                    height=axs[letter].get_ylim()[1],
                    facecolor="#cf6d0c",
                    alpha=0.3,
                )
                relaxation_patch = patches.Rectangle(
                    xy=(training_length + dark_length, axs[letter].get_ylim()[0]),
                    width=relaxation_length,
                    height=axs[letter].get_ylim()[1],
                    facecolor="#1c5bc7",
                    alpha=0.3,
                )
                memory_patch = patches.Rectangle(
                    xy=(dark_length + training_length + relaxation_length, axs[letter].get_ylim()[0]),
                    width=memory_length,
                    height=axs[letter].get_ylim()[1],
                    facecolor="#D10A0D",
                    alpha=0.3,
                )
                
                for key, annotated_patch in {'Training': training_patch, 'Relaxation': relaxation_patch, 'Memory': memory_patch}.items():
                    axs[letter].add_patch(annotated_patch)
                    if annotated_patch.get_width() != 0:
                        rx, ry = annotated_patch.get_xy()
                        cx = rx + annotated_patch.get_width() / 2
                        cy = ry + annotated_patch.get_height() * 0.1
                        axs[letter].annotate(
                            annotation_labels[key],
                            (cx, cy),
                            ha="center",
                            va="center",
                            color="#323336",
                            alpha=1,
                            backgroundcolor="#9296a4",
                        )                
            else:
                light_patch = patches.Rectangle(
                    xy=(dark_length, axs[letter].get_ylim()[0]),
                    width=max_time - dark_length,
                    height=axs[letter].get_ylim()[1],
                    facecolor="#cf6d0c",
                    alpha=0.3,
                )
                
                axs[letter].add_patch(light_patch)
            
    return fig