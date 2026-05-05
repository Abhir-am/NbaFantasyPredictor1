from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def train_knn(df):
    features = ["avg_fp_5","avg_fp_10","avg_fp_20",
                "days_rest","travel_distance","is_home"]
    X = df[features].fillna(0)
    y = df["fantasy_points"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )
    scaler = StandardScaler() #SCALES ALL THE DATA - Makes some features irrelevant
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    knn = KNeighborsRegressor(n_neighbors=10)
    knn.fit(X_train, y_train)
    preds = knn.predict(X_test)
    return knn, scaler, X_test, y_test, preds