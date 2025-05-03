from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MatchData(BaseModel):
    team1: str
    team2: str
    venue: str
    venue_team: str
    recent_wins: int
    recent_matches: int

@app.post("/predict")
async def predict(data: MatchData) -> Dict[str, str | int]:
    win_ratio = data.recent_wins / data.recent_matches if data.recent_matches > 0 else 0
    predicted_winner = data.team1 if win_ratio > 0.5 else data.team2

    return {
        "predicted_winner": predicted_winner,
        "predicted_winner_score": 180 if predicted_winner == data.team1 else 165,
        "predicted_loser_score": 160 if predicted_winner == data.team1 else 150,
        "reasoning": f"{predicted_winner} has a better recent performance based on win ratio of {win_ratio:.2f}."
    }
