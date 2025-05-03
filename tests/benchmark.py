import time
import requests

def benchmark_prediction():
    payload = {
        "team1": "RCB",
        "team2": "MI",
        "venue": "Wankhede",
        "venue_team": "MI",
        "recent_wins": "3",
        "recent_matches": "5"
    }

    start = time.time()
    response = requests.post("http://127.0.0.1:8000/predict", json=payload)
    end = time.time()

    print(f"Response time: {end - start:.3f} seconds")
