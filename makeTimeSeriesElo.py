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

targetName = "TAMU"
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

	predWinProbArray = []
	obsWinProbArray = []
	delataWinProbArray = []

	stDelataWinArray = []
	btDelataWinArray = []
	FtDelataWinArray = []

	eloArray = []
	stArray = []
	btArray = []
	FtArray = []
	timeArray = []
	for i in range(nGames+1):

		predWin = team.predWin[i]
		obsWin = team.obsWin[i]
		delta = obsWin - predWin
		predWinProbArray.append(predWin)
		obsWinProbArray.append(obsWin)
		delataWinProbArray.append(delta)
		year = team.year[i]
		week = team.week[i]
		#this is ugly date hack:
		if week ==16: week = 14
		yearFrac = week*365/16
		month = int(yearFrac/31+1)
		if week == 16: month = month - 2
		#day  = (week%4)*7+1
		day  = int(yearFrac - (month-1)*31)
		print month, week, day


		if i == 0: #or week == 1:
			stDelataWinArray.append(delta)
			btDelataWinArray.append(0)
		elif i == 2: #or week == 2:
			stDelataWinArray.append(delta)
			btDelataWinArray.append(0) #team.elo[i] - team.elo[i-1])
		else:
			st = stDelataWinArray[i-1]
			bt = btDelataWinArray[i-1]
			alpha = .05
			beta = .1
			stDelataWinArray.append(alpha*delta +(1-alpha)*(st+bt) )
			btDelataWinArray.append(beta*(stDelataWinArray[i] -st ) + (1-beta)*bt )
		m = 1
		if week == 1:
			m = 2
		FtDelataWinArray.append(stDelataWinArray[i] + m*btDelataWinArray[i])




		if i == 0: #or week == 1:
			stArray.append(team.elo[i])
			btArray.append(0)
		elif i == 2: #or week == 2:
			stArray.append(team.elo[i])
			btArray.append(0) #team.elo[i] - team.elo[i-1])
		else:
			st = stArray[i-1]
			bt = btArray[i-1]
			alpha = .2
			beta = .05
			stArray.append(alpha*team.elo[i] +(1-alpha)*(st+bt) )
			btArray.append(beta*(stArray[i] -st ) + (1-beta)*bt )
		m = 1
		if week == 1:
			m = 2
		FtArray.append(stArray[i] + m*btArray[i])

		#stArray.append(team.st[i])
		#eloArray.append(team.st[i])
		#FtArray.append(team.Ft[i])
		eloArray.append(team.elo[i])

		timeArray.append(datetime.datetime(year, month, day, 19, 0))
		print team.elo[i], year , month, day

	eloArray = np.array(eloArray)
	timeArray = np.array(timeArray)

	plt.plot(timeArray,eloArray)
	plt.plot(timeArray,stArray)
	plt.plot(timeArray,FtArray)
	#plt.plot(eloArray)
	#plt.plot(stArray)
	#plt.plot(FtArray)
	plt.title("Time Series of {}'s Elo".format(name))
	plt.xlabel('year')
	plt.ylabel('Elo')
	plt.grid(True)

	#plt.show()
	plt.savefig('output/{}_elo_timeSeries.png'.format(name))
	plt.clf()

	#plt.plot(timeArray,predWinProbArray)
	#plt.plot(timeArray,obsWinProbArray)
	#plt.plot(timeArray,delataWinProbArray)
	plt.plot(timeArray,stDelataWinArray)
	plt.plot(timeArray,FtDelataWinArray)
	#plt.plot(eloArray)
	#plt.plot(stArray)
	#plt.plot(FtArray)
	plt.title("Time Series of {}'s predicted Win Prob, Observed Win Prob, and delta".format(name))
	plt.xlabel('year')
	plt.ylabel('p')
	plt.grid(True)

	#plt.show()
	plt.savefig('output/{}_winProb_timeSeries.png'.format(name))
	plt.clf()

	plt.plot(timeArray,btArray)
	plt.title("Time Series of {}'s bt".format(name))
	plt.xlabel('year')
	plt.ylabel('bt')
	plt.grid(True)
	plt.savefig('output/{}_bt_imeSeries.png'.format(name))

	plt.close()

	#plt.show()
	#ts = Series(randn(1000), index=date_range('1/1/2000', periods=1000))

	#ts = ts.cumsum()

	#eloArray.plot()
 

 #  year = 2017
 #  week = 10
 #  elo =  teamDict[keys].returnEloByTime(year, week)
 #  print elo, teamDict[keys].name