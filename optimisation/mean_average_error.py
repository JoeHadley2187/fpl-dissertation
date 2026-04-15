from helper import xp_eo_csv_creator


def mean_average_error(mongo,gw_start,gw_end):
    total = 0
    total_players = 0
    for gw in range(gw_start,gw_end+1):
        expected_players = xp_eo_csv_creator.xp_csv_creator(mongo,gw)
        total_players += len(expected_players)
        for index,player in expected_players.iterrows():
            total += expected_actual_difference(player,mongo,gw)
    return total/total_players



def expected_actual_difference(player,mongo,gw):
    print(player)
    player_history = mongo.db["all_histories"].find_one({
        "round": gw,
        "element": int(player["player_id"])
    })
    difference = abs(player_history["total_points"] - player["expected_points"])
    return difference





