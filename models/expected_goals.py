from utils import scoring_rules


class ExpectedGoals:
    def playerExpectedGoals(self,player,position):
        i = 0
        j = 0
        for doc in player:
            i = i + float(doc["expected_goals"]) * scoring_rules.FPL_SCORING.goal_scored[position]
            j = j + float(doc["expected_assists"])* scoring_rules.FPL_SCORING.assists
        return i + j






