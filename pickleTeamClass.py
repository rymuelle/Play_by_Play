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


        # 262590248 reversed home and away team
        self.quarter  = playDict['quarter']
        clock = playDict['clock'].split(":")
        self.clock  = playDict['clock']

        self.driveIndex  = playDict['driveIndex']


        self.yardLine  = int(playDict['yardLine'])
        self.endYardLine  = int(playDict['endYardLine'])
        self.yardsGained  = int(playDict['yardsGained'])

        self.down  = int(playDict['down'])
        self.distance  = int(playDict['distance'])
        self.endYardLine  = int(playDict['endYardLine'])

        self.homeScore  = int(playDict['homeScore'])
        self.awayScore  = int(playDict['awayScore'])

       
        if self.offense == playDict['homeId']:
            self.offenseScore  = self.homeScore
            self.defenseScore  = self.awayScore
            self.homeIsOffense = 1
        elif self.defense == playDict['homeId']:
            self.offenseScore  = self.awayScore
            self.defenseScore  = self.homeScore
            self.homeIsOffense = -1          
        else: print "mismatched team error"


        self.type  = playDict['type']

        self.description  = playDict['description']
        if verbose > 12: print "\t\toffense: {} defense: {} type: {} down: {} distance: {} yardsGained: {} yardLine: {} score home: {} score away: {}".format(playDict['offenseId'], playDict['defenseId'], self.type, self.down, self.distance, self.yardsGained,self.yardLine, self.homeScore ,self.awayScore )
        if verbose > 12: print "\t\t description: {}".format(playDict['description'])

    def printDetails(self):
        print "\t\toffense: {} defense: {} type: {} down: {} distance: {} yardsGained: {} yardLine: {} score home: {} score away: {} score o: {} d: {}".format(self.offense ,  self.defense, self.type, self.down, self.distance, self.yardsGained,self.yardLine, self.homeScore ,self.awayScore, self.offenseScore , self.defenseScore )
        print "\t\t description: {}".format(self.description)

class drive():
    def __init__(self, playz, verbose, driveIndexRelative):
        self.offenseId  = playz.offense
        self.defenseId  = playz.defense

        self.homeIsOffense = playz.homeIsOffense
       
        self.driveIndexRelative = driveIndexRelative
        self.driveIndexAbsolute = playz.driveIndex

        self.quarter = playz.quarter
        self.clockStart = playz.clock
        self.clockEnd = [0,0]

        self.downStart = playz.down
        self.downEnd = -1000

        self.driveStart = playz.yardLine
        self.driveEnd = -1000
        self.driveLastYardLine = -1000
        self.yardsGained = -1000
        self.yardsGainedPass = -1000
        self.yardsGainedRush = -1000
        self.yardsGainedSack = -1000
        self.yardsGainedPenalty = -1000
        self.yardsGainedPunt = -1000
        self.yardsGainedKickoff = -1000
        self.nPlay = 0
        self.nPass = 0
        self.nRush = 0
        self.nSack = 0
        self.nPenalty = 0
        self.nPunt = 0
        self.nKickoff = 0
        
        self.plays = []
        self.nPlays = 0

        self.endType = ""

        driveStart = self.driveStart
        if self.homeIsOffense == 1:
            driveStart = 100 - self.driveStart

        self.startDriveValue = 4.95 - .0535*driveStart
        self.fourthDownDriveValue = -1000
        self.turnoverValue = -1000
        self.kickValue = -1000
        self.fieldGoalValue  = -1000
        self.puntValue = -1000
        self.deltaDriveValue = -1000

        self.homeScore = -1000
        self.awayScore = -1000
        self.deltaScore = -1000
        self.deltaHomeScore = -1000
        self.deltaAwayScore = -1000
        self.result = -1000

        if (verbose > 13): print "\tdriveIndex: {} quarter: {} clockStart: {} driveStart: {}".format(self.driveIndexAbsolute, self.quarter, self.clockStart, self.driveStart) 

    def addPlay(self, playz, verbose):
        self.nPlays = self.nPlays + 1


        self.plays.append(playz)
       

        #self.endDrive()

    def endDrive(self, score, verbose):
        #if self.plays[self.nPlays-1].offense = self.plays[0].offense:
        #    self.deltaScore =  self.plays[self.nPlays-1].offenseScore - self.plays[0].offenseScore - (self.plays[self.nPlays-1].defenseScore - self.plays[0].defenseScore)
        #else:
        #    self.deltaScore =  self.plays[self.nPlays-1].offenseScore - self.plays[0].defenseScore - (self.plays[self.nPlays-1].offenseScore - self.plays[0].defenseScore)


        self.deltaHomeScore = self.plays[self.nPlays-1].homeScore - score[0]
        self.deltaAwayScore = self.plays[self.nPlays-1].awayScore - score[0]
        self.deltaScore = (self.deltaHomeScore - self.deltaAwayScore)*self.plays[self.nPlays-1].homeIsOffense
        #print self.plays[self.nPlays-1].homeScore, self.plays[self.nPlays-1].awayScore
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

        self.endType = self.plays[len(self.plays)-1].type
        #print self.endType
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


        self.downEnd = self.plays[self.nPlays-1].down

        self.driveEnd = self.plays[self.nPlays-1].endYardLine
        self.driveLastYardLine = self.plays[self.nPlays-1].yardLine

        self.yardsGained = self.yardsGainedPass + self.yardsGainedRush + self.yardsGainedSack  +  self.yardsGainedPenalty

        driveEnd = self.driveEnd
        driveLastYardLine = self.driveLastYardLine

        if self.homeIsOffense == 1:
            driveEnd = 100 - self.driveEnd
            driveLastYardLine = 100 - self.driveLastYardLine

        #if self.downEnd == 4:

        self.fourthDownDriveValue = 1.98-.0491*driveLastYardLine # now just last drive value

        self.turnoverValue = -(4.95 - .0535*(100-driveEnd))
        if self.deltaScore != 0:
            self.turnoverValue = self.deltaScore

        self.deltaDriveValue  = self.turnoverValue - self.startDriveValue

        if "Kickoff" in self.endType :
            print "kickoff"
            yardLine =  self.plays[len(self.plays)-1].yardLine
            endYardLine =  self.plays[len(self.plays)-1].endYardLine
            self.kickValue = 1 + self.turnoverValue
            if yardLine == 65:
                 self.kickValue = 0.969157327275 + self.turnoverValue
            if yardLine == 75:
                 self.kickValue = 1.08534969786 + self.turnoverValue
        elif "Punt" in self.endType:
            self.puntValue = self.turnoverValue - self.fourthDownDriveValue 
        #    self.deltaDriveValue = self.fourthDownDriveValue - self.startDriveValue
        #elif self.deltaScore > 5 or self.deltaScore < 0: # not field goal
        #    self.deltaDriveValue  = self.deltaScore - self.startDriveValue
        elif "Field Goal" in self.endType:
            self.deltaDriveValue  = self.fourthDownDriveValue - self.startDriveValue
            self.fieldGoalValue  = self.turnoverValue - self.fourthDownDriveValue
            #self.fieldGoalValue  = self.deltaScore - self.fourthDownDriveValue
            #if self.deltaScore == 3:
            #    self.fieldGoalValue  =  self.turnoverValue - self.fourthDownDriveValue





        print "offense: ",  self.offenseId, "defense: ",  self.defenseId
        print "\tvalueStart: {} value 4th: {} delta: {} value Turnover: {} fieldGoalValue: {} puntValue: {} kickoffValue: {}  positive is better for kicking team".format(self.startDriveValue, self.fourthDownDriveValue, self.deltaDriveValue, self.turnoverValue, self.fieldGoalValue, self.puntValue,  self.kickValue)

            #flipField = 1
            #if self.quarter == 2 or self.quarter ==4:
            #    flipField = -1

            #self.yardsGained = (self.driveLastYardLine - self.driveStart)

       # self.driveEnd = self.plays[self.nPlays-1].endYardLine
        #self.driveLastYardLine = self.plays[self.nPlays-1].endYardLine
        #self.deltaScore = self.homeIsOffense*self.deltaScore

        #self.clockEnd = self.plays[self.nPlays-1].clock

        #print self.plays[self.nPlays-1].homeScore, self.plays[0].homeScore, self.plays[self.nPlays-1].awayScore ,self.plays[0].awayScore
        if verbose > 11: print "\tdelta score: {} yardsGained: {} rush: {} pass: {} start: {} end: {} result: {} down start: {} end: {} last play: {}".format(self.deltaScore, self.yardsGained,self.yardsGainedRush, self.yardsGainedPass, self.driveStart,self.driveLastYardLine,  self.driveEnd, self.downStart, self.downEnd,self.endType)
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

        if(verbose > 5): print "gameId: {} homeTeam: {} awayTeam: {} year: {} week: {}".format(self.gameId, self.homeAbbr, self.awayAbbr, self.year, self.week) 


    def addPlay(self, playDict, verbose):
        verbose = 10
        self.plays.append(play(playDict, verbose))

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
        print "endgame"
        newDrive = True

        self.homeScore = self.plays[len(self.plays) - 1].homeScore
        self.awayScore = self.plays[len(self.plays) - 1].awayScore

        for count, play in enumerate(self.plays):
            #print "..."
            beforeKickOff = False
            KickOff = False
            Punt = False
            Turnover = False
            Half = False
            End = False
            deltaScore = 0
            deltaScoreBefore = 0
            deltaTeam = 0
            afterKickOff = False
            endWithExtra = False
            extraPoint = False
            deltaDriveIndex = 0
            

            if verbose > 12: play.printDetails()
#
            #print "drive index: ", play.driveIndex
#escription:# Swayze Waters kickoff for 65 yards returned b
            #if len(self.plays) > count+1: 
            #    deltaScore = ( self.plays[count+1].homeScore - self.plays[count ].homeScore - (self.plays[count+1].awayScore - self.plays[count].awayScore) )
#
            #    deltaTeam = not(self.plays[count+1].offense == self.plays[count].offense)
            ##    print deltaScore, deltaTeam, play.homeIsOffense
##
            #if count > 0: 
            #    deltaScoreBefore = ( +self.plays[count].homeScore - self.plays[count-1].homeScore - (self.plays[count].awayScore - self.plays[count-1].awayScore) )
            #    deltaDriveIndex = int(self.plays[count].driveIndex) - int(self.plays[count-1].driveIndex)
#
            #if endWithExtra:# and "Kickoff":
            #    extraPoint = True
#
            #if deltaDriveIndex !=0:
            #    print "------------drive index------------"

            #if deltaScoreBefore == 7 or deltaScoreBefore == 3:


            #if (deltaTeam):
            #    if deltaScore==0:
            #        Turnover = True
            #      #  print "------------Turnover-------------"
            #    else:
            #        endWithExtra = True
##
            ##count > 0 and 

            #if count !=0 and len(self.plays) > count+1 and  "Kickoff" in self.plays[count+1].type and  ("Field" not in self.plays[count+1].type  or "Penalty" not in self.plays[count+1].type):
            #    beforeKickOff = True
            #    print "------------kickoff next ------------"

            #if "Kickoff" in self.plays[count].type and deltaScore==0:
            #     if deltaScore==0 or extraPoint:
            #      #  print "------------After Kickoff posession-------------"
            #    afterKickOff = True
            #    print "------------ kickoff ------------"
            #     else:
            #        endWithExtra = True
#
            #if len(self.plays) > count+1 and "Kickoff" in self.plays[count+1].type:
            #    #print "------------Before Kickoff posession-------------"
            #    beforeKickOff = True
##
           ##
            ##if len(self.plays) > count+1 and self.plays[count+1].offense != play.offense and "Extra Point" not in self.plays[count+1].type:
            ##    #print "------------Turnover Change Posession-------------"
            ##    Turnover = True
##
            ##if 0 < count and self.plays[count-1].offense != play.offense and "Extra Point" in self.plays[count].type:
            ##    #print "------------Turnover Change Posession-------------"
            ##    Turnover = True
##
##
            #if len(self.plays) > count+1 and self.plays[count+1].quarter != play.quarter and int(play.quarter) == 2:
            #     #print "------------End of Half Change Posession-------------"
            #     Half = True #this halftime flag might be inperfect, i've seen one situaiton in a game where the first play in second half is marked as first half
##
            #if len(self.plays) == count:
            #    #print "------------End of Game-------------"
            #    End = True
            #
            #    
#
            
            if newDrive==True:
                self.driveIndexRelative = self.driveIndexRelative + 1
                print "------------ new Drive ------------"
                self.drives.append(drive(play, verbose, self.driveIndexRelative))
                newDrive=False

##
            
            self.drives[self.driveIndexRelative].addPlay(play, verbose)
#
            #print count, len(self.plays)-1, newDrive, afterKickOff
##

            if deltaDriveIndex != 0 or afterKickOff or beforeKickOff: #count == len(self.plays)-1 or (newDrive == False and count > 0 and (afterKickOff or Half or End or Turnover or extraPoint or beforeKickOff)):
                #self.drives[self.driveIndexRelative].addPlay(play, verbose)
                print "------------ endDrive ------------"
                score = 0,0 
                if self.driveIndexRelative - 1 > -1: score = self.drives[self.driveIndexRelative-1].homeScore, self.drives[self.driveIndexRelative-1].awayScore
                self.drives[self.driveIndexRelative-1].endDrive(score, verbose)
               
                #print "------------End Drive------------"
                newDrive = True



        #self.startDriveValue = 4.95 - .0535*driveStart
        #self.fourthDownDriveValue = -1000
        #self.turnoverValue = -1000
        #self.kickValue = -1000
        #self.fieldGoalValue  = -1000
        #self.puntValue = -1000
        #self.deltaDriveValue = -1000
        self.homeOvsAwayD = 0
        self.awayOvsHomeD = 0
        self.homeKickoff = 0
        self.awayKickoff = 0
        self.homePunt = 0
        self.awayPunt = 0
        self.homeFieldGoal = 0
        self.awayFieldGoal = 0
        for drivez in self.drives:

            if "Kickoff" not in drivez.endType:
                if drivez.homeIsOffense == 1:
                    self.homeOvsAwayD = drivez.deltaDriveValue + self.homeOvsAwayD
                    if "Punt"  in drivez.endType: self.homePunt = drivez.puntValue +  self.homePunt
                    if "Field"  in drivez.endType: self.homeFieldGoal = drivez.fieldGoalValue +  self.homeFieldGoal


                elif drivez.homeIsOffense == -1:
                    self.awayOvsHomeD = drivez.deltaDriveValue +  self.awayOvsHomeD
                    if "Punt"  in drivez.endType: self.awayPunt = drivez.puntValue +  self.awayPunt
                    if "Field"  in drivez.endType: self.awayFieldGoal = drivez.fieldGoalValue +  self.awayFieldGoal

            if "Kickoff" in drivez.endType:
                if drivez.homeIsOffense == 1:
                    self.homeKickoff = drivez.kickValue + self.homeKickoff
                elif drivez.homeIsOffense == -1:
                    self.awayKickoff = drivez.kickValue +  self.awayKickoff


        self.sumHomeValue = self.homeOvsAwayD +  self.homeKickoff + self.homePunt + self.homeFieldGoal
        self.sumAwayValue = self.awayOvsHomeD +  self.awayKickoff + self.awayPunt + self.awayFieldGoal

        if verbose > 10:
            print "endgame id: {} homeScore: {} awayScore: {} home offense vs away defense: {} away offense vs home defense: {} ".format(self.gameId, self.homeScore, self.awayScore, self.homeOvsAwayD, self.awayOvsHomeD)
            print "home kick: {} away kick: {} home punt: {} away punt: {} home field Goal: {} away field goal: {} sum Home: {} sum away: {}".format( self.homeKickoff, self.awayKickoff, self.homePunt, self.awayPunt, self.homeFieldGoal, self.awayFieldGoal, self.sumHomeValue, self.sumAwayValue)

           
     



      #  # finish last drive
      #  self.drives[self.driveIndexRelative].endDrive(verbose)
#
      #  self.homeScore =  self.drives[self.driveIndexRelative].homeScore
#
      #  for drivez in self.drives:
      #      if drivez.homeIsOffense > 0: 
      #          self.homeOffenseYards = self.homeOffenseYards + drivez.yardsGained
      #      if drivez.homeIsOffense < 0: 
      #          self.awayOffenseYards = self.awayOffenseYards + drivez.yardsGained
#
      #  self.awayScore =  self.drives[self.driveIndexRelative].awayScore
      #  if verbose > 10: print "end of game: homeScore: {} awayScore: {} homeYards: {} awayYards: {}".format(self.homeScore, self.awayScore, self.homeOffenseYards, self.awayOffenseYards)

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
            summaryDict['deltaDriveValue'] = drivez.deltaDriveValue
            summaryDict['puntValue'] = drivez.puntValue
            summaryDict['fieldGoalValue'] = drivez.fieldGoalValue
            summaryDict['kickValue'] = drivez.kickValue
            summaryDict['turnoverValue'] = drivez.turnoverValue
            summaryDict['startDriveValue'] = drivez.startDriveValue

            summaryDict['driveEnd'] = drivez.driveEnd
            summaryDict['endType'] = drivez.endType
            listOfDrives.append(summaryDict)
            jsonString = json.dumps(listOfDrives)
        if (verbose > 15): 
            print jsonString
        return jsonString

    def returnJSONForDriveWorth(self, verbose):
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
            summaryDict['endType'] = drivez.endType
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

