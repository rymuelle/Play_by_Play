import numpy
import matplotlib
import matplotlib.pyplot as plt
import csv

import filelist


readers = []

for file in filelist.fileList:
	#readers.append(csv.reader(open(file, 'r')))
	readers.append(csv.DictReader(open(file)) )




current_gameID = 0 

nGames = 0

scoringTypes = []

homeScore = 0

awayScore = 0

nHomeTD = 0
nAwayTD = 0

games = {}

f = open('output.csv','wb')
w = csv.DictWriter(f,games.keys())

#"gameId","year","week","homeId","homeTeam","homeAbbr","awayId","awayTeam","awayAbbr","driveIndex","playIndex","offenseId","offenseTeam","offenseAbbr","defenseId","defenseTeam",
#"defenseAbbr","homeScore","awayScore","isScoringPlay","quarter","clock","type","down","distance","yardLine","yardsGained","endYardLine","description"

# 0: game id

# 13: home abrv

# 17: homeScore
# 18: awayScore
# 19: is scoring play
# 20: quarter
# 21: time
# 22: play type

# 25: yards gained
# 26: endYardLIne
# 27: description

#Field Goal Missed

#Field Goal Good


for reader in readers:

	good_game = False
	for row in reader:

		#print row['homeScore']
		#if current_gameID == row['gameId']:
		#	delta_home_score = int(row['homeScore']) - homeScore
	#
		#	if delta_home_score < 0:
		#		print  row['description'], homeScore , row['homeScore'], row['quarter']
		#	homeScore = int(row['homeScore'])
		#	if delta_home_score != 0 and delta_home_score not in scoringTypes:
		#		scoringTypes.append(delta_home_score)


		if current_gameID == row['gameId'] and good_game==True:
			if "touchdown" in row['description'] or "TOUCHDOWN" in row['description']:
				print clock, row['quarter'], row['homeScore'], row['awayScore'], row['description'], row['homeTeam'], row['awayTeam'], row['year'], row['type']
				if row['homeTeam'] == row['offenseTeam']:
					nHomeTD = nHomeTD +1

				if row['awayTeam'] == row['offenseTeam']:
					nAwayTD = nAwayTD +1

		if current_gameID != row['gameId']:
			
			#last play
	 		if nGames > 0:
				w.writerows(games)

				print nHomeTD, nAwayTD

			#first play
			games = {}

			games['gameId'] = row['gameId']

			current_gameID = row['gameId']
			homeScore = int(row['homeScore'])
			clock = row['clock'].split(":")
			clock =  int(clock[0]), int(clock[1])

			nGames = nGames +1
			nHomeTD = 0
			nAwayTD = 0
			if clock[0] > 13 and clock[1] > 30:

				
				good_game =True
			#if homeScore==0 and clock[0] > 13 and clock[1] > 30:
			#if homeScore==0 and "Kickoff" in row['type']:
			#	print row['type']
				
				
			#print row
			#if homeScore==0 and row['driveIndex'] == 
			#	good_game == true


f.close()
#print scoringTypes


#	next(reader, None) 
#
#
#	for row in reader:
#		if current_gameID == int(row[0]):
#			#print row[17], row[18]
#			#if homeScore != row[17]:
#			if  row[19] == "true":
#				print  row[19]
#
#
#
##			if  row[19] == "true" and row[22] == "Pass Reception" :
##				print row[28]
##				if row[22] not in scoringTypes:
##					scoringTypes.append(row[22])
#
#	
#		if current_gameID != int(row[0]):
#			nGames = nGames + 1;
#			current_gameID = int(row[0])
#
#print scoringTypes
#
#
#