import pymongo

from data import fpl_mongo
from data import elite_ownsership
from data import fpl_api
from models import fixture_difficulty
from helper import position_xp_calculator
from helper.position_dict import position_dict
from helper.xp_eo_csv_creator import xp_eo_csv_creator
from optimisation import pareto
from optimisation import mean_average_error
from config.settings import Settings
import pandas as pd
import plotly.express as px
import streamlit as st


mongo = fpl_mongo.FplMongo("mongodb://localhost:27017/", "fpl_db")
fpl = fpl_api.FplApi()
if not Settings.USE_XP_CSV:
    xp = xp_eo_csv_creator(mongo,Settings.CURRENT_GAMEWEEK)
    expected_points_df = pd.DataFrame(xp)
    expected_points_df.sort_values(by="expected_points", ascending=False, inplace=True)
    expected_points_df.to_csv("expected_points.csv", index=False)
try:
    expected_points_df = pd.read_csv('expected_points.csv')
except FileNotFoundError:
    print("Expected points file not found.")
gk_players = expected_points_df[expected_points_df["position"] == "GK"]
gk_quantiles = gk_players["expected_points"].quantile([0.25,0.5])
def_players = expected_points_df[expected_points_df["position"] == "DEF"]
def_quantiles = def_players["expected_points"].quantile([0.25,0.5])
mid_players = expected_points_df[expected_points_df["position"] == "MID"]
mid_quantiles = mid_players["expected_points"].quantile([0.25,0.5])
fwd_players = expected_points_df[expected_points_df["position"] == "FWD"]
fwd_quantiles = fwd_players["expected_points"].quantile([0.25,0.5])
pareto_mask_gk = pareto.pareto(gk_players)
pareto_mask_def = pareto.pareto(def_players)
pareto_mask_mid = pareto.pareto(mid_players)
pareto_mask_fwd = pareto.pareto(fwd_players)
quantile_dict = {
    "GK": gk_quantiles,
    "DEF": def_quantiles,
    "MID": mid_quantiles,
    "FWD": fwd_quantiles,
}



#eo_fig = px.pie(expected_points_df, values="expected_points", names="web_name")
#eo_fig.show()

# gk_fig = px.scatter(gk_players, x="effective_ownership", y="expected_points", hover_name="web_name",color=pareto_mask_gk)
# gk_fig.show()
#
# def_fig = px.scatter(def_players, x="effective_ownership", y="expected_points",hover_name="web_name",color = pareto_mask_def)
# def_fig.show()
#
# mid_fig = px.scatter(mid_players, x="effective_ownership", y="expected_points",hover_name="web_name",color = pareto_mask_mid)
# mid_fig.show()
#
# fwd_fig = px.scatter(fwd_players, x="effective_ownership", y="expected_points",hover_name="web_name",color = pareto_mask_fwd)
# fwd_fig.show()

manager_id = st.text_input("Please enter your manager ID")
if manager_id:
    manager_team = []
    manager_picks = fpl.get_managers_picks_for_gw(manager_id,Settings.CURRENT_GAMEWEEK)
    st.write(f"Gameweek: {Settings.CURRENT_GAMEWEEK}")
    for pick in manager_picks:
        xp_player = expected_points_df[expected_points_df["player_id"] == pick["element"]]
        if xp_player.empty:
            xp = 0
        else:
            xp = xp_player["expected_points"].iloc[0]
        strength = "strong"
        player = mongo.db["players"].find_one({"id": pick["element"]})
        red, yellow = quantile_dict.get(position_dict.get(pick["element_type"]))
        if xp < red:
            strength = "weak"
        elif xp < yellow:
            strength = "medium"
        manager_team.append({"Name": player["web_name"],
                             "XP": xp,
                             "Strength": strength,
                             })
    manager_team_df = pd.DataFrame(manager_team)
    manager_team_df["Select"] = False
    edited_df = st.data_editor(manager_team_df)
    if "Select" in edited_df.columns:
        selected = edited_df[edited_df["Select"]]
    else:
        selected = pd.DataFrame()

    if not selected.empty:
        with st.sidebar:
            st.write(selected.iloc[0]["Name"])


else:
    st.write("Please enter your manager ID")




















































































