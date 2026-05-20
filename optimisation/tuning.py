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

#for d in [i/100 for i in range(5,41,5)]:
    #mae = mean_average_error.elite_average_error(mongo,5,15,d)
    #results.append({"decay": d,
                #"MAE": mae})
#df = pd.DataFrame(results)
#df.to_csv("fpl_results3.csv")

import pandas as pd
import plotly.express as px

df1 = pd.read_csv("fpl_results.csv")
df2 = pd.read_csv("fpl_results2.csv")

df1["source"] = "ALL_MAE"
df2["source"] = "EEO_MAE"

combined = pd.concat([df1, df2])

combined = combined.sort_values("decay")

fig = px.line(
    combined,
    x="decay",
    y="MAE",
    color="source",
    markers=True
)

fig.show()
