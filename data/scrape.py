import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_team_def_ratings(season_year="2024"):
    url = f"https://www.basketball-reference.com/leagues/NBA_{season_year}.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    table = soup.find("table", {"id": "misc_stats"})
    df = pd.read_html(str(table))[0]
    return df[["Team", "DRtg"]]