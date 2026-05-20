import models
from models.defensive_contributions import DefensiveContributions
from models.expected_clean_sheets import ExpectedCleanSheets
from models.expected_goals import ExpectedGoals
from models.expected_minutes import ExpectedMinutes
from models.gk_saves import gk_saves
from models.bonus_points import BonusPoints
from helper.position_dict import position_dict



def positionXpCalculator(validation_period,position,decay):
    """

    :param validation_period: The period of form to be analysed
    :param position: The players position
    :param decay: the decay rate for weighted gameweeks
    :return: a players expected points ready for fixture multiplier
    """
    expected_minutes = ExpectedMinutes()
    expected_goals = ExpectedGoals()
    expected_defensive_contributions = DefensiveContributions()
    expected_clean_sheets = ExpectedCleanSheets()
    expected_bonus_points = BonusPoints()
    pos = position_dict.get(position)
    xp = expected_minutes.playerExpectedMinutes(validation_period,decay)
    xp += expected_goals.playerExpectedGoals(validation_period,pos,decay)
    xp += expected_defensive_contributions.playerDefensiveContributions(validation_period,pos,decay)
    xp += expected_bonus_points.bonus_points(validation_period,decay)
    if pos != "FWD":
        xp += expected_clean_sheets.playerExpectedCleanSheets(validation_period,pos,decay)
    if pos == "GK":
        xp += gk_saves(validation_period,decay)
    return xp
