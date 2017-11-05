import numpy
import math
import matplotlib
import matplotlib.pyplot as plt
import csv
from scipy.stats import poisson, norm
import pickle

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
            #print "name: {} i: {} week: {}  year: {} looking at week: {} year: {} elo: {}".format(self.name, i, week, year, self.week[i], self.year[i], self.elo[i])
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