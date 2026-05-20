"""
This model decides which multiplier should be applied to a players xp
taking into account fixture difficulty and how many fixtures a team has in a
gameweek
"""

def fixture_difficulty(mongo,player,gw,xp):
 """
 :param mongo: the mongo db
 :param player: the players whose multiplier is being calculated
 :param gw: the gameweek in which the players next fixture takes place
 :param xp: the xp before multiplier is being applied
 :return: the xp with multipliers applied
 """
 difficulty = 0
 next_fixtures = list(mongo.db["all_fixtures"].find({
    "event":gw,
    "element": player["id"]
    }))
 #checks to see if a game is yet to be played
 if len(next_fixtures) > 0:
     #loops to account fot the potential of double gameweeks
        for f in next_fixtures:
            difficulty += f["difficulty"]
        return xp * len(next_fixtures) * (1.6 - (0.2 * difficulty/len(next_fixtures)))
 else:
        history = list(mongo.db["all_histories"].find({
            "round": gw,
            "element": player["id"]
        }))
        #no fixture = blank gameweek so player gets 0 points automatically
        if len(history) == 0:
            return 0
        fixture_ids = [h["fixture"] for h in history]

        next_fixtures = list(mongo.db["fixtures"].find({
            "id": {"$in": fixture_ids}
        }))
        #loops similar to above and also assigns difficulty separately
        #due to difficulty being stored separately in API for historical fixtures
        for f in next_fixtures:
            if player["team"] == f["team_h"]:
                difficulty += f["team_h_difficulty"]
            else:
                difficulty += f["team_a_difficulty"]
        return xp * len(next_fixtures) * (1.6 - (0.2 * difficulty/len(next_fixtures)))


