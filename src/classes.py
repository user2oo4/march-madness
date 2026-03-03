# Generic classes. Expand with more attributes (roster, stats, etc.) as needed.
class Team:
    def __init__(self, name, conference, season):
        self.name = name
        self.conference = conference
        self.season = season
    
class Player:
    def __init__(self, name, team, position):
        self.name = name
        self.team = team
        self.position = position

class Game:
    def __init__(self, team1, team2, date):
        self.team1 = team1
        self.team2 = team2
        self.date = date
    

