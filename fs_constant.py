EVENT_TYPE = {"P": {"color": "32", "desc": "Penalty"},
              "OG": {"color": "34", "desc": "Own Goal"},
              "G": {"color": "36", "desc": "Goal"},
              "A": {"color": "36", "desc": "Assist"},
              "YC": {"color": "33", "desc": "Yellow Card"},
              "2YC": {"color": "35", "desc": "2nd Yellow Card"},
              "RC": {"color": "31", "desc": "Red Card"}
}

MATCH_STATUS = [{"status": "not_play", "color": "36"},
                {"status": "playing", "color": "32"},
                {"status": "played", "color": "34"}]

LEAGUE_INFOS = [
    {
        "leagueName": "Premier League",
        "country": "England",
        "area": "Europe",
        "url": "http://www.livescores.com/soccer/england/premier-league/",
        "qualifications": [{"qualification": "Champions League", "positions": ['1', '2', '3', '4'], "color": "34"},
                           {"qualification": "Europa League", "positions": ['5'], "color": "32"},
                           {"qualification": "Relegation", "positions": ['18', '19', '20'], "color": "31"}]
    },
    {
        "leagueName": "Championship",
        "country": "England",
        "area": "Europe",
        "url": "http://www.livescores.com/soccer/england/championship/",
        "qualifications": [{"qualification": "Promotion", "positions": ['1', '2'], "color": "34"},
                           {"qualification": "Promotion play-off", "positions": ['3', '4', '5', '6'], "color": "36"},
                           {"qualification": "Relegation", "positions": ['22', '23', '24'], "color": "31"}]
    },
    {
        "leagueName": "LaLiga",
        "country": "Spain",
        "area": "Europe",
        "url": "http://www.livescores.com/soccer/spain/primera-division/",
        "qualifications": [{"qualification": "Champions League", "positions": ['1', '2', '3', '4'], "color": "34"},
                           {"qualification": "Europa League", "positions": ['5'], "color": "32"},
                           {"qualification": "Europa League qualification", "positions": ['6'], "color": "33"},
                           {"qualification": "Relegation", "positions": ['18', '19', '20'], "color": "31"}]
    },
    {
        "leagueName": "Serie A",
        "country": "Italy",
        "area": "Europe",
        "url": "http://www.livescores.com/soccer/italy/serie-a/",
        "qualifications": [{"qualification": "Champions League", "positions": ['1', '2', '3', '4'], "color": "34"},
                           {"qualification": "Europa League", "positions": ['5'], "color": "32"},
                           {"qualification": "Europa League qualification", "positions": ['6'], "color": "33"},
                           {"qualification": "Relegation", "positions": ['18', '19', '20'], "color": "31"}]
    },
    {
        "leagueName": "Bundesliga",
        "country": "Germany",
        "area": "Europe",
        "url": "http://www.livescores.com/soccer/germany/bundesliga/",
        "qualifications": [{"qualification": "Champions League", "positions": ['1', '2', '3', '4'], "color": "34"},
                           {"qualification": "Europa League", "positions": ['5'], "color": "32"},
                           {"qualification": "Europa League qualification", "positions": ['6'], "color": "33"},
                           {"qualification": "Relegation play-off", "positions": ['16'], "color": "35"},
                           {"qualification": "Relegation", "positions": ['17', '18'], "color": "31"}]
    },
    {
        "leagueName": "Ligue 1",
        "country": "France",
        "area": "Europe",
        "url": "http://www.livescores.com/soccer/france/ligue-1/",
        "qualifications": [{"qualification": "Champions League", "positions": ['1', '2'], "color": "34"},
                           {"qualification": "Champions League qualification", "positions": ['3'], "color": "36"},
                           {"qualification": "Europa League", "positions": ['4'], "color": "32"},
                           {"qualification": "Relegation play-off", "positions": ['18'], "color": "35"},
                           {"qualification": "Relegation", "positions": ['19', '20'], "color": "31"}]
    },
    {
        "leagueName": "Eredivisie",
        "country": "Netherlands",
        "area": "Europe",
        "url": "http://www.livescores.com/soccer/holland/eredivisie/",
        "qualifications": [{"qualification": "Champions League qualification", "positions": ['1', '2'], "color": "36"},
                           {"qualification": "Europa League qualification", "positions": ['3'], "color": "33"},
                           {"qualification": "Relegation play-off", "positions": ['16'], "color": "35"},
                           {"qualification": "Relegation", "positions": ['17', '18'], "color": "31"}]
    },
    {
        "leagueName": "Primeira Liga",
        "country": "Portugal",
        "area": "Europe",
        "url": "http://www.livescores.com/soccer/portugal/liga-sagres/",
        "qualifications": [{"qualification": "Champions League", "positions": ['1'], "color": "34"},
                           {"qualification": "Champions League qualification", "positions": ['2'], "color": "36"},
                           {"qualification": "Europa League qualification", "positions": ['3', '4'], "color": "33"},
                           {"qualification": "Relegation", "positions": ['17', '18'], "color": "31"}]
    },
    {
        "leagueName": "Super League",
        "country": "China",
        "area": "Asia",
        "url": "http://www.livescores.com/soccer/china/premier-league/",
        "qualifications": [{"qualification": "AFC Champions League", "positions": ['1', '2'], "color": "34"},
                           {"qualification": "Champions League qualification", "positions": ['3'], "color": "36"},
                           {"qualification": "Relegation", "positions": ['15', '16'], "color": "31"}]
    }
]
