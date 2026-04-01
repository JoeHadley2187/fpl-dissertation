from utils import scoring_rules

def gk_saves(validation_period):
    saves = 0
    for doc in validation_period:
        saves += doc['saves']
    return saves * scoring_rules.FPL_SCORING.goalkeeper_saves * 1/4