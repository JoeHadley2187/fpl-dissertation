from utils import scoring_rules

class ExpectedMinutes():
    def playerExpectedMinutes(self, player):
        i = 0
        decay = 0.8
        weight_sum = 0
        for k,doc in enumerate(player):
            weight = decay ** k
            weight_sum += weight
            if int(doc['minutes']) == 0:
                continue
            elif int(doc['minutes']) < 50:
                i += scoring_rules.FPL_SCORING.under_sixty_minutes_played * weight
            elif int(doc['minutes']) < 70:
                i += (scoring_rules.FPL_SCORING.under_sixty_minutes_played * 1.5) * weight
            else:
                i += scoring_rules.FPL_SCORING.over_sixty_minutes_played * weight
        return i / weight_sum

