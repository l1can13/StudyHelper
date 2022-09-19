class Team:
    def __init__(self, teamname, admin):
        self.teamname = teamname
        self.admin = admin

    def get_admin(self):
        return self.admin
