from utils import scoring_rules

class BonusPoints:
    def bonus_points(self,player):
        total = 0
        decay = 0.7
        weight_sum = 0
        for i,docs in enumerate(player):
            weight = decay ** i
            if docs["bonus"] == "3":
                total += weight * scoring_rules.FPL_SCORING.three_bonus
            elif docs["bonus"] == "2":
                total += weight * scoring_rules.FPL_SCORING.two_bonus
            elif docs["bonus"] == "1":
                total += weight * scoring_rules.FPL_SCORING.one_bonus
            weight_sum += weight
        return total/weight_sum









