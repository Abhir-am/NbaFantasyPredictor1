import pandas as pd

def rolling_avg(series, window):
    result = []
    for i in range(len(series)):
        if i == 0:
            result.append(None)
        elif i < window:
            subset = series.iloc[:i]
            result.append(subset.mean())
        else:
            start = i - window
            end = i
            subset = series.iloc[start:end]
            result.append(subset.mean())
    return pd.Series(result, index=series.index)

def build_features(df):
    df = df.sort_values(["player_id", "game_id"])
    for w in [5, 10, 20]:
        col = "avg_fp_" + str(w)
        df[col] = None
        for pid in df["player_id"].unique():
            mask = df["player_id"] == pid
            vals = df.loc[mask, "fantasy_points"]
            df.loc[mask, col] = rolling_avg(vals, w)

    return df