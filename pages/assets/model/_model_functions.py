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

    # Create and legend
    plt.legend(loc = 'best', ncols = 2, frameon = False, labelcolor = 'linecolor', fontsize = 12, prop = {'weight':'bold'})

    return fig

def make_4Bio_plot(text: Callable[[str], str], xlabel1, xlabel2, ylabel, values, max_time, dark_length, width, height, variables):
    
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
    
    plot_mosaic = [['A' if i < 6 else 'D' for i in range(0, 10)], ['B' if i < 5 else 'C' for i in range(0, 10)]]
    
    with plt.rc_context(plot_style):
        fig, axs = plt.subplot_mosaic(mosaic=plot_mosaic, constrained_layout=True)
        
        #Create fake legend
        axs['D'].set_axis_off()
        
        custom_legend_lines = [
            Line2D([0], [0], color = style_dict['Fluo']['color'], linestyle = style_dict['Fluo']['linestyle'], alpha = style_dict['Fluo']['alpha'])
        ]
        custom_legend_text = [
            'New'
        ]
        
        if values.get('old Fluo'):
            custom_legend_lines.append(
                Line2D([0], [0], color = style_dict['old Fluo']['color'], linestyle = style_dict['old Fluo']['linestyle'], alpha = style_dict['old Fluo']['alpha'])
            )
            custom_legend_text.append('Old')
            variable_numbers_old = f"{variables['old slider_light']}\n{variables['old slider_saturate']}"
            
        variable_text = "LP [μmol m⁻² s⁻¹]\nSP [μmol m⁻² s⁻¹]"
        
        variable_numbers_new = f"{variables['slider_light']}\n{variables['slider_saturate']}"
        
        axs['D'].text(0, 0.9, variable_text, linespacing=1.5, verticalalignment = 'top')
        axs['D'].text(0.6, 0.9, variable_numbers_new, linespacing=1.5, verticalalignment = 'top', horizontalalignment = 'center')
        axs['D'].text(0.85, 0.9, variable_numbers_old, linespacing=1.5, verticalalignment = 'top', horizontalalignment = 'center')
            
        axs['D'].legend(custom_legend_lines, custom_legend_text, ncols=2, frameon = False, labelcolor = 'linecolor', loc = [0.5,1])
        
        # Plot the graphs
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
    
def make_both_plots(text: Callable[[str], str], xlabel1, xlabel2, ylabel_4Bio, ylabel_4STEM, session_state_values, slider_time, slider_darklength, slider_values):
    
    fig_1 = make_4Bio_plot(
                text=text,
                xlabel1=xlabel1,
                xlabel2=xlabel2,
                ylabel=ylabel_4Bio,
                values=session_state_values,
                max_time=slider_time * 60,
                dark_length=slider_darklength,
                width=15,
                height=6,
                variables=slider_values
            )
    
    fig_2 = make_4STEM_plot(
                text=text,
                xlabel1=xlabel1,
                xlabel2=xlabel2,
                ylabel=ylabel_4STEM,
                values=session_state_values,
                max_time=slider_time * 60,
                dark_length=slider_darklength,
                width=15,
                height=3,
            )
    
    return fig_1, fig_2    

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

def make_matplotlib_plot_memory_4STEM(
    text: Callable[[str], str],
    xlabel1,
    xlabel2,
    ylabel,
    values,
    dark_length,
    width,
    height,
    training_length,
    relaxation_length,
    memory_length,
):
    max_time = dark_length + training_length + relaxation_length + memory_length

    style_plot = plot_stylings()
    style_plot.update({"figure.figsize": (width, height)})
    
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
    
    with plt.rc_context(style_plot):
        
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
        training_patch = patches.Rectangle(
            xy=(dark_length, ax.get_ylim()[0]),
            width=training_length,
            height=ax.get_ylim()[1],
            facecolor="#cf6d0c",
            alpha=0.3,
        )
        relaxation_patch = patches.Rectangle(
            xy=(training_length + dark_length, ax.get_ylim()[0]),
            width=relaxation_length,
            height=ax.get_ylim()[1],
            facecolor="#1c5bc7",
            alpha=0.3,
        )
        memory_patch = patches.Rectangle(
            xy=(dark_length + training_length + relaxation_length, ax.get_ylim()[0]),
            width=memory_length,
            height=ax.get_ylim()[1],
            facecolor="#D10A0D",
            alpha=0.3,
        )
        
        patch_list = [dark_patch, training_patch, relaxation_patch, memory_patch]
        anno_list = [text("MEM_ANNO_TRAINING"), text("MEM_ANNO_RELAXATION"), text("MEM_ANNO_MEMORY")]

        for i in range(len(patch_list)):
            ax.add_patch(patch_list[i])
            if i != 0 and patch_list[i].get_width() != 0:
                rx, ry = patch_list[i].get_xy()
                cx = rx + patch_list[i].get_width() / 2
                cy = ry + patch_list[i].get_height() * 0.1
                ax.annotate(
                    anno_list[i - 1],
                    (cx, cy),
                    ha="center",
                    va="center",
                    color="#323336",
                    alpha=1,
                    backgroundcolor="#9296a4",
                )

        ax.grid(visible=True, which="both", axis="both", color="#9296a4", alpha=0.5)
        
        ax.legend(loc = 'best', ncols=2, frameon = False, labelcolor = 'linecolor', fontsize = 12, prop = {'weight':'bold'})
    
    return fig

def make_matplotlib_plot_memory_4Bio(
    text: Callable[[str], str],
    xlabel1,
    xlabel2,
    ylabel,
    values,
    dark_length,
    width,
    height,
    training_length,
    relaxation_length,
    memory_length,
):
    max_time = dark_length + training_length + relaxation_length + memory_length

    style_plot = plot_stylings()
    style_plot.update({"figure.figsize": (width, height)})
    
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
    
    with plt.rc_context(style_plot):
        fig, axs = plt.subplot_mosaic(mosaic=[["A", "A"], ["B", "C"]], constrained_layout=True)
        
        graph_belong = {
            'Fluo': 'A',
            'NPQ': 'B',
            'PhiPSII': 'C'
        }
        
        for i in {'Fluo', 'NPQ', 'PhiPSII'}:
            ax = axs[graph_belong[i]]
            if values.get('old ' + i):
                ax.plot(
                        values['old ' + i][0],
                        values['old ' + i][1],
                        color = style_dict['old ' + i]['color'],
                        linestyle = style_dict['old ' + i]['linestyle'],
                        alpha = style_dict['old ' + i]['alpha'],
                        label = style_dict['old ' + i]['label']
                    )
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
            ax.set_ylabel(ylabel[i], weight = 'bold', size = 12)
            ax_top.set_xlabel(xlabel2, weight = 'bold', size = 12)
            
            # Add the dark phase length to the xticks
            default_xticks = ax.get_xticks()
            new_xticks = []
            for i in range(len(default_xticks)):
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
            training_patch = patches.Rectangle(
                xy=(dark_length, ax.get_ylim()[0]),
                width=training_length,
                height=ax.get_ylim()[1],
                facecolor="#cf6d0c",
                alpha=0.3,
            )
            relaxation_patch = patches.Rectangle(
                xy=(training_length + dark_length, ax.get_ylim()[0]),
                width=relaxation_length,
                height=ax.get_ylim()[1],
                facecolor="#1c5bc7",
                alpha=0.3,
            )
            memory_patch = patches.Rectangle(
                xy=(dark_length + training_length + relaxation_length, ax.get_ylim()[0]),
                width=memory_length,
                height=ax.get_ylim()[1],
                facecolor="#D10A0D",
                alpha=0.3,
            )
    
            patch_list = [dark_patch, training_patch, relaxation_patch, memory_patch]
            anno_list = [text("MEM_ANNO_TRAINING"), text("MEM_ANNO_RELAXATION"), text("MEM_ANNO_MEMORY")]

            for i in range(len(patch_list)):
                ax.add_patch(patch_list[i])
                if i != 0 and patch_list[i].get_width() != 0:
                    rx, ry = patch_list[i].get_xy()
                    cx = rx + patch_list[i].get_width() / 2
                    cy = ry + patch_list[i].get_height() * 0.1
                    ax.annotate(
                        anno_list[i - 1],
                        (cx, cy),
                        ha="center",
                        va="center",
                        color="#323336",
                        alpha=1,
                        backgroundcolor="#9296a4",
                    )

            ax.grid(visible=True, which="both", axis="both", color="#9296a4", alpha=0.5)
            
        axs[graph_belong['Fluo']].legend(loc = 'best', ncols=2, frameon = False, labelcolor = 'linecolor', fontsize = 12, prop = {'weight':'bold'})
    
    return fig

def make_both_plots_memory(text: Callable[[str], str], xlabel1, xlabel2, ylabel_4Bio, ylabel_4STEM, session_state_values, slider_darklength, slider_training, slider_relaxation, slider_memory):
    
    fig_1 = make_matplotlib_plot_memory_4Bio(
                text=text,
                xlabel1=xlabel1,
                xlabel2=xlabel2,
                ylabel=ylabel_4Bio,
                values=session_state_values,
                dark_length=slider_darklength,
                width=15,
                height=6,
                training_length=slider_training,
                relaxation_length=slider_relaxation,
                memory_length=slider_memory
            )
    
    fig_2 = make_matplotlib_plot_memory_4STEM(
                text=text,
                xlabel1=xlabel1,
                xlabel2=xlabel2,
                ylabel=ylabel_4STEM,
                values=session_state_values,
                dark_length=slider_darklength,
                width=15,
                height=3,
                training_length=slider_training,
                relaxation_length=slider_relaxation,
                memory_length=slider_memory
            )
    
    return fig_1, fig_2

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
    max_time,
    new_label,
    old_label
):
    
    plot_style = plot_stylings()
    
    alpha_old = 0.5
    
    style_dict = {
        'Old': {
            'color': '#FF4B4B',
            'alpha': alpha_old,
            'linestyle': 'dashdot',
            'label': old_label
        },
        'New': {
            'color': '#FF4B4B',
            'alpha': 1,
            'linestyle': 'solid',
            'label': new_label
        }
    }
    
    plot_style.update({"figure.figsize": (width, height)})
    
    plot_mosaic = [['A' if i < 6 else 'D' for i in range(0, 10)]]
    
    if version == '4Bio':
        plot_mosaic.append(['B' if i < 5 else 'C' for i in range(0, 10)])
    
    with plt.rc_context(plot_style):
        fig, axs = plt.subplot_mosaic(mosaic=plot_mosaic, constrained_layout=True)
        
        #Create fake legend
        axs['D'].set_axis_off()
        
        
        
        custom_legend_lines = [
            Line2D([0], [0], color = style_dict['New']['color'], linestyle = style_dict['New']['linestyle'], alpha = style_dict['New']['alpha'])
        ]
        custom_legend_text = [
            style_dict['New']['label']
        ]
        
        variable_numbers_old = ''
        
        if values.get('old Fluo'):
            custom_legend_lines.append(
                Line2D([0], [0], color = style_dict['Old']['color'], linestyle = style_dict['Old']['linestyle'], alpha = style_dict['Old']['alpha'])
            )
            custom_legend_text.append(style_dict['Old']['label'])
            
            variable_numbers_old = f"{variables['old slider_light']}\n{variables['old slider_saturate']}"
        
        legend = axs['D'].legend(custom_legend_lines, custom_legend_text, ncols=2, frameon = False, labelcolor = 'linecolor', loc = 'right', bbox_to_anchor = (1, 1))
        
        for handle in legend.legend_handles:
            bbox = handle.get_bbox()
            x, y, handle_width, handle_height = bbox.x0, bbox.y0, bbox.width, bbox.height
            if handle.get_label() == new_label:
                variable_numbers = variable_numbers_new
            else:
                variable_numbers = variable_numbers_old
            axs['D'].text()
                
        variable_text = "LP [μmol m⁻² s⁻¹]\nSP [μmol m⁻² s⁻¹]"
        
        variable_numbers_new = f"{variables['slider_light']}\n{variables['slider_saturate']}"
        
        axs['D'].text(0, 0.9, variable_text, linespacing=1.5, verticalalignment = 'top')
        axs['D'].text(0.6, 0.9, variable_numbers_new, linespacing=1.5, verticalalignment = 'top', horizontalalignment = 'center')
        axs['D'].text(0.85, 0.9, variable_numbers_old, linespacing=1.5, verticalalignment = 'top', horizontalalignment = 'center')
        
        

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
            axs[letter].set_xlabel(xlabel1, weight = 'bold', size = 12)
            axs[letter].set_ylabel(ylabel[graph], weight = 'bold', size = 12)
            ax_top.set_xlabel(xlabel2, weight = 'bold', size = 12)

            default_xticks = axs[letter].get_xticks()
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
            light_patch = patches.Rectangle(
                xy=(dark_length, axs[letter].get_ylim()[0]),
                width=max_time - dark_length,
                height=axs[letter].get_ylim()[1],
                facecolor="#cf6d0c",
                alpha=0.3,
            )

            axs[letter].add_patch(dark_patch)
            axs[letter].add_patch(light_patch)
            
    return fig