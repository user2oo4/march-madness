from utils import get_team_ratings, win_probability, simulate_game
from classes import Team, Player, Game

def main():
    t1 = Team("Duke", "ACC", 2026)
    t2 = Team("Georgia", "SEC", 2026)

    team1_ratings = get_team_ratings(team_name=t1.name, season=t1.season)
    team2_ratings = get_team_ratings(team_name=t2.name, season=t2.season)
    print(f"{t1.name} Ratings: {team1_ratings}")
    print(f"{t2.name} Ratings: {team2_ratings}")

    print("\nSimulating with Elo:")
    simulate_game(t1, t2, lambda t1, t2: win_probability(t1, t2, type='elo'))

    print("\nSimulating with Adjusted:")
    simulate_game(t1, t2, lambda t1, t2: win_probability(t1, t2, type='adjusted'))

    print("\nSimulating with SRS:")
    simulate_game(t1, t2, lambda t1, t2: win_probability(t1, t2, type='srs'))

if __name__ == "__main__":
    main()