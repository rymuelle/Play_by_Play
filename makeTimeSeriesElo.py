import numpy
import math
import matplotlib
import matplotlib.pyplot as plt
import csv
from scipy.stats import poisson, norm
import pickle

import datetime
import numpy as np

from teamClass import team

#from pandas import Series

teamDict = pickle.load(open('pickledTeamDict.dat', 'rb'))

targetName = "CLEM"
name = ""

for key in teamDict:
	if targetName ==  teamDict[key].name:
		team = teamDict[key]
		name = teamDict[key].name

if name == "":
	print "no team found"
else:
	nGames = team.nGames
	print "found team: {} with {} games from {} to {}".format(name, nGames , team.year[0], team.year[nGames])

	eloArray = []
	timeArray = []
	for i in range(nGames+1):
		eloArray.append(team.elo[i])
		year = team.year[i]
		week = team.week[i]
		month = int(week/4) +8
		day  = (week%4)*7+1
		timeArray.append(datetime.datetime(year, month, day, 19, 0))
		print team.elo[i], year , month, day

	eloArray = np.array(eloArray)
	timeArray = np.array(timeArray)

	plt.plot(timeArray,eloArray)
	plt.title("Time Series of {}'s Elo".format(name))
	plt.xlabel('year')
	plt.ylabel('Elo')
	plt.savefig('output/{}_elo_timeSeries.png'.format(name))

	#plt.show()
	#ts = Series(randn(1000), index=date_range('1/1/2000', periods=1000))

	#ts = ts.cumsum()

	#eloArray.plot()
 

 #  year = 2017
 #  week = 10
 #  elo =  teamDict[keys].returnEloByTime(year, week)
 #  print elo, teamDict[keys].name