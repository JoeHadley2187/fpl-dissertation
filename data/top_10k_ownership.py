
def effective_ownership(fpl,managers,gw):
    top_10k_effective_ownership = {}
    i =0
    for m in managers.find():
        i += 1
        manager_picks = fpl.get_managers_picks_for_gw(m["entry_id"],gw)
        print(i)
        for player in manager_picks:
            if int(player["multiplier"]) != 0:
                top_10k_effective_ownership[player["element"]] = top_10k_effective_ownership.get(player["element"],0) + int(player["multiplier"])
    top_10k_effective_ownership = dict(
        sorted(
            top_10k_effective_ownership.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )
    return top_10k_effective_ownership

