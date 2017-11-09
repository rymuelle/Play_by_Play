import numpy
import math
import matplotlib
import matplotlib.pyplot as plt
import csv
from scipy.stats import poisson, norm
import json



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

        self.homeScore  = int(playDict['homeScore'])
        self.awayScore  = int(playDict['awayScore'])

        self.type  = playDict['type']
        if verbose > 12: print "\t\toffense: {} defense: {} type: {} down: {} distance: {} yardsGained: {} yardLine: {}".format(playDict['offenseId'], playDict['defenseId'], self.type, self.down, self.distance, self.yardsGained,self.yardLine )
        if verbose > 12: print "\t\t description: {}".format(playDict['description'])

class drive():
    def __init__(self, playDict, verbose, driveIndexRelative):
        self.offenseId  = playDict['offenseId']
        self.defenseId  = playDict['defenseId']

        self.homeId  = playDict['homeId']
        self.homeIsOffense = 1
        if  self.homeId == self.offenseId:
            self.homeIsOffense = -1

        self.driveIndexRelative = driveIndexRelative
        self.driveIndexAbsolute = playDict["driveIndex"]

        self.quarter = playDict["quarter"]
        clock = playDict['clock'].split(":")
        self.clockStart = int(clock[0]), int(clock[1])
        self.clockEnd = [0,0]

        self.downStart = int(playDict["down"])
        self.downEnd = -100

        self.driveStart = int(playDict["yardLine"])
        self.driveEnd = -100
        self.driveLastYardLine = -100
        self.yardsGained = -100
        self.yardsGainedPass = -100
        self.yardsGainedRush = -100
        self.yardsGainedSack = -100
        self.yardsGainedPenalty = -100
        self.yardsGainedPunt = -100
        self.yardsGainedKickoff = -100
        self.nPlay = 0
        self.nPass = 0
        self.nRush = 0
        self.nSack = 0
        self.nPenalty = 0
        self.nPunt = 0
        self.nKickoff = 0
        
        self.plays = []
        self.nPlays = 0

        self.homeScore = -1000
        self.awayScore = -1000
        self.deltaScore = 0
        self.result = -100
        if (verbose > 11): print "\tdriveIndex: {} quarter: {} clockStart: {} driveStart: {}".format(self.driveIndexAbsolute, self.quarter, self.clockStart, self.driveStart) 

    def addPlay(self, playDict, verbose):
        self.nPlays = self.nPlays + 1

       # print playDict['down'], self.driveIndexAbsolute
        self.plays.append(play(playDict, verbose))
       # print "self.plays" , self.plays[nPlays-1].down

        #self.endDrive()

    def endDrive(self, verbose):
        self.deltaScore =  self.plays[self.nPlays-1].homeScore - self.plays[0].homeScore - (self.plays[self.nPlays-1].awayScore - self.plays[0].awayScore)

        self.homeScore = int(self.plays[self.nPlays-1].homeScore)
        self.awayScore = int(self.plays[self.nPlays-1].awayScore)
        self.yardsGained = 0
        self.yardsGainedPass = 0
        self.yardsGainedRush = 0
        self.yardsGainedSack = 0
        self.yardsGainedPenalty = 0
        self.yardsGainedPunt = 0
        self.yardsGainedKickoff = 0
        #offensivePlays = ["Pass", "Rush", "Pen"]
        #deffensivePlays  =["Interception" , ]
        for count, playz in enumerate(self.plays):
            if playz.down > 0:
                if "Pass" in playz.type and "Interception" not in playz.type: 
                    self.yardsGainedPass = self.yardsGainedPass + playz.yardsGained
                    self.nPass =  self.nPass +1
                if "Rush" in playz.type: 
                    self.yardsGainedRush = self.yardsGainedRush + playz.yardsGained
                    self.nRush =  self.nRush +1
                if "Sack" in playz.type: 
                    self.yardsGainedSack = self.yardsGainedSack + playz.yardsGained
                    self.nSack =  self.nSack +1
                if "Penalty" in playz.type: 
                    self.yardsGainedPenalty = self.yardsGainedPenalty + playz.yardsGained
                    self.nPenalty =  self.nPenalty +1
                if "Punt" in playz.type: 
                    self.yardsGainedPunt = self.yardsGainedPunt + playz.yardsGained
                    self.nPunt =  self.nPunt +1
                if "Kickoff" in playz.type: 
                    self.yardsGainedKickoff = self.yardsGainedKickoff + playz.yardsGained
                    self.nKickoff =  self.nKickoff +1

                #if count != self.nPlays-1:
                ##self.deltaScore
                #    if "Pass" in playz.type: 
                #        self.yardsGainedPass = self.yardsGainedPass + playz.yardsGained
                #        self.nPass =  self.nPass +1
                #    if "Rush" in playz.type: 
                #        self.yardsGainedRush = self.yardsGainedRush + playz.yardsGained
                #        self.nRush =  self.nRush +1
                #    if "Sack" in playz.type: 
                #        self.yardsGainedSack = self.yardsGainedSack + playz.yardsGained
                #        self.nSack =  self.nSack +1
                #    if "Penalty" in playz.type: 
                #        self.yardsGainedPenalty = self.yardsGainedPenalty + playz.yardsGained
                #        self.nPenalty =  self.nPenalty +1
#
                self.nPlay =  self.nPlay +1


                self.downEnd = playz.down

                self.driveEnd = playz.endYardLine
                self.driveLastYardLine = playz.yardLine

            self.yardsGained = self.yardsGainedPass + self.yardsGainedRush + self.yardsGainedSack  +  self.yardsGainedPenalty

            flipField = 1
            if self.quarter == 2 or self.quarter ==4:
                flipField = -1

            #self.yardsGained = (self.driveLastYardLine - self.driveStart)

       # self.driveEnd = self.plays[self.nPlays-1].endYardLine
        #self.driveLastYardLine = self.plays[self.nPlays-1].endYardLine
        if  self.homeId != self.offenseId: self.deltaScore = -1*self.deltaScore

        #self.clockEnd = self.plays[self.nPlays-1].clock

        if verbose > 11: print "\tdelta score: {} yardsGained: {} rush: {} pass: {} start: {} end: {} result: {} down start: {} end: {}".format(self.deltaScore, self.yardsGained,self.yardsGainedRush, self.yardsGainedPass, self.driveStart,self.driveLastYardLine,  self.driveEnd, self.downStart, self.downEnd)
        #for count, i in enumerate(self.plays):
            #print "\tdown: {}".format(i.down)




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
        
        self.plays = []
        self.drives = []
        self.driveIndexRelative = -1
        self.driveIndexAbsolute = -1

        self.homeScore = 0
        self.homeOffenseYards = 0
        self.homeRushOffenseYards = 0
        self.homePassOffenseYards = 0
        self.homeTFLOffenseYards = 0

        self.awayScore = 0
        self.awayOffenseYards = 0
        self.awayRushOffenseYards = 0
        self.awayPassOffenseYards = 0
        self.awayTFLOffenseYards = 0

        if(verbose > 10): print "gameId: {} homeTeam: {} awayTeam: {} year: {} week: {}".format(self.gameId, self.homeAbbr, self.awayAbbr, self.year, self.week) 


    def addPlay(self, playDict, verbose):

        #currentDrive = int(playDict['driveIndex'])
#
        #currentOffense = ""
#
        ##print playDict['down'] , playDict
#
        #if currentOffense!= playDict['offenseId'] and self.driveIndexAbsolute  != currentDrive:
        #    self.driveIndexAbsolute = currentDrive
        #    currentOffense = playDict['offenseId']
#
        #    if  self.driveIndexRelative > -1 : self.drives[self.driveIndexRelative].endDrive(verbose)
#
        #    self.driveIndexRelative = self.driveIndexRelative +1 
        #    self.drives.append(drive(playDict, verbose, currentDrive))
#
        #self.drives[self.driveIndexRelative].addPlay(playDict, verbose)
#
        #if "Kickoff" in playDict['type'] or "Punt" in playDict['type']:
         #   print "------------change posession-------------"


    def endGame(self, verbose):
        # finish last drive
        self.drives[self.driveIndexRelative].endDrive(verbose)

        self.homeScore =  self.drives[self.driveIndexRelative].homeScore

        for drivez in self.drives:
            if drivez.homeIsOffense > 0: 
                self.homeOffenseYards = self.homeOffenseYards + drivez.yardsGained
            if drivez.homeIsOffense < 0: 
                self.awayOffenseYards = self.awayOffenseYards + drivez.yardsGained

        self.awayScore =  self.drives[self.driveIndexRelative].awayScore
        if verbose > 10: print "end of game: homeScore: {} awayScore: {} homeYards: {} awayYards: {}".format(self.homeScore, self.awayScore, self.homeOffenseYards, self.awayOffenseYards)

    def returnSmallSummaryJSON(self, verbose):
        listOfDrives = []
        for drivez in self.drives:
            summaryDict = {} 
            summaryDict['startDown'] = drivez.downStart
            summaryDict['homeIsOffense'] = drivez.homeIsOffense
            summaryDict['startYards'] = drivez.driveStart
            summaryDict['driveLastYardLine'] = drivez.driveLastYardLine
            summaryDict['yardsGained'] = drivez.yardsGained
            summaryDict['endDown'] = drivez.downEnd
            summaryDict['deltaScore'] = drivez.deltaScore
            summaryDict['driveValue'] = drivez.deltaScore
            summaryDict['driveEnd'] = drivez.driveEnd
            listOfDrives.append(summaryDict)
            jsonString = json.dumps(listOfDrives)
        if (verbose > 15): 
            print jsonString
        return jsonString



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

