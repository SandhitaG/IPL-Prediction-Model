# ml_model/predict.py

import joblib
import numpy as np

# Load models
clf = joblib.load("ml_model/match_winner_model.pkl")
reg_win = joblib.load("ml_model/winner_score_model.pkl")
reg_lose = joblib.load("ml_model/loser_score_model.pkl")

def predict_outcome(input_features):
    # input_features should be a DataFrame with same columns used during training
    winner = clf.predict(input_features)[0]
    win_score = reg_win.predict(input_features)[0]
    lose_score = reg_lose.predict(input_features)[0]
    
    return {
        "predicted_winner": winner,
        "predicted_winner_score": int(win_score),
        "predicted_loser_score": int(lose_score)
    }
