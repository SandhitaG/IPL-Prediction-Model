import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import GradientBoostingClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder

# Load dataset
data = pd.read_csv("ipl_dataset.csv")

# Feature Engineering + Label Encoding
def preprocess_data(df):
    df['recent_win_ratio'] = df['recent_wins'] / df['recent_matches']
    df['home_advantage'] = (df['venue_team'] == df['team1']).astype(int)

    # Encode categorical columns
    le_dict = {}
    for col in ['team1', 'team2', 'venue', 'venue_team', 'match_winner']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_dict[col] = le
        joblib.dump(le, f"label_encoder_{col}.pkl")  # Save encoder for future use

    return df, le_dict

# Preprocess
data, le_dict = preprocess_data(data)

# Targets
target_class = 'match_winner'
target_reg_win = 'winner_score'
target_reg_lose = 'loser_score'

# Features and labels
X = data.drop([target_class, target_reg_win, target_reg_lose], axis=1)
y_class = data[target_class]
y_win = data[target_reg_win]
y_lose = data[target_reg_lose]

# Split all targets together
X_train, X_test, y_class_train, y_class_test, y_win_train, y_win_test, y_lose_train, y_lose_test = train_test_split(
    X, y_class, y_win, y_lose, test_size=0.2, random_state=42
)

# Train models
clf = GradientBoostingClassifier().fit(X_train, y_class_train)
reg_win = RandomForestRegressor().fit(X_train, y_win_train)
reg_lose = RandomForestRegressor().fit(X_train, y_lose_train)

# Evaluation
print("🎯 Classification Accuracy:", accuracy_score(y_class_test, clf.predict(X_test)))
print("📈 Winner Score RMSE:", np.sqrt(mean_squared_error(y_win_test, reg_win.predict(X_test))))
print("📉 Loser Score RMSE:", np.sqrt(mean_squared_error(y_lose_test, reg_lose.predict(X_test))))

# Save models
joblib.dump(clf, "match_winner_model.pkl")
joblib.dump(reg_win, "winner_score_model.pkl")
joblib.dump(reg_lose, "loser_score_model.pkl")

print("✅ Models and encoders saved successfully.")
