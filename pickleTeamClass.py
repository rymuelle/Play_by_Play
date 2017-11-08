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
    def __init__(self, playDict, verbose):
        self.offense  = playDict['offenseId']
        self.defense  = playDict['defenseId']


        self.yardLine  = int(playDict['yardLine'])
        self.endYardLine  = int(playDict['endYardLine'])
        self.yardsGained  = int(playDict['yardsGained'])

        self.down  = int(playDict['down'])
        self.distance  = int(playDict['distance'])
        self.endYardLine  = int(playDict['endYardLine'])

        self.type  = playDict['type']
        if verbose > 11: print "\t\toffense: {} defense: {} type: {} down: {} distance: {} yardsGained: {} yardLine: {}".format(playDict['offenseId'], playDict['defenseId'], self.type, self.down, self.distance, self.yardsGained,self.yardLine )


class drive():
    def __init__(self, playDict, verbose, driveIndexRelative):
        self.driveIndexRelative = driveIndexRelative
        self.driveIndexAbsolute = playDict["driveIndex"]

        self.quarter = playDict["quarter"]
        clock = playDict['clock'].split(":")
        self.clockStart = int(clock[0]), int(clock[1])
        self.clockEnd = [0,0]

        self.driveStart = playDict["yardLine"]
        self.driveEnd = -100
        
        self.plays = []
        self.nPlays = 0

        self.result = -100
        if (verbose > 12): print "\tdriveIndex: {} quarter: {} clockStart: {} driveStart: {}".format(self.driveIndexAbsolute, self.quarter, self.clockStart, self.driveStart) 

    def addPlay(self, playDict, verbose):
        nPlays = self.nPlays
       # print playDict['down'], self.driveIndexAbsolute
        self.plays.append(play(playDict, verbose))
       # print "self.plays" , self.plays[nPlays-1].down

        #self.endDrive()

    def endDrive(self):

        for count, i in enumerate(self.plays):
            print "\tdown: {}".format(i.down)




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
        self.driveIndexRelative = -1
        self.driveIndexAbsolute = -1

        if(verbose > 10): print "gameId: {} homeTeam: {} awayTeam: {} year: {} week: {}".format(self.gameId, self.homeAbbr, self.awayAbbr, self.year, self.week) 


    def addPlay(self, playDict, verbose):

        currentDrive = int(playDict['driveIndex'])

        currentOffense = ""

        #print playDict['down'] , playDict

        if currentOffense!= playDict['offenseId'] and self.driveIndexAbsolute  != currentDrive:
            self.driveIndexAbsolute = currentDrive
            currentOffense = playDict['offenseId']

            if  self.driveIndexRelative > -1 : self.drives[self.driveIndexRelative].endDrive()

            self.driveIndexRelative = self.driveIndexRelative +1 
            self.drives.append(drive(playDict, verbose, currentDrive))

        self.drives[self.driveIndexRelative].addPlay(playDict, verbose)




class team():
    
    def __init__(self, row ,teamId, teamName, verbose):
        self.elo = []
        self.eloPerformance = []
        self.predWin = []
        self.obsWin = []
        self.predWinFast = []
        self.st = []
        self.bt = []
        self.Ft = []
        self.year = int(row['year'])
        self.week = get_week(row['week'])
        self.home = []
        self.nGames = 0
        self.Games = []
        self.id = teamId
        self.name = teamName

        if verbose > 10: print "new team: {}".format(self.name)

    def addGame(self, gameClass):
        self.Games.append[gameClass]
        self.nGames = self.nGames +1


#   def returnEloByTime(self, year, week):
#       year = int(year)
#       week = get_week(week)
#       goal = week + year*100

#       elo = -1000
#       for i in range(self.nGames+1):
#           current = self.week[i] + self.year[i]*100
#           print "name: {} i: {} week: {}  year: {} looking at week: {} year: {} elo: {}".format(self.name, i, week, year, self.week[i], self.year[i], self.elo[i])
#           if (goal - current) < 5:
#               elo = self.elo[i]
#           if goal == current and i != 0:
#               elo = self.elo[i]
#               break
#           if goal < current and week!=16: break
#       #print self.elo
#       return elo

#   def probCountAGreaterThanB(self, countA, countB):
#       prob = 0
#       integral_factor = 5
#       for i in range((int(countA+countB)+1)*integral_factor):
#           dprob = poisson.pmf(i, countB)*poisson.sf(i, countA)
#           prob = prob + dprob
#           if dprob < .0001: break
#       return prob

#   def double_exp_smooth(self, verbose): 
#       nGames = self.nGames
#       week = self.week[nGames]
#       st = self.st[nGames]
#       st1 = self.st[nGames-1]
#       bt = self.bt[nGames]
#       bt1 = self.bt[nGames-1]
#       Ft = self.Ft[nGames]
#       eloPerformance = self.elo[nGames+1]
#       if nGames == 0:
#           st = eloPerformance
#           bt = 0
#           self.st.append(st)
#           self.bt.append(0)
#       if nGames == 1:
#           st = eloPerformance
#           bt = 0
#           lastEloPerformance = self.elo[nGames] 
#           self.st.append(st)
#           self.bt.append(eloPerformance - lastEloPerformance)
#       else:
#           alpha = .05
#           beta = .05
#           st = alpha*eloPerformance + (1-alpha)*(st+bt)
#           bt = beta*(st-st1)+(1-beta)*bt1
#           
#           self.st.append(st)
#           self.bt.append(bt)
#       Ft = st +bt
#       self.Ft.append(Ft)
#       if verbose: print "st: {} bt: {} Ft: {}".format(st, bt, Ft)


#   def obsWinProb(self, countA, countB):
#       homeWinProb = self.probCountAGreaterThanB(countA,countB)
#       awayWinProb = self.probCountAGreaterThanB(countB,countA)
#       homeWinProbAdjusted = (homeWinProb)/(homeWinProb + awayWinProb) 
#       return homeWinProbAdjusted

#   def computedWinProb(self, homeElo, awayElo):
#       return 1/(10**(-( float(homeElo) - float(awayElo))/400) +1 ) 

#   def computeElofromProb(self, prob):
#        return (-math.log(1/prob -1)/math.log(10)*400)

#   def addGame(self, newElo, eloPerformance, predWin, osbWin, year, week, home):
#       self.elo.append(newElo)
#       self.eloPerformance.append(eloPerformance)
#       self.year.append(int(year))
#       self.week.append(get_week(week))
#       self.home.append(home)
#       self.double_exp_smooth(True)
#       self.predWin.append(predWin)
#       self.obsWin.append(osbWin)
#       self.nGames = self.nGames  +1

#   def returnElo(self):
#       return self.elo[self.nGames]


#   def newGame(self, score, opponentScore, kFactor, oponenetClass, year, week, verbose):
#       elo = self.elo[self.nGames]
#       score = float(score)/7.0 + .1
#       opponentScore = float(opponentScore)/7.0 + .1

#       opponentElo = oponenetClass.returnElo()

#       if verbose: print "year: {} week: {}".format(year, week)
#       if verbose: print "home Team: {} away Team: {}".format(self.name, oponenetClass.name)
#      
#       predProb = self.computedWinProb(elo, opponentElo)
#       obsProb = self.obsWinProb(score, opponentScore)
#       if verbose: print "elo: {} opponent elo: {} win prediction: {} score: {} {} obsWinProb: {}".format(elo, opponentElo, predProb, score, opponentScore, obsProb)

#       elo = elo + kFactor*(obsProb - predProb)
#       opponentElo = opponentElo - kFactor*(obsProb-predProb)

#       eloPerformance = opponentElo + self.computeElofromProb(obsProb)
#       opponentEloPerformance = elo - self.computeElofromProb(obsProb)

#      

#       if verbose: print "uptdated elo: {} opponent elo: {} elo performance: {} opponent elo performance: {} k factor: {}".format(elo, opponentElo, eloPerformance, opponentEloPerformance, kFactor)
#       self.addGame(elo, eloPerformance, predProb, obsProb, year, week, True)
#       oponenetClass.addGame(opponentElo, opponentEloPerformance, 1.0-predProb, 1.0-obsProb, year, week, False)
#       #add stuff

