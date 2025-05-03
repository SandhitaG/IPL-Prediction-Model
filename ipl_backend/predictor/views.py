from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Team, Player, Match, Prediction
from .serializers import TeamSerializer, PlayerSerializer, MatchSerializer, PredictionSerializer
import pandas as pd
import joblib
from ollama_llm.reasoning import get_prediction_reasoning
clf = joblib.load("ml_model/match_winner_model.pkl")
reg_win = joblib.load("ml_model/winner_score_model.pkl")
reg_lose = joblib.load("ml_model/loser_score_model.pkl")
le_team1 = joblib.load("ml_model/label_encoder_team1.pkl")
le_team2 = joblib.load("ml_model/label_encoder_team2.pkl")
le_venue = joblib.load("ml_model/label_encoder_venue.pkl")
le_venue_team = joblib.load("ml_model/label_encoder_venue_team.pkl")
le_winner = joblib.load("ml_model/label_encoder_match_winner.pkl")

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer

    def create(self, request, *args, **kwargs):
        match_id = request.data.get("match")
        try:
            match = Match.objects.get(id=match_id)
        except Match.DoesNotExist:
            return Response({"error": "Match not found"}, status=404)

        team1 = match.team1.name
        team2 = match.team2.name
        venue = match.venue
        venue_team = match.team1.name  
        recent_wins = 4
        recent_matches = 5
        win_ratio = recent_wins / recent_matches
        home_adv = int(team1 == venue_team)

        team1_enc = le_team1.transform([team1])[0]
        team2_enc = le_team2.transform([team2])[0]
        venue_enc = le_venue.transform([venue])[0]
        venue_team_enc = le_venue_team.transform([venue_team])[0]

        features = pd.DataFrame([{
            "team1": team1_enc,
            "team2": team2_enc,
            "venue": venue_enc,
            "venue_team": venue_team_enc,
            "recent_wins": recent_wins,
            "recent_matches": recent_matches,
            "recent_win_ratio": win_ratio,
            "home_advantage": home_adv
        }])

        features = features[clf.feature_names_in_]

        winner_encoded = clf.predict(features)[0]
        winner = le_winner.inverse_transform([winner_encoded])[0]
        win_score = int(reg_win.predict(features[reg_win.feature_names_in_])[0])
        lose_score = int(reg_lose.predict(features[reg_lose.feature_names_in_])[0])

        try:
            reasoning = get_prediction_reasoning({
                "winner": winner,
                "winner_score": win_score,
                "loser_score": lose_score
            }, {
                "team1": team1,
                "team2": team2,
                "venue": venue,
                "venue_team": venue_team,
                "recent_wins": recent_wins,
                "recent_matches": recent_matches
            })
        except:
            reasoning = "LLM reasoning unavailable."

        predicted_winner_team = Team.objects.get(name=winner)
        prediction = Prediction.objects.create(
            match=match,
            predicted_winner=predicted_winner_team,
            predicted_winner_score=win_score,
            predicted_loser_score=lose_score,
            reasoning=reasoning
        )

        serializer = PredictionSerializer(prediction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
