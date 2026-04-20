import sqlite3
import pandas as pd

def get_all_gamelogs():
    conn = sqlite3.connect("nba_predictor.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM gamelogs")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    conn.close()
    return pd.DataFrame(rows, columns=columns)