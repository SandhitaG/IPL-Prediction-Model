import requests

def test_full_prediction():
    payload = {
        "team1": "KKR",
        "team2": "CSK",
        "venue": "Eden Garden",
        "venue_team": "KKR",
        "recent_wins": "5",
        "recent_matches": "5"
    }

    response = requests.post("http://127.0.0.1:8000/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_winner" in data
    assert "predicted_winner_score" in data
    assert "reasoning" in data
