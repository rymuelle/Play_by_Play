import numpy
import math
import matplotlib
import matplotlib.pyplot as plt
import csv
from scipy.stats import poisson, norm
#import pickle

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

class team():
    
    def __init__(self, year, week, teamId, teamName):
        self.elo = [1500]
        self.eloPerformance = [1500]
        self.year = [int(year)]
        self.week = [get_week(week)]
        self.home = []
        self.nGames = 0
        self.id = teamId
        self.name = teamName

    def probCountAGreaterThanB(self, countA, countB):
        prob = 0
        integral_factor = 5
        for i in range(int(countA+countB)*integral_factor):
            dprob = poisson.pmf(i, countB)*poisson.sf(i, countA)
            prob = prob + dprob
            if dprob < .0001: break
        return prob

    def obsWinProb(self, countA, countB):
        homeWinProb = self.probCountAGreaterThanB(countA,countB)
        awayWinProb = self.probCountAGreaterThanB(countB,countA)
        homeWinProbAdjusted = (homeWinProb)/(homeWinProb + awayWinProb)
        return homeWinProbAdjusted

    def computedWinProb(self, homeElo, awayElo):
        return 1/(10**(-( float(homeElo) - float(awayElo))/400) +1 ) 

    def computeElofromProb(self, prob):
         return (-math.log(1/prob -1)/math.log(10)*400)

    def addGame(self, newElo, eloPerformance, year, week, home):
        self.nGames = self.nGames  +1
        self.elo.append(newElo)
        self.eloPerformance.append(eloPerformance)
        self.year.append(int(year))
        self.week.append(get_week(week))
        self.home.append(home)

    def returnElo(self):
        return self.elo[self.nGames]


    def newGame(self, score, opponentScore, kFactor, oponenetClass, year, week, verbose):
        elo = self.elo[self.nGames]
        score = float(score)/7.0 + .1
        opponentScore = float(opponentScore)/7.0 + .1

        opponentElo = oponenetClass.returnElo()

        if verbose: print "year: {} week: {}".format(year, week)
        if verbose: print "home Team: {} away Team: {}".format(self.name, oponenetClass.name)
       
        predProb = self.computedWinProb(elo, opponentElo)
        obsProb = self.obsWinProb(score, opponentScore)
        if verbose: print "elo: {} opponent elo: {} win prediction: {} score: {} {} obsWinProb: {}".format(elo, opponentElo, predProb, score, opponentScore, obsProb)

        eloPerformance = opponentElo + self.computeElofromProb(obsProb)
        opponentEloPerformance = elo - self.computeElofromProb(obsProb)

        elo = elo + kFactor*(obsProb - predProb)
        opponentElo = opponentElo - kFactor*(obsProb-predProb)

        if verbose: print "uptdated elo: {} opponent elo: {} elo performance: {} opponent elo performance: {} k factor: {}".format(elo, opponentElo, eloPerformance, opponentEloPerformance, kFactor)
        self.addGame(elo, eloPerformance, year, week, True)
        oponenetClass.addGame(opponentElo, opponentEloPerformance, year, week, False)
        #add stuff


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

    year = row['year']
    week = get_week(row['week'])

    homeId = row['homeId']
    homeTeam = row['homeTeam']
    awayTeam = row['awayTeam']
    awayId = row['awayId']
    teamID_to_Ab[homeId]=  row['homeTeam']
    teamID_to_Ab[awayId]=  row['awayTeam']

    homeScore = float(row['homeScore'])
    awayScore = float(row['awayScore'])

    if homeId not in teamDict:
        teamDict[homeId] = team(year, week, homeId, homeTeam)
    if awayId not in teamDict:
        teamDict[awayId] = team(year, week, awayId, awayTeam)

    kFactor = 120 +80/week
    teamDict[homeId].newGame(homeScore, awayScore, kFactor, teamDict[awayId], year, week, True)

    # set default elo to new teams
    if homeId not in teamElo.keys():
        #crossElo[homeId] = 0

      
        double_smoothing[homeId] = {"st": 0, "st-1":0, "bt": 0, "bt-1":0, "F+": 0}
        teamElo[homeId] = 1500
        teamElo[homeId+"_count"] = 0
        teamEloFast[homeId] = 1500
    if awayId not in teamElo.keys():
       # crossElo[awayId] = 0
        double_smoothing[awayId] = {"st": 0, "st-1":0, "bt": 0, "bt-1":0, "F+": 0}
        teamElo[awayId] = 1500
        teamElo[awayId+"_count"] = 0
        teamEloFast[awayId] = 1500

    #if homeId > awayId:
    #    if homeId not in crossElo:
    #        crossElo[homeId] = {}
    #    if awayId not in crossElo[homeId]:
    #        crossElo[homeId][awayId] = 0
    #if awayId > homeId:
    #    if awayId not in crossElo:
    #        crossElo[awayId]  = {}
    #    if awayId not in crossElo[awayId]:
    #        crossElo[homeId][homeId] = 0


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
    
    

    
        #update ELOs
        
        week = get_week(row['week'])
    
    
        print "year, week ", row['year'], week
        kRaw = 24
 
        
        #homeWinValuePred = norm.ppf(homeWinPred)
        #homeWinValuePredFast = norm.ppf(homeWinPredFast)
        #homeWinValueObs = norm.ppf(adjustedHomeWinProb)
        homeWinValuePred = homeWinPred
        homeWinValuePredFast = homeWinPredFast #homeEloFast-awayEloFast
        homeWinValueObs = adjustedHomeWinProb
        print "obs, pred, predFast: ", homeWinValueObs, homeWinValuePred, homeWinValuePredFast

        if homeElo-awayElo  != 0: print -math.log(1/homeWinPred -1)/math.log(10)*400 , homeElo-awayElo 

        #k = (kRaw*chaosFactor + 200/(teamCountTotal + 2) + 80/(week))
        k = 120 +80/week
        chaosFactor = 1
        #chaosFactor = (abs(homeEloFast-homeElo) + abs(awayEloFast - awayElo))/(k)

        homeElo = (homeElo + k*(homeWinValueObs - homeWinValuePred))
        awayElo = (awayElo - k*(homeWinValueObs - homeWinValuePred))
        #kFast = (k + 160/(week+2))#200/(teamCountTotal + 2) + 80/(week))
        kFast = .04 +.02/week
        if adjustedHomeWinProb > .99: adjustedHomeWinProb = .99
        #homeEloFast = (homeEloFast + kFast*(-math.log(1/adjustedHomeWinProb -1)/math.log(10)*400  - homeWinValuePredFast))
        #awayEloFast = (awayEloFast - kFast*(-math.log(1/adjustedHomeWinProb -1)/math.log(10)*400  - homeWinValuePredFast))
        
        homeEloPerformance = (-math.log(1/adjustedHomeWinProb -1)/math.log(10)*400) + awayElo
        awayEloPerformance = ( math.log(1/adjustedHomeWinProb -1)/math.log(10)*400) + homeElo

        writeDict["homeEloPerformance"] = int(homeEloPerformance)
        writeDict["awayEloPerformance"] = int(awayEloPerformance)


        def double_exp_smooth(smoothingDict, eloPerformance):
            st = smoothingDict['st'] 
            bt = smoothingDict['bt']
            st1 = smoothingDict['st-1'] 
            bt1 = smoothingDict['bt-1']  

            if week == 1:
                st = eloPerformance
                bt = 0

            if week == 2: 
                st = eloPerformance 
                bt = 0 
            else:
                alpha = .5
                beta = 0.1
                st1 = st
                bt1 = bt
                st = alpha*eloPerformance + (1-alpha)*(st+bt)
                bt = beta*(st-st1)+(1-beta)*bt1
            Ft = st + bt
            print "predicted Elo: {}, Elo perf: {}, st: {}, bt: {}".format(Ft,eloPerformance,st,bt)
            smoothingDict = {"st": st, "st-1": st1, "bt": bt, "bt-1":bt1, "F+": Ft}
            return smoothingDict

        double_smoothing[homeId] = double_exp_smooth(double_smoothing[homeId], homeElo)
        double_smoothing[awayId] = double_exp_smooth(double_smoothing[awayId], awayElo)
        homeEloFast = int(double_smoothing[homeId]['F+'])
        awayEloFast = int(double_smoothing[awayId]['F+'])
    


        print "k factor , kFast , chaos factor", k, kFast, chaosFactor
    
        
        teamElo[homeId] = homeElo  
        teamElo[awayId] = awayElo

        teamEloFast[homeId] = homeEloFast
        teamEloFast[awayId] = awayEloFast
    
        print "elo performance rating home: {}, away: {}".format(int(homeEloPerformance),int(awayEloPerformance))
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
    if "count" not in key: eloArray.append([key, teamEloFast[key]])


eloArray.sort(key = lambda x: x[1], reverse=True)


for team in eloArray:
    print rank, teamID_to_Ab[team[0]], team[1]
    rank = rank +1

print "\n"

print crossElo
f.close
