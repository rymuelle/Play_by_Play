import numpy
import matplotlib
import matplotlib.pyplot as plt
import csv
from scipy.stats import poisson

reader = csv.DictReader(open("output.csv"), delimiter = '\t') 

f = open('output_step2.csv','wb')
field_names=["gameId", "homeTeam", "homeId", "awayTeam", "awayId", "year", "homeScore", "awayScore", "nHomeTD", "nAwayTD", "HomeOffenseScore", "HomeDefenseScore", "AwayOffenseScore", "AwayDefenseScore", "homeElo", "awayElo"]
w = csv.DictWriter(f,fieldnames=field_names, delimiter='\t')
w.writeheader()

teamElo = {}
for row in reader:
    print "\n"

    print "game ID ", row['gameId']

    writeDict = {}
    for key in row:
        if key in field_names:
            writeDict[key] = row[key]

    homeId = row['homeId']
    awayId = row['awayId']
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
    print "starting Elo " , teamElo[homeId], teamElo[awayId], " win prediction ", homeWinPred, " score ", homeScore, awayScore
    # calculate observed prob
    homeWinProb = 0
    for i in range(int(homeScore+awayScore)*10):
        homeWinProb = homeWinProb + poisson.pmf(i, awayScore)*poisson.sf(i, homeScore)
    

    awayWinProb = 0
    for i in range(int(homeScore+awayScore)*10):
        awayWinProb = awayWinProb + poisson.pmf(i, homeScore)*poisson.sf(i, awayScore)
        
    #adjust win prob to get rid of tie problem resulting in lower than expected win probs
    print "prob home, away ", homeWinProb, awayWinProb, row['homeScore'], row['awayScore']

    if (homeWinProb+awayWinProb) == 0: continue
    adjustedHomeWinProb = homeWinProb/(homeWinProb+awayWinProb)

    adjustedAwayWinProb = awayWinProb/(homeWinProb+awayWinProb)

    print "adjprob home", adjustedHomeWinProb, adjustedAwayWinProb


    def get_week(s):
        try:
            int(s)
            return int(s)
        except ValueError:
            return 16

    #update ELOs
    
    week = get_week(row['week'])
    homeElo = homeElo + k*(adjustedHomeWinProb - homeWinPred)
    awayElo = awayElo + k*(adjustedAwayWinProb - (1.0-homeWinPred))

    print "year, week ", row['year'], week
    k = (24 + 200/(teamCountTotal + 2) + 80/(week))
    
    print "k factor ", k

    
    teamElo[homeId] = homeElo

    
    teamElo[awayId] = awayElo


    print "new Elo ", teamElo[homeId], teamElo[awayId]
    homeElo = float(teamElo[homeId])
    awayElo = float(teamElo[awayId])
    homeWinPred = 1/(10**(-( homeElo - awayElo)/400) +1 ) 
    print "new home win prediction ", homeWinPred
    writeDict["homeElo"] = homeElo
    writeDict["awayElo"] = awayElo
    w.writerow(writeDict)


print teamElo
