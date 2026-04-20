import sqlite3

def create_tables():
    conn = sqlite3.connect("nba_predictor.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY,
            name TEXT,
            team_id INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            game_id TEXT PRIMARY KEY,
            date TEXT,
            home_team_id INTEGER,
            away_team_id INTEGER,
            season INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gamelogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            game_id TEXT,
            team_id INTEGER,
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
            days_rest INTEGER,
            travel_distance REAL,
            opp_def_rating REAL
        )
    """)

    conn.commit()
    conn.close()