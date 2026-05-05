import sqlite3
import pandas as pd

def get_all_gamelogs():
    conn = sqlite3.connect("nba_predictor.db")
    df = pd.read_sql("SELECT * FROM gamelogs", conn)
    conn.close()
    return df