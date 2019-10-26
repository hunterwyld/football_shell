from fs_constant import MATCH_STATUS
import fs_utils


class Score(object):

    def __init__(self, country, leagueName, matchList):
        self.country = country
        self.leagueName = leagueName
        self.matchList = matchList

    def print(self):
        title = "{} {} Scores".format(self.country, self.leagueName)
        print("{0:{0}^78}".format('+'))
        print("{0:{1}^78}".format(title, ' '))
        print("{0:{0}^78}".format('+'))
        for match in self.matchList:
            match.print()
        print("{0:{0}^78}".format('+'))


class Match(object):

    def __init__(self, time, home, score, away, status, detailUrl):
        self.time = time
        self.home = home
        self.score = score
        self.away = away
        self.status = status
        self.detailUrl = detailUrl

    # 带颜色左对齐打印
    def print(self):
        color = '0'
        for matchSatus in MATCH_STATUS:
            if matchSatus['status'] == self.status:
                color = matchSatus['color']
                break
        printFormat = "\033[{5}m" + "{0:{4}<18}{1:{4}<25}{2:{4}<10}{3:{4}<25}" + "\033[0m"
        paddingChar = ' '
        aLine = printFormat.format(self.time, self.home, self.score, self.away, paddingChar, color)
        print(aLine)


class MatchDetail(object):

    def __init__(self, homeTeam, awayTeam, finalScore, events):
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.finalScore = finalScore
        self.events = events

    def print(self):
        title = "{} {} {} Match Details".format(self.homeTeam.strip(), self.finalScore.strip(), self.awayTeam.strip())
        print("{0:{0}^83}".format('+'))
        print("{0:{1}^83}".format(title, ' '))
        print("{0:{0}^83}".format('+'))
        for event in self.events:
            time = event['time']
            score = event['score']
            homeType = event['home']['type']
            homePlayer = event['home']['player']
            homeAssist = event['home']['assist']
            if homeType is not None:
                if homeType == 'penalty':
                    home = "{}{}".format(homePlayer, '(P)')
                elif homeType == 'owngoal':
                    home = "{}{}".format(homePlayer, '(OG)')
                elif homeType == 'goal':
                    if homeAssist is None:
                        home = "{}{}".format(homePlayer, '(G)')
                    else:
                        home = "{}{}{}".format(homePlayer, '(G)', '(' + homeAssist + '(A))')
                elif homeType == 'yellowcard':
                    home = "{}{}".format(homePlayer, '(YC)')
                elif homeType == 'redyellowcard':
                    home = "{}{}".format(homePlayer, '(2YC)')
                elif homeType == 'redcard':
                    home = "{}{}".format(homePlayer, '(RC)')
                else:
                    home = ''
            else:
                home = ''

            awayType = event['away']['type']
            awayPlayer = event['away']['player']
            awayAssist = event['away']['assist']
            if awayType is not None:
                if awayType == 'penalty':
                    away = "{}{}".format(awayPlayer, '(P)')
                elif awayType == 'owngoal':
                    away = "{}{}".format(awayPlayer, '(OG)')
                elif awayType == 'goal':
                    if awayAssist is None:
                        away = "{}{}".format(awayPlayer, '(G)')
                    else:
                        away = "{}{}{}".format(awayPlayer, '(G)', '(' + awayAssist + '(A))')
                elif awayType == 'yellowcard':
                    away = "{}{}".format(awayPlayer, '(YC)')
                elif awayType == 'redyellowcard':
                    away = "{}{}".format(awayPlayer, '(2YC)')
                elif awayType == 'redcard':
                    away = "{}{}".format(awayPlayer, '(RC)')
                else:
                    away = ''
            else:
                away = ''

            color = '34'
            aEvent = ("\033[{5}m" + "{0:{4}^5}{1:{4}^35}{2:{4}^8}{3:{4}^35}" + "\033[0m") \
                .format(time, home, score, away, ' ', color)
            print(aEvent)
        print("{0:{0}^83}".format('-'))
        color = '36'
        print(("\033[{5}m" + "{0:{4}<20}{1:{4}<20}{2:{4}<20}{3:{4}<20}" + "\033[0m")
              .format('G = Goal', 'A = Assist', 'P = Penalty', 'OG = Own Goal', ' ', color))
        print(("\033[{4}m" + "{0:{3}<20}{1:{3}<25}{2:{3}<20}" + "\033[0m")
              .format('YC = Yellow Card', '2YC = 2nd Yellow Card', 'RC = Red Card', ' ', color))
        print("{0:{0}^83}".format('+'))


class MatchSquad(object):

    def __init__(self, homeTeam, awayTeam, finalScore,
                 homeFormation, homeLineup, homeSubstitutions, homeSubstitutes, homeCoach,
                 awayFormation, awayLineup, awaySubstitutions, awaySubstitutes, awayCoach):
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.finalScore = finalScore
        self.homeFormation = homeFormation
        self.homeLineup = homeLineup
        self.homeSubstitutions = homeSubstitutions
        self.homeSubstitutes = homeSubstitutes
        self.homeCoach = homeCoach
        self.awayFormation = awayFormation
        self.awayLineup = awayLineup
        self.awaySubstitutions = awaySubstitutions
        self.awaySubstitutes = awaySubstitutes
        self.awayCoach = awayCoach

    def print(self):
        title = "{} {} {} Match Squad".format(self.homeTeam.strip(), self.finalScore.strip(), self.awayTeam.strip())
        print("{0:{0}^70}".format('+'))
        print("{0:{1}^70}".format(title, ' '))
        print("{0:{0}^70}".format('+'))
        print("{0:{1}^70}".format('Starting XI', ' '))
        for i in range(max(len(self.homeLineup), len(self.awayLineup))):
            homePlayer = self.homeLineup[i] if i in range(len(self.homeLineup)) else ''
            awayPlayer = self.awayLineup[i] if i in range(len(self.awayLineup)) else ''
            color = '34'
            print("\033[{3}m{0:{2}^35}{1:{2}^35}\033[0m".format(homePlayer, awayPlayer, ' ', color))
        print("{0:{0}^70}".format('-'))

        print("{0:{1}^70}".format('Substitutions', ' '))
        for i in range(max(len(self.homeSubstitutions), len(self.awaySubstitutions))):
            if i in range(len(self.homeSubstitutions)):
                homeSubOutPlayer = self.homeSubstitutions[i]['subOut'] + '↓'
                homeSubInPlayer = self.homeSubstitutions[i]['subIn'] + '↑'
                homeSubTime = self.homeSubstitutions[i]['subTime']
            else:
                homeSubTime = ''
                homeSubOutPlayer = ''
                homeSubInPlayer = ''
            if i in range(len(self.awaySubstitutions)):
                awaySubOutPlayer = self.awaySubstitutions[i]['subOut'] + '↓'
                awaySubInPlayer = self.awaySubstitutions[i]['subIn'] + '↑'
                awaySubTime = self.awaySubstitutions[i]['subTime']
            else:
                awaySubTime = ''
                awaySubOutPlayer = ''
                awaySubInPlayer = ''
            color = '36'
            printFormat = "\033[{5}m{0:{4}<5}{1:{4}^30}{2:{4}^30}{3:{4}>5}\033[0m"
            print(printFormat.format(homeSubTime, homeSubOutPlayer, awaySubOutPlayer, awaySubTime, ' ', color))
            print(printFormat.format('', homeSubInPlayer, awaySubInPlayer, '', ' ', color))
        print("{0:{0}^70}".format('-'))

        print("{0:{1}^70}".format('Substitutes', ' '))
        for i in range(max(len(self.homeSubstitutes), len(self.awaySubstitutes))):
            homePlayer = self.homeSubstitutes[i] if i in range(len(self.homeSubstitutes)) else ''
            awayPlayer = self.awaySubstitutes[i] if i in range(len(self.awaySubstitutes)) else ''
            color = '35'
            print("\033[{3}m{0:{2}^35}{1:{2}^35}\033[0m".format(homePlayer, awayPlayer, ' ', color))
        print("{0:{0}^70}".format('-'))

        print("{0:{1}^70}".format('Coach', ' '))
        homeCoach = self.homeCoach if self.homeCoach is not None else 'Unknown'
        awayCoach = self.awayCoach if self.awayCoach is not None else 'Unknown'
        color = '33'
        print("\033[{3}m{0:{2}^35}{1:{2}^35}\033[0m".format(homeCoach, awayCoach, ' ', color))
        print("{0:{0}^70}".format('+'))


class MatchStats(object):

    def __init__(self, homeTeam, awayTeam, finalScore, matchStatList):
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.finalScore = finalScore
        self.matchStatList = matchStatList

    def print(self):
        color = '34'
        title = "{} {} {} Match Stats".format(self.homeTeam.strip(), self.finalScore.strip(), self.awayTeam.strip())
        print("{0:{0}^94}".format('+'))
        print("{0:{1}^94}".format(title, ' '))
        print("{0:{0}^94}".format('+'))
        for matchStat in self.matchStatList:
            statName = matchStat['statName']
            homeStatNum = matchStat['homeStatNum']
            awayStatNum = matchStat['awayStatNum']
            homePercent = int(round(homeStatNum * 100 / (homeStatNum + awayStatNum)))
            awayPercent = 100 - homePercent
            homeProgressBar = fs_utils.get_progress_bar('negative', homePercent, 30)
            awayProgressBar = fs_utils.get_progress_bar('positive', awayPercent, 30)

            printFormat = "\033[{6}m" + "{0:{5}>5}{1:{5}>32}{2:{5}^20}{3:{5}<32}{4:{5}<5}" + "\033[0m"
            aMatchStat = printFormat.format(homeStatNum, homeProgressBar, statName,
                                            awayProgressBar, awayStatNum, ' ', color)
            print(aMatchStat)
        print("{0:{0}^94}".format('+'))
