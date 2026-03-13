# Bracket simulation logic will go here
from game import Game
from classes import Team

class Matchup:
    def __init__(self, team1, team2, season):
        self.team1 = team1
        self.team2 = team2
        self.season = season
        self.winner = None
    
    def find_winner(self):
        self.team1 = self.team1.find_winner() if isinstance(self.team1, Matchup) else self.team1
        self.team2 = self.team2.find_winner() if isinstance(self.team2, Matchup) else self.team2
        game = Game(self.team1, self.team2, self.season)
        game.simulate_game(period_cnt=2, adjusted=True)
        self.winner = self.team1 if game.score[self.team1.name] > game.score[self.team2.name] else self.team2
        return self.winner
        
class Bracket:
    def __init__(self, season):
        self.season = season
        self.matchups = []
    
    def add_matchup(self):
        current_n = len(self.matchups)
        print("Enter matchup details for game", current_n + 1)
        print(f"Enter team 1 details (either a number from 1 to {current_n} to select a previous matchup winner, or team name, conference, and season")
        # input here
        line = input()
        space_count = line.count(" ")
        if space_count == 0:
            team1 = self.matchups[int(line) - 1].find_winner()
        elif space_count >= 2:
            # team name can have spaces
            parts = line.split(" ")            
            name = " ".join(parts[:-2])
            conference = parts[-2]
            season = parts[-1]
            team1 = Team(name, conference, int(season))
        else:
            print("Invalid input format for team 1. Please try again.")
            return
        print(f"Enter team 2 details (either a number from 1 to {current_n} to select a previous matchup winner, or team name, conference, and season")
        line = input()
        space_count = line.count(" ")
        if space_count == 0:
            team2 = self.matchups[int(line) - 1].find_winner()
        elif space_count >= 2:
            parts = line.split(" ")            
            name = " ".join(parts[:-2])
            conference = parts[-2]
            season = parts[-1]
            team2 = Team(name, conference, int(season))
        else:
            print("Invalid input format for team 2. Please try again.")
            return
        matchup = Matchup(team1, team2, self.season)
        self.matchups.append(matchup)
    
    def enter_bracket(self):
        while True:
            print("Enter 'done' when finished entering matchups, or press Enter to add another matchup")
            line = input()
            if line.lower() == 'done':
                break
            self.add_matchup()
    
    def simulate_bracket(self):
        if not self.matchups:
            print("No matchups entered. Please enter matchups before simulating the bracket.")
            return
        final_matchup = self.matchups[-1]
        winner = final_matchup.find_winner()
        print("Winner of the bracket:", winner.name)
        print("Detailed bracket:")
        self.print_finished_bracket()
    
    def print_finished_bracket(self):
        # This method can be implemented to print the entire bracket with winners of each matchup after simulation
        for i, matchup in enumerate(self.matchups):
            team1_name = matchup.team1.name if isinstance(matchup.team1, Team) else f"Winner of Matchup {self.matchups.index(matchup.team1) + 1}"
            team2_name = matchup.team2.name if isinstance(matchup.team2, Team) else f"Winner of Matchup {self.matchups.index(matchup.team2) + 1}"
            winner_name = matchup.winner.name if matchup.winner else "TBD"
            print(f"Matchup {i + 1}: {team1_name} vs {team2_name} - Winner: {winner_name}")
        
        print("Final Winner:", self.matchups[-1].winner.name if self.matchups[-1].winner else "TBD")

def main():
    bracket = Bracket(season=2026)
    bracket.enter_bracket()
    bracket.simulate_bracket()

if __name__ == "__main__":
    main()