from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1_matches")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2_matches")
    venue = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"{self.team1} vs {self.team2} on {self.date}"

class Prediction(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    predicted_winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='wins')
    predicted_winner_score = models.IntegerField()
    predicted_loser_score = models.IntegerField()
    reasoning = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.predicted_winner} wins"
