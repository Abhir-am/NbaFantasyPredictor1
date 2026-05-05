import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from nba_api.stats.static import players as nba_players
from db.schema import create_tables
from db.query import get_all_gamelogs
from db.insert import insert_gamelog
from data.fetch_gamelogs import get_all_player_logs
from data.fantasyPoints import calculate_fantasy_points
from data.context_features import add_context_features
from features.build_features import build_features
from models.knn import train_knn

create_tables()

# CHECK DB FIRST
df_existing = get_all_gamelogs()
if len(df_existing) == 0:
    df_raw = get_all_player_logs("2024-25")
    fp_list = []
    for i in range(len(df_raw)):
        row = df_raw.iloc[i]
        fp = calculate_fantasy_points(row)
        fp_list.append(fp)
    df_raw["fantasy_points"] = fp_list
    processed = []
    for pid in df_raw["Player_ID"].unique():
        temp = df_raw[df_raw["Player_ID"] == pid]
        temp = add_context_features(temp)
        processed.append(temp)
    df_raw = pd.concat(processed, ignore_index=True)
    for i in range(len(df_raw)):
        insert_gamelog(df_raw.iloc[i])
    df = get_all_gamelogs()
else:
    df = df_existing

# BUILD FEATURES (ONLY ONCE) - Or else will duplicate database
df = build_features(df)
df = df[df["fantasy_points"].notna()]
features = ["avg_fp_5","avg_fp_10","avg_fp_20",
            "days_rest","travel_distance","is_home"]
if len(df) == 0:
    print("No data")
    exit()
# TRAIN KNN
knn, scaler, X_test, y_test, preds = train_knn(df)
X_all = df[features].fillna(0)
X_all_scaled = scaler.transform(X_all)
df["knn_pred"] = knn.predict(X_all_scaled)
print("KNN MAE:", mean_absolute_error(y_test, preds))

# SEARCH FUNCTION
def search_player():
    name = input("Player name: ").strip()
    results = nba_players.find_players_by_full_name(name)
    if not results:
        print("No player found")
        return
    player = results[0]
    player_id = player["id"]
    player_name = player["full_name"]
    print("Showing:", player_name)
    player_df = df[df["player_id"] == player_id]
    if len(player_df) == 0:
        print("No data")
        return
    actual = player_df["fantasy_points"].values[:50]
    knn_line = player_df["knn_pred"].values[:50]
    plt.figure(figsize=(12,6))
    plt.plot(knn_line, label="KNN Prediction", linewidth=3)
    plt.plot(actual, label="Actual", linestyle="--")
    plt.title(player_name + " 2024-2025")
    plt.xlabel("Game")
    plt.ylabel("Fantasy Points")
    plt.legend()
    plt.show()


search_player()