sird = sir.copy()
sird.add_compound("d")
sird.add_parameter("mu", 0.05)
sird.add_reaction_from_args("death", proportional, {"i": -1, "d": 1}, ["mu", "i"])
