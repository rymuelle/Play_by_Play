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

HomeOffenseScore = 0
HomeDefenseScore = 0
AwayOffenseScore = 0
AwayDefenseScore = 0



f = open('output.csv','wb')
field_names=["gameId", "homeTeam", "homeId", "awayTeam", "awayId", "year", "week", "homeScore", "awayScore", "nHomeTD", "nAwayTD", "HomeOffenseScore", "HomeDefenseScore", "AwayOffenseScore", "AwayDefenseScore", "elo", "eloOffense", "eloDefense"]
w = csv.DictWriter(f,fieldnames=field_names, delimiter='\t')
w.writeheader()

#"gameId","year","week","homeId","homeTeam","homeAbbr","awayId","awayTeam","awayAbbr","driveIndex","playIndex","offenseId","offenseTeam","offenseAbbr","defenseId","defenseTeam",
#"defenseAbbr","homeScore","awayScore","isScoringPlay","quarter","clock","type","down","distance","yardLine","yardsGained","endYardLine","description"

TD = ['Rush', 'Pass Completion', 'Pass', 'Touchdown' ]

#['Rush', 'Pass Completion', 'Interception Return Touchdown', 'Punt Return Touchdown', 'Fumble Return Touchdown', 'Blocked Punt Touchdown', 'Fumble Recovery (Own)', 'Kickoff Return Touchdown', 'Blocked Field Goal Touchdown', 'Missed Field Goal Return Touchdown', 'Pass', 'Punt', 'Kickoff', 'Pass Interception', 'Sack', 'Extra Point Good', 'Field Goal Good', '2pt Conversion', 'Penalty', 'Timeout', 'Pass Incompletion', 'Safety', 'Field Goal Missed', 'Extra Point Missed', 'Kickoff Return (Offense)', 'Fumble Recovery (Opponent)']

playtype = ""
for reader in readers:

	good_game = False
	for row in reader:

		# add up stats
		if current_gameID == row['gameId'] and good_game==True:
			if homeScore- int(row['homeScore']) + awayScore - int(row['awayScore']) < 0:
				#print current_gameID, clock, row['quarter'], row['homeScore'], row['awayScore'], row['description'], row['homeTeam'], row['awayTeam'], row['year'], row['type']

				if homeScore- int(row['homeScore']) !=0 and row['offenseId'] == row['homeId']:
					HomeOffenseScore = HomeOffenseScore - homeScore + int(row['homeScore']) 


				if homeScore- int(row['homeScore']) !=0 and row['offenseId'] != row['homeId']:
					HomeDefenseScore = HomeDefenseScore - homeScore +  int(row['homeScore']) 


				if awayScore- int(row['awayScore']) !=0 and row['offenseId'] == row['awayId']:
					AwayOffenseScore = AwayOffenseScore - awayScore + int(row['awayScore']) 


				if awayScore- int(row['awayScore']) !=0 and row['offenseId'] != row['awayId']:
					AwayDefenseScore = AwayDefenseScore -  awayScore + int(row['awayScore'])
					


				if not row['type']  in scoringTypes:
					scoringTypes.append(row['type'])



			homeScore = int(row['homeScore'])
			awayScore = int(row['awayScore'])
			playtype = row['type']

				
		if current_gameID != row['gameId']:
			
			#last play
	 		if good_game and awayScore + homeScore != 0 and quarter > 3:

				
				
	 			#dict finish and write stuff
	 			games["awayScore"] = awayScore
	 			games["homeScore"] = homeScore
				games["nHomeTD"] = nHomeTD
				games["nAwayTD"] = nAwayTD
				games["HomeOffenseScore"] = HomeOffenseScore
				games["HomeDefenseScore"] = HomeDefenseScore
				games["AwayOffenseScore"] = AwayOffenseScore
				games["AwayDefenseScore"] = AwayDefenseScore
				#print playtype
				w.writerow(games)


			#first play
			#dict init stuff
			games = {}

			games["gameId"] = row['gameId']
			games["homeTeam"] = row['homeAbbr']
			games["awayTeam"] = row['awayAbbr']
			games["homeId"] = row['homeId']
			games["awayId"] = row['awayId']
			games["year"] = row['year']
			games["week"] = row['week']


			current_gameID = row['gameId']
			homeScore = int(row['homeScore'])
			awayScore = int(row['awayScore'])
			clock = row['clock'].split(":")
			clock =  int(clock[0]), int(clock[1])

			#reset things
			nGames = nGames +1
			nHomeTD = 0
			nAwayTD = 0
			HomeOffenseScore = 0
			HomeDefenseScore = 0
			AwayOffenseScore = 0
			AwayDefenseScore = 0

			
			#if clock[0] > 13 and clock[1] > 30 and "isScoringPlay" in row.keys():
			if clock[0] > 13 and int(row['homeScore'])+int(row['awayScore']) == 0:
				

				
				good_game =True
			
			quarter = row['quarter']



f.close()
print scoringTypes
