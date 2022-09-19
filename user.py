class User:
    def __init__(self, username):
        self.teamname = None
        self.username = username

    def set_team(self, teamname):
        self.teamname = teamname

    def get_team(self):
        return self.teamname

