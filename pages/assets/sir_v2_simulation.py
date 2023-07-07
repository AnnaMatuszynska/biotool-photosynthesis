s = Simulator(sir)
s.initialise({"S": 900, "I": 100, "R": 0})
res = s.simulate(t_end=20)
fig, ax = s.plot(xlabel="Time / months", ylabel="Population size")
