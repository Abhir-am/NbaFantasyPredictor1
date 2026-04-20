from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas as pd
import time

def get_player_gamelogs(player_id, season="2023-24"):
    log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season=season
    )
    df = log.get_data_frames()[0]
    time.sleep(0.6)
    return df

def get_all_player_logs(season="2023-24"):
    all_players = players.get_active_players()
    all_logs = []

    for player in all_players:
        try:
            df = get_player_gamelogs(player["id"], season)
            df["player_id"] = player["id"]
            df["player_name"] = player["full_name"]
            all_logs.append(df)
            print(f"Fetched: {player['full_name']}")
        except Exception as e:
            print(f"Failed: {player['full_name']} — {e}")

    return pd.concat(all_logs, ignore_index=True)