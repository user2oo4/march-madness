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
        self.game_stats = {} # Simulated stats at the end of the game (2pts, 3pts, ft, tovs, rebounds)

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
        self.game_stats[t1] = {'2pt_made': 0, '3pt_made': 0, 'ft_made': 0, 'tov': 0, 'offensive_rebound': 0, '2pt_attempted': 0, '3pt_attempted': 0, 'ft_attempted': 0, 'off_rebounds': 0, 'def_rebounds': 0}
        self.game_stats[t2] = {'2pt_made': 0, '3pt_made': 0, 'ft_made': 0, 'tov': 0, 'offensive_rebound': 0, '2pt_attempted': 0, '3pt_attempted': 0, 'ft_attempted': 0, 'off_rebounds': 0, 'def_rebounds': 0}

    def calculate_realized_stats(self, adjusted: bool):
        for team, opp in [(self.teams[0], self.teams[1]), (self.teams[1], self.teams[0])]:
            t, o = team.name, opp.name
            stats = self.stats[t]['teamStats']
            realized = self.realized_stats[t]
            realized['possession'] = stats['possessions'] / self.stats[t]['games']
            realized['possession_time'] = 20 * 60 / realized['possession']
            realized['tov_rate'] = stats['fourFactors']['turnoverRatio']
            realized['offensive_rebound_rate'] = stats['fourFactors']['offensiveReboundPct']
            realized['ft_rate'] = stats['fourFactors']['freeThrowRate']
            realized['2pt_distribution'] = stats['twoPointFieldGoals']['attempted'] / stats['fieldGoals']['attempted']
            realized['3pt_distribution'] = stats['threePointFieldGoals']['attempted'] / stats['fieldGoals']['attempted']
            realized['2pt_percentage'] = stats['twoPointFieldGoals']['pct']
            realized['3pt_percentage'] = stats['threePointFieldGoals']['pct']
            realized['ft_percentage'] = stats['freeThrows']['pct']
            if adjusted:
                realized['2pt_percentage'] *= realized['adjustment_factor']
                realized['3pt_percentage'] *= realized['adjustment_factor']
                realized['tov_rate'] *= realized['adjustment_factor']
                realized['offensive_rebound_rate'] *= realized['adjustment_factor']
                realized['ft_rate'] *= realized['adjustment_factor']

    def simulate_game(self, period_cnt=2, adjusted=False):
        self.get_data()
        self.calculate_adjustment_factor()
        self.calculate_realized_stats(adjusted)
        print("Realized stats for simulation:")
        for team in self.teams:
            print(f"{team.name}: {self.realized_stats[team.name]}")
        self.play_by_play.append(f"Start of game: {self.teams[0].name} vs {self.teams[1].name}")
        for period in range(period_cnt):
            self.play_by_play.append(f"Start of period {period + 1}")
            start_team = random.choice(self.teams)
            self.simulate_period(start_team, period_length=20*60)
            start_team = self.teams[1] if start_team == self.teams[0] else self.teams[0]
        while self.score[self.teams[0].name] == self.score[self.teams[1].name]:
            self.play_by_play.append("Start of overtime")
            self.simulate_period(start_team, period_length=5*60)
        self.play_by_play.append("End of game")
        print(f"Final Score: {self.teams[0].name} {self.score[self.teams[0].name]} - {self.teams[1].name} {self.score[self.teams[1].name]}")

    def simulate_period(self, team_start, period_length=20*60):
        time_left = period_length
        attack_team = team_start
        while time_left > 0:
            self.play_by_play.append(f"\nCurrent attacking team: {attack_team.name}, time left in period: {time_left:.2f} seconds")
            current_attacking_team = attack_team.name
            result, possesion_time = self.simulate_play(attack_team, time_left)
            time_left -= possesion_time
            if result == 'turnover':
                self.game_stats[attack_team.name]['tov'] += 1
                attack_team = self.teams[1] if attack_team == self.teams[0] else self.teams[0]
            elif result in ['2pt_made', '3pt_made']:
                points = 2 if result == '2pt_made' else 3
                self.score[attack_team.name] += points
                self.game_stats[attack_team.name][f'{result[0]}pt_made'] += 1
                attack_team = self.teams[1] if attack_team == self.teams[0] else self.teams[0]
            elif result.endswith('ft_made'):
                ft_made = int(result.split()[0])
                self.score[attack_team.name] += ft_made
                self.game_stats[attack_team.name]['ft_made'] += ft_made
                attack_team = self.teams[1] if attack_team == self.teams[0] else self.teams[0]
            elif result == 'offensive_rebound':
                self.game_stats[attack_team.name]['off_rebounds'] += 1
            elif result == 'missed':
                attack_team = self.teams[1] if attack_team == self.teams[0] else self.teams[0]
                self.game_stats[attack_team.name]['def_rebounds'] += 1
            self.play_by_play.append(f"{current_attacking_team} {result} with {time_left:.2f} seconds left in period")
            self.play_by_play.append(f"Current score: {self.teams[0].name} {self.score[self.teams[0].name]} - {self.teams[1].name} {self.score[self.teams[1].name]}")

    def simulate_play(self, attack_team, time_left):
        print("attacking team", attack_team.name)
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
        shot_type = random.choices(['2pt', '3pt'], weights=[self.realized_stats[attack_team.name]['2pt_distribution'], self.realized_stats[attack_team.name]['3pt_distribution']])[0]
        print("shot_type", shot_type)
        success_rate = self.realized_stats[attack_team.name][f'{shot_type}_percentage'] * success_rate_mul
        fouled_rate = self.realized_stats[attack_team.name]['ft_rate'] * (1.0/2) * self.realized_stats[attack_team.name]['2pt_distribution'] + self.realized_stats[attack_team.name]['ft_rate'] * (1.0/3) * self.realized_stats[attack_team.name]['3pt_distribution']
        print("fouled_rate", fouled_rate)
        print("success_rate", success_rate)
        if random.random() * 100 < fouled_rate:
            print("Fouled!")
            success_rate = self.realized_stats[attack_team.name]['ft_percentage']
            if shot_type == '2pt':
                # shoot 2 free throws
                ft_made = sum(random.random() * 100 < success_rate for _ in range(2))
                self.game_stats[attack_team.name]['ft_attempted'] += 2
                return f"{ft_made} ft_made", possession_time
            elif shot_type == '3pt':
                # shoot 3 free throws
                ft_made = sum(random.random() * 100 < success_rate for _ in range(3))
                self.game_stats[attack_team.name]['ft_attempted'] += 3
                return f"{ft_made} ft_made", possession_time
        # Not account for and-1 situations
        elif random.random() * 100 < success_rate:
            print(f"{shot_type} shot made!")
            self.game_stats[attack_team.name][f'{shot_type}_attempted'] += 1
            return f'{shot_type}_made', possession_time
        else:
            print(f"{shot_type} shot missed.")
            offensive_rebound_rate = self.realized_stats[attack_team.name]['offensive_rebound_rate']
            self.game_stats[attack_team.name][f'{shot_type}_attempted'] += 1
            print("offensive_rebound_rate", offensive_rebound_rate)
            if random.random() * 100 < offensive_rebound_rate:
                return 'offensive_rebound', possession_time
            else:
                return 'missed', possession_time


