import pickle
import numpy
import matplotlib
import matplotlib.pyplot as plt
import csv
from  filelist_sorted import fileList


from teamClass import team , play, game

readers = []


for file in fileList:
	readers.append(csv.DictReader(open(file)) )

#"gameId","year","week","homeId","homeTeam","homeAbbr","awayId","awayTeam","awayAbbr","driveIndex","playIndex","offenseId","offenseTeam","offenseAbbr","defenseId","defenseTeam",
#"defenseAbbr","homeScore","awayScore","isScoringPlay","quarter","clock","type","down","distance","yardLine","yardsGained","endYardLine","description"

for reader in readers:

	good_game = False

	gameId = 0
	for row in reader:
		if gameId != row['gameId']:
			gameEx = game(row, 11)
			gameId = gameEx.gameId

		gameEx.addPlay(row)
		





f.close()
print scoringTypes
