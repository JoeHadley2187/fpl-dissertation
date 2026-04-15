
def effective_ownership(fpl,managers,gw):
    elite_effective_ownership = {}
    i =0
    for m in managers.find():
        i += 1
        manager_picks = fpl.get_managers_picks_for_gw(m["entry_id"],gw)
        print(i)
        for player in manager_picks:
            if int(player["multiplier"]) != 0:
                elite_effective_ownership[player["element"]] = elite_effective_ownership.get(player["element"],0) + int(player["multiplier"])
    elite_effective_ownership = dict(
        sorted(
            elite_effective_ownership.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )
    return elite_effective_ownership

