from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def train_rf(df):
    features = ["avg_fp_5","avg_fp_10","avg_fp_20",
                "days_rest","travel_distance","is_home"]
    X = df[features].fillna(0)
    y = df["fantasy_points"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    return model, X_test, y_test, preds