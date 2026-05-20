import numpy as np

import mean_average_error
import plotly.express as px
from data import fpl_mongo
import pandas as pd
mongo = fpl_mongo.FplMongo("mongodb+srv://Joey2187:Man-city4163@fpl-cluster.dnjflbx.mongodb.net/?appName=fpl-cluster", "fpl_db")
results = []
#for d in [i/100 for i in range(40,91,5)]:
 #   mae = mean_average_error.mean_average_error(mongo,5,15,d)
#results.append({"decay": d,
  #                 "MAE": mae})
#df = pd.DataFrame(results)
#df.to_csv("fpl_results.csv")

#for i in range(25,35,1):
 #   mae = mean_average_error.mean_average_error(mongo,i,i,0.4)
  #  results.append({"gw":i,
   #             "MAE": mae})
#df = pd.DataFrame(results)
#df.to_csv("fpl_results4.csv")

