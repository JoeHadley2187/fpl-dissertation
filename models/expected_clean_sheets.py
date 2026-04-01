from utils import scoring_rules
import math


class ExpectedCleanSheets:
    def playerExpectedCleanSheets(self,player,position):
        total = 0.0
        for doc in player:
            if doc["minutes"]<60:
                continue
            total += math.exp(-(float(doc["expected_goals_conceded"]))) * scoring_rules.FPL_SCORING.clean_sheet[position]
        return total






