class User:
    def __init__(self, *args):
        if len(args) == 1:
            self.username = args[0]
        elif len(args) == 2:
            self.username = args[0]
            self.teamname = args[1]
        else:
            self.username = None
            self.teamname = None

    def set_team(self, teamname):
        self.teamname = teamname

    def get_team(self):
        return self.teamname

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username
