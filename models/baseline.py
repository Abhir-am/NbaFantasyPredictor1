from sklearn.metrics import mean_absolute_error

def baseline_predict(df):
    preds = df["avg_fp_5"]
    actual = df["fantasy_points"]
    print("Baseline MAE:", mean_absolute_error(actual, preds))
    return preds