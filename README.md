# NBA Fantasy Basketball Performance Predictor

A machine learning project that predicts NBA fantasy basketball performance using historical NBA statistics, contextual game information, and regression models such as K Nearest Neighbors and Random Forest Regression. The project uses publicly available NBA data and generates visualizations comparing actual and predicted fantasy point performance.

<img width="1307" height="721" alt="image" src="https://github.com/user-attachments/assets/86b68ffd-30ed-4cb4-b99b-26d231c3f913" />


## How It's Made:

Tech used: Python, pandas, SQLite, Matplotlib, nba_api

The goal of this project was to build a fantasy basketball prediction system that could go beyond simple season averages and include contextual features that may affect NBA player performance. The project uses the `nba_api` Python library to collect public NBA game log data from the 2024–2025 NBA season. This data includes player statistics such as points, rebounds, assists, steals, blocks, turnovers, minutes played, and matchup information for each game.

After collecting the data, I cleaned and processed the dataset by removing irrelevant columns, formatting dates consistently, and handling missing values with rolling averages. Additional contextual features such as days of rest, home versus away games, and estimated travel distance between consecutive games were engineered from the raw data. Fantasy basketball scoring was then calculated using standard DraftKings fantasy scoring rules.

The processed data was stored in a SQLite database to avoid repeated API calls and improve efficiency during development. From there, I trained and compared multiple machine learning models. I first implemented a K Nearest Neighbors regression model because it was simple and effective at finding patterns among players with similar recent performances. Later, I implemented a Random Forest Regression model because it could better capture nonlinear relationships between player statistics and contextual features.

To evaluate the models, I used Mean Absolute Error (MAE) and generated visualizations comparing actual fantasy basketball points against model predictions. The project also includes a player search function that allows users to generate prediction graphs for any NBA player.

## Optimizations

During development, several optimizations and fixes were implemented to improve the project’s stability and performance. One issue encountered was duplicate database entries when repeatedly fetching NBA game logs. This was solved by checking whether a player’s game already existed in the database before inserting it again.

Another optimization involved limiting repeated API calls by storing processed game logs locally in SQLite. This significantly reduced loading times after the first run of the program. I also implemented a delay between API requests to prevent rate limiting from the NBA statistics servers.

The KNN model required feature scaling because it relied on distance calculations between data points. Without scaling, larger numerical features such as travel distance could overpower smaller contextual features such as days of rest. Random Forest Regression did not require scaling because it naturally determines feature importance through decision tree splitting.

## Lessons Learned:

This project helped me better understand the full machine learning workflow, including data collection, cleaning, feature engineering, database management, model training, evaluation, and visualization. One of the biggest lessons I learned was that adding more complex contextual features does not always dramatically improve prediction accuracy. Although the Random Forest model performed slightly better than KNN, the improvement was relatively small because recent player performance averages were already extremely strong predictors.

I also learned how important proper preprocessing and database management are in real world machine learning projects. Small issues such as duplicate database entries or inconsistent column formatting created major debugging challenges during development. Through solving these problems, I became much more comfortable working with pandas, SQLite, and machine learning pipelines in Python.

Future improvements for this project could include adding injury reports, opponent defensive ratings, player usage rates, and live game updates to improve prediction accuracy even further.


