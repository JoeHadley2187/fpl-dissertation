def actual_points(player_id,gw,mongo):
    """

    :param player_id: The player
    :param gw: The gameweek to check
    :param mongo: Where the history is stored
    :return: the total points a player got in that gameweek
    """
    player_history = mongo.db["all_histories"].find_one({
        "round": gw,
        "element": player_id
    })
    return player_history["total_points"]