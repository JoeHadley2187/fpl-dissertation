import pymongo

from data import fpl_mongo
from data import elite_ownsership
from data import fpl_api
from helper.position_dict import position_dict
from helper.xp_eo_csv_creator import xp_eo_csv_creator
from helper import actual_points
from optimisation import pareto
from optimisation import mean_average_error
from config.settings import Settings
import pandas as pd
import plotly.express as px
import streamlit as st


mongo = fpl_mongo.FplMongo("mongodb+srv://Joey2187:Man-city4163@fpl-cluster.dnjflbx.mongodb.net/?appName=fpl-cluster", "fpl_db")
fpl = fpl_api.FplApi()
try:
    expected_points_only_df = pd.read_csv("data/expected_points14.csv")
    expected_points_df = pd.read_csv("data/expected_points_eo14.csv")

except FileNotFoundError:
    print("Generate CSVS first")
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

differntial_picks = expected_points_df[
    (expected_points_df["EEO"] < 20) &
    (expected_points_df["web_name"] != "Henderson")
]


eo_fig = px.pie(expected_points_df.nlargest(10,"EEO"), values="EEO", names="web_name",color_discrete_sequence=px.colors.sequential.Rainbow_r)
eo_fig.update_traces(textinfo='label')
#eo_fig.show()

gk_fig = px.scatter(gk_players, x="EEO", y="XP", hover_name="web_name",color=pareto_mask_gk,color_discrete_map={
        True: "orange",
        False: "blue"
    })
#gk_fig.show()
def_fig = px.scatter(def_players, x="EEO", y="XP",hover_name="web_name",color = pareto_mask_def,color_discrete_map={
        True: "orange",
        False: "blue"
    })
def_fig.update_layout(
    xaxis_title="EEO(%)",
    yaxis_title="XP",
)

#def_fig.show()

mid_fig = px.scatter(mid_players, x="EEO", y="XP",hover_name="web_name",color = pareto_mask_mid,color_discrete_map={
        True: "orange",
        False: "blue"
    })
#mid_fig.show()

fwd_fig = px.scatter(fwd_players, x="EEO", y="XP",hover_name="web_name",color = pareto_mask_fwd,color_discrete_map={
        True: "orange",
        False: "blue"
    })
#fwd_fig.show()
manager_id = st.text_input("Enter manager ID")
gw = st.radio("Select gameweek", [14, 38])
if manager_id and gw:
        expected_points_df = pd.read_csv(f"data/expected_points_eo{gw}.csv")
        expected_points_only_df = pd.read_csv(f"data/expected_points{gw}.csv")
        Settings.TARGET_GAMEWEEK = gw
        manager_team = []
        manager_picks = fpl.get_managers_picks_for_gw(manager_id,Settings.TARGET_GAMEWEEK-1)
        manager_budget = fpl.get_manager_budget_for_gw(manager_id,Settings.TARGET_GAMEWEEK-1)
        st.write(f"Gameweek: {Settings.TARGET_GAMEWEEK}")
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
    st.write("Select gameweek")






















































































