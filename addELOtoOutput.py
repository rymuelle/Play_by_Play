import numpy
import math
import matplotlib
import matplotlib.pyplot as plt
import csv
from scipy.stats import poisson, norm

reader = csv.DictReader(open("output.csv"), delimiter = '\t') 

f = open('output_step2.csv','wb')
field_names=["gameId", "homeTeam", "homeId", "awayTeam", "awayId", "year", "week", "homeScore", "awayScore", "nHomeTD", "nAwayTD", "HomeOffenseScore", "HomeDefenseScore", "AwayOffenseScore", "AwayDefenseScore", "homeElo", "awayElo", "predWin", "homeEloFast", "awayEloFast", "predWinFast" ,"obsWin"]
w = csv.DictWriter(f,fieldnames=field_names, delimiter='\t')
w.writeheader()

teamElo = {}
teamEloFast = {}
teamID_to_Ab = {}
for row in reader:
    #if row['year'] == "2007": break

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
        teamEloFast[homeId] = 1500
    if awayId not in teamElo.keys():
        teamElo[awayId] = 1500
        teamElo[awayId+"_count"] = 0
        teamEloFast[awayId] = 1500

    teamElo[awayId+"_count"] = int(teamElo[awayId+"_count"]) + 1 
    teamElo[homeId+"_count"] = int(teamElo[homeId+"_count"]) + 1 
    teamCountTotal = int(teamElo[awayId+"_count"]) + int(teamElo[homeId+"_count"])
    print "team count total ", teamCountTotal

    #get elo from temp dict

    homeElo = float(teamElo[homeId])
    awayElo = float(teamElo[awayId])

    homeEloFast = float(teamEloFast[homeId])
    awayEloFast = float(teamEloFast[awayId])

    #get scores and divide by 7, this is approximating scores as all TDs and poissions
    homeScore = (float(row['homeScore'])/7)+.1
    awayScore = (float(row['awayScore'])/7)+.1
    #homeScore = float(row['HomeOffenseScore'])/7+.1
    #awayScore = float(row['AwayOffenseScore'])/7+.1

    # calculated expected prob
    homeWinPred = 1/(10**(-( homeElo - awayElo)/400) +1 ) 
    homeWinPredFast = 1/(10**(-( homeEloFast - awayEloFast)/400) +1 ) 
    writeDict["predWin"] = round(homeWinPred,3)
    writeDict["predWinFast"] = round(homeWinPredFast,3)
    print "starting Elo " , int(teamElo[homeId]), int(teamElo[awayId]), " win prediction ", homeWinPred, " score ", homeScore, awayScore
    # calculate observed prob
    homeWinProb = 0
    integral_factor = 5
    for i in range(int(homeScore+awayScore)*integral_factor):
        dprob = poisson.pmf(i, awayScore)*poisson.sf(i, homeScore)
        homeWinProb = homeWinProb + dprob
        if dprob < .0001: break
       

    awayWinProb = 0
    for i in range(int(homeScore+awayScore)*integral_factor):
        dprob = poisson.pmf(i, homeScore)*poisson.sf(i, awayScore)
        awayWinProb = awayWinProb + dprob
        
        if dprob < .0001: break


        
    #adjust win prob to get rid of tie problem resulting in lower than expected win probs
    print "prob home, away ", homeWinProb, awayWinProb, homeScore, awayScore

    writeDict["obsWin"] = 0
    if (homeWinProb+awayWinProb) != 0: 
        adjustedHomeWinProb = homeWinProb/(homeWinProb+awayWinProb)
        #adjustedHomeWinProb = (homeScore - awayScore)
        #predScore = (homeElo - awayElo)/24
        #predScoreFast = (homeEloFast - awayEloFast)/240
    
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
        kRaw = 24
 
        
        #homeWinValuePred = norm.ppf(homeWinPred)
        #homeWinValuePredFast = norm.ppf(homeWinPredFast)
        #homeWinValueObs = norm.ppf(adjustedHomeWinProb)
        homeWinValuePred = homeWinPred
        homeWinValuePredFast = homeEloFast-awayEloFast
        homeWinValueObs = adjustedHomeWinProb
        print "obs, pred, predFast: ", homeWinValueObs, homeWinValuePred, homeWinValuePredFast

        if homeElo-awayElo  != 0: print -math.log(1/homeWinPred -1)/math.log(10)*400 , homeElo-awayElo 

        #k = (kRaw*chaosFactor + 200/(teamCountTotal + 2) + 80/(week))
        k = 120 +80/week
        chaosFactor = 1
        #chaosFactor = (abs(homeEloFast-homeElo) + abs(awayEloFast - awayElo))/(k)

        homeElo = (homeElo + chaosFactor*k*(homeWinValueObs - homeWinValuePred))
        awayElo = (awayElo - chaosFactor*k*(homeWinValueObs - homeWinValuePred))
        #kFast = (k + 160/(week+2))#200/(teamCountTotal + 2) + 80/(week))
        kFast = .04 +.02/week
        if adjustedHomeWinProb > .99: adjustedHomeWinProb = .99
        homeEloFast = (homeEloFast + kFast*(-math.log(1/adjustedHomeWinProb -1)/math.log(10)*400  - homeWinValuePredFast))
        awayEloFast = (awayEloFast - kFast*(-math.log(1/adjustedHomeWinProb -1)/math.log(10)*400  - homeWinValuePredFast))
     

        
        print "k factor , kFast , chaos factor", k, kFast, chaosFactor
    
        
        teamElo[homeId] = homeElo  
        teamElo[awayId] = awayElo

        teamEloFast[homeId] = homeEloFast
        teamEloFast[awayId] = awayEloFast
    

        print "new Elo , new EloFast", int(teamElo[homeId]), int(teamElo[awayId]), int(teamEloFast[homeId]), int(teamEloFast[awayId])
        homeElo = float(teamElo[homeId])
        awayElo = float(teamElo[awayId])
        homeWinPred = 1/(10**(-( homeElo - awayElo)/400) +1 ) 
        print "new home win prediction , fast , adjustment", homeWinPred, homeWinPredFast, k*(adjustedHomeWinProb - homeWinPred)
    writeDict["homeElo"] = int(homeElo)
    writeDict["awayElo"] = int(awayElo)
    writeDict["homeEloFast"] = int(homeEloFast)
    writeDict["awayEloFast"] = int(awayEloFast)
    w.writerow(writeDict)


print "\n"
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
