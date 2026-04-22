import pandas as pd
from paretoset import paretoset

def all_pareto(selected_players,df):
    stripped_pareto = pareto_strip(selected_players,df)
    return recursive_pareto(pd.DataFrame(),stripped_pareto)

def pareto(players):
    mask = paretoset(players[["expected_points", "effective_ownership"]], sense=["max", "min"])
    pareto_players = players[mask]
    return pareto_players


def pareto_strip(selected_players,df):
    selected_ids = selected_players["player_id"]
    selected_positions = set(
        df.loc[df["player_id"].isin(selected_ids),"position"]
    )
    print(selected_positions)

    filtered_df = df[df["position"].isin(selected_positions) & (~df["player_id"].isin(selected_ids))]
    xp_filtered_df = filtered_df[filtered_df["expected_points"] >= filtered_df["expected_points"].quantile(0.5)]
    return xp_filtered_df

def recursive_pareto(pareto_players,players):
    if len(pareto_players) >= 8:
        return pareto_players
    current_pareto_layer = pareto(players)
    pareto_players = pd.concat([pareto_players, current_pareto_layer])
    filtered_players = players[~players["player_id"].isin(current_pareto_layer["player_id"])]
    return recursive_pareto(pareto_players,filtered_players)


