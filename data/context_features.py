import pandas as pd
import math
# USED FOR EXTRA FEAUTRES
# ALL 30 NBA TEAMS COORDINATES
team_coords = {
    "ATL": (33.7490, -84.3880),
    "BOS": (42.3601, -71.0589),
    "BKN": (40.6782, -73.9442),
    "CHA": (35.2271, -80.8431),
    "CHI": (41.8781, -87.6298),
    "CLE": (41.4993, -81.6944),
    "DAL": (32.7767, -96.7970),
    "DEN": (39.7392, -104.9903),
    "DET": (42.3314, -83.0458),
    "GSW": (37.7749, -122.4194),
    "HOU": (29.7604, -95.3698),
    "IND": (39.7684, -86.1581),
    "LAC": (34.0522, -118.2437),
    "LAL": (34.0522, -118.2437),
    "MEM": (35.1495, -90.0490),
    "MIA": (25.7617, -80.1918),
    "MIL": (43.0389, -87.9065),
    "MIN": (44.9778, -93.2650),
    "NOP": (29.9511, -90.0715),
    "NYK": (40.7128, -74.0060),
    "OKC": (35.4676, -97.5164),
    "ORL": (28.5383, -81.3792),
    "PHI": (39.9526, -75.1652),
    "PHX": (33.4484, -112.0740),
    "POR": (45.5152, -122.6784),
    "SAC": (38.5816, -121.4944),
    "SAS": (29.4241, -98.4936),
    "TOR": (43.6532, -79.3832),
    "UTA": (40.7608, -111.8910),
    "WAS": (38.9072, -77.0369)
}

def get_distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111
def add_context_features(df):
    #Date
    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"], format="%b %d, %Y")
    df = df.sort_values("GAME_DATE")

    #Dats of Rest
    days_rest = []
    prev_date = None
    for i in range(len(df)):
        curr_date = df.iloc[i]["GAME_DATE"]
        if prev_date is None:
            days_rest.append(0)
        else:
            diff = (curr_date - prev_date).days
            days_rest.append(diff)
        prev_date = curr_date
    df["days_rest"] = days_rest
    #Home/Away
    is_home = []
    for i in range(len(df)):
        matchup = str(df.iloc[i]["MATCHUP"])
        if "vs." in matchup:
            is_home.append(1)
        else:
            is_home.append(0)
    df["is_home"] = is_home

    #Travel Distance
    travel = []
    prev_team = None
    for i in range(len(df)):
        matchup = str(df.iloc[i]["MATCHUP"])
        parts = matchup.split(" ")
        if "vs." in matchup:
            team = parts[0]      # home team selected
        else:
            team = parts[-1]     # away opponent location selected
        if prev_team is None:
            travel.append(0)
        else:
            if team in team_coords and prev_team in team_coords:
                lat1, lon1 = team_coords[prev_team]
                lat2, lon2 = team_coords[team]
                dist = get_distance(lat1, lon1, lat2, lon2)
                travel.append(dist)
            else:
                travel.append(0)
        prev_team = team

    df["travel_distance"] = travel

    return df