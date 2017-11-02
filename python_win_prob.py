import numpy
import matplotlib
import matplotlib.pyplot as plt
import csv

import filelist


readers = []

for file in filelist.fileList:
	readers.append(csv.DictReader(open(file)) )




current_gameID = 0 

nGames = 0

scoringTypes = []

homeScore = 0

awayScore = 0

nHomeTD = 0
nAwayTD = 0



f = open('output.csv','wb')
field_names=["gameId", "homeTeam", "awayTeam", "year", "homeScore", "awayScore", "nHomeTD", "nAwayTD"]
w = csv.DictWriter(f,fieldnames=field_names, delimiter='\t')
w.writeheader()

#"gameId","year","week","homeId","homeTeam","homeAbbr","awayId","awayTeam","awayAbbr","driveIndex","playIndex","offenseId","offenseTeam","offenseAbbr","defenseId","defenseTeam",
#"defenseAbbr","homeScore","awayScore","isScoringPlay","quarter","clock","type","down","distance","yardLine","yardsGained","endYardLine","description"

TD = ['Rush', 'Pass Completion', 'Pass',  ]

#['Rush', 'Pass Completion', 'Interception Return Touchdown', 'Punt Return Touchdown', 'Fumble Return Touchdown', 'Blocked Punt Touchdown', 'Fumble Recovery (Own)', 'Kickoff Return Touchdown', 'Blocked Field Goal Touchdown', 'Missed Field Goal Return Touchdown', 'Pass', 'Punt', 'Kickoff', 'Pass Interception', 'Sack', 'Extra Point Good', 'Field Goal Good', '2pt Conversion', 'Penalty', 'Timeout', 'Pass Incompletion', 'Safety', 'Field Goal Missed', 'Extra Point Missed', 'Kickoff Return (Offense)', 'Fumble Recovery (Opponent)']


for reader in readers:

	good_game = False
	for row in reader:

		# add up stats
		if current_gameID == row['gameId'] and good_game==True:
			if "touchdown" in row['description'] or "TOUCHDOWN" in row['description'] or "TouchDown" in row['type'] or "TD" in row['description']:
				print current_gameID, clock, row['quarter'], row['homeScore'], row['awayScore'], row['description'], row['homeTeam'], row['awayTeam'], row['year'], row['type']
				if row['homeTeam'] == row['offenseTeam'] and row['type'] in TD:
					nHomeTD = nHomeTD +1
					if row['type'] not in scoringTypes:  scoringTypes.append(row['type'])

				if row['awayTeam'] == row['offenseTeam'] and row['type'] in TD:
					nAwayTD = nAwayTD +1
					if row['type'] not in scoringTypes:  scoringTypes.append(row['type'])

			homeScore = row['homeScore']
			awayScore = row['awayScore']



		if current_gameID != row['gameId']:
			
			#last play
	 		if nGames > 0:

				
				
	 			#dict finish and write stuff
	 			games["awayScore"] = awayScore
	 			games["homeScore"] = homeScore
				games["nHomeTD"] = nHomeTD
				games["nAwayTD"] = nAwayTD
				w.writerow(games)


			#first play
			#dict init stuff
			games = {}

			games["gameId"] = row['gameId']
			games["homeTeam"] = row['homeAbbr']
			games["awayTeam"] = row['awayAbbr']
			games["year"] = row['year']


			current_gameID = row['gameId']
			homeScore = int(row['homeScore'])
			clock = row['clock'].split(":")
			clock =  int(clock[0]), int(clock[1])

			nGames = nGames +1
			nHomeTD = 0
			nAwayTD = 0
			if clock[0] > 13 and clock[1] > 30 and "isScoringPlay" in row.keys():

				
				good_game =True



f.close()
print scoringTypes
