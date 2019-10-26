import socket
from fs_constant import LEAGUE_INFOS


# test network is reachable or not
def is_reachable(domain):
    try:
        host = socket.gethostbyname(domain)
        print(host)
        socket.create_connection((host, 80), 3)
        return True
    except:
        return False


# dateStr: such as 20191019113000
def get_date(dateStr):
    if len(dateStr) < 14:
        raise Exception("date_str: {} length unexpected".format(dateStr))
    year = dateStr[0:4]
    month = dateStr[4:6]
    day = dateStr[6:8]
    return "{}-{}-{}".format(year, month, day)


def get_league_info(country, leagueName):
    leagueInfo = None
    for info in LEAGUE_INFOS:
        if info['country'] == country and info['leagueName'] == leagueName:
            leagueInfo = info
            break

    if leagueInfo is None:
        raise Exception("country: {}, leagueName: {} unexpected".format(country, leagueName))
    else:
        return leagueInfo


def get_url(country, leagueName):
    leagueInfo = get_league_info(country, leagueName)
    return leagueInfo['url']


def get_qualifications(country, leagueName):
    leagueInfo = get_league_info(country, leagueName)
    return leagueInfo['qualifications']


def get_progress_bar(type, percent, totalLength):
    ch = '*'
    length = int(round(totalLength * percent / 100))
    if type == 'positive':
        return ch * length + ' ' * (totalLength - length)
    elif type == 'negative':
        return ' ' * (totalLength - length) + ch * length
    else:
        raise Exception("type: {} unexpected".format(type))


def get_supported_leagues():
    leagues = []
    for info in LEAGUE_INFOS:
        country = info['country']
        leagueName = info['leagueName']
        leagues.append("[" + country + "] " + leagueName)
    return leagues


def get_available_matches(score):
    matches = []
    for (idx, match) in enumerate(score.matchList):
        notAvailable = match.status == 'not_play' or match.detailUrl is None or match.detailUrl == ''
        if notAvailable is False:
            matches.append(idx+1)
    return matches
