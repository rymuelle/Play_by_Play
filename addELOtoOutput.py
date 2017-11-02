import numpy
import matplotlib
import matplotlib.pyplot as plt
import csv
from scipy.stats import poisson

reader = csv.DictReader(open("output.csv"), delimiter = '\t') 

f = open('output_step2.csv','wb')
field_names=["gameId", "homeTeam", "homeId", "awayTeam", "awayId", "year", "homeScore", "awayScore", "nHomeTD", "nAwayTD", "HomeOffenseScore", "HomeDefenseScore", "AwayOffenseScore", "AwayDefenseScore", "elo", "eloOffense", "eloDefense"]
w = csv.DictWriter(f,fieldnames=field_names, delimiter='\t')
w.writeheader()

teamELO = {}
for row in reader:
	if row['homeId'] not in teamELO.keys():
		teamELO[row['homeId']] = 1500
	if row['awayId'] not in teamELO.keys():
		teamELO[row['awayId']] = 1500

	homeElo = float(teamELO[row['homeId']])
	awayElo = float(teamELO[row['awayId']])

	homeScore = float(row['homeScore'])/7
	awayScore = float(row['awayScore'])/7

	if homeScore > awayScore:
		winScore = homeScore
		lossScore = awayScore
	if awayScore > homeScore:
		winScore = awayScore
		lossScore = homeScore



	homeWinProb = 1/(10**(-( homeElo - awayElo)/400) +1 ) 

	integral = 0
	for i in range(100):
		integral = integral + poisson.cdf(i, lossScore)*poisson.pmf(i, winScore)
	

	print "prob ", integral, winScore , lossScore

	#outcome = 

	print homeWinProb

print teamELO
