# Simulate a game like in notes.txt
from utils import get_team_ratings
from data_loader import fetch_team_stats_for_season, fetch_team_shooting_stats_for_season

class Game:
    def __init__(self, team1, team2, season):
        self.team1 = team1
        self.team2 = team2
        self.season = season

    def simulate(self):
        self.get_data()
    
    def get_data(self):
        team1_stats = fetch_team_stats_for_season(self.team1.name, self.season)
        team2_stats = fetch_team_stats_for_season(self.team2.name, self.season)
        team1_ratings = get_team_ratings(team_name=self.team1.name, season=self.season)
        team2_ratings = get_team_ratings(team_name=self.team2.name, season=self.season)

    
    def calculate_realized_stats(self):
        pass
