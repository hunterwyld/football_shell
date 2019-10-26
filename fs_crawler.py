from bs4 import BeautifulSoup
import requests
import fs_utils
from model.Match import Match
from model.Match import Score
from model.Match import MatchDetail
from model.Match import MatchStats
from model.Match import MatchSquad
from model.LeagueTable import LeagueTableItem
from model.LeagueTable import LeagueTable


def get_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    [content] = soup.select('body > div.wrapper > div.content')
    extract_tag(content, 'div', 'cal-wrap')
    extract_tag(content, 'div', 'row mt4 bb bt')
    extract_tag(content, 'div', 'row row-tall mt4')
    extract_tag(content, 'div', 'cal clear')
    return content


def get_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    details = soup.find_all('div', attrs={'data-id': 'details'})
    newDetails = []
    for detail in details:
        if detail.find('div', class_='min') is not None:
            newDetails.append(detail)

    return newDetails


def get_stats(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    stats = soup.find('div', attrs={'data-id': 'stats'})
    extract_tag(stats, 'div', 'row mt4 bt')
    return stats


def get_squad(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find('div', attrs={'data-id': 'substitutions'})


def extract_tag(tree, tag, css_class):
    for t in tree.find_all(tag, class_=css_class):
        t.extract()


def get_match_squad(match):
    squadTag = get_squad(match.detailUrl)
    lineupTag = []
    substitutionsTag = []
    substitutesTag = []

    itemTag = squadTag.find('div', class_='row mt4 bt')
    formationTag = itemTag.find_next_sibling()
    itemTag = formationTag.find_next_sibling()
    nextTag = itemTag.find_next_sibling()
    while True:
        if nextTag.string is not None and nextTag.string.strip() == 'substitutions :':
            break
        else:
            lineupTag.append(nextTag)
            nextTag = nextTag.find_next_sibling()
    nextTag = nextTag.find_next_sibling()
    while True:
        if nextTag.string is not None and nextTag.string.strip() == 'substitute players :':
            break
        else:
            substitutionsTag.append(nextTag)
            nextTag = nextTag.find_next_sibling()
    nextTag = nextTag.find_next_sibling()
    while True:
        if nextTag.string is not None and nextTag.string.strip() == 'coach :':
            break
        else:
            substitutesTag.append(nextTag)
            nextTag = nextTag.find_next_sibling()
    coachTag = nextTag.find_next_sibling()

    homeFormation = None
    awayFormation = None
    if formationTag is not None:
        for (idx, iTag) in enumerate(formationTag.find_all('i')):
            if idx == 0:
                homeFormation = iTag.find_parent().contents[1].strip()
            elif idx == 1:
                awayFormation = iTag.find_parent().contents[1].strip()
            else:
                pass
    else:
        homeFormation = None
        awayFormation = None

    if lineupTag is not None and lineupTag != []:
        homeLineup = []
        awayLineup = []
        for tag in lineupTag:
            for (idx, iTag) in enumerate(tag.find_all('i')):
                if idx == 0:
                    homeLineup.append(iTag.find_parent().contents[2].strip())
                elif idx == 1:
                    awayLineup.append(iTag.find_parent().contents[2].strip())
                else:
                    pass
    else:
        homeLineup = None
        awayLineup = None

    if substitutionsTag is not None and substitutionsTag != []:
        homeSubstitutions = []
        awaySubstitutions = []
        for tag in substitutionsTag:
            for (idx, timeTag) in enumerate(tag.find_all('div', class_='col-1 ln36')):
                subTag = timeTag.find_next_sibling()
                if idx == 0:
                    subTime = timeTag.string.strip() if timeTag.string is not None else None
                    if subTime is not None:
                        subOut = subTag.find('i', class_='inc sub-out').find_parent().contents[1].strip()
                        subIn = subTag.find('i', class_='inc sub-in').find_parent().contents[1].strip()
                        homeSubstitution = {'subTime': subTime, 'subOut': subOut, 'subIn': subIn}
                        homeSubstitutions.append(homeSubstitution)
                elif idx == 1:
                    subTime = timeTag.string.strip() if timeTag.string is not None else None
                    if subTime is not None:
                        subOut = subTag.find('i', class_='inc sub-out').find_parent().contents[1].strip()
                        subIn = subTag.find('i', class_='inc sub-in').find_parent().contents[1].strip()
                        awaySubstitution = {'subTime': subTime, 'subOut': subOut, 'subIn': subIn}
                        awaySubstitutions.append(awaySubstitution)
                else:
                    pass
    else:
        homeSubstitutions = None
        awaySubstitutions = None

    if substitutesTag is not None and substitutesTag != []:
        homeSubstitutes = []
        awaySubstitutes = []
        for tag in substitutesTag:
            for (idx, iTag) in enumerate(tag.find_all('i')):
                if idx == 0:
                    homeSubstitutes.append(iTag.find_parent().contents[2].strip())
                elif idx == 1:
                    awaySubstitutes.append(iTag.find_parent().contents[2].strip())
                else:
                    pass
    else:
        homeSubstitutes = None
        awaySubstitutes = None

    homeCoach = None
    awayCoach = None
    if coachTag is not None:
        for (idx, iTag) in enumerate(coachTag.find_all('i')):
            if idx == 0:
                homeCoach = iTag.find_parent().contents[1].strip()
            elif idx == 1:
                awayCoach = iTag.find_parent().contents[1].strip()
            else:
                pass
    else:
        homeCoach = None
        awayCoach = None

    return MatchSquad(match.home, match.away, match.score,
                      homeFormation, homeLineup, homeSubstitutions, homeSubstitutes, homeCoach,
                      awayFormation, awayLineup, awaySubstitutions, awaySubstitutes, awayCoach)


def get_match_stats(match):
    stats = get_stats(match.detailUrl)
    statNameTags = stats.find_all('div', class_='col-2 tcenter')
    matchStatList = []
    for statNameTag in statNameTags:
        statNumHomeTag = statNameTag.find_previous_sibling().find_previous_sibling()
        statNumAwayTag = statNameTag.find_next_sibling().find_next_sibling()
        statNumHome = statNumHomeTag.string.strip() if statNumHomeTag.string is not None else None
        statNumAway = statNumAwayTag.string.strip() if statNumAwayTag.string is not None else None
        if statNumHome is not None and statNumAway is not None:
            matchStat = {'statName': statNameTag.string.strip(),
                         'homeStatNum': int(statNumHome), 'awayStatNum': int(statNumAway)}
            matchStatList.append(matchStat)
    return MatchStats(match.home, match.away, match.score, matchStatList)


def get_match_detail(match):
    details = get_details(match.detailUrl)
    events = []
    for detail in details:
        timeTag = detail.find('div', class_='min')
        homeTag = timeTag.find_next_sibling()
        scoreTag = homeTag.find_next_sibling()
        awayTag = scoreTag.find_next_sibling()
        if timeTag is None or homeTag is None or scoreTag is None or awayTag is None:
            raise Exception("detail: {} unexpected".format(detail))

        eventTime = timeTag.string.strip() if timeTag.string is not None else None
        eventScore = scoreTag.string.strip() if scoreTag.string is not None else None
        eventScore = eventScore if events != '' else None

        homeEventPlayer = homeTag.find('span', class_='name').string
        homeEventPlayer = homeEventPlayer.strip() if homeEventPlayer is not None else None
        homeEventAssist = None
        if homeTag.find('span', class_='inc goal') is not None:
            goalHow = homeTag.find('span', class_='ml4').string
            if goalHow is None:
                homeEventType = None
            elif goalHow.strip() == '(pen.)':
                homeEventType = "penalty"
            elif goalHow.strip() == '(o.g.)':
                homeEventType = "owngoal"
            else:
                homeEventType = "goal"
                homeEventAssistTag = homeTag.find('span', class_='assist name')
                if homeEventAssistTag is not None:
                    homeEventAssist = homeEventAssistTag.string.replace('(assist)', '')
                    homeEventAssist = homeEventAssist.strip()
        elif homeTag.find('span', class_='inc yellowcard') is not None:
            homeEventType = "yellowcard"
        elif homeTag.find('span', class_='inc redyellowcard') is not None:
            homeEventType = "redyellowcard"
        elif homeTag.find('span', class_='inc redcard') is not None:
            homeEventType = "redcard"
        else:
            homeEventType = None
        eventHome = {"type": homeEventType, "player": homeEventPlayer, "assist": homeEventAssist}

        awayEventPlayer = awayTag.find('span', class_='name').string
        awayEventPlayer = awayEventPlayer.strip() if awayEventPlayer is not None else None
        awayEventAssist = None
        if awayTag.find('span', class_='inc goal') is not None:
            goalHow = awayTag.find('span', class_='mr4').string
            if goalHow is None:
                awayEventType = None
            elif goalHow.strip() == '(pen.)':
                awayEventType = "penalty"
            elif goalHow.strip() == '(o.g.)':
                awayEventType = "owngoal"
            else:
                awayEventType = "goal"
                awayEventAssistTag = awayTag.find('span', class_='assist name')
                if awayEventAssistTag is not None:
                    awayEventAssist = awayEventAssistTag.string.replace('(assist)', '')
                    awayEventAssist = awayEventAssist.strip()
        elif awayTag.find('span', class_='inc yellowcard') is not None:
            awayEventType = "yellowcard"
        elif awayTag.find('span', class_='inc redyellowcard') is not None:
            awayEventType = "redyellowcard"
        elif awayTag.find('span', class_='inc redcard') is not None:
            awayEventType = "redcard"
        else:
            awayEventType = None
        eventAway = {"type": awayEventType, "player": awayEventPlayer, "assist": awayEventAssist}

        event = {'time': eventTime, 'home': eventHome, 'score': eventScore, 'away': eventAway}
        events.append(event)

    return MatchDetail(match.home, match.away, match.score, events)


def get_score(country, leagueName):
    url = fs_utils.get_url(country, leagueName)
    content = get_content(url)
    matchList = []
    for minTag in content.select('div.min'):
        rowTag = minTag.find_parent()
        minStr = minTag.string.strip() if minTag.string is not None else minTag.contents[1].strip()
        if minStr == 'FT':
            matchStatus = 'played'
        elif ':' in minStr:
            matchStatus = 'not_play'
        else:
            matchStatus = 'playing'

        matchTime = "{} {}".format(fs_utils.get_date(rowTag['data-esd']), minStr)

        homeTeamTag = minTag.find_next_sibling()
        scoreTag = homeTeamTag.find_next_sibling()
        awayTeamTag = scoreTag.find_next_sibling()
        detailUrl = "http://www.livescores.com" + scoreTag.a['href']
        match = Match(matchTime, homeTeamTag.string, scoreTag.a.string, awayTeamTag.string,
                      matchStatus, detailUrl)
        matchList.append(match)

    return Score(country, leagueName, matchList)


def get_league_table(country, leagueName):
    url = fs_utils.get_url(country, leagueName)
    content = get_content(url)
    leagueTableItems = []
    for (idx, teamTag) in enumerate(content.select('div.team')):
        if idx > 0:
            rankTag = teamTag.find_previous_sibling().find('span', class_=None)
            playedTag = teamTag.find_next_sibling()
            winsTag = playedTag.find_next_sibling()
            drawsTag = winsTag.find_next_sibling()
            lostsTag = drawsTag.find_next_sibling()
            goalsForTag = lostsTag.find_next_sibling()
            goalsAgainstTag = goalsForTag.find_next_sibling()
            goalsDiffTag = goalsAgainstTag.find_next_sibling()
            pointsTag = goalsDiffTag.find_next_sibling()

            leagueTableItem = LeagueTableItem(rankTag.string, teamTag.string, playedTag.string, winsTag.string,
                                              drawsTag.string, lostsTag.string, goalsForTag.string,
                                              goalsAgainstTag.string, goalsDiffTag.string, pointsTag.string,
                                              country, leagueName)
            leagueTableItems.append(leagueTableItem)

    return LeagueTable(country, leagueName, leagueTableItems)

# leagueTable = get_league_table("China", "Super League")
# leagueTable.print()
#
# score = get_score("China", "Super League")
# score.print()
# match = score.matchList[1]

# matchDetail = get_match_detail(match)
# matchDetail.print()

# matchStats = get_match_stats(match)
# matchStats.print()
# if match.status == 'not_play' or match.detailUrl is None or match.detailUrl == '':
#     print("match info not available yet")
# else:
#     matchSquad = get_match_squad(match)
#     matchSquad.print()

# fc_utils.is_reachable('www.livescores.com')
