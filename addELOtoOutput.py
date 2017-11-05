import numpy
import math
import matplotlib
import matplotlib.pyplot as plt
import csv
from scipy.stats import poisson, norm
import pickle


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
        self.predWin = [.5]
        self.obsWin = [.5]
        self.predWinFast = [.5]
        self.st = [1500]
        self.bt = [0]
        self.Ft = [1500]
        self.year = [int(year)]
        self.week = [get_week(week)]
        self.home = [True]
        self.nGames = 0
        self.id = teamId
        self.name = teamName

    def returnEloByTime(self, year, week):
        year = int(year)
        week = get_week(week)
        goal = week + year*100

        elo = -1000
        for i in range(self.nGames):
            current = self.week[i] + self.year[i]*100
            print "name: {} i: {} week: {}  year: {} looking at week: {} year: {} elo: {}".format(self.name, i, week, year, self.week[i], self.year[i], self.elo[i])
            if (goal - current) < 5:
                elo = self.elo[i]
            if goal == current and i != 0:
                elo = self.elo[i]
                break
            if goal < current and week!=16: break
        print self.elo
        return elo

    def probCountAGreaterThanB(self, countA, countB):
        prob = 0
        integral_factor = 5
        for i in range((int(countA+countB)+1)*integral_factor):
            dprob = poisson.pmf(i, countB)*poisson.sf(i, countA)
            prob = prob + dprob
            if dprob < .0001: break
        return prob

    def double_exp_smooth(self, verbose): 
        nGames = self.nGames
        week = self.week[nGames]
        st = self.st[nGames]
        st1 = self.st[nGames-1]
        bt = self.bt[nGames]
        bt1 = self.bt[nGames-1]
        Ft = self.Ft[nGames]
        eloPerformance = self.elo[nGames+1]
        if nGames == 0:
            st = eloPerformance
            bt = 0
            self.st.append(st)
            self.bt.append(0)
        if nGames == 1:
            st = eloPerformance
            bt = 0
            lastEloPerformance = self.elo[nGames] 
            self.st.append(st)
            self.bt.append(eloPerformance - lastEloPerformance)
        else:
            alpha = .1
            beta = .1
            st = alpha*eloPerformance + (1-alpha)*(st+bt)
            bt = beta*(st-st1)+(1-beta)*bt1
            
            self.st.append(st)
            self.bt.append(bt)
        Ft = st +bt
        self.Ft.append(Ft)
        if verbose: print "st: {} bt: {} Ft: {}".format(st, bt, Ft)

    def obsWinProb(self, countA, countB):
        homeWinProb = self.probCountAGreaterThanB(countA,countB)
        awayWinProb = self.probCountAGreaterThanB(countB,countA)
        homeWinProbAdjusted = (homeWinProb)/(homeWinProb + awayWinProb) 
        return homeWinProbAdjusted

    def computedWinProb(self, homeElo, awayElo):
        return 1/(10**(-( float(homeElo) - float(awayElo))/400) +1 ) 

    def computeElofromProb(self, prob):
         return (-math.log(1/prob -1)/math.log(10)*400)

    def addGame(self, newElo, eloPerformance, predWin, osbWin, year, week, home):
        self.elo.append(newElo)
        self.eloPerformance.append(eloPerformance)
        self.year.append(int(year))
        self.week.append(get_week(week))
        self.home.append(home)
        self.double_exp_smooth(True)
        self.predWin.append(predWin)
        self.obsWin.append(osbWin)
        self.nGames = self.nGames  +1

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

        elo = elo + kFactor*(obsProb - predProb)
        opponentElo = opponentElo - kFactor*(obsProb-predProb)

        eloPerformance = opponentElo + self.computeElofromProb(obsProb)
        opponentEloPerformance = elo - self.computeElofromProb(obsProb)

       

        if verbose: print "uptdated elo: {} opponent elo: {} elo performance: {} opponent elo performance: {} k factor: {}".format(elo, opponentElo, eloPerformance, opponentEloPerformance, kFactor)
        self.addGame(elo, eloPerformance, predProb, obsProb, year, week, True)
        oponenetClass.addGame(opponentElo, opponentEloPerformance, 1.0-predProb, 1.0-obsProb, year, week, False)
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
    if year > 2007: break

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