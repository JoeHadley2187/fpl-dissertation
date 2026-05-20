import pandas as pd
from paretoset import paretoset
import plotly.express as px

def all_pareto(manager_team,selected_players,df,xp_only):
    """

    :param manager_team: the managers team who need to be taken out of pareto
    :param selected_players: the players who are selected for transfer
    :param df: the dataframe containing EEO
    :param xp_only: the dataframe that contains all players, used to find positions of players with 0 EEO
    :return: Pareto Optimal solutions through the recurisve algorithm called
    """
    stripped_pareto = pareto_strip(manager_team,selected_players,df,xp_only)
    return recursive_pareto(pd.DataFrame(),stripped_pareto)

def pareto(players):
    """

    :param players: Player to generate Pareto frontier with
    :return: Pareto Set
    """
    mask = paretoset(players[["XP", "EEO"]], sense=["max", "min"])
    px.scatter(players, x="EEO", y="XP",hover_name="web_name",color = mask)
    pareto_players = players[mask]
    return pareto_players
def pareto_graphs(players):
    """

    :param players: Players to generate pareto set mask with
    :return: Mask of Pareto optimal solutions
    """
    mask = paretoset(players[["XP", "EEO"]], sense=["max", "min"])
    return mask

def pareto_strip(manager_team,selected_players,df,xp_only):
    """

    :param manager_team: managers team to be stripped from Pareto
    :param selected_players: selected players, separate from manager team as position constraint needs to be applied
    :param df: EEO dataframe
    :param xp_only: dataframe that contains all players, used to find positions of players with 0 EEO
    :return: Filtered dataframe ready for Pareto optimisation
    """
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


