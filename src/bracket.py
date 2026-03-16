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
        t1 = self.team1.find_winner() if isinstance(self.team1, Matchup) else self.team1
        t2 = self.team2.find_winner() if isinstance(self.team2, Matchup) else self.team2
        self.game = Game(t1, t2, self.season)
        self.game.simulate_game(period_cnt=2, adjusted=True)
        self.winner = t1 if self.game.score[t1.name] > self.game.score[t2.name] else t2
        return self.winner

def parse_bracket_file(filename, season):
    """
    Parse a bracket file with round names and matchup labels.
    Format:
    - Lines starting with 'Round:' indicate a new round.
    - Lines starting with 'Label:' indicate a matchup label.
    - Each matchup consists of two entries (team name or label reference).
    - Reference previous winners by label (e.g., 'First Four Game 1 Winner').
    Returns the root Matchup and a list of all matchups.
    """
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip() != '']

    matchups = []
    label_to_matchup = {}
    round_name = None
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('Round:'):
            round_name = line[len('Round:'):].strip()
            i += 1
            continue
        label = None
        if line.startswith('Label:'):
            label = line[len('Label:'):].strip()
            i += 1
            line = lines[i]
        entry1 = line
        entry2 = lines[i+1]
        def get_entry(entry):
            if entry.endswith('Winner'):
                ref_label = entry[:-len('Winner')].strip()
                return label_to_matchup[ref_label].find_winner()
            else:
                # Parse team name and seed
                parts = entry.split()
                if len(parts) > 1 and parts[-1].isdigit():
                    seed = int(parts[-1])
                    name = ' '.join(parts[:-1])
                else:
                    seed = None
                    name = entry
                team = Team(name, '', season)
                team.seed = seed
                return team
        team1 = get_entry(entry1)
        team2 = get_entry(entry2)
        matchup = Matchup(team1, team2, season)
        matchup.round_name = round_name
        matchup.label = label
        matchups.append(matchup)
        if label:
            label_to_matchup[label] = matchup
        i += 2

def simulate_bracket_from_file(filename, season=2026, output_file='bracket_results.txt'):
    root, matchups = parse_bracket_file(filename, season)
    winner = root.find_winner()
    results = []
    for idx, matchup in enumerate(matchups):
        def team_str(team):
            if isinstance(team, Team):
                return f"{team.name} ({team.seed})" if getattr(team, 'seed', None) is not None else team.name
            else:
                return f"{team.label} Winner"
        t1 = team_str(matchup.team1)
        t2 = team_str(matchup.team2)
        round_str = f"Round: {matchup.round_name}" if hasattr(matchup, 'round_name') and matchup.round_name else ""
        label_str = f"Label: {matchup.label}" if hasattr(matchup, 'label') and matchup.label else f"Matchup {idx+1}"
        winner_str = team_str(matchup.winner)
        scoreline = f"{round_str} | {label_str}: {t1} vs {t2} | Winner: {winner_str} | Score: {matchup.game.score[matchup.team1.name]} - {matchup.game.score[matchup.team2.name]}"
        pbp = '\n'.join(matchup.game.play_by_play)
        results.extend([scoreline, pbp, ''])
    with open(output_file, 'w') as f:
        f.write(f"Tournament Winner: {winner.name}\n\n")
        for line in results:
            f.write(line + '\n')

# Utility to get all matchups in order (for output)
def _all_matchups(self):
    result = []
    if isinstance(self.team1, Matchup):
        result.extend(self.team1._all_matchups())
    if isinstance(self.team2, Matchup):
        result.extend(self.team2._all_matchups())
    result.append(self)
    return result
Matchup._all_matchups = _all_matchups
        
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