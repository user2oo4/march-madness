# Simulate a game like in notes.txt
from utils import get_team_ratings
from data_loader import fetch_team_stats_for_season, fetch_team_shooting_stats_for_season

class Game:
    def __init__(self, team1, team2, season):
        self.team1 = team1
        self.team2 = team2
        self.season = season
        self.team1_realized_stats = {}
        self.team2_realized_stats = {}
    
    def get_data(self):
        self.team1_stats = fetch_team_stats_for_season(self.team1.name, self.season)
        self.team2_stats = fetch_team_stats_for_season(self.team2.name, self.season)
        self.team1_ratings = get_team_ratings(team_name=self.team1.name, season=self.season)
        self.team2_ratings = get_team_ratings(team_name=self.team2.name, season=self.season)
    
    def calculate_adjustment_factor(self):
        self.team1_realized_stats['adjustment_factor'] = self.team2_ratings['ratings_adjusted']['defensiveRating'] / 100.0
        self.team2_realized_stats['adjustment_factor'] = self.team1_ratings['ratings_adjusted']['defensiveRating'] / 100.0


    
    def calculate_realized_stats(self, adjusted: bool):
        # Team 1
        # posession
        self.team1_realized_stats['possession'] = self.team1_stats['teamStats']['possessions'] / self.team1_stats['teamStats']['games']
        self.team1_realized_stats['possession_time'] = 20 * 60 / self.team1_realized_stats['possession'] # College basketball: full game = 40 minutes
        # ???
        # TOV rate, offensive rebound
        self.team1_realized_stats['tov_rate'] = self.team1_stats['teamStats']['fourFactors']['turnoverRatio']
        self.team1_realized_stats['offensive_rebound_rate'] = self.team1_stats['teamStats']['fourFactors']['offensiveReboundPct']
        # Shot type distribution and percentages
        self.team1_realized_stats['2pt_distribution'] = self.team1_stats['teamStats']['twoPointFieldGoals']['attempted'] / self.team1_stats['teamStats']['fieldGoals']['attempted']
        self.team1_realized_stats['3pt_distribution'] = self.team1_stats['teamStats']['threePointFieldGoals']['attempted'] / self.team1_stats['teamStats']['fieldGoals']['attempted']
        self.team1_realized_stats['ft_distribution'] = self.team1_stats['teamStats']['freeThrows']['attempted'] / self.team1_stats['teamStats']['fieldGoals']['attempted']
        self.team1_realized_stats['2pt_percentage'] = self.team1_stats['teamStats']['twoPointFieldGoals']['pct']
        self.team1_realized_stats['3pt_percentage'] = self.team1_stats['teamStats']['threePointFieldGoals']['pct']
        self.team1_realized_stats['ft_percentage'] = self.team1_stats['teamStats']['freeThrows']['pct']
        # Team 2
        self.team2_realized_stats['possession'] = self.team2_stats['teamStats']['possessions'] / self.team2_stats['teamStats']['games']
        self.team2_realized_stats['possession_time'] = 20 * 60 / self.team2_realized_stats['possession']
        self.team2_realized_stats['tov_rate'] = self.team2_stats['teamStats']['fourFactors']['turnoverRatio']
        self.team2_realized_stats['offensive_rebound_rate'] = self.team2_stats['teamStats']['fourFactors']['offensiveReboundPct']
        self.team2_realized_stats['2pt_distribution'] = self.team2_stats['teamStats']['twoPointFieldGoals']['attempted'] / self.team2_stats['teamStats']['fieldGoals']['attempted']
        self.team2_realized_stats['3pt_distribution'] = self.team2_stats['teamStats']['threePointFieldGoals']['attempted'] / self.team2_stats['teamStats']['fieldGoals']['attempted']
        self.team2_realized_stats['ft_distribution'] = self.team2_stats['teamStats']['freeThrows']['attempted'] / self.team2_stats['teamStats']['fieldGoals']['attempted']
        self.team2_realized_stats['2pt_percentage'] = self.team2_stats['teamStats']['twoPointFieldGoals']['pct']
        self.team2_realized_stats['3pt_percentage'] = self.team2_stats['teamStats']['threePointFieldGoals']['pct']
        self.team2_realized_stats['ft_percentage'] = self.team2_stats['teamStats']['freeThrows']['pct']
        # Adjusted
        if adjusted == True:
            self.team1_realized_stats['2pt_percentage'] *= self.team1_realized_stats['adjustment_factor']
            self.team1_realized_stats['3pt_percentage'] *= self.team1_realized_stats['adjustment_factor']
            self.team1_realized_stats['tov_rate'] *= self.team1_realized_stats['adjustment_factor']
            self.team1_realized_stats['offensive_reound_rate'] *= self.team1_realized_stats['adjustment_factor']
            self.team2_realized_stats['2pt_percentage'] *= self.team2_realized_stats['adjustment_factor']
            self.team2_realized_stats['3pt_percentage'] *= self.team2_realized_stats['adjustment_factor']
            self.team2_realized_stats['tov_rate'] *= self.team2_realized_stats['adjustment_factor']
            self.team2_realized_stats['offensive_reound_rate'] *= self.team2_realized_stats['adjustment_factor']
            
    def simulate_game(self, period_cnt=2, adjusted=False):
        # Calculate all the realized stats
        self.get_data()
        self.calculate_adjustment_factor()
        self.calculate_realized_stats(adjusted)

    def simulate_period(team_start):
        # either half or quarter
        

