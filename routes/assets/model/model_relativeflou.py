import matplotlib.pyplot as plt

simulator.simulate(100)

sim_results = simulator.get_full_results_dict() #Store the Results fo the sim

fig, ax = plt.subplots()
ax.plot(simulator.get_time(), sim_results['Fluo']/max(sim_results['Fluo']))

plt.show()