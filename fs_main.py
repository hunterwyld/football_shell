import re
import random
import fs_utils
import fs_crawler


def print_welcome():
    print("{0:{0}^60}".format('+'))
    print("{0:{1}<30}{0:{1}>30}".format('+', ' '))
    print("{1:{2}<10}{0:{2}^40}{1:{2}>10}".format("Welcome to football shell!", '+', ' '))
    print("{0:{1}<30}{0:{1}>30}".format('+', ' '))
    print("{1:{2}<10}{0:{2}^40}{1:{2}>10}".format("Author: hunterwyld", '+', ' '))
    print("{0:{1}<30}{0:{1}>30}".format('+', ' '))
    print("{0:{0}^60}".format('+'))


def print_bye():
    byes = ['bye bye', 'see you', 'catch you later', 'farewell', 'goodbye']
    print(random.choice(byes))


def print_1st_level_help():
    printFormat = "{0:{2}<15}{1:{2}<45}"
    print(printFormat.format("q:", "quit program", ' '))
    print(printFormat.format("l:", "list supported leagues", ' '))


def print_2nd_level_help(availableLeagues):
    printFormat = "{0:{2}<15}{1:{2}<45}"
    print(printFormat.format("q:", "quit to upper level", ' '))
    print(printFormat.format("i.table:", "show league table", ' '))
    print(printFormat.format("i.score:", "show live scores", ' '))
    print("where i is in {}".format(availableLeagues))


def print_3rd_level_help(availableMatches):
    printFormat = "{0:{2}<15}{1:{2}<45}"
    print(printFormat.format("q:", "quit to upper level", ' '))
    print(printFormat.format("i.detail:", "show match detail", ' '))
    print(printFormat.format("i.squad:", "show match squad", ' '))
    print(printFormat.format("i.stat:", "show match statistics", ' '))
    print("where i is in {}".format(availableMatches))


def print_supported_leagues():
    supportedLeagues = fs_utils.get_supported_leagues()
    color = '34'
    for (idx, league) in enumerate(supportedLeagues):
        print("\033[{1}m{0}\033[0m".format('. '.join([str(idx + 1), league]), color))
    print("{0:{0}^60}".format('+'))
    return supportedLeagues


def main():
    print_welcome()
    try:
        while True:
            print_1st_level_help()
            c = input(">>>")
            if c == 'q':
                break
            elif c == 'l':
                supportedLeagues = print_supported_leagues()
                while True:
                    availableLeagues = [x for x in range(1, len(supportedLeagues) + 1)]
                    print_2nd_level_help(availableLeagues)
                    c = input(">>>")
                    if c == 'q':
                        break
                    if re.match(r'^\d\.\w+$', c) is None:
                        continue
                    seq = int(c.split('.')[0])
                    opt = c.split('.')[1]
                    if seq not in range(1, len(supportedLeagues) + 1):
                        continue
                    league = supportedLeagues[seq - 1]
                    m = re.match(r'^\[(.+)\]\s(.+)$', league)
                    if m is None:
                        raise Exception("league: {} unexpected".format(league))
                    country = m.group(1)
                    leagueName = m.group(2)
                    if opt == 'table':
                        leagueTable = fs_crawler.get_league_table(country, leagueName)
                        leagueTable.print()
                    elif opt == 'score':
                        leagueScore = fs_crawler.get_score(country, leagueName)
                        leagueScore.print()
                        while True:
                            availableMatches = fs_utils.get_available_matches(leagueScore)
                            print_3rd_level_help(availableMatches)
                            c = input(">>>")
                            if c == 'q':
                                break
                            if re.match(r'^\d\.\w+$', c) is None:
                                continue
                            seq = int(c.split('.')[0])
                            opt = c.split('.')[1]
                            if seq not in availableMatches:
                                print("match info not available yet :(")
                                print("{0:{0}^60}".format('+'))
                                continue
                            match = leagueScore.matchList[seq - 1]
                            if opt == 'detail':
                                matchDetail = fs_crawler.get_match_detail(match)
                                matchDetail.print()
                            elif opt == 'squad':
                                matchSquad = fs_crawler.get_match_squad(match)
                                matchSquad.print()
                            elif opt == 'stat':
                                matchStats = fs_crawler.get_match_stats(match)
                                matchStats.print()
                            else:
                                pass
                    else:
                        pass
            else:
                pass
        print_bye()
        exit(0)
    except KeyboardInterrupt:
        print_bye()
        exit(0)


if __name__ == '__main__':
    main()
