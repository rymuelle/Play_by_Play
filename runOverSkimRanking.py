import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import json
import numpy 
import math
import pprint
from fileListJSON_sorted import fileListJson 
from scipy.stats import poisson, norm 

def winProb(countA,countB):
    prob = 0
    integral_factor = 5
    for i in range((int(countA+countB)+1)*integral_factor):
        dprob = poisson.pmf(i, countB)*poisson.sf(i, countA)
        prob = prob + dprob
        if dprob < .0001: break
    #print "{} {} {}".format(countA, countB, prob)
    return prob

def loseProb(countA,countB):
    prob = 0
    integral_factor = 5
    for i in range((int(countA+countB)+1)*integral_factor):
        dprob = poisson.pmf(i, countB)*poisson.sf(i, countA)
        prob = prob + dprob
        if dprob < .0001: break
    #print "{} {} {}".format(countA, countB, prob)
    return prob

def computedWinProb( homeElo, awayElo):
    winProb = .5
    if homeElo != awayElo:
        winProb = 1/(10**(-( float(homeElo) - float(awayElo))/400) +1 ) 
    return winProb

def computeElofromProb( prob):
    return (-math.log(1/prob -1)/math.log(10)*400)

teamDict = {}
with open("gameSummaryJsonForRanking.txt", 'r') as f:
    datastore = json.load(f)
    count = 0
    teamAiD = ""
    teamAname = ""
    
    teamAGames = {}
    teamBiD = ""
    teamBname = ""
    
    teamBGames = {}
    for key in datastore:
        count = 0
        for subkey in key:
            #print subkey
            #pprint.pprint(key[subkey])
            if type(key[subkey]) == type(key):
                if "score" in key[subkey]:
                    score = float(key[subkey]['score']) + .01
                    if count ==0: 
                        scoreA = score
                        count = 1
                        
                        teamAiD = subkey
                        teamAname = key[subkey]['name']
                    else:  
                        scoreB = score
                        teamBiD = subkey
                        teamBname = key[subkey]['name']
                    #print "score {}".format(score)


        chanceWinning = winProb(scoreA/7.0,scoreB/7.0)
        chanceLoosing = winProb(scoreB/7.0,scoreA/7.0)

        chanceTie = 1.0 - (chanceWinning + chanceLoosing)

        score = chanceWinning + chanceTie*.5

        if teamAiD not in teamDict:
            teamDict[teamAiD] = {}
            teamDict[teamAiD]['games'] = {}
        teamDict[teamAiD]['games'][teamBiD] = score
        teamDict[teamAiD]["elo"] = 1500.0
        teamDict[teamAiD]["error"] = 100.0
        teamDict[teamAiD]["chi2"] = 100.0
        teamDict[teamAiD]["name"] = teamAname

        if teamBiD not in teamDict:
            teamDict[teamBiD] = {}
            teamDict[teamBiD]['games'] = {}
        teamDict[teamBiD]['games'][teamAiD] = 1.0-score
        teamDict[teamBiD]["elo"] = 1500.0
        teamDict[teamBiD]["error"] = 100.0
        teamDict[teamBiD]["chi2"] = 100.0
        teamDict[teamBiD]["name"] = teamBname

        #print "score: {} win {} tie {} lose {}".format(score, chanceWinning, chanceTie, chanceLoosing)
        #print "----------"

#pprint.pprint(teamDict)



def minimizeElo(teamDict, kFactor):
    nIterations = 0.0
    sumSquareDeltaElo = 0.0

    for teamKey in teamDict:
        #pprint.pprint(teamKey)
        nOponentes = 0.0
        sumDeltaElo = 0.0
        name = teamDict[teamKey]['name']
        nGames = len(teamDict[teamKey]['games'])
        if nGames < 5: continue

        eloErrorArray = []
        opponentErrorNormalization = 0
        for games in teamDict[teamKey]['games']:
            opponent = games
            nOpponentGames = len(teamDict[opponent]['games'])
            if nOpponentGames < 5: continue

            winProbability = (teamDict[teamKey]['games'][games])
            elo = teamDict[teamKey]['elo']
            opponentElo = teamDict[opponent]['elo']
            opponentError = teamDict[opponent]['error']
            nOponentes = nOponentes + 1
            
            compWinProb = (computedWinProb(elo,opponentElo))

            deltaWinProb = winProbability - compWinProb
            #print deltaWinProb
            #deltaElo = computeElofromProb(deltaWinProb)
            sumDeltaElo = kFactor*deltaWinProb/(1/opponentError*opponentError) + sumDeltaElo
            opponentErrorNormalization = opponentErrorNormalization + (1/opponentError*opponentError)
    
            sumSquareDeltaElo = sumSquareDeltaElo + abs(deltaWinProb)
           
            nIterations = nIterations +1

            eloPerf =  computeElofromProb(winProbability) + opponentElo
            eloErrorArray.append(eloPerf)
    
            if "WIU" == name : print opponent, winProbability, compWinProb, deltaWinProb, elo, opponentElo

        #print eloErrorArray

        sumDeltaElo = sumDeltaElo/opponentErrorNormalization

        if nIterations < 5: continue 
        stdDev = numpy.std(eloErrorArray)

        teamDict[teamKey]['error'] = stdDev/math.sqrt(float(nOponentes))
        deltaEloPerGame = sumDeltaElo/nOponentes
        if "WIU" == name :  print name, deltaEloPerGame, elo + deltaEloPerGame, nOponentes
        teamDict[teamKey]['elo'] = deltaEloPerGame + elo
        for games in teamDict[teamKey]['games']:
            opponent = games
            deltaEloPerGamePerGame = deltaEloPerGame/nOponentes
            teamDict[opponent]['elo'] = teamDict[opponent]['elo'] - deltaEloPerGamePerGame
            #print opponent, teamDict[opponent]['elo'], -deltaEloPerGamePerGame, deltaEloPerGame, nOponentes
    
    print " {}".format(sumSquareDeltaElo/nIterations)
    return teamDict, sumSquareDeltaElo/nIterations

#minimizeElo(teamDict)

for i in range(156):
    teamDict, error = minimizeElo(teamDict, 5000)

k = 5000
error2 = error
print "=-----------"

for i in range(3000):
    teamDict, error = minimizeElo(teamDict, k)
    if error > error2:
        k = k/2
    if k < 1: break
    error2 = error

#for i in range(156):
#    teamDict = minimizeElo(teamDict, 50)

#for i in range(100):
#    teamDict = minimizeElo(teamDict, 250)

#for i in range(500):
#    teamDict = minimizeElo(teamDict,150)
#
#for i in range(300):
#    teamDict = minimizeElo(teamDict,50)
#
#for i in range(300):
#    teamDict = minimizeElo(teamDict,25)
#
#for i in range(300):
#    teamDict = minimizeElo(teamDict,5)

#for i in range(300):
#    teamDict = minimizeElo(teamDict,10)

#pprint.pprint(teamDict)

shortTeamDict = {}
for teamKey in teamDict:
    elo = teamDict[teamKey]['elo']
    name = teamDict[teamKey]['name']
    error = teamDict[teamKey]['error']
   # elo = elo - error
    shortTeamDict[elo] = (name, error)

pprint.pprint(shortTeamDict)

#for x in reversed(shortTeamDict):
#    print shortTeamDict[x]
#for count, key in sorted(shortTeamDict.iterkeys()):
#    print count, key, shortTeamDict[key]

    #prob = 0
    #integral_factor = 5
    #for i in range((int(countA+countB)+1)*integral_factor):
    #    dprob = poisson.pmf(i, countB)*poisson.sf(i, countA)
    #    prob = prob + dprob
    #    if dprob < .0001: break
    #print "{} {} {}".format(countA, countB, prob)


    #pprint.pprint(datastore)





# {u'193': {u'EP': 0.0,
#           u'FGM': -1.8169499999999994,
#           u'K': -0.33899999999999864,
#           u'PEN': 1.6434000000000006,
#           u'PUNT': -1.2603999999999953,
#           u'Pass Incompletion': -8.149750000000001,
#           u'REC': 6.0470500000000005,
#           u'REC TD': 7.925200000000001,
#           u'RUSH': 2.5490399999999975,
#           u'extraPointValueAdded': {u'd': 0, u'o': 0},
#           u'fieldGoalValueAdded': {u'd': 1.8557999999999995,
#                                    u'o': -1.8169499999999994},
#           u'ishome': True,
#           u'kickValueAdded': {u'd': -0.3390000000000004,
#                               u'o': -0.33899999999999864},
#           u'nDTD': 1,
#           u'nDrives': 11,
#           u'nFG': 0,
#           u'nOTD': 3,
#           u'name': u'M-OH',
#           u'passValueAdded': {u'd': 8.38019, u'o': 13.97225},
#           u'puntValueAdded': {u'd': 1.7802999999999962,
#                               u'o': -1.2603999999999953},
#           u'rushValueAdded': {u'd': -13.945640000000001,
#                               u'o': 2.5490399999999975},
#           u'score': 28,
#           u'valueAdded': {u'd': 14.48399999999999, u'o': 6.598590000000001},
#           u'valueAddedDriveLevel': {u'd': 0, u'o': 0}},
#  u'2050': {u'EP': 0.0,
#            u'FGM': -1.8557999999999995,
#            u'Fumble Recovery (Opponent)': -4.242449999999999,
#            u'INT TD': -9.9313,
#            u'INTR': -4.295799999999998,
#            u'K': 0.3390000000000004,
#            u'PEN': -0.36775000000000035,
#            u'PUNT': -1.7802999999999962,
#            u'Pass Incompletion': -12.14215,
#            u'REC': 5.846910000000001,
#            u'RUSH': 10.061639999999999,
#            u'RUSH TD': 3.884,
#            u'extraPointValueAdded': {u'd': 0, u'o': 0},
#            u'fieldGoalValueAdded': {u'd': 1.8169499999999994,
#                                     u'o': -1.8557999999999995},
#            u'ishome': True,
#            u'kickValueAdded': {u'd': 0.33899999999999864,
#                                u'o': 0.3390000000000004},
#            u'nDTD': 0,
#            u'nDrives': 12,
#            u'nFG': 0,
#            u'nOTD': 1,
#            u'name': u'BALL',
#            u'passValueAdded': {u'd': -13.97225, u'o': -8.38019},
#            u'puntValueAdded': {u'd': 1.2603999999999953,
#                                u'o': -1.7802999999999962},
#            u'rushValueAdded': {u'd': -2.5490399999999975,
#                                u'o': 13.945640000000001},
#            u'score': 7,
#            u'valueAdded': {u'd': -6.598590000000001,
#                            u'o': -14.48399999999999},
#            u'valueAddedDriveLevel': {u'd': 0, u'o': 0}},
#  u'gameID': u'400945027',
#  u'neutralSite': False,
#  u'week': 13,
#  u'year': 2017}]#