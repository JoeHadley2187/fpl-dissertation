import pymongo

from data import fpl_mongo
from data import fpl_api
from helper.position_dict import position_dict
from optimisation import pareto
from config.settings import Settings
import pandas as pd
import plotly.express as px
import streamlit as st



"""
This file controls the main flow of the program
it initially sets up quantiles for xP interpolation
before presenting a streamlit application which allows users
to view their own teams and view recommended changes 
"""
mongo = fpl_mongo.FplMongo("mongodb+srv://Joey2187:XXXXXXX@fpl-cluster.dnjflbx.mongodb.net/?appName=fpl-cluster", "fpl_db")
fpl = fpl_api.FplApi()
try:
    expected_points_only_df = pd.read_csv("data/expected_points.csv")
    expected_points_df = pd.read_csv("data/expected_points_eo.csv")

except FileNotFoundError:
    print("Generate CSVS first")

#This section sets up the inetrpolation for how strong players are compared to other
#in their relative position
gk_players = expected_points_df[expected_points_df["position"] == "GK"]
gk_quantiles = gk_players["XP"].quantile([0.25,0.5])
def_players = expected_points_df[expected_points_df["position"] == "DEF"]
def_quantiles = def_players["XP"].quantile([0.25,0.5])
mid_players = expected_points_df[expected_points_df["position"] == "MID"]
mid_quantiles = mid_players["XP"].quantile([0.25,0.5])
fwd_players = expected_points_df[expected_points_df["position"] == "FWD"]
fwd_quantiles = fwd_players["XP"].quantile([0.25,0.5])
pareto_mask_gk = pareto.pareto_graphs(gk_players)
pareto_mask_def = pareto.pareto_graphs(def_players)
pareto_mask_mid = pareto.pareto_graphs(mid_players)
pareto_mask_fwd = pareto.pareto_graphs(fwd_players)
quantile_dict = {
    "GK": gk_quantiles,
    "DEF": def_quantiles,
    "MID": mid_quantiles,
    "FWD": fwd_quantiles,
}
low_eo,mid_eo = expected_points_df["EEO"].quantile([0.25,0.75])

#Start of main User Interface
manager_id = st.text_input("Enter manager ID")
if manager_id :
        expected_points_df = pd.read_csv(f"data/expected_points_eo{Settings.TARGET_GAMEWEEK}.csv")
        expected_points_only_df = pd.read_csv(f"data/expected_points{Settings.TARGET_GAMEWEEK}.csv")
        manager_team = []
        manager_picks = fpl.get_managers_picks_for_gw(manager_id,Settings.TARGET_GAMEWEEK-1)
        manager_budget = fpl.get_manager_budget_for_gw(manager_id,Settings.TARGET_GAMEWEEK-1)
        st.write(f"Gameweek: {Settings.TARGET_GAMEWEEK}")
        #Displays manager picks to main screen
        for pick in manager_picks:
            xp_player = expected_points_only_df[expected_points_only_df["player_id"] == pick["element"]]
            if xp_player.empty:
                xp = 0
            else:
                xp = xp_player["XP"].iloc[0]
            strength = "Strong"
            player = mongo.db["players"].find_one({"id": pick["element"]})
            red, yellow = quantile_dict.get(position_dict.get(pick["element_type"]))
            if xp <= red:
                strength = "Weak"
            elif xp <= yellow:
                strength = "Average"
            manager_team.append({"Name": player["web_name"],
                             "player_id": player["id"],
                             "XP": xp,
                             "Strength": strength,
                             "Price":player["now_cost"],
                             })
        manager_team_df = pd.DataFrame(manager_team)
        manager_team_df["Select"] = False
        manager_team_df["Price"] = manager_team_df["Price"] / 10
        edited_df = st.data_editor(
            manager_team_df,
            column_config={
                "player_id": None,
                "Price": st.column_config.NumberColumn(
                "Price",
                format="£%.1f",
                ),
                "XP": st.column_config.NumberColumn(
                    "XP",
                        format="%.2f"
                )


            }
        )
        if "Select" in edited_df.columns:
            selected = edited_df[edited_df["Select"]]
        else:
            selected = pd.DataFrame()
        #If transfer is selected open sidebar and provide transfer recomendations
        if not selected.empty:
            with st.sidebar:
                ignore_budget = st.checkbox("Ignore budget?",False)
                if ignore_budget:
                    pareto_df = pareto.all_pareto(manager_team_df,selected,expected_points_df,expected_points_only_df)
                else:
                    available_budget = ((selected["Price"].sum() * 10) + manager_budget)/10
                    st.write(f" Available budget : ${available_budget}")
                    pareto_df = pareto.all_pareto(manager_team_df,selected,expected_points_df[(expected_points_df["Price"]/10)<=available_budget],expected_points_only_df)
                pareto_df["Select"] = False
                pareto_df["Price"] = pareto_df["Price"]/10
                differential_eo_pareto = pareto_df[pareto_df["EEO"] < 2]
                balanced_eo_pareto = pareto_df[(pareto_df["EEO"] >= 2) & (pareto_df["EEO"] < 10)]
                safe_eo_pareto = pareto_df[pareto_df["EEO"] >= 10]
                st.subheader("Safe")
                safe_eo_pareto = st.data_editor(
                    safe_eo_pareto,
                    key="safe_eo_pareto",
                    column_config={
                    "player_id": None,
                    "Price": st.column_config.NumberColumn(
                        "Price",
                        format="£%.1f",
                    ),
                    "XP": st.column_config.NumberColumn(
                        "XP",
                        format="%.2f"
                    )
                }

            )
                st.subheader("Balanced")
                balanced_eo_pareto = st.data_editor(
                    balanced_eo_pareto,
                    key="balanced_eo_pareto",
                    column_config={
                    "player_id": None,
                    "Price": st.column_config.NumberColumn(
                        "Price",
                        format="£%.1f",
                    ),
                    "XP": st.column_config.NumberColumn(
                        "XP",
                        format="%.2f"
                    )
                }
            )
                st.subheader("Differential")
                differential_eo_pareto = st.data_editor(
                    differential_eo_pareto,
                    key = "differential_eo_pareto",
                    column_config={
                    "player_id": None,
                    "Price": st.column_config.NumberColumn(
                        "Price",
                        format="£%.1f",
                    ),
                    "XP": st.column_config.NumberColumn(
                        "XP",
                        format="%.2f"
                    )
                }
            )
                differential_selected = differential_eo_pareto[differential_eo_pareto["Select"]]
                balanced_selected = balanced_eo_pareto[balanced_eo_pareto["Select"]]
                safe_selected = safe_eo_pareto[safe_eo_pareto["Select"]]

                all_targets = pd.concat(
                [differential_selected, balanced_selected, safe_selected],
                ignore_index=True
                )
                target_xp = all_targets["XP"].sum()
                selected_xp = selected["XP"].sum()
                if len(all_targets) != len(selected):
                    st.write(f" You need to pick {len(selected)} replacements")
                else:
                    if (ignore_budget==False ) and ( available_budget - all_targets["Price"].sum() < 0):
                        st.write(f" You have overspent by { available_budget - all_targets['Price'].sum()}")
                    else:
                        st.write(f"XP gain = {target_xp - selected_xp:.2f}")



else:
    #Wait until manager_id is selected
    st.write("Enter manager_id")






















































































