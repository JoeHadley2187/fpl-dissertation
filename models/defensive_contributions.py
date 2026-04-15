from utils import scoring_rules

class DefensiveContributions:
    def playerDefensiveContributions(self, player,position):
        total = 0
        decay = 0.8
        weight_sum = 0
        if position == "GK":
            return total
        #Defenders require only ten defensive contributions compared to 12 for Forwards and Midfielders
        thresholds = (8, 11) if position == "DEF" else (10, 13)
        low, high = thresholds
        for i,doc in enumerate(player):
            weight = decay ** i
            if int(doc["defensive_contribution"]) > high:
                total += scoring_rules.FPL_SCORING.defensive_contributions * weight
            elif int(doc["defensive_contribution"]) > low:
                total += scoring_rules.FPL_SCORING.defensive_contributions * 0.5 * weight
            weight_sum += weight
        return total/weight_sum


                
