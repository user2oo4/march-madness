# Simulate a game like in notes.txt
from utils import get_team_ratings
from data_loader import fetch_team_stats_for_season, fetch_team_shooting_stats_for_season
import random

class Game:
    def __init__(self, team1, team2, season):
        self.teams = [team1, team2]
        self.score = {team1.name: 0, team2.name: 0}
        self.play_by_play = []
        self.season = season
        # Use team name as key for all stats/ratings
        self.stats = {}
        self.ratings = {}
        self.realized_stats = {}

    def get_data(self):
        for team in self.teams:
            self.stats[team.name] = fetch_team_stats_for_season(team.name, self.season)
            self.ratings[team.name] = get_team_ratings(team_name=team.name, season=self.season)

    def calculate_adjustment_factor(self):
        # adjustment factor for each team is based on opponent's defensive rating
        t1, t2 = self.teams[0].name, self.teams[1].name
        self.realized_stats[t1] = {}
        self.realized_stats[t2] = {}
        self.realized_stats[t1]['adjustment_factor'] = self.ratings[t2]['ratings_adjusted']['defensiveRating'] / 100.0
        self.realized_stats[t2]['adjustment_factor'] = self.ratings[t1]['ratings_adjusted']['defensiveRating'] / 100.0

    def calculate_realized_stats(self, adjusted: bool):
        for team, opp in [(self.teams[0], self.teams[1]), (self.teams[1], self.teams[0])]:
            t, o = team.name, opp.name
            stats = self.stats[t]['teamStats']
            realized = self.realized_stats[t]
            realized['possession'] = stats['possessions'] / self.stats[t]['games']
            realized['possession_time'] = 20 * 60 / realized['possession']
            realized['tov_rate'] = stats['fourFactors']['turnoverRatio']
            realized['offensive_rebound_rate'] = stats['fourFactors']['offensiveReboundPct']
            realized['2pt_distribution'] = stats['twoPointFieldGoals']['attempted'] / stats['fieldGoals']['attempted']
            realized['3pt_distribution'] = stats['threePointFieldGoals']['attempted'] / stats['fieldGoals']['attempted']
            realized['ft_distribution'] = stats['freeThrows']['attempted'] / stats['fieldGoals']['attempted']
            realized['2pt_percentage'] = stats['twoPointFieldGoals']['pct']
            realized['3pt_percentage'] = stats['threePointFieldGoals']['pct']
            realized['ft_percentage'] = stats['freeThrows']['pct']
            if adjusted:
                realized['2pt_percentage'] *= realized['adjustment_factor']
                realized['3pt_percentage'] *= realized['adjustment_factor']
                realized['tov_rate'] *= realized['adjustment_factor']
                realized['offensive_rebound_rate'] *= realized['adjustment_factor']

    def simulate_game(self, period_cnt=2, adjusted=False):
        self.get_data()
        self.calculate_adjustment_factor()
        self.calculate_realized_stats(adjusted)
        self.play_by_play.append(f"Start of game: {self.teams[0].name} vs {self.teams[1].name}")
        for period in range(period_cnt):
            self.play_by_play.append(f"Start of period {period + 1}")
            start_team = random.choice(self.teams)
            self.simulate_period(start_team, period_length=20*60)
            start_team = self.teams[1] if start_team == self.teams[0] else self.teams[0]
        print(f"Final Score: {self.teams[0].name} {self.score[self.teams[0].name]} - {self.teams[1].name} {self.score[self.teams[1].name]}")

    def simulate_period(self, team_start, period_length=20*60):
        time_left = period_length
        attack_team = team_start
        while time_left > 0:
            result, possesion_time = self.simulate_play(attack_team, time_left)
            time_left -= possesion_time
            if result == 'turnover':
                attack_team = self.teams[1] if attack_team == self.teams[0] else self.teams[0]
            elif result in ['2pt_made', '3pt_made', 'ft_made']:
                if result == '2pt_made':
                    self.score[attack_team.name] += 2
                elif result == '3pt_made':
                    self.score[attack_team.name] += 3
                elif result == 'ft_made':
                    self.score[attack_team.name] += 1
                attack_team = self.teams[1] if attack_team == self.teams[0] else self.teams[0]
            elif result == 'offensive_rebound':
                continue
            elif result == 'missed':
                attack_team = self.teams[1] if attack_team == self.teams[0] else self.teams[0]
            self.play_by_play.append(f"{attack_team.name} {result} with {time_left:.2f} seconds left in period")

    def simulate_play(self, attack_team, time_left):
        tov_rate = self.realized_stats[attack_team.name]['tov_rate']
        possession_time = self.realized_stats[attack_team.name]['possession_time']
        success_rate_mul = 1.0
        possession_time *= random.uniform(0.8, 1.2)
        if possession_time > time_left:
            success_rate_mul = time_left / possession_time
            tov_rate *= success_rate_mul
            possession_time = time_left
        if random.random() < tov_rate:
            return 'turnover', possession_time
        shot_type = random.choices(['2pt', '3pt', 'ft'], weights=[self.realized_stats[attack_team.name]['2pt_distribution'], self.realized_stats[attack_team.name]['3pt_distribution'], self.realized_stats[attack_team.name]['ft_distribution']])[0]
        success_rate = self.realized_stats[attack_team.name][f'{shot_type}_percentage'] * success_rate_mul
        if random.random() < success_rate:
            return f'{shot_type}_made', possession_time
        else:
            offensive_rebound_rate = self.realized_stats[attack_team.name]['offensive_rebound_rate']
            if random.random() < offensive_rebound_rate:
                return 'offensive_rebound', possession_time
            else:                
                return 'missed', possession_time


