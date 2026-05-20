import pandas as pd
from paretoset import paretoset
import plotly.express as px

def all_pareto(manager_team,selected_players,df,xp_only):
    stripped_pareto = pareto_strip(manager_team,selected_players,df,xp_only)
    return recursive_pareto(pd.DataFrame(),stripped_pareto)

def pareto(players):
    mask = paretoset(players[["XP", "EEO"]], sense=["max", "min"])
    px.scatter(players, x="EEO", y="XP",hover_name="web_name",color = mask)
    pareto_players = players[mask]
    return pareto_players
def pareto_graphs(players):
    mask = paretoset(players[["XP", "EEO"]], sense=["max", "min"])
    return mask

def pareto_strip(manager_team,selected_players,df,xp_only):
    selected_ids = selected_players["player_id"]
    manager_ids = manager_team["player_id"]
    selected_positions = set(
        xp_only.loc[xp_only["player_id"].isin(selected_ids),"position"]
    )
    print(selected_positions)

    filtered_df = df[df["position"].isin(selected_positions) & (~df["player_id"].isin(manager_ids))]
    xp_filtered_df = filtered_df[filtered_df["XP"] >= filtered_df["XP"].quantile(0.5)]
    return xp_filtered_df






def recursive_pareto(pareto_players,players,stack_depth=0):
    """
    :param pareto_players: The list of Pareto optimal players - initially empty.
    :param players: the players used to generate a Pareto Frontier
    :param stack_depth: the depth of recursion
    :return: pareto_players
    """
    if len(pareto_players) >= 10 or stack_depth >3 :
        return pareto_players
    #pareto_fig.show()
    current_pareto_layer = pareto(players)
    pareto_players = pd.concat([pareto_players, current_pareto_layer])
    #Remove players so duplicates do not occur
    filtered_players = players[~players["player_id"].isin(current_pareto_layer["player_id"])]
    return recursive_pareto(pareto_players,filtered_players,stack_depth=stack_depth+1)


