from data import fpl_api as api
from data import elite_ownsership
from models import fixture_difficulty
from helper import position_xp_calculator
from config.settings import Settings
from helper.position_dict import position_dict
import pandas as pd



def xp_eo_csv_creator(mongo,gw,decay):
    fpl = api.FplApi()
    eo = elite_ownsership.effective_ownership(fpl, mongo.db["elite_managers"],gw)
    expected_points_rows = []
    for playertocheck in eo:
        player = mongo.db["players"].find_one({"id": playertocheck})
        validation_period = list(
            mongo.db["all_histories"].find({
                "round": {"$lte": gw},
                "element": player["id"]
            }).sort([
                ("round",-1),
                ("kickoff_time",-1)]).limit(Settings.FORM_PERIOD))

        xp = position_xp_calculator.positionXpCalculator(validation_period, player["element_type"],decay)
        adjusted_xp = fixture_difficulty.fixture_difficulty(mongo, player, gw + 1, xp)
        expected_points_rows.append({
            "player_id": player["id"],
            "web_name": player["web_name"],
            "position": position_dict.get(player["element_type"]),
            "XP": adjusted_xp,
            "EEO": eo[playertocheck],
            "Price": player["now_cost"]
        })
    return pd.DataFrame(expected_points_rows)
def xp_csv_creator(mongo,gw,decay):
        expected_points_rows = []
        players = mongo.db["players"].find()
        for player in players:
            validation_period = list(
            mongo.db["all_histories"].find({
                "round": {"$lte": gw},
                "element": player["id"]
            }).sort([
                ("round",-1),
                ("kickoff_time",-1)]).limit(Settings.FORM_PERIOD))
            if len(validation_period) > 0:
                xp = position_xp_calculator.positionXpCalculator(validation_period, player["element_type"],decay)
                adjusted_xp = fixture_difficulty.fixture_difficulty(mongo, player, gw + 1, xp)
                expected_points_rows.append({
                    "player_id": player["id"],
                    "web_name": player["web_name"],
                    "position": position_dict.get(player["element_type"]),
                    "XP": adjusted_xp,
                    "Price": player["now_cost"]})
        return pd.DataFrame(expected_points_rows)