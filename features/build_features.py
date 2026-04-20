import pandas as pd

def rolling_avg(group, window):
    result = []
    for i in range(len(group)):
        if i == 0:
            result.append(None)
        elif i < window:
            result.append(group.iloc[:i].mean())
        else:
            result.append(group.iloc[i-window:i].mean())
    return pd.Series(result, index=group.index)

def build_features(df):
    df = df.sort_values(["player_id", "game_id"])

    for window in [5, 10, 20]:
        col_name = f"avg_fp_{window}"
        df[col_name] = None

        for player_id in df["player_id"].unique():
            player_mask = df["player_id"] == player_id
            player_fp = df.loc[player_mask, "fantasy_points"]
            avg = rolling_avg(player_fp, window)
            df.loc[player_mask, col_name] = avg

    df["days_rest"] = 0

    return df