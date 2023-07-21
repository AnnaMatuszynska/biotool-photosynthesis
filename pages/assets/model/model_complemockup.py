from matplotlib import pyplot as plt, patches

max_time = 600
saturating_pulse = 5000
length_pulse = 0.8
dark_length = 30
dark_light = 0
light_light= 100
number_pulses = 10

for i in range(max_time):
    if i == 1:
        simulator.update_parameter("PFD", dark_light)
        simulator.simulate(i)
        simulator.update_parameter("PFD", saturating_pulse)
        simulator.simulate(i + length_pulse)
    elif i == dark_length:
        simulator.update_parameter("PFD", dark_light)
        simulator.simulate(i)
        simulator.update_parameter("PFD", saturating_pulse)
        simulator.simulate(i + length_pulse)
    elif i % round(max_time/number_pulses) == 0:
        simulator.update_parameter("PFD", light_light)
        simulator.simulate(i)
        simulator.update_parameter("PFD", saturating_pulse)
        simulator.simulate(i + length_pulse)
    elif i == max_time - 1:
        simulator.update_parameter("PFD", light_light)
        simulator.simulate(i)
        simulator.simulate(max_time)

sim_results = simulator.get_full_results_dict() #Store the Results fo the sim

with plt.rc_context(
    {
        "axes.spines.right": False,
        "axes.spines.top": False,
        "figure.frameon": True,
        "figure.figsize": (10, 5),
        "axes.facecolor": "None",
        "figure.edgecolor": "None",
        "text.color": "#9296a4",
        "axes.labelcolor": "#9296a4",
        "xtick.color": "#9296a4",
        "ytick.color": "#9296a4"
    }
):
    fig, ax = plt.subplots()
    ax.plot(simulator.get_time(),
            sim_results['Fluo']/max(sim_results['Fluo']),
            color = '#FF4B4B'    
        )

# Change the left and down limit
plt.xlim(0, max_time)
plt.ylim(0, 1)

# Set the tick values
plt.xticks([i for i in range(0, max_time + 1, 50)])

# Highlight dark and light phase
dark_patch = patches.Rectangle((0,0), dark_length, 1, facecolor = '#1c5bc7', alpha = 0.3)
light_patch = patches.Rectangle((dark_length,0), max_time - dark_length, 1, facecolor = '#cf6d0c', alpha = 0.3)

ax.add_patch(dark_patch)
ax.add_patch(light_patch)

#Change color of axis
ax.spines['bottom'].set_color("#9296a4")
ax.spines['left'].set_color("#9296a4")

#Add labels
ax.set_xlabel("Time [s]")
ax.set_ylabel("Fluorescence [F´ₘ /Fₘ]")

plt.show()