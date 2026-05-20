from helper import xp_eo_csv_creator


def mean_average_error(mongo,gw_start,gw_end,decay):
    """

    :param mongo: Needed to access players actual points that gamweek
    :param gw_start: the first gw to be observed
    :param gw_end: last gw to be observed
    :param decay: the decay rate
    :return: the mean average error across that period of time
    """
    total = 0
    total_players = 0
    for gw in range(gw_start,gw_end+1):
        expected_players = xp_eo_csv_creator.xp_csv_creator(mongo,gw,decay)
        total_players += len(expected_players)
        for index,player in expected_players.iterrows():
            total += expected_actual_difference(player,mongo,gw)
    return total/total_players



def expected_actual_difference(player,mongo,gw):
    player_history = mongo.db["all_histories"].find_one({
        "round": gw,
        "element": int(player["player_id"])
    })
    if player_history  is None or player is None:
        return 3
    difference = abs(player_history["total_points"] - player["XP"])
    return difference


def elite_average_error(mongo,gw_start,gw_end,decay):
    """

    :param mongo: Needed to access players actual points that gameweek
    :param gw_start: the first gw to be observed
    :param gw_end: last gw to be observed
    :param decay: the decay rate
    :return: the mean average error across that period of time only for players who don't have EEO of 0
    """
    total = 0
    total_players = 0
    for gw in range(gw_start, gw_end + 1):
        expected_players = xp_eo_csv_creator.xp_eo_csv_creator(mongo, gw,decay)
        total_players += len(expected_players)
        for index, player in expected_players.iterrows():
            total += expected_actual_difference(player, mongo, gw)
    return total / total_players


