from utils import scoring_rules

def gk_saves(validation_period):
    saves = 0
    decay = 0.7
    weight_sum = 0
    for i,doc in enumerate(validation_period):
        weight = decay ** i
        saves += doc['saves'] * weight
        weight_sum += weight
    return saves * scoring_rules.FPL_SCORING.goalkeeper_saves * 1/4 / weight_sum