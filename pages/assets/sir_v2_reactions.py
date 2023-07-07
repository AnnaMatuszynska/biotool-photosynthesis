sir.add_reaction_from_args("infection", infection, {"S": -1, "I": 1}, ["alpha", "S", "I", "R"])
sir.add_reaction_from_args("recovery", recovery, {"I": -1, "R": 1}, ["beta", "I"])
