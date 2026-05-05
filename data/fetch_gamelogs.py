import pandas as pd
import time
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players

def get_player_gamelogs(player_id, season="2024-25"):
    log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
    df = log.get_data_frames()[0]
    time.sleep(0.6)  # avoid rate limiting
    return df
def get_all_player_logs(season="2024-25"):
    all_players = players.get_active_players()
    all_logs = []
    for i, player in enumerate(all_players):
        #Fetch every player
        print(i+1, "/", len(all_players), "-", player["full_name"])
        try:
            df = get_player_gamelogs(player["id"], season)
            df["player_id"] = player["id"]
            df["player_name"] = player["full_name"]
            all_logs.append(df)
        except:
            continue
    return pd.concat(all_logs, ignore_index=True)