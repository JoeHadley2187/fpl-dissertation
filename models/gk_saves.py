from utils import scoring_rules

def gk_saves(validation_period,decay):
    """

    :param validation_period: form period to be observed
    :param decay: the decay rate
    :return: weighted expected points from saves
    """
    saves = 0
    weight_sum = 0
    for i,doc in enumerate(validation_period):
        weight = decay ** i
        saves += doc['saves'] * weight
        weight_sum += weight
    return saves * scoring_rules.FPL_SCORING.goalkeeper_saves * 1/4 / weight_sum