from utils import scoring_rules

class DefensiveContributions:
    def playerDefensiveContributions(self, player,position):
        total = 0
        if position == "GK":
            return 0
        #Defenders require only ten defensive contributions compared to 12 for Forwards and Midfielders
        thresholds = (8, 11) if position == "DEF" else (10, 13)
        low, high = thresholds
        for doc in player:
            if int(doc["defensive_contribution"]) > high:
                total += scoring_rules.FPL_SCORING.defensive_contributions
            elif int(doc["defensive_contribution"]) > low:
                total += scoring_rules.FPL_SCORING.defensive_contributions * 0.5
        return total


                
