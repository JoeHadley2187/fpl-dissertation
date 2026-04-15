from utils import scoring_rules


class ExpectedGoals:
    def playerExpectedGoals(self,player,position):
        i = 0
        j = 0
        decay = 0.8
        weight_sum = 0
        for k ,doc in enumerate(player):
            weight = decay ** k
            i = i + float(doc["expected_goals"]) * scoring_rules.FPL_SCORING.goal_scored[position] * weight
            j = j + float(doc["expected_assists"])* scoring_rules.FPL_SCORING.assists * weight
            weight_sum += weight
        return (i + j)/weight_sum






