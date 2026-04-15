from data import fpl_api as api
from data import elite_ownsership
from models import fixture_difficulty
from helper import position_xp_calculator
from config.settings import Settings
from helper.position_dict import position_dict
import pandas as pd



def xp_eo_csv_creator(mongo,gw):
    fpl = api.FplApi()
    eo = elite_ownsership.effective_ownership(fpl, mongo.db["elite_managers"],gw)
    expected_points_rows = []
    for playertocheck in eo:
        player = mongo.db["players"].find_one({"id": playertocheck})
        validation_period = list(
            mongo.db["all_histories"].find({
                "round": {"$gte": gw - Settings.FORM_PERIOD, "$lte": gw},
                "element": player["id"]
            }).sort("round",-1))
        xp = position_xp_calculator.positionXpCalculator(validation_period, player["element_type"])
        adjusted_xp = fixture_difficulty.fixture_difficulty(mongo, player, gw + 1, xp)
        expected_points_rows.append({
            "player_id": player["id"],
            "web_name": player["web_name"],
            "position": position_dict.get(player["element_type"]),
            "expected_points": adjusted_xp,
            "effective_ownership": eo[playertocheck]
        })
    return pd.DataFrame(expected_points_rows)
def xp_csv_creator(mongo,gw):
        expected_points_rows = []
        players = mongo.db["players"].find()
        for player in players:
            print(player["web_name"])
            print("wooooo")
            validation_period = list(
                mongo.db["all_histories"].find({
                    "round": {"$gte": gw - Settings.FORM_PERIOD, "$lte": gw},
                    "element": player["id"]
                }).sort("round",-1))
            if len(validation_period) > 0:
                xp = position_xp_calculator.positionXpCalculator(validation_period, player["element_type"])
                adjusted_xp = fixture_difficulty.fixture_difficulty(mongo, player, gw + 1, xp)
                expected_points_rows.append({
                    "player_id": player["id"],
                    "web_name": player["web_name"],
                    "position": position_dict.get(player["element_type"]),
                    "expected_points": adjusted_xp})
        return pd.DataFrame(expected_points_rows)