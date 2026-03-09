# How to simulate a game of basketball??

## Available Data
1. Box score data of teams
2. Box score data of players
3. Play-by-play data of teams
4. Play-by-play data of players

## Possible Approaches (Statistical Models)

### **Monte Carlo Simulation**: 
1. Overview: This model can be used to simulate the sequence of events in a basketball game. Each state can represent a specific situation in the game (e.g., possession, scoring, turnover), and the transitions between states can be determined based on historical data.
2. Implementation:
    - Not player dependent: Just based on box score data of teams, calculate the probabilities of different events (e.g., scoring, turnovers) and simulate the game based on these probabilities.
    - Player dependent: Use player-specific data to calculate the probabilities of events for each player and simulate the game based on these probabilities.
    - Player dependent will help adjust in events of injuries, substitutions, and other factors that can affect the outcome of the game.
3. Details of implementations
    - Not player dependent:
        - Available stats: 
            - fieldGoals, twoPointFieldGoals, threePointFieldGoals, freeThrows: "pct", "attempted", "made"
            - rebounds: "offensive", "defensive", "total"
            - turnovers: "total", "teamTotal" (how are these two different??)
            - "fourFactors": "freeThrowRate", "offensiveReboundPct", "turnoverRatio", "effectiveFieldGoalPct"
            - "assists", "blocks", "steals", "possessions", "rating"
        - Opponent stats: Exact same thing available for opponents of this team as well
        - Details:
            - Calculate the probabilities of different events
                - Time of possession: average time possession, fast break rate (use some normal distribution to adjust from 15-30 seconds for non-fast break and for fast break just like maybe between 3-5 seconds?)
                - Scoring: 
                    - Turnover: apply turnover ratio to calculate the probability of a turnover
                    - Scoring: Calculate the rate for twoPointFieldGoals, threePointFieldGoals, and freeThrows. Use these rates to determine the probability of scoring and the type of score (2 points, 3 points, or free throws). After that, use the percentage of made shots to determine if the shot is successful or not.
                    - Rebound: If the shot is missed, calculate the probability of an offensive or defensive rebound based on the team's rebounding stats and the opponent's rebounding stats.
                - How to calculate match-based stats:
                    - Team A's offensive possesion:
                        - Team A offensive stats
                        - Team B's opponent stats
                        - Stats of team A will be a weighted average of Team A's stats and Team B's opponent stats. Weights can be determined based on offensive and defensive ratings.
                - Necessary realized stats:
                    - Time of possession
                    - Shot type percentages (2pts, 3pts, ft)
                    - Rebound percentages (offensive, defensive)
                    - Turnover percentage
                - Potential adjustments:
                    - Home/Away: Adjust the probabilities based on whether the team is playing at home or away, as teams often perform better at home. (Maybe apply a fixed constant of boost)
                    - Injuries/substitutions: Use player dependent model instead.
    - Player dependent:
        To be continued...
