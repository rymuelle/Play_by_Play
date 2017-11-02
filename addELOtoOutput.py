import numpy
import matplotlib
import matplotlib.pyplot as plt
import csv
from scipy.stats import poisson

reader = csv.DictReader(open("output.csv"), delimiter = '\t') 

f = open('output_step2.csv','wb')
field_names=["gameId", "homeTeam", "homeId", "awayTeam", "awayId", "year", "homeScore", "awayScore", "nHomeTD", "nAwayTD", "HomeOffenseScore", "HomeDefenseScore", "AwayOffenseScore", "AwayDefenseScore", "homeElo", "awayElo", "predWin", "obsWin"]
w = csv.DictWriter(f,fieldnames=field_names, delimiter='\t')
w.writeheader()

teamElo = {}
teamID_to_Ab = {}
for row in reader:
    #if row['year'] == "2004": break

    print "\n"

    print "game ID ", row['gameId']


  
    writeDict = {}
    for key in row:
        if key in field_names:
            writeDict[key] = row[key]

    homeId = row['homeId']
    awayId = row['awayId']
    teamID_to_Ab[homeId]=  row['homeTeam']
    teamID_to_Ab[awayId]=  row['awayTeam']

    # set default elo to new teams
    if homeId not in teamElo.keys():
        teamElo[homeId] = 1500
        teamElo[homeId+"_count"] = 0
    if awayId not in teamElo.keys():
        teamElo[awayId] = 1500
        teamElo[awayId+"_count"] = 0

    teamElo[awayId+"_count"] = int(teamElo[awayId+"_count"]) + 1 
    teamElo[homeId+"_count"] = int(teamElo[homeId+"_count"]) + 1 
    teamCountTotal = int(teamElo[awayId+"_count"]) + int(teamElo[homeId+"_count"])
    print "team count total ", teamCountTotal

    #get elo from temp dict

    homeElo = float(teamElo[homeId])
    awayElo = float(teamElo[awayId])

    #get scores and divide by 7, this is approximating scores as all TDs and poissions
    homeScore = (float(row['homeScore'])/7)+.1
    awayScore = (float(row['awayScore'])/7)+.1

    # calculated expected prob
    homeWinPred = 1/(10**(-( homeElo - awayElo)/400) +1 ) 
    writeDict["predWin"] = round(homeWinPred,3)
    print "starting Elo " , int(teamElo[homeId]), int(teamElo[awayId]), " win prediction ", homeWinPred, " score ", homeScore, awayScore
    # calculate observed prob
    homeWinProb = 0
    for i in range(int(homeScore+awayScore)*10):
        homeWinProb = homeWinProb + poisson.pmf(i, awayScore)*poisson.sf(i, homeScore)
    

    awayWinProb = 0
    for i in range(int(homeScore+awayScore)*10):
        awayWinProb = awayWinProb + poisson.pmf(i, homeScore)*poisson.sf(i, awayScore)
        
    #adjust win prob to get rid of tie problem resulting in lower than expected win probs
    print "prob home, away ", homeWinProb, awayWinProb, row['homeScore'], row['awayScore']

    writeDict["obsWin"] = 0
    if (homeWinProb+awayWinProb) != 0: 
        adjustedHomeWinProb = homeWinProb/(homeWinProb+awayWinProb)
    
        adjustedAwayWinProb = awayWinProb/(homeWinProb+awayWinProb)
    
        print "adjprob home", adjustedHomeWinProb, adjustedAwayWinProb

        writeDict["obsWin"] = round(adjustedHomeWinProb,3)
    
    
        def get_week(s):
            try:
                int(s)
                return int(s)
            except ValueError:
                return 16
    
        #update ELOs
        
        week = get_week(row['week'])
    
    
        print "year, week ", row['year'], week
        k = (24 + 200/(teamCountTotal + 2) + 80/(week))
        homeElo = (homeElo + k*(adjustedHomeWinProb - homeWinPred))
        awayElo = (awayElo + k*(adjustedAwayWinProb - (1.0-homeWinPred)))
        
        print "k factor ", k
    
        
        teamElo[homeId] = homeElo
    
        
        teamElo[awayId] = awayElo
    

        print "new Elo ", int(teamElo[homeId]), int(teamElo[awayId])
        homeElo = float(teamElo[homeId])
        awayElo = float(teamElo[awayId])
        homeWinPred = 1/(10**(-( homeElo - awayElo)/400) +1 ) 
        print "new home win prediction ", homeWinPred
    writeDict["homeElo"] = int(homeElo)
    writeDict["awayElo"] = int(awayElo)
    w.writerow(writeDict)


keylist = teamElo.keys()

rank = 1
eloArray = []
for key in teamElo:
    if "count" not in key: eloArray.append([key, teamElo[key]])


eloArray.sort(key = lambda x: x[1], reverse=True)


for team in eloArray:
    print rank, teamID_to_Ab[team[0]], team[1]
    rank = rank +1



f.close
