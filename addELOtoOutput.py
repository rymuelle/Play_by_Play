import numpy
import math
import matplotlib
import matplotlib.pyplot as plt
import csv
from scipy.stats import poisson, norm
import pickle
from teamClass import team


reader = csv.DictReader(open("output.csv"), delimiter = '\t') 

f = open('output_step2.csv','wb')
field_names=["gameId", "homeTeam", "homeId", "awayTeam", "awayId", "year", "week", "homeScore", "awayScore", "nHomeTD", "nAwayTD", "HomeOffenseScore", "HomeDefenseScore", "AwayOffenseScore", "AwayDefenseScore", "homeElo", "awayElo", "predWin", "homeEloFast", "awayEloFast", "predWinFast" ,"homeEloPerformance", "awayEloPerformance" ,"obsWin"]
w = csv.DictWriter(f,fieldnames=field_names, delimiter='\t')
w.writeheader()

#crossElo = {}

def get_week(s):
    try:
        int(s)
        return int(s)
    except ValueError:
        return 16


teamDict = {}

double_smoothing = {}
teamElo = {}
teamEloFast = {}
teamID_to_Ab = {}
for row in reader:
   # if row['year'] == "2006": break

    print "\n"

    print "game ID ", row['gameId']


    
    writeDict = {}
    for key in row:
        if key in field_names:
            writeDict[key] = row[key]

    year = int(row['year'])
    week = get_week(row['week'])

    homeId = row['homeId']
    homeTeam = row['homeTeam']
    awayTeam = row['awayTeam']
    awayId = row['awayId']
    teamID_to_Ab[homeId]=  row['homeTeam']
    teamID_to_Ab[awayId]=  row['awayTeam']

    homeScore = float(row['homeScore'])
    awayScore = float(row['awayScore'])
    #if year > 2007: break

    if homeId not in teamDict:
        teamDict[homeId] = team(year, week, homeId, homeTeam)
    if awayId not in teamDict:
        teamDict[awayId] = team(year, week, awayId, awayTeam)

    kFactor = 120 +80/week
    teamDict[homeId].newGame(homeScore, awayScore, kFactor, teamDict[awayId], year, week, True)

    nGamesHome =  int(teamDict[homeId].nGames)
    nGamesAway =  int(teamDict[awayId].nGames)
    writeDict["predWin"] = round(teamDict[homeId].predWin[nGamesHome],3)
    writeDict["predWinFast"] = 0
    writeDict["obsWin"] = round(teamDict[homeId].obsWin[nGamesHome],3 )
    writeDict["homeEloPerformance"] = int(teamDict[homeId].eloPerformance[nGamesHome])
    writeDict["awayEloPerformance"] = int(teamDict[awayId].eloPerformance[nGamesAway])
    writeDict["homeElo"] = int(teamDict[homeId].elo[nGamesHome])
    writeDict["awayElo"] = int(teamDict[awayId].elo[nGamesAway])
    writeDict["homeEloFast"] = int(teamDict[homeId].Ft[nGamesHome])
    writeDict["awayEloFast"] = int(teamDict[awayId].Ft[nGamesAway])
    w.writerow(writeDict)


pickleFile  = open('pickledTeamDict.dat','wb')
pickle.dump(teamDict, pickleFile)
pickleFile.close()

print "\n"



#keylist = teamElo.keys()
#
#
#rank = 1
#eloArray = []
#for key in teamElo:
#    if "count" not in key: eloArray.append([key, teamEloFast[key]])
#
#
#eloArray.sort(key = lambda x: x[1], reverse=True)
#
#
#for team in eloArray:
#    print rank, teamID_to_Ab[team[0]], team[1]
#    rank = rank +1
#
#print "\n"
#
#f.close
#