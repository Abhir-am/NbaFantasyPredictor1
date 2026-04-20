import sqlite3

def insert_gamelog(row):
    conn = sqlite3.connect("nba_predictor.db")
    cursor = conn.cursor()

    # Determine home/away from MATCHUP column (e.g. "LAL vs. GSW" = home, "LAL @ GSW" = away)
    is_home = 1 if "vs." in str(row["MATCHUP"]) else 0

    cursor.execute("""
        INSERT OR IGNORE INTO gamelogs (
            player_id, game_id, team_id, is_home,
            points, rebounds, assists, steals, blocks,
            turnovers, minutes, fg_pct, fantasy_points,
            days_rest, travel_distance, opp_def_rating
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["Player_ID"], row["Game_ID"], 0, is_home,
        row["PTS"], row["REB"], row["AST"], row["STL"], row["BLK"],
        row["TOV"], row["MIN"], row["FG_PCT"], row["fantasy_points"],
        0, 0, 0
    ))

    conn.commit()
    conn.close()