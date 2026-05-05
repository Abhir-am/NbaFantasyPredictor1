import sqlite3

def create_tables():
    conn = sqlite3.connect("nba_predictor.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS gamelogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            game_id TEXT,
            is_home INTEGER,
            points INTEGER,
            rebounds INTEGER,
            assists INTEGER,
            steals INTEGER,
            blocks INTEGER,
            turnovers INTEGER,
            minutes REAL,
            fg_pct REAL,
            fantasy_points REAL,
            days_rest REAL,
            travel_distance REAL,
            UNIQUE(player_id, game_id)
        )
    """)

    conn.commit()
    conn.close()