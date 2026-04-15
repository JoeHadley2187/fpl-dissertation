from config.settings import Settings
from data import fpl_api as api
from data import fpl_mongo

fpl = api.FplApi()
mongo = fpl_mongo.FplMongo("mongodb://localhost:27017/", "fpl_db")
mongo.db.drop_collection("players")
mongo.db.drop_collection("fixtures")
mongo.db.drop_collection("player-summary")
mongo.db.drop_collection("fixtures-summary")
mongo.db.drop_collection("all_histories")
mongo.db.drop_collection("all_fixtures")
mongo.db.drop_collection("top_10k_managers")
mongo.insert_new_collection("players",fpl.get_players())
mongo.insert_new_collection("fixtures",fpl.get_fixtures())
mongo.db.create_collection("player-summary")
mongo.db.create_collection("all_histories")
mongo.db.create_collection("all_fixtures")
mongo.db.create_collection("elite_managers")

all_histories = []
all_fixtures = []


i = 0
for player in mongo.db["players"].find():
    i+=1
    print(i)
    element_id = player["id"]
    element_summary = fpl.get_player_summary(element_id)

    for match in element_summary.get("history", []):
        all_histories.append(match)

    for fixture in element_summary.get("fixtures", []):
        fixture["element"] = element_id
        all_fixtures.append(fixture)
if all_histories:
    mongo.db["all_histories"].insert_many(all_histories)

if all_fixtures:
    mongo.db["all_fixtures"].insert_many(all_fixtures)
print(mongo.db["all_histories"].count_documents({}))

page_limit =  Settings.ELITE_MANAGERS// 50
for page in range(1, page_limit + 1):
    managers = fpl.get_id_elite_managers(page)
    mongo.db["elite_managers"].insert_many([{"entry_id": m["entry"]} for m in managers])


