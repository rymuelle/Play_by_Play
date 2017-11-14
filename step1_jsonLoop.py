import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import json
import numpy 
import math
import pprint
from fileListJSON_sorted import fileListJson  



for file in fileListJson:
    with open(file, 'r') as f:
        gameId = 0
        datastore = json.load(f)

        #pprint.pprint(datastore, width=1) 
        gameId =  datastore['competitions'][0]['id']

        year = datastore['season']['year']

        #if year < 2004: continue
       
        #pprint.pprint(datastore['drives'])

        #pprint.pprint(datastore['competitions'])
        if datastore['competitions'][0]['boxscoreAvailable']:
            teams = datastore['competitions'][0]['competitors']

            homeTeamAbbrv = teams[0]['team']['abbreviation']
            isHome = False
            if "home" == teams[0]['homeAway']:
                isHome = True

            print "gameid: {}".format(gameId)
            print "team: {} {} id: {} {} score: {} {}".format(teams[0]['team']['abbreviation'], teams[1]['team']['abbreviation'], teams[0]['id'], teams[1]['id'], teams[0]['score'], teams[1]['score'])
            #pprint.pprint(teams[0])
            #pprint.pprint(teams[1])
            print "year: {}".format(year)

            sumScoreHome = 0
            sumScoreAway = 0


        for drive in datastore['drives']['previous']:

            isHomeOffense = {}
            isScore = drive['isScore']
            if "shortDisplayResult" in drive: shortDisplayResult = drive['shortDisplayResult']
           # else: pprint.pprint(drive)
            offensivePlays = drive['offensivePlays']
            yards = drive['yards']
            yardLineFPStart = drive['plays'][0]['start']['yardLine']
            yardsToEndzoneFPStart = drive['plays'][0]['start']['yardsToEndzone']
          #  deltaScore = drive['plays'][len(drive['plays']) - 1]['homeScore'] - drive['plays'][0]['homeScore'] + drive['plays'][len(drive['plays']) - 1]['awayScore'] - drive['plays'][0]['awayScore']
            deltaScore = drive['plays'][len(drive['plays']) - 1]['homeScore'] - sumScoreHome - (drive['plays'][len(drive['plays']) - 1]['awayScore'] - sumScoreAway)
            teamAbbr = drive['team']['abbreviation']
            homeIsOffense = False
            if teamAbbr == homeTeamAbbrv and isHome:
                homeIsOffense = True
                sumScoreHome = sumScoreHome + drive['plays'][len(drive['plays']) - 1]['homeScore'] - sumScoreHome
            else: sumScoreAway = sumScoreAway + drive['plays'][len(drive['plays']) - 1]['awayScore'] - sumScoreAway

            #scoringTypeAbbrv = ""
            #if isScore: scoringTypeAbbrv = drive['plays'][0]['scoringType']['abbreviation']
            print "isScore {} shortDisplayResult {} offensivePlays {} yardLineFPStart {} yardsToEndzoneFPStart {}".format(isScore, shortDisplayResult, offensivePlays, yardLineFPStart, yardsToEndzoneFPStart)
            print "yards: {} deltaScore: {} homeIsOffense {} team {}".format(yards, deltaScore, homeIsOffense,teamAbbr)
            #pprint.pprint(drive)
        print "Calculated: homeScore {} awayScore {}".format(sumScoreHome,sumScoreAway)





#{u'description': u'1 play, 95 yards, 0:00',
# u'displayResult': u'Interception TD',
# u'end': {u'clock': {u'displayValue': u'6:54'},
#          u'period': {u'number': 1, u'type': u'quarter'},
#          u'text': u'SDSU 0',
#          u'yardLine': 100},
# u'id': u'23249019407',
# u'isScore': True,
# u'offensivePlays': 1,
# u'plays': [{u'awayScore': 7,
#             u'clock': {u'displayValue': u'6:54'},
#             u'end': {u'distance': 10,
#                      u'down': 1,
#                      u'team': {u'id': u'194'},
#                      u'yardLine': 100,
#                      u'yardsToEndzone': 0},
#             u'homeScore': 9,
#             u'id': u'2324901940701',
#             u'modified': u'2003-09-06',
#             u'period': {u'number': 1},
#             u'priority': True,
#             u'scoringPlay': True,
#             u'scoringType': {u'abbreviation': u'TD',
#                              u'displayName': u'Touchdown',
#                              u'name': u'touchdown'},
#             u'start': {u'distance': 5,
#                        u'down': 1,
#                        u'downDistanceText': u'1st and 5 at OSU 5',
#                        u'possessionText': u'OSU 5',
#                        u'shortDownDistanceText': u'1st and 5',
#                        u'team': {u'id': u'21'},
#                        u'yardLine': 5,
#                        u'yardsToEndzone': 0},
#             u'statYardage': 100,
#             u'text': u'Matt Dlugolecki (SDSU) pass right side intercepted by Will Allen (OSU). Returned for a 100 yard touchdown.',
#             u'type': {u'abbreviation': u'TD',
#                       u'id': u'36',
#                       u'text': u'Interception Return Touchdown'}},
#            {u'awayScore': 7,
#             u'clock': {u'displayValue': u'6:54'},
#             u'end': {u'distance': 0,
#                      u'down': 0,
#                      u'team': {u'id': u'194'},
#                      u'yardLine': 0,
#                      u'yardsToEndzone': 0},
#             u'homeScore': 10,
#             u'id': u'2324901940702',
#             u'modified': u'2003-09-06',
#             u'period': {u'number': 1},
#             u'priority': False,
#             u'scoringPlay': True,
#             u'scoringType': {u'abbreviation': u'XP',
#                              u'displayName': u'Extra Point',
#                              u'name': u'extra-point'},
#             u'start': {u'distance': 0,
#                        u'down': 0,
#                        u'downDistanceText': u' and Goal at OSU 0',
#                        u'possessionText': u'OSU 0',
#                        u'shortDownDistanceText': u' and Goal',
#                        u'team': {u'id': u'194'},
#                        u'yardLine': 0,
#                        u'yardsToEndzone': 0},
#             u'statYardage': 0,
#             u'text': u'Extra point by Mike Nugent (OSU) is good.'}],
# u'result': u'INT TD',
# u'shortDisplayResult': u'INT TD',
# u'start': {u'clock': {u'displayValue': u'6:54'},
#            u'period': {u'number': 1, u'type': u'quarter'},
#            u'text': u'OSU 5',
#            u'yardLine': 5},
# u'team': {u'abbreviation': u'OSU',
#           u'displayName': u'Ohio State Buckeyes',
#           u'logos': [{u'alt': u'',
#                       u'height': 500,
#                       u'href': u'http://a.espncdn.com/i/teamlogos/ncaa/500/194.png',
#                       u'rel': [u'full', u'default'],
#                       u'width': 500},
#                      {u'alt': u'',
#                       u'height': 500,
#                       u'href': u'http://a.espncdn.com/i/teamlogos/ncaa/500-dark/194.png',
#                       u'rel': [u'full', u'dark'],
#                       u'width': 500}],
#           u'name': u'Buckeyes',
#           u'shortDisplayName': u'Buckeyes'},
# u'timeElapsed': {u'displayValue': u'0:00'},
# u'yards': 95}#