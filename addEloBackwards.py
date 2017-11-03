import numpy
import matplotlib
import matplotlib.pyplot as plt
import csv
from matplotlib.colors import LogNorm

test_week = 10
test_year = 2017
reader = csv.DictReader(open("output_step2.csv"), delimiter = '\t') 


f = open('output_backwards.csv','wb')
field_names=["gameId", "homeTeam", "homeId", "awayTeam", "awayId", "year", "week", "homeScore", "awayScore", "nHomeTD", "nAwayTD", "HomeOffenseScore", "HomeDefenseScore", "AwayOffenseScore", "AwayDefenseScore", "homeElo", "awayElo", "predWin", "homeEloBackwards", "awayEloBackwards", "homeEloFast", "awayEloFast", "homeWinPredFast" ,"obsWin"]
w = csv.DictWriter(f,fieldnames=field_names, delimiter='\t')
w.writeheader()


def get_week(s):
    try:
        int(s)
        return int(s)
    except ValueError:
        return 16

teamElo = {}
teamID_to_Ab = {}

for row in reversed(list(reader)):

    if get_week(row['week']) > test_week - 1: continue
    if int(row['year']) > test_year: continue
    if int(row['year']) < test_year: break

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
        teamElo[homeId] = row['homeElo']
        teamElo[homeId+"_count"] = 0
    if awayId not in teamElo.keys():
        teamElo[awayId] = row['awayElo']
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
    #homeScore = float(row['HomeOffenseScore'])/7+.1
    #awayScore = float(row['AwayOffenseScore'])/7+.1

    # calculated expected prob
    homeWinPred = 1/(10**(-( homeElo - awayElo)/400) +1 ) 
    
    writeDict["predWin"] = round(homeWinPred,3)
  
    print "starting Elo " , int(teamElo[homeId]), int(teamElo[awayId]), " win prediction ", homeWinPred, " score ", homeScore, awayScore
    # calculate observed prob
    homeWinProb = float(row['obsWin'])
    

    awayWinProb = 1.0-float(row['obsWin'])


        
    #adjust win prob to get rid of tie problem resulting in lower than expected win probs
    print "prob home, away ", homeWinProb, awayWinProb, homeScore, awayScore

    writeDict["obsWin"] = 0
    if (homeWinProb+awayWinProb) != 0: 
        adjustedHomeWinProb = homeWinProb

    
        adjustedAwayWinProb =awayWinProb
    
        print "adjprob home", adjustedHomeWinProb, adjustedAwayWinProb


        writeDict["obsWin"] = round(adjustedHomeWinProb,3)
    
    

    
        #update ELOs
        
        week = get_week(row['week'])
    
    
        print "year, week ", row['year'], week
        kRaw = 24
 
        
        #homeWinValuePred = norm.ppf(homeWinPred)
        #homeWinValuePredFast = norm.ppf(homeWinPredFast)
        #homeWinValueObs = norm.ppf(adjustedHomeWinProb)
        homeWinValuePred = homeWinPred
    
        homeWinValueObs = adjustedHomeWinProb
        print "obs, pred, predFast: ", homeWinValueObs, homeWinValuePred

        

        #k = (kRaw*chaosFactor + 200/(teamCountTotal + 2) + 80/(week))
        k =  24#(160 +200/week)*25
        chaosFactor = 1
        #chaosFactor = (abs(homeEloFast-homeElo) + abs(awayEloFast - awayElo))/(k)

        homeElo = (homeElo + chaosFactor*k*(homeWinValueObs - homeWinValuePred))
        awayElo = (awayElo - chaosFactor*k*(homeWinValueObs - homeWinValuePred))
        

        
        print "k factor ,  chaos factor", k,  chaosFactor
    
        
        teamElo[homeId] = homeElo  
        teamElo[awayId] = awayElo

    

        print "new Elo ", int(teamElo[homeId]), int(teamElo[awayId])
        homeElo = float(teamElo[homeId])
        awayElo = float(teamElo[awayId])
        homeWinPred = 1/(10**(-( homeElo - awayElo)/400) +1 ) 
        print "new home win prediction  , adjustment", homeWinPred, k*(adjustedHomeWinProb - homeWinPred)
    writeDict["homeEloBackwards"] = int(homeElo)
    writeDict["awayEloBackwards"] = int(awayElo)
    w.writerow(writeDict)
f.close()


reader2 = csv.DictReader(open("output_backwards.csv"), delimiter = '\t') 
f2 = open('output_backwards2.csv','wb')
w2 = csv.DictWriter(f2,fieldnames=field_names, delimiter='\t')
w2.writeheader()

print "------------------------------------"

for row in reader2:
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
        teamElo[homeId] = row['homeEloBackwards']
        teamElo[homeId+"_count"] = 0
    if awayId not in teamElo.keys():
        teamElo[awayId] = row['awayEloBackwards']
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
    #homeScore = float(row['HomeOffenseScore'])/7+.1
    #awayScore = float(row['AwayOffenseScore'])/7+.1

    # calculated expected prob
    homeWinPred = 1/(10**(-( homeElo - awayElo)/400) +1 ) 
    
    writeDict["predWin"] = round(homeWinPred,3)
  
    print "starting Elo " , int(teamElo[homeId]), int(teamElo[awayId]), " win prediction ", homeWinPred, " score ", homeScore, awayScore
    # calculate observed prob
    homeWinProb = float(row['obsWin'])
    

    awayWinProb = 1.0-float(row['obsWin'])


        
    #adjust win prob to get rid of tie problem resulting in lower than expected win probs
    print "prob home, away ", homeWinProb, awayWinProb, homeScore, awayScore

    writeDict["obsWin"] = 0
    if (homeWinProb+awayWinProb) != 0: 
        adjustedHomeWinProb = homeWinProb

    
        adjustedAwayWinProb =awayWinProb
    
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
    
        homeWinValueObs = adjustedHomeWinProb
        print "obs, pred, predFast: ", homeWinValueObs, homeWinValuePred

        

        #k = (kRaw*chaosFactor + 200/(teamCountTotal + 2) + 80/(week))
        k =  24#(160 +200/week)*.25        
        chaosFactor = 1
        #chaosFactor = (abs(homeEloFast-homeElo) + abs(awayEloFast - awayElo))/(k)

        homeElo = (homeElo + chaosFactor*k*(homeWinValueObs - homeWinValuePred))
        awayElo = (awayElo - chaosFactor*k*(homeWinValueObs - homeWinValuePred))
        

        
        print "k factor ,  chaos factor", k,  chaosFactor
    
        
        teamElo[homeId] = homeElo  
        teamElo[awayId] = awayElo

    

        print "new Elo ", int(teamElo[homeId]), int(teamElo[awayId])
        homeElo = float(teamElo[homeId])
        awayElo = float(teamElo[awayId])
        homeWinPred = 1/(10**(-( homeElo - awayElo)/400) +1 ) 
        print "new home win prediction  , adjustment", homeWinPred, k*(adjustedHomeWinProb - homeWinPred)
    writeDict["homeElo"] = int(homeElo)
    writeDict["awayElo"] = int(awayElo)
    w2.writerow(writeDict)

f2.close()


#----------------------------------------#


reader = csv.DictReader(open("output_backwards2.csv"), delimiter = '\t') 


f = open('output_backwards3.csv','wb')
field_names=["gameId", "homeTeam", "homeId", "awayTeam", "awayId", "year", "week", "homeScore", "awayScore", "nHomeTD", "nAwayTD", "HomeOffenseScore", "HomeDefenseScore", "AwayOffenseScore", "AwayDefenseScore", "homeElo", "awayElo", "predWin", "homeEloBackwards", "awayEloBackwards"  ,"obsWin"]
w = csv.DictWriter(f,fieldnames=field_names, delimiter='\t')
w.writeheader()

for row in reversed(list(reader)):

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
        teamElo[homeId] = row['homeElo']
        teamElo[homeId+"_count"] = 0
    if awayId not in teamElo.keys():
        teamElo[awayId] = row['awayElo']
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
    #homeScore = float(row['HomeOffenseScore'])/7+.1
    #awayScore = float(row['AwayOffenseScore'])/7+.1

    # calculated expected prob
    homeWinPred = 1/(10**(-( homeElo - awayElo)/400) +1 ) 
    
    writeDict["predWin"] = round(homeWinPred,3)
  
    print "starting Elo " , int(teamElo[homeId]), int(teamElo[awayId]), " win prediction ", homeWinPred, " score ", homeScore, awayScore
    # calculate observed prob
    homeWinProb = float(row['obsWin'])
    

    awayWinProb = 1.0-float(row['obsWin'])


        
    #adjust win prob to get rid of tie problem resulting in lower than expected win probs
    print "prob home, away ", homeWinProb, awayWinProb, homeScore, awayScore

    writeDict["obsWin"] = 0
    if (homeWinProb+awayWinProb) != 0: 
        adjustedHomeWinProb = homeWinProb

    
        adjustedAwayWinProb =awayWinProb
    
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
    
        homeWinValueObs = adjustedHomeWinProb
        print "obs, pred, predFast: ", homeWinValueObs, homeWinValuePred

        

        #k = (kRaw*chaosFactor + 200/(teamCountTotal + 2) + 80/(week))
        k =  24#(160 +200/week)*.2
        chaosFactor = 1
        #chaosFactor = (abs(homeEloFast-homeElo) + abs(awayEloFast - awayElo))/(k)

        homeElo = (homeElo + chaosFactor*k*(homeWinValueObs - homeWinValuePred))
        awayElo = (awayElo - chaosFactor*k*(homeWinValueObs - homeWinValuePred))
        

        
        print "k factor ,  chaos factor", k,  chaosFactor
    
        
        teamElo[homeId] = homeElo  
        teamElo[awayId] = awayElo

    

        print "new Elo ", int(teamElo[homeId]), int(teamElo[awayId])
        homeElo = float(teamElo[homeId])
        awayElo = float(teamElo[awayId])
        homeWinPred = 1/(10**(-( homeElo - awayElo)/400) +1 ) 
        print "new home win prediction  , adjustment", homeWinPred, k*(adjustedHomeWinProb - homeWinPred)
    writeDict["homeEloBackwards"] = int(homeElo)
    writeDict["awayEloBackwards"] = int(awayElo)
    w.writerow(writeDict)
f.close()


reader2 = csv.DictReader(open("output_backwards3.csv"), delimiter = '\t') 
f2 = open('output_backwards4.csv','wb')
w2 = csv.DictWriter(f2,fieldnames=field_names, delimiter='\t')
w2.writeheader()

print "------------------------------------"

for row in reader2:
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
        teamElo[homeId] = row['homeEloBackwards']
        teamElo[homeId+"_count"] = 0
    if awayId not in teamElo.keys():
        teamElo[awayId] = row['awayEloBackwards']
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
    #homeScore = float(row['HomeOffenseScore'])/7+.1
    #awayScore = float(row['AwayOffenseScore'])/7+.1

    # calculated expected prob
    homeWinPred = 1/(10**(-( homeElo - awayElo)/400) +1 ) 
    
    writeDict["predWin"] = round(homeWinPred,3)
  
    print "starting Elo " , int(teamElo[homeId]), int(teamElo[awayId]), " win prediction ", homeWinPred, " score ", homeScore, awayScore
    # calculate observed prob
    homeWinProb = float(row['obsWin'])
    

    awayWinProb = 1.0-float(row['obsWin'])


        
    #adjust win prob to get rid of tie problem resulting in lower than expected win probs
    print "prob home, away ", homeWinProb, awayWinProb, homeScore, awayScore

    writeDict["obsWin"] = 0
    if (homeWinProb+awayWinProb) != 0: 
        adjustedHomeWinProb = homeWinProb

    
        adjustedAwayWinProb =awayWinProb
    
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
    
        homeWinValueObs = adjustedHomeWinProb
        print "obs, pred, predFast: ", homeWinValueObs, homeWinValuePred

        

        #k = (kRaw*chaosFactor + 200/(teamCountTotal + 2) + 80/(week))
        k =  24#(160 +200/week)*.25
        chaosFactor = 1
        #chaosFactor = (abs(homeEloFast-homeElo) + abs(awayEloFast - awayElo))/(k)

        homeElo = (homeElo + chaosFactor*k*(homeWinValueObs - homeWinValuePred))
        awayElo = (awayElo - chaosFactor*k*(homeWinValueObs - homeWinValuePred))
        

        
        print "k factor ,  chaos factor", k,  chaosFactor
    
        
        teamElo[homeId] = homeElo  
        teamElo[awayId] = awayElo

    

        print "new Elo ", int(teamElo[homeId]), int(teamElo[awayId])
        homeElo = float(teamElo[homeId])
        awayElo = float(teamElo[awayId])
        homeWinPred = 1/(10**(-( homeElo - awayElo)/400) +1 ) 
        print "new home win prediction  , adjustment", homeWinPred, k*(adjustedHomeWinProb - homeWinPred)
    writeDict["homeElo"] = int(homeElo)
    writeDict["awayElo"] = int(awayElo)
    w2.writerow(writeDict)

f2.close()

reader = csv.DictReader(open("output_step2.csv"), delimiter = '\t') 

field_names=["gameId", "homeTeam", "homeId", "awayTeam", "awayId", "year", "week", "homeScore", "awayScore", "nHomeTD", "nAwayTD", "HomeOffenseScore", "HomeDefenseScore", "AwayOffenseScore", "AwayDefenseScore", "homeElo", "awayElo", "predWin", "homeEloBackwards", "awayEloBackwards", "homeEloFast", "awayEloFast", "predWinFast" ,"obsWin"]
f2 = open('output_backwards5.csv','wb')
w2 = csv.DictWriter(f2,fieldnames=field_names, delimiter='\t')
w2.writeheader()

for row in reversed(list(reader)):
    if int(row['year']) > test_year: continue
    if int(row['year']) < test_year: break
    if get_week(row['week']) > test_week: continue
    if get_week(row['week']) < test_week: break
    writeDict = {}
    for key in row:
        if key in field_names:
            writeDict[key] = row[key]
    if row['homeId'] in teamElo and row['awayId'] in teamElo:
        homeElo = teamElo[(row['homeId'])]
        awayElo = teamElo[(row['awayId'])]
        homeWinPred = 1/(10**(-( homeElo - awayElo)/400) +1 ) 
        writeDict["homeEloFast"] = int(homeElo)
        writeDict["awayEloFast"] = int(awayElo)
        writeDict["predWinFast"] = round(homeWinPred, 3)
        w2.writerow(writeDict)

f2.close()

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
