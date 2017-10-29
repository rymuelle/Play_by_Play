import numpy
import matplotlib
import matplotlib.pyplot as plt
import csv

import filelist

#path_2017_week_7 = "./2017/CSV/"


#"gameId","year","week","homeId","homeTeam","homeAbbr","awayId","awayTeam","awayAbbr","driveIndex","playIndex","offenseId","offenseTeam","offenseAbbr","defenseId","defenseTeam",
#"defenseAbbr","homeScore","awayScore","isScoringPlay","quarter","clock","type","down","distance","yardLine","yardsGained","endYardLine","description"


#week7 = numpy.loadtxt(open(path_2017_week_7 + "PBP - 2017 - Week 7.csv", "rb"), delimiter=",", skiprows=1)
readers = []

for file in filelist.fileList:
	readers.append(csv.reader(open(file, 'r')))

#years = ["2015","2016"]
#for year in years:
#	for x in range(1,15):
#		path =  "./{}/Play By Play/CSV/PBP - {} - Week {}.csv".format(year, year, x)
#		readers.append(csv.reader(open(path, 'r')))

#reader = csv.reader(open(path_2017_week_7 + "PBP - 2017 - Week 7.csv", 'r'))



current_gameID = 0 

nGames = 0

nPunts_home = 0 
nTD_home = 0
nFumble_home = 0


offenseTeam = ""
driveNplays = 0
driveLength = 0


driveNplays_Array = []
driveLength_Array = []

# 0: game id

# 13: home abrv
# 20: quarter
# 21: time
# 22: play type

# 25: yards gained
# 26: endYardLIne
# 27: description

#Field Goal Missed

#Field Goal Good

for reader in readers:
	next(reader, None) 


	for row in reader:
	
	
		if current_gameID == int(row[0]) and offenseTeam != row[12]:
			#print driveNplays
			driveNplays_Array.append(driveNplays)
			driveLength_Array.append(driveLength)

			#print "change"
			driveNplays = 0 
			driveLength = 0
	
	
			# update after this
	
		offenseTeam = row[12]
		if row[22] != "Kickoff" and row[22] != "Punt":
			
			driveNplays =driveNplays + 1
			driveLength = driveLength + float(row[25])
	
		if current_gameID != int(row[0]):
			nGames = nGames + 1;
			current_gameID = int(row[0])
			#print row[0]
	
		#print row[12]
		#print row[25]
	
	
	#print driveNplays_Array

n, bins, patches = plt.hist(driveNplays_Array, 50, (0,50), normed=1, facecolor='g', alpha=0.75)

plt.xlabel('# plays')
plt.ylabel('Probability')
plt.title('Histogram of # plays in drive')
#plt.axis([0, 25, 0, 0.08])
plt.show()


n, bins, patches = plt.hist(driveLength_Array, 130, (-20,110), normed=1, facecolor='g', alpha=0.75)

plt.xlabel('Drive Length')
plt.ylabel('Probability')
plt.title('Histogram of Drive Length')
#plt.axis([0, 25, 0, 0.08])
plt.show()


