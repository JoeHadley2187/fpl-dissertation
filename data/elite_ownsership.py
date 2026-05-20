
def effective_ownership(fpl,managers,gw):
    """
    Tallies ownership based on base,captain or triple captain
    :param fpl: Fpl API object
    :param managers: the Elite Managers
    :param gw: the gw being considered
    :return: the EEO of all players featured at least once in an Elite Manager team
    """
    elite_effective_ownership = {}
    for m in managers.find():
        manager_picks = fpl.get_managers_picks_for_gw(m["entry_id"],gw)
        for player in manager_picks:
            #Multiplier 1 = in team 2 = Captain 3 = Triple captain
            if int(player["multiplier"]) != 0:
                elite_effective_ownership[player["element"]] = elite_effective_ownership.get(player["element"],0) + int(player["multiplier"])
    elite_effective_ownership = dict(
        sorted(
            elite_effective_ownership.items(),
            key=lambda x: x[1],
            reverse=True
        )

    )
    #Normalises percentages
    elite_effective_ownership = {
        k: v / 10 for k, v in elite_effective_ownership.items()
    }
    return elite_effective_ownership

