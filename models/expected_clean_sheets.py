from utils import scoring_rules
import math


class ExpectedCleanSheets:
    def playerExpectedCleanSheets(self,player,position,decay):
        total = 0.0
        weight_sum = 0
        for i,doc in enumerate(player):
            print(doc)
            weight = decay ** i
            weight_sum += weight
            if doc["minutes"]<60:
                continue
            total += math.exp(-(float(doc["expected_goals_conceded"]))) * scoring_rules.FPL_SCORING.clean_sheet[position] * weight
        return total/weight_sum






