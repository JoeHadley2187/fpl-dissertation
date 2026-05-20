from utils import scoring_rules
import math


class ExpectedCleanSheets:
    def playerExpectedCleanSheets(self,player,position,decay):
        """

        :param player: The player being assessed
        :param position: Players position influences how many points a clean sheet earns them
        :param decay: Weighted decay value
        :return: The weighted xP value for expected clean sheets
        """
        total = 0.0
        weight_sum = 0
        for i,doc in enumerate(player):
            print(doc)
            weight = decay ** i
            weight_sum += weight
            if doc["minutes"]<60:
                continue
                #Poisson modelling is use to simulate chance of team keeping clean sheet
            total += (math.exp(-(float(doc["expected_goals_conceded"])))
                      * scoring_rules.FPL_SCORING.clean_sheet[position] * weight)
        return total/weight_sum






