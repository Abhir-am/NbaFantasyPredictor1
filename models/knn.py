from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def train_knn(df):
    features = ["avg_fp_5", "avg_fp_10", "avg_fp_20",
                "days_rest", "travel_distance", "opp_def_rating", "is_home"]

    X = df[features].fillna(0)
    y = df["fantasy_points"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Find best k
    best_k, best_mae = 5, float("inf")
    for k in [5, 10, 15, 20, 25]:
        knn = KNeighborsRegressor(n_neighbors=k)
        knn.fit(X_train, y_train)
        mae = mean_absolute_error(y_test, knn.predict(X_test))
        print(f"k={k}, MAE: {mae:.2f}")
        if mae < best_mae:
            best_k, best_mae = k, mae

    # Train final model with best k
    knn = KNeighborsRegressor(n_neighbors=best_k)
    knn.fit(X_train, y_train)
    preds = knn.predict(X_test)

    print(f"Best KNN k={best_k}, MAE: {best_mae:.2f}")
    return knn, scaler, X_test, y_test, preds