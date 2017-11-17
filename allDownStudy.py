import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import json
import numpy 
import math
import pprint
from fileListJSON_sorted import fileListJson  


jsonFile = open("downValue.txt", "w")
jsonFile.write("[")
first =  True


for file in fileListJson:
    with open(file, 'r') as f:
        gameId = 0
        datastore = json.load(f)

        #pprint.pprint(datastore, width=1) 
        gameId =  datastore['competitions'][0]['id']

        year = datastore['season']['year']

        if year < 2006: continue
       
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
            scoreHome = int(teams[0]['score'])
            scoreAway = int(teams[1]['score'])

        arrayCount = 0
        firstDownPlayArray = []
        
        homeTeamWeight = 1.0/float(len(datastore['drives']['previous'])) # not perfect, but simple
        downCount = [0,0,0,0,0]
        jsonString = ""
        for count, drive in enumerate(datastore['drives']['previous']):
            
            if "team" in drive:
                down = drive['plays'][0]['start']['down']
                isHomeOffense = {}
                isScore = drive['isScore']
                shortDisplayResult = "Not Found"
                if "shortDisplayResult" in drive: shortDisplayResult = drive['shortDisplayResult']
           #     else: pprint.pprint(drive)
                offensivePlays = drive['offensivePlays']
                yards = drive['yards']
                yardLineFPStart = drive['plays'][0]['start']['yardLine']
                yardsToEndzoneFPStart = drive['plays'][0]['start']['yardsToEndzone'] #from the original offenses perspective
                endYard = -1000
                if "end" in drive: endYard = drive['end']['yardLine'] # last point of possetion by the first offense
                endYardToEndZone = drive['plays'][len(drive['plays']) - 1]['end']['yardsToEndzone'] #from the offenses point of view, so if punt, now new offense has x yards to go
    
    
          #      deltaScore = drive['plays'][len(drive['plays']) - 1]['homeScore'] - drive['plays'][0]['homeScore'] + drive['plays'][len(drive['plays']) - 1]['awayScore'] - drive['plays'][0]['awayScore']
                deltaHomeScore = drive['plays'][len(drive['plays']) - 1]['homeScore'] - sumScoreHome - (drive['plays'][len(drive['plays']) - 1]['awayScore'] - sumScoreAway)
                deltaOffenseScore = -deltaHomeScore
                teamAbbr = drive['team']['abbreviation']
                homeIsOffense = False
                if teamAbbr == homeTeamAbbrv and isHome:
                    deltaOffenseScore = deltaHomeScore
                    homeIsOffense = True
                    sumScoreHome = sumScoreHome + drive['plays'][len(drive['plays']) - 1]['homeScore'] - sumScoreHome
                else: sumScoreAway = sumScoreAway + drive['plays'][len(drive['plays']) - 1]['awayScore'] - sumScoreAway
    
    
    
                #scoringTypeAbbrv = ""
                #if isScore: scoringTypeAbbrv = drive['plays'][0]['scoringType']['abbreviation']
                print "isScore {} shortDisplayResult {} offensivePlays {} yardLineFPStart {} yardsToEndzoneFPStart {}".format(isScore, shortDisplayResult, offensivePlays, yardLineFPStart, yardsToEndzoneFPStart)
                print "yards: {} deltaScore: {} homeIsOffense {} team {}".format(yards, deltaOffenseScore, homeIsOffense,teamAbbr)

                flipField = False
                if yardLineFPStart != yardsToEndzoneFPStart:
                    endYard = 100 - endYard

                    flipField = True
                

                for count, play in enumerate(drive['plays']):
                    #print play
                    if 'type' not in play: continue
                    downDict = {}

                    playYardLineStart = play['start']['yardLine'] 

                    if flipField : playYardLineStart = 100-playYardLineStart
                    down = (play['start']['down'])
                    if down > 0: 
                        #print down
                        downCount[down-1] = downCount[down-1] +1
                    distanceToGo = play['start']['distance']
                    endYardToEndZonePlay = play['end']['yardsToEndzone']
                    typePlay = play['type']['text']

                    downDict['playYardLineStart'] =playYardLineStart
                    downDict['down']    = down   
                    downDict['distanceToGo']    = distanceToGo   
                    downDict['shortDisplayResult']  = shortDisplayResult   
                    downDict['yardsToEndzoneFPStart']   = yardsToEndzoneFPStart     
                    downDict['deltaOffenseScore']   = deltaOffenseScore   
                    downDict['endYardToEndZone']    = endYardToEndZone   
                    downDict['endYardToEndZonePlay']    = endYardToEndZonePlay   
                    downDict['typePlay']    = typePlay   
                    downDict['downCount']   = downCount[down-1]   

                    jsonString =  jsonString + ", \n" + json.dumps(downDict)
                    #print "playYardLineStart {} down {} distanceToGo {} result {} {} score {} yardsToEndzoneFPStart {} type {}  downCount {}".format(playYardLineStart, down, distanceToGo, shortDisplayResult,yardsToEndzoneFPStart ,deltaOffenseScore, endYardToEndZone, typePlay, downCount[down-1])

        if sumScoreHome - scoreHome == 0 and sumScoreAway - scoreAway == 0:
               #if first:
                   jsonFile.write(jsonString)
                   #first = False
              # else:
                  # jsonFile.write(", \n " + jsonString)




jsonFile.write("]")
jsonFile.close()

