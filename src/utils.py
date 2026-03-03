# Helper methods
import os
import json


DEFAULT_DATA_DIR = 'data'
RATINGS_FILE = {'ratings_adjusted': 'ratings_adjusted.json', 'ratings_srs': 'ratings_srs.json', 'ratings_elo': 'ratings_elo.json'}

# Data reading and processing methods

def get_team_ratings(team_name, season=2026, data_dir=DEFAULT_DATA_DIR):
    """
    Fetch ratings for a specific team and season from local JSON files.
    Returns a dictionary with keys 'srs', 'adjusted', 'elo' and their corresponding ratings.
    """
    ratings = {}
    for key, filename in RATINGS_FILE.items():
        filepath = os.path.join(data_dir, filename)
        if not os.path.exists(filepath):
            print(f"Ratings file {filepath} not found.")
            ratings[key] = None
            continue
        with open(filepath, 'r') as f:
            data = json.load(f)
            team_data = next((item for item in data if item['team'] == team_name and item['season'] == season), None)
            if team_data:
                if key == 'ratings_adjusted':
                    ratings[key] = {
                        'offensiveRating': team_data.get('offensiveRating'),
                        'defensiveRating': team_data.get('defensiveRating'),
                        'netRating': team_data.get('netRating')
                    }
                if key == 'ratings_srs':
                    ratings[key] = team_data.get('rating')
                if key == 'ratings_elo':
                    ratings[key] = team_data.get('elo')
            else:
                print(f"No {key} rating found for {team_name} in season {season}.")
                ratings[key] = None
    return ratings

# Simulation methods
def win_probability(team1, team2, type='elo'):

    print("Calculating win probability using type:", type)

    team1_ratings = get_team_ratings(team1.name, season=team1.season)
    team2_ratings = get_team_ratings(team2.name, season=team2.season)

    if team1_ratings is None or team2_ratings is None:
        print("Missing ratings for one or both teams. Cannot simulate game.")
        return None
    rating1 = team1_ratings.get(f"ratings_{type}")
    rating2 = team2_ratings.get(f"ratings_{type}")
    if rating1 is None or rating2 is None:
        print(f"Missing {type} rating for one or both teams. Cannot simulate game.")
        return None

    if type == 'elo':
        team1_elo = rating1 if isinstance(rating1, (int, float)) else rating1.get("elo", 0)
        team2_elo = rating2 if isinstance(rating2, (int, float)) else rating2.get("elo", 0)
        if team1_elo == 0 or team2_elo == 0:
            print("Elo rating missing for one or both teams. Cannot simulate game.")
            return None
        prob_team1_wins = 1 / (1 + 10 ** ((team2_elo - team1_elo) / 400))

    elif type == 'adjusted':
        team1_offense = rating1.get("offensiveRating", 0)
        team2_offense = rating2.get("offensiveRating", 0)
        team1_defense = rating1.get("defensiveRating", 0)
        team2_defense = rating2.get("defensiveRating", 0)
        if team1_offense == 0 or team2_offense == 0 or team1_defense == 0 or team2_defense == 0:
            print("Adjusted ratings missing for one or both teams. Cannot simulate game.")
            return None
        team1_score = team1_offense / 100 * team2_defense / 100
        team2_score = team2_offense / 100 * team1_defense / 100
        # using normal distribution to convert score difference to win probability
        std_dev = 15
        score_diff = team1_score - team2_score
        print(f"Score difference: {score_diff:.2f}")
        # generate distribution of score differences based on normal distribution with jump of 1/15 (since std_dev is 15)
        distribution = [score_diff + (i - 7) * std_dev / 15 for i in range(15)]
        # calculate win probability as the proportion of distribution where team1_score > team2_score
        prob_team1_wins = sum(1 for x in distribution if x > 0) / len(distribution)
        # import math
        # import random
        # std_dev = 10
        # team1_score += random.gauss(-std_dev, std_dev)
        # team2_score += random.gauss(-std_dev, std_dev)
        # prob_team1_wins = 1 / (1 + math.exp(team2_score - team1_score))

    elif type == 'srs':
        team1_srs = rating1 if isinstance(rating1, (int, float)) else rating1.get("rating", 0)
        team2_srs = rating2 if isinstance(rating2, (int, float)) else rating2.get("rating", 0)
        if team1_srs == 0 or team2_srs == 0:
            print("SRS rating missing for one or both teams. Cannot simulate game.")
            return None
        prob_team1_wins = 1 / (1 + 10 ** ((team2_srs - team1_srs) / 400))

    print(f"Win probability for {team1.name} vs {team2.name} using {type}: {prob_team1_wins:.2f}")
    return prob_team1_wins

def simulate_game(team1, team2, win_prob_function):
    win_prob = win_prob_function(team1, team2)
    if win_prob is None:
        print("Cannot simulate game due to missing ratings.")
        return None
    
    import random
    outcome = random.choices([team1.name, team2.name], weights=[win_prob, 1 - win_prob])[0]
    print(f"Simulated game result: {team1.name} vs {team2.name}: {outcome} wins (win probability: {win_prob:.2f})")
    return outcome
    
    