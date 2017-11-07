import numpy
import math
import matplotlib
import matplotlib.pyplot as plt
import csv
from scipy.stats import poisson, norm
import pickle



#"gameId","year","week","homeId","homeTeam","homeAbbr","awayId","awayTeam","awayAbbr","driveIndex","playIndex","offenseId","offenseTeam","offenseAbbr","defenseId","defenseTeam",
#"defenseAbbr","homeScore","awayScore","isScoringPlay","quarter","clock","type","down","distance","yardLine","yardsGained","endYardLine","description"

#field_names=["gameId", "homeTeam", "homeId", "awayTeam", "awayId", "year", "week", 
#"homeScore", "awayScore", "nHomeTD", "nAwayTD", "HomeOffenseScore", "HomeDefenseScore", "AwayOffenseScore", "AwayDefenseScore", "elo", "eloOffense", "eloDefense"]

def get_week(s):
    try:
        int(s)
        return int(s)
    except ValueError:
        return 16

class play():
	def __init__(self, playDict):
		playDict['offenseId'] = self.offense 

class drive():
	def __init__(self, playDict):
		self.driveIndex = playDict["driveIndex"]

		self.quarter = playDict["quarter"]
		self.clockStart = playDict['clock'].split(":")
		self.clockEnd = [0,0]

		self.driveStart = playDict["yardLine"]
		self.driveEnd = -100

		self.result = -100





class game():
	def __init__(self, playDict, verbose):

		self.gameId  = playDict['gameId']

		self.homeID  = playDict['homeId']
		self.homeAbbr  = playDict['homeAbbr']
		self.awayID  = playDict['awayId']
		self.awayAbbr  = playDict['awayAbbr']

		self.year  = int(playDict['year'])
		self.week  = get_week(playDict['week'])
		clock = playDict['clock'].split(":")
		self.startTime  = int(clock[0]), int(clock[1])
		self.startHomeScore = int(playDict['homeScore'])
		self.startAwayScore = int(playDict['awayScore'])

		self.goodGame = False
		if clock[0] > 13 and  self.startHomeScore + self.startAwayScore < 7:
			self.goodGame = True
		
		self.drives = []
		self.nDrives = 0

		if(verbose > 10): print "gameId: {} homeTeam: {} awayTeam: {} year: {} week: {}".format(self.gameId, self.homeAbbr, self.awayAbbr, self.year, self.week) 


	def addPlay(self, playDict):
		if self.nDrives  != playDict['driveIndex']:
			print "new drive", playDict['driveIndex']
			self.nDrives = playDict['driveIndex']




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
        for i in range(self.nGames+1):
            current = self.week[i] + self.year[i]*100
            print "name: {} i: {} week: {}  year: {} looking at week: {} year: {} elo: {}".format(self.name, i, week, year, self.week[i], self.year[i], self.elo[i])
            if (goal - current) < 5:
                elo = self.elo[i]
            if goal == current and i != 0:
                elo = self.elo[i]
                break
            if goal < current and week!=16: break
        #print self.elo
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
            alpha = .05
            beta = .05
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