
def fixture_difficulty(mongo,player,gw,xp):
    next_fixture = mongo.db["all_fixtures"].find_one({
        "event": gw,
        "element": player["id"]
    })
    if next_fixture is None:
        history = mongo.db["all_histories"].find_one({
            "round": gw,
            "element": player["id"]
        })
        if history is None:
            return 0
        next_fixture = mongo.db["fixtures"].find_one({
            "id": history["fixture"],
        })
        if player["team"] == next_fixture["team_h"]:
            difficulty = next_fixture["team_h_difficulty"]
        else:
            difficulty = next_fixture["team_a_difficulty"]
    else:
        difficulty = next_fixture["difficulty"]
    return xp * (1.6 - (0.2 * difficulty))


