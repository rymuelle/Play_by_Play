import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import json
import numpy 
import math
import pprint
from fileListJSON_sorted import fileListJson  


jsonFile = open("gameSummaryJsonForRanking.txt", "w")
jsonFile.write("[")
first =  True



def valueDown(startDown, assumedFirstDownYard, distanceToGo):
    startValue = 4.97 - .0565*assumedFirstDownYard
    #print "down {} first down yard {} first down value {} distance to go {}".format(startDown, assumedFirstDownYard, startValue , distanceToGo)
    if startDown == 1:
        startValue = startValue + .918 - .13*distanceToGo + .0011*distanceToGo**2
    if startDown == 2:
        startValue = startValue + 1.03 - .19*distanceToGo + .0028*distanceToGo**2
    if startDown == 3:
        startValue = startValue + .308 - .19*distanceToGo + .00311*distanceToGo**2
    if startDown == 4:
        startValue = startValue -1.11 - .137*distanceToGo + .00245*distanceToGo**2
    return startValue

def downValue(play):
    filedIsFliped = False
    if play['end']['yardsToEndzone'] != play['end']['yardLine']:
        filedIsFliped = True

    startDown = play['start']['down'] 
    endDown = play['end']['down'] 
    
    startYards =  play['start']['yardLine'] 
    endYards =  play['end']['yardLine']  

    if filedIsFliped:
        startYards = 100 - startYards
        endYards = 100 - endYards

    if startDown < 0 or startDown>4: "bad down value: {}".format(down)

    distanceToGoStart = play['start']['distance']
    distanceToGoEnd = play['start']['distance']

    assumedFirstDownYard = 10-distanceToGoStart + startYards

    startValue = valueDown(startDown, assumedFirstDownYard, startYards)
    
    assumedFirstDownYardEnd = 10-distanceToGoEnd + endYards

    endValue = valueDown(endDown, assumedFirstDownYard, startYards)


    return endValue - startValue
    

    


for file in fileListJson:
    with open(file, 'r') as f:
        gameId = 0
        datastore = json.load(f)

        #pprint.pprint(datastore, width=1) 
        gameId =  datastore['competitions'][0]['id']

        year = datastore['season']['year']

        if year < 2017: continue
       
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
        playDict = {}
        previousScore = [0,0 ]
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
                #print "isScore {} shortDisplayResult {} offensivePlays {} yardLineFPStart {} yardsToEndzoneFPStart {}".format(isScore, shortDisplayResult, offensivePlays, yardLineFPStart, yardsToEndzoneFPStart)
                #print "yards: {} deltaScore: {} homeIsOffense {} team {}".format(yards, deltaOffenseScore, homeIsOffense,teamAbbr)

                flipField = False
                if yardLineFPStart != yardsToEndzoneFPStart:
                    endYard = 100 - endYard

                    flipField = True
                

                
                for count, play in enumerate(drive['plays']):

                    currentScore = [play['homeScore'],play['awayScore'] ]
                   
                    if 'type' not in play: 
                        print "----------------missing play type 1------------------------"
                        pprint.pprint(tempDict)
                        continue
                    if 'abbreviation' not in play['type']: continue
                    tempDict = {}

                    tempDict["playType"] = play['type']["abbreviation"]
                    tempDict["playId"] = play['type']["id"]
                    tempDict["playText"] = play['type']["text"]

                    missingPlayFlag = False
                   # print tempDict["playType"]
                    if  "shortDownDistanceText" not in  play['start'] : 
                        print "----------------missing play 2------------------------"
                        pprint.pprint(tempDict)
                        #missingPlayFlag = True
                        #print "missingPlayFlag"
                        continue

                    tempDict["startTeam"] = play['start']['team']['id']
                    tempDict["startDown"] = play['start']['down']
                    tempDict["startDistanceToEndzone"] = play['start']['yardsToEndzone']
                   # print play['start']
                    tempDict["startShortDownDistanceText"] = play['start']['shortDownDistanceText']
                    startShortDownDistanceTextArray = tempDict["startShortDownDistanceText"].split(" ")
                    tempDict["startDistanceToFirstDown"] = (startShortDownDistanceTextArray[len(startShortDownDistanceTextArray)-1])
                    tempDict["startDistanceToFirstDown"] = play['start']['distance']
                    #tempDict["startYardsToEndzone"] = play['start']['yardsToEndzone']
                    #print play['end']

                    if "shortDownDistanceText" in  play['end']:

                        tempDict["endTeam"] = play['end']['team']['id']
                        tempDict["endDown"] = play['end']['down']
                        tempDict["endDistanceToEndzone"] = play['end']['yardsToEndzone']
                        tempDict["endShortDownDistanceText"] = play['end']['shortDownDistanceText']
                        endShortDownDistanceTextArray = tempDict["endShortDownDistanceText"].split(" ")
                        tempDict["endDistanceToFirstDown"] = (endShortDownDistanceTextArray[len(endShortDownDistanceTextArray)-1])
                        tempDict["endDistanceToFirstDown"] = play['end']['distance']
    
                        if "Goal" == tempDict["endDistanceToFirstDown"]:
                            tempDict["endDistanceToFirstDown"] = tempDict["endDistanceToEndzone"]
                        if "Goal" == tempDict["startDistanceToFirstDown"]:
                            tempDict["startDistanceToFirstDown"] = tempDict["startDistanceToEndzone"]
    
                        tempDict["startDistanceToFirstDown"] = int(tempDict["startDistanceToFirstDown"])
                        tempDict["endDistanceToFirstDown"] = int(tempDict["endDistanceToFirstDown"])

                        endAssumedFirstDownYard = 10 - int(tempDict['endDistanceToFirstDown']) + tempDict["endDistanceToEndzone"]
                        endValue = valueDown(tempDict['endDown'], endAssumedFirstDownYard, tempDict["endDistanceToFirstDown"])
                    elif "TD" in tempDict["playType"] or "EP" in tempDict["playType"] or "FG" in tempDict["playType"]:
                        endValue = currentScore[0] -  previousScore[0] - (currentScore[1] -  previousScore[1])
                        tempDict["endTeam"] = play['end']['team']['id']
                        if not homeIsOffense: endValue = -endValue
                    else: 
                        #print "----------------missing play 2------------------------"
                        #pprint.pprint(tempDict)
                        continue

                   # if  tempDict["endDistanceToFirstDown"] == "Goal" or tempDict["startDistanceToFirstDown"] == "Goal": continue
                    #tempDict["endYardsToEndzone"] = play['end']['yardsToEndzone']

                    startAssumedFirstDownYard = 10 - int(tempDict['startDistanceToFirstDown']) + tempDict["startDistanceToEndzone"]
                    #endAssumedFirstDownYard = 10 - int(tempDict['endDistanceToFirstDown']) + tempDict["endDistanceToEndzone"]

                    startValue = valueDown(tempDict['startDown'], startAssumedFirstDownYard, tempDict["startDistanceToFirstDown"])
                    #endValue = valueDown(tempDict['endDown'], endAssumedFirstDownYard, tempDict["endDistanceToFirstDown"])

                    if tempDict["startTeam"] !=  tempDict["endTeam"]: endValue = -1*endValue
                    #pprint.pprint(tempDict)


                    if "ickoff" in tempDict["playText"] : 
                        startValue = -1

                    #print "value start {} end {}  \t delta {} type {} ".format(startValue,endValue, endValue- startValue, tempDict["playType"] )
                    
                    previousScore = [play['homeScore'],play['awayScore'] ]

                    if tempDict["startTeam"] not in playDict:
                        playDict[tempDict["startTeam"]] = {}
                    if tempDict["playType"] not in playDict[tempDict["startTeam"]]:
                        playDict[tempDict["startTeam"]][tempDict["playType"]] = 0.0

                    #print playDict[tempDict["startTeam"]][tempDict["playType"]], playDict[tempDict["startTeam"]][tempDict["playType"]] + endValue - startValue
                    playDict[tempDict["startTeam"]][tempDict["playType"]] =  playDict[tempDict["startTeam"]][tempDict["playType"]] + endValue - startValue

        pprint.pprint(playDict)

        #for team in playDict:
        #    value = 0.0
        #    for play in team:
        #        value = play + value
        #    print "team {} total value {}".format(team,value)
                  
        #if sumScoreHome - scoreHome == 0 and sumScoreAway - scoreAway == 0:
               #if first:
                   #jsonFile.write(jsonString)
                   #first = False
              # else:
                  # jsonFile.write(", \n " + jsonString)




jsonFile.write("]")
jsonFile.close()

