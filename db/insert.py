import sqlite3

def insert_gamelog(row):
    conn = sqlite3.connect("nba_predictor.db")
    cursor = conn.cursor()

    if "vs." in str(row["MATCHUP"]):
        is_home = 1
    else:
        is_home = 0
    cursor.execute("""
        INSERT OR IGNORE INTO gamelogs (
            player_id, game_id, is_home,
            points, rebounds, assists, steals, blocks,
            turnovers, minutes, fg_pct, fantasy_points,
            days_rest, travel_distance
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["Player_ID"],
        row["Game_ID"],
        is_home,
        row["PTS"],
        row["REB"],
        row["AST"],
        row["STL"],
        row["BLK"],
        row["TOV"],
        row["MIN"],
        row["FG_PCT"],
        row["fantasy_points"],
        0,
        0
    ))

    conn.commit()
    conn.close()