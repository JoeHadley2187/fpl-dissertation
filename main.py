import pymongo

from data import fpl_api as api
from data import fpl_mongo
from data import top_10k_ownership
from models import fixture_difficulty
from helper import position_xp_calculator
from helper.position_dict import position_dict
from optimisation import pareto
import pandas as pd
import plotly.express as px

CURRENT_GAMEWEEK = 31
NEXT_GAMEWEEK = CURRENT_GAMEWEEK + 1
FORM_PERIOD = 4
try:
    expected_points_df = pd.read_csv('expected_points.csv')
except FileNotFoundError:
    fpl = api.FplApi()
    mongo = fpl_mongo.FplMongo("mongodb://localhost:27017/", "fpl_db")
    eo = top_10k_ownership.effective_ownership(fpl, mongo.db["top_10k_managers"], CURRENT_GAMEWEEK)
    print(eo)
    expected_points_rows = []
    for playertocheck in eo:
        player = mongo.db["players"].find_one({"id": playertocheck})
        validation_period = list(
            mongo.db["all_histories"].find({
                "round": {"$gte": CURRENT_GAMEWEEK - FORM_PERIOD, "$lte": CURRENT_GAMEWEEK},
                "element": player["id"]
            }))
        xp = position_xp_calculator.positionXpCalculator(validation_period, player["element_type"])
        adjusted_xp = fixture_difficulty.fixture_difficulty(mongo, player, NEXT_GAMEWEEK, xp)
        expected_points_rows.append({
            "web_name": player["web_name"],
            "position": position_dict.get(player["element_type"]),
            "expected_points": adjusted_xp,
            "effective_ownership": eo[playertocheck]
        })
    expected_points_df = pd.DataFrame(expected_points_rows)
    expected_points_df.sort_values(by="expected_points", ascending=False, inplace=True)
    expected_points_df.to_csv("expected_points.csv", index=False)

def_players = expected_points_df[expected_points_df["position"] == "DEF"]
mid_players = expected_points_df[expected_points_df["position"] == "MID"]
fwd_players = expected_points_df[expected_points_df["position"] == "FWD"]

pareto_mask_def = pareto.pareto(def_players)
pareto_mask_mid = pareto.pareto(mid_players)
pareto_mask_fwd = pareto.pareto(fwd_players)

#eo_fig = px.pie(expected_points_df, values="expected_points", names="web_name")
#eo_fig.show()
def_fig = px.scatter(def_players, x="effective_ownership", y="expected_points",hover_name="web_name",color = pareto_mask_def)
def_fig.show()

mid_fig = px.scatter(mid_players, x="effective_ownership", y="expected_points",hover_name="web_name",color = pareto_mask_mid)
mid_fig.show()

fwd_fig = px.scatter(fwd_players, x="effective_ownership", y="expected_points",hover_name="web_name",color = pareto_mask_fwd)
fwd_fig.show()


