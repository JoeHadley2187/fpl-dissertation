from dataclasses import dataclass
@dataclass(frozen=True)

class ScoringRules:
    goal_scored: dict
    clean_sheet: dict
    over_sixty_minutes_played: int
    under_sixty_minutes_played: int
    one_bonus:int
    two_bonus:int
    three_bonus:int
    yellow_card:int
    red_card:int
    defensive_contributions:int
    assists:int
    goalkeeper_saves:int
    own_goal:int
    penalty_saved:int
    penalty_missed:int


FPL_SCORING = ScoringRules(
        goal_scored={
            "FWD": 4,
            "MID": 5,
            "DEF": 6,
            "GK": 10,
        },
        clean_sheet={
            "FWD": 0,
            "MID": 1,
            "DEF": 4,
            "GK": 4,
        },
        over_sixty_minutes_played=2,
        under_sixty_minutes_played=1,
        one_bonus=1,
        two_bonus=2,
        three_bonus=3,
        yellow_card=-1,
        red_card=-3,
        defensive_contributions=2,
        assists=3,
        goalkeeper_saves=1,
        own_goal=-2,
        penalty_saved=5,
        penalty_missed=2)

