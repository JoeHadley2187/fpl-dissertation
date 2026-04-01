import models
from models.defensive_contributions import DefensiveContributions
from models.expected_clean_sheets import ExpectedCleanSheets
from models.expected_goals import ExpectedGoals
from models.expected_minutes import ExpectedMinutes
from models.gk_saves import gk_saves
from helper.position_dict import position_dict

def positionXpCalculator(validation_period,position):
    expected_minutes = ExpectedMinutes()
    expected_goals = ExpectedGoals()
    expected_defensive_contributions = DefensiveContributions()
    expected_clean_sheets = ExpectedCleanSheets()
    pos = position_dict.get(position)

    xp = expected_minutes.playerExpectedMinutes(validation_period)
    xp += expected_goals.playerExpectedGoals(validation_period,pos)
    xp += expected_defensive_contributions.playerDefensiveContributions(validation_period,pos)
    if pos != "FWD":
        xp += expected_clean_sheets.playerExpectedCleanSheets(validation_period,pos)
    if pos != "GK":
        xp += expected_goals.playerExpectedGoals(validation_period,pos)
    if pos == "GK":
        xp += gk_saves(validation_period)
    return xp/5
