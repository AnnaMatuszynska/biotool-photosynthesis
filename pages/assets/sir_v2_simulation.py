s = Simulator(sir)
s.initialise({"s": 0.9, "i": 0.1, "r": 0})
res = s.simulate(t_end=100)
