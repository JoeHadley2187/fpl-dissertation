from paretoset import paretoset
def pareto(players):
    mask = paretoset(players[["expected_points", "effective_ownership"]], sense=["max", "min"])
    return mask