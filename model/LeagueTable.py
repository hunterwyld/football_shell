import fs_utils


class LeagueTable(object):

    def __init__(self, country, leagueName, leagueTableItems):
        self.country = country
        self.leagueName = leagueName
        self.leagueTableItems = leagueTableItems

    def print(self):
        title = "{} {} Table".format(self.country, self.leagueName)
        bannerFormat = "{0:{10}<5}{1:{10}<25}{2:{10}<5}{3:{10}<5}{4:{10}<5}{5:{10}<5}" \
                       "{6:{10}<5}{7:{10}<5}{8:{10}<5}{9:{10}<5}"
        print("{0:{0}^70}".format('+'))
        print("{0:{1}^70}".format(title, ' '))
        print("{0:{0}^70}".format('+'))
        print(bannerFormat.format('#', 'Team Name', 'GP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts', ' '))
        print("{0:{0}^70}".format('-'))
        for item in self.leagueTableItems:
            item.print()
        print("{0:{0}^70}".format('-'))
        for q in fs_utils.get_qualifications(self.country, self.leagueName):
            qualification = q['qualification']
            color = q['color']
            print("\033[" + color + "m" + qualification + "\033[0m")
        print("{0:{0}^70}".format('+'))


class LeagueTableItem(object):

    def __init__(self, rank, teamName, played, wins, draws, losts, goalsFor, goalsAgainst, goalsDiff, points,
                 country, leagueName):
        self.rank = rank
        self.teamName = teamName
        self.played = played
        self.wins = wins
        self.draws = draws
        self.losts = losts
        self.goalsFor = goalsFor
        self.goalsAgainst = goalsAgainst
        self.goalsDiff = goalsDiff
        self.points = points
        self.country = country
        self.leagueName = leagueName

    # 带颜色左对齐打印
    def print(self):
        color = '0'
        for q in fs_utils.get_qualifications(self.country, self.leagueName):
            if self.rank in q['positions']:
                color = q['color']
                break

        printFormat = "\033[{11}m" + "{0:{10}<5}{1:{10}<25}{2:{10}<5}{3:{10}<5}{4:{10}<5}{5:{10}<5}" \
                                     "{6:{10}<5}{7:{10}<5}{8:{10}<5}{9:{10}<5}" + "\033[0m"
        paddingChar = ' '
        aLine = printFormat.format(self.rank, self.teamName, self.played, self.wins, self.draws, self.losts,
                                   self.goalsFor, self.goalsAgainst,
                                   self.goalsDiff, self.points, paddingChar, color)
        print(aLine)
