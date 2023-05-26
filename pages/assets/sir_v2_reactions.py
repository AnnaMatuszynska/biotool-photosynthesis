sir.add_reaction_from_args("infection", infection, {"s": -1, "i": 1}, ["beta", "s", "i", "r"])
sir.add_reaction_from_args("recovery", proportional, {"i": -1, "r": 1}, ["gamma", "i"])
