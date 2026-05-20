from utils import scoring_rules


class ExpectedGoals:
    def playerExpectedGoals(self,player,position,decay):
        """

        :param player: The form period to be observed
        :param position: the players position as goal points vary on position
        :param decay: The decay rate
        :return: Combined expected points from goals and assists
        """
        i = 0
        j = 0
        weight_sum = 0
        for k ,doc in enumerate(player):
            weight = decay ** k
            i = i + float(doc["expected_goals"]) * scoring_rules.FPL_SCORING.goal_scored[position] * weight
            j = j + float(doc["expected_assists"])* scoring_rules.FPL_SCORING.assists * weight
            weight_sum += weight
        return (i + j)/weight_sum






