def main():

    from classes import Team
    from game import Game

    t1 = Team("Ole Miss", "SEC", 2026)
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

    t1_wins = 0
    t2_wins = 0
    for iter in range(100):
        print(iter)
        game = Game(t1, t2, 2026)
        game.simulate_game(period_cnt=2, adjusted=True)
        final_score = f"Final Score: {t1.name} {game.score[t1.name]} - {t2.name} {game.score[t2.name]}"
        raw_game_stats = game.game_stats
        # print(raw_game_stats)
        game_stats = f"""
Game Stats:
2-pt: {t1.name} {game.game_stats[t1.name]['2pt_made']}/{game.game_stats[t1.name]['2pt_attempted']} ({game.game_stats[t1.name]['2pt_made'] / game.game_stats[t1.name]['2pt_attempted']:.1%}) | {t2.name} {game.game_stats[t2.name]['2pt_made']}/{game.game_stats[t2.name]['2pt_attempted']} ({game.game_stats[t2.name]['2pt_made'] / game.game_stats[t2.name]['2pt_attempted']:.1%})
3-pt: {t1.name} {game.game_stats[t1.name]['3pt_made']}/{game.game_stats[t1.name]['3pt_attempted']} ({game.game_stats[t1.name]['3pt_made'] / game.game_stats[t1.name]['3pt_attempted']:.1%}) | {t2.name} {game.game_stats[t2.name]['3pt_made']}/{game.game_stats[t2.name]['3pt_attempted']} ({game.game_stats[t2.name]['3pt_made'] / game.game_stats[t2.name]['3pt_attempted']:.1%})
ft: {t1.name} {game.game_stats[t1.name]['ft_made']}/{game.game_stats[t1.name]['ft_attempted']} ({game.game_stats[t1.name]['ft_made'] / game.game_stats[t1.name]['ft_attempted']:.1%}) | {t2.name} {game.game_stats[t2.name]['ft_made']}/{game.game_stats[t2.name]['ft_attempted']} ({game.game_stats[t2.name]['ft_made'] / game.game_stats[t2.name]['ft_attempted']:.1%})
turnovers: {t1.name} {game.game_stats[t1.name]['tov']} | {t2.name} {game.game_stats[t2.name]['tov']}
offensive rebounds: {t1.name} {game.game_stats[t1.name]['off_rebounds']} | {t2.name} {game.game_stats[t2.name]['off_rebounds']}
defensive rebounds: {t1.name} {game.game_stats[t1.name]['def_rebounds']} | {t2.name} {game.game_stats[t2.name]['def_rebounds']}
        """
        # print(game_stats)
        print(final_score)
        # print(game_stats)
        if game.score[t1.name] > game.score[t2.name]:
            # print(f"{t1.name} wins!")
            t1_wins += 1
        elif game.score[t1.name] < game.score[t2.name]:
            # print(f"{t2.name} wins!")
            t2_wins += 1
    
    print(f"{t1.name} wins: {t1_wins} times, {t2.name} wins: {t2_wins} times")
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