def calculate_fantasy_points(row):
    pts = row['PTS']
    reb = row['REB'] * 1.25
    ast = row['AST'] * 1.5
    stl = row['STL'] * 2
    blk = row['BLK'] * 2
    tov = row['TOV'] * -0.5

    stats = [row['PTS'], row['REB'], row['AST'], row['STL'], row['BLK']]

    dd = 0
    for s in stats:
        if s >= 10:
            dd = dd + 1

    double_double = 1.5 if dd >= 2 else 0
    triple_double = 3 if dd >= 3 else 0

    return pts + reb + ast + stl + blk + tov + double_double + triple_double

# DRAFTKINGS CALCULATIONS