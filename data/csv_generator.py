import pandas as pd
from config.settings import Settings
from data import fpl_mongo
from helper.xp_eo_csv_creator import xp_eo_csv_creator
from helper.xp_eo_csv_creator import xp_csv_creator

#This code is used to generate both the xP csv and the EEO csv
#Configure settings first before running this file


mongo = fpl_mongo.FplMongo("mongodb+srv://Joey2187:Man-city4163@fpl-cluster.dnjflbx.mongodb.net/?appName=fpl-cluster", "fpl_db")
xp_eo = xp_eo_csv_creator(mongo, Settings.TARGET_GAMEWEEK - 1, 0.6)
expected_points_df = pd.DataFrame(xp_eo)
expected_points_df.sort_values(by="XP", ascending=False, inplace=True)
expected_points_df.to_csv("expected_points_eo.csv", index=False)

xp = xp_csv_creator(mongo, Settings.TARGET_GAMEWEEK - 1, 0.6)
expected_points_df = pd.DataFrame(xp)
expected_points_df.sort_values(by="XP", ascending=False, inplace=True)
expected_points_df.to_csv("expected_points.csv", index=False)
