def main():

    from classes import Team
    from game import Game

    t1 = Team("Duke", "ACC", 2026)
    t2 = Team("Georgia", "SEC", 2026)

    # Check if data is available for both teams before simulating
    from data_loader import fetch_team_stats_for_season
    t1_stats = fetch_team_stats_for_season(t1.name, t1.season)
    t2_stats = fetch_team_stats_for_season(t2.name, t2.season)
    print(f"Fetched stats for {t1.name}: {'Success' if t1_stats else 'Failed'}")
    print(f"Fetched stats for {t2.name}: {'Success' if t2_stats else 'Failed'}")
    if t1_stats is None or t2_stats is None:
        print(f"Error: Could not fetch stats for one or both teams.\nDuke stats: {t1_stats is not None}\nGeorgia stats: {t2_stats is not None}")
        print("Check your API key, BASE_URL, and that the API is returning valid data.")
        return

    game = Game(t1, t2, 2026)
    game.simulate_game(period_cnt=2, adjusted=True)

    final_score = f"Final Score: {t1.name} {game.score[t1.name]} - {t2.name} {game.score[t2.name]}"
    print(final_score)
    # print("\nPlay by Play Log:")
    # for log in game.play_by_play:
    #     print(log)

    # Write results and play by play to a file
    with open("game_result.txt", "w") as f:
        f.write(final_score + "\n\n")
        f.write("Play by Play Log:\n")
        for log in game.play_by_play:
            f.write(log + "\n")

if __name__ == "__main__":
    main()