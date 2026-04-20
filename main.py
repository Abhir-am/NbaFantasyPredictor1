import matplotlib.pyplot as plt
from db.schema import create_tables
from db.query import get_all_gamelogs
from db.insert import insert_gamelog
from data.fetch_gamelogs import get_all_player_logs, get_player_gamelogs
from data.fantasyPoints import calculate_fantasy_points
from features.build_features import build_features
from models.baseline import baseline_predict
from models.knn import train_knn
from models.random_forest import train_rf
from sklearn.metrics import mean_absolute_error
from nba_api.stats.static import players as nba_players

create_tables()

#fetch and store all players (comment out after first successful run)
df_raw = get_all_player_logs("2023-24")
df_raw["fantasy_points"] = df_raw.apply(calculate_fantasy_points, axis=1)
for _, row in df_raw.iterrows():
    insert_gamelog(row)
print("Data inserted!")

df = get_all_gamelogs()
print("Rows in db:", len(df))

df = build_features(df)
df = df.dropna(subset=["fantasy_points", "avg_fp_5"])

baseline_preds = baseline_predict(df)
knn, scaler, X_test_knn, y_test, knn_preds = train_knn(df)
rf, X_test_rf, y_test_rf, rf_preds = train_rf(df)

print("\n--- Model Performance ---")
print("Baseline MAE:", mean_absolute_error(y_test, baseline_preds[-len(y_test):]))
print("KNN MAE:     ", mean_absolute_error(y_test, knn_preds))
print("RF MAE:      ", mean_absolute_error(y_test, rf_preds))

def search_player():
    name = input("\nEnter player name to search (or 'all' for full chart): ").strip()

    if name.lower() == "all":
        plt.figure(figsize=(12, 5))
        plt.plot(y_test.values[:100], label="Actual")
        plt.plot(knn_preds[:100], label="KNN")
        plt.plot(rf_preds[:100], label="Random Forest")
        plt.plot(baseline_preds[-len(y_test):][:100].values, label="Baseline")
        plt.legend()
        plt.title("All Players — Predicted vs Actual Fantasy Points")
        plt.xlabel("Game")
        plt.ylabel("Fantasy Points")
        plt.tight_layout()
        plt.show()

    else:
        results = nba_players.find_players_by_full_name(name)

        if not results:
            print(f"No player found with name '{name}'")
            search_player()
            return

        if len(results) > 1:
            print("Multiple players found:")
            for i, p in enumerate(results):
                print(f"{i} — {p['full_name']}")
            idx = int(input("Enter number to select: "))
            player = results[idx]
        else:
            player = results[0]

        player_id = player["id"]
        print(f"\nShowing stats for: {player['full_name']} (ID: {player_id})")

        player_df = df[df["player_id"] == player_id].copy()

        if len(player_df) == 0:
            print("No data found for this player in the database")
            search_player()
            return

        actual = player_df["fantasy_points"].values
        baseline = player_df["avg_fp_5"].values

        print(f"Games found:        {len(player_df)}")
        print(f"Avg fantasy points: {actual.mean():.1f}")
        print(f"Max fantasy points: {actual.max():.1f}")
        print(f"Min fantasy points: {actual.min():.1f}")

        plt.figure(figsize=(12, 5))
        plt.plot(actual, label="Actual")
        plt.plot(baseline, label="Baseline (5 game avg)")
        plt.legend()
        plt.title(f"{player['full_name']} — Predicted vs Actual Fantasy Points")
        plt.xlabel("Game")
        plt.ylabel("Fantasy Points")
        plt.tight_layout()
        plt.show()

    again = input("\nSearch another player? (y/n): ")
    if again.lower() == "y":
        search_player()

search_player()