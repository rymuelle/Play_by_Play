import pickle
import numpy
import matplotlib
import matplotlib.pyplot as plt
import csv
from  filelist_sorted import fileList

gameDict  = {}

from pickleTeamClass import play, drive, game

readers = []

verbose = 15

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

    gameId = 0
    for row in reader:

       if gameId != row['gameId']:
           gameId = row['gameId']
           gameDict[gameId] = (game(row, verbose))
           print "-------new game------------"
    
    
       gameDict[gameId].addPlay(row, verbose)
        






f.close()
#print scoringTypes
