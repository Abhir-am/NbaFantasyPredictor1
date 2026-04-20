from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def train_rf(df):
    features = ["avg_fp_5", "avg_fp_10", "avg_fp_20",
                "days_rest", "travel_distance", "opp_def_rating", "is_home"]

    X = df[features].fillna(0)
    y = df["fantasy_points"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)
    preds = rf.predict(X_test)

    print("Random Forest MAE:", mean_absolute_error(y_test, preds))
    return rf, X_test, y_test, preds