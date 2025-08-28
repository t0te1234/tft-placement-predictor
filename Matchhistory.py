from riotwatcher import LolWatcher, RiotWatcher, ApiError, TftWatcher
import pandas as pd

api_key = 'api-key'
riot_watcher = RiotWatcher(api_key)
watcher = TftWatcher(api_key)
region = 'americas'
region2 = 'na1'
summoner_name = 't0te1234'
tagline = 'NA1'
data = []
df = pd.read_csv("players.csv")
players = df.to_dict(orient="records")
count = 0
for player in players:
    summoner_name = player['name']
    tagline = player['tag']
    account = riot_watcher.account.by_riot_id(region, summoner_name, tagline)
    me = watcher.summoner.by_puuid(region2, account['puuid'])
    matches_ids = watcher.match.by_puuid(region, account['puuid'], count=1)
    matches = [watcher.match.by_id(region, item) for item in matches_ids]
    
    for match in matches:
        participants = match["info"]["participants"]
        for player in participants:
            filtered_player = {
                "level": player.get("level"),
                "placement": player.get("placement"),
                "traits": player.get("traits", []),
                "units": player.get("units", []),
            }
            data.append(filtered_player)
    count += 1
    print(count)
        

df1 = pd.DataFrame(data)
df1.to_csv("data.csv", index=False)

