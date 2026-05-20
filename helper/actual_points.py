def actual_points(player_id,gw,mongo):
    player_history = mongo.db["all_histories"].find_one({
        "round": gw,
        "element": player_id
    })
    return player_history["total_points"]