import matplotlib.pyplot as plt

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

fig, ax = plt.subplots()
ax.plot(simulator.get_time(), sim_results['Fluo']/max(sim_results['Fluo']))