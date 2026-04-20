def calculate_fantasy_points(row):
    pts = row['PTS'] * 1.0
    reb = row['REB'] * 1.25
    ast = row['AST'] * 1.5
    stl = row['STL'] * 2.0
    blk = row['BLK'] * 2.0
    tov = row['TOV'] * -0.5

    stats = [row['PTS'], row['REB'], row['AST'], row['STL'], row['BLK']]
    double_digit = sum(1 for s in stats if s >= 10)
    double_double = 1.5 if double_digit >= 2 else 0
    triple_double = 3.0 if double_digit >= 3 else 0

    return pts + reb + ast + stl + blk + tov + double_double + triple_double