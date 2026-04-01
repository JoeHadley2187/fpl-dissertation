from utils import scoring_rules

class ExpectedMinutes():
    def playerExpectedMinutes(self, player):
        i = 0
        for doc in player:
            if int(doc['minutes']) == 0:
                continue
            elif int(doc['minutes']) < 50:
                i = i + scoring_rules.FPL_SCORING.under_sixty_minutes_played
            elif int(doc['minutes']) < 70:
                i = i + (scoring_rules.FPL_SCORING.under_sixty_minutes_played * 1.5)
            else:
                i = i + 2
        return i

