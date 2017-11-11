#import pickle
import numpy
import matplotlib
import matplotlib.pyplot as plt
import csv
from  filelist_sorted import fileList

gameDict  = {}

from pickleTeamClass import play, drive, game

import json

readers = []

verbose = 15

jsonFile = open("jsonOutput.txt", "w")
jsonFile.write("[")

for file in fileList:
    readers.append(csv.DictReader(open(file)) )

#"gameId","year","week","homeId","homeTeam","homeAbbr","awayId","awayTeam","awayAbbr","driveIndex","playIndex","offenseId","offenseTeam","offenseAbbr","defenseId","defenseTeam",
#"defenseAbbr","homeScore","awayScore","isScoringPlay","quarter","clock","type","down","distance","yardLine","yardsGained","endYardLine","description"


#make game dict:
#   add plays
    # makes Drives
        # makes Plays

playArray = []

gameId, driveIndex, playIndex = 0,0,0
for reader in readers:

    good_game = False

    gameId = -1
    for row in reader:

        if int(row['year']) < 2006: continue
        #if int(row['year']) > 2006: continue

        if gameId != row['gameId']:
            if gameId > 0: 
                gameDict[gameId].endGame(verbose)
                jsonString = gameDict[gameId].returnSmallSummaryJSON(verbose)
                jsonString = jsonString[1:-1]
                jsonFile.write(jsonString+ ", ")
                gameDict  = {} # clear it for now
            gameId = row['gameId']
            gameDict[gameId] = (game(row, verbose))
            print "-------new game------------"
    
    
        gameDict[gameId].addPlay(row, verbose)
        


jsonFile.write("]")

#pickleFile  = open('pickledGameDict.dat','wb')
#pickle.dump(gameDict, pickleFile)
#pickleFile.close()


#f.close()
#print scoringTypes

#jsonFile.close()