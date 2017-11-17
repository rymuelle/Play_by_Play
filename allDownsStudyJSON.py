import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import json
import numpy as np
import math




startYardsArray = []
scoreArray = []
with open("downValue.txt", 'r') as f:
    datastore = json.load(f)

possibleScores = [3,6,7,8, -2, -6, -7, -8, 0]

badYards = [100, 0]

dictYardValueStart = {}
dictYardValueStartWeights = {}


#{u'homeIsOffense': -1, u'startDown': 1, u'endDown': 3, u'driveEnd': 21, u'deltaScore': 0, u'driveValue': 0, u'startYards': 18}
def loopOverDrives(dictYardValueStart,dictYardValueStartResult, datastore):
    dictYardValueStart = {}
    {"distanceToGo": 10, "playYardLineStart": 17, "yardsToEndzoneFPStart": 80, "endYardToEndZone": 80, "downCount": 4, "down": 1, "typePlay": "Pass", "deltaOffenseScore": 0, "shortDisplayResult": "INT"}
    previousDown = (0,0)
    for count, play in  enumerate(datastore):

        #print play

        typePlay = play['typePlay']

        downCount = play['downCount']

        score = (play['deltaOffenseScore'])

        distanceToGo = (play['distanceToGo']) # playLastYardLine #int(play['startYards'])
      
        result = (play['endYardToEndZone'])

        playYardLineStart = (play['playYardLineStart'])

        down = (play['down'])


        firstDownYard = (10-distanceToGo) + playYardLineStart
        #if down >4 or down < 1: continue
        #if down == 1 and (previousDown[0] != 1 or previousDown[1] != playYardLineStart -  distanceToGo):
        #    firstDownResult = (play['endYardToEndZone'])
        #    firstDownYard = playYardLineStart
        #    #firstDownYard = (10-distanceToGo) + playYardLineStart
#
        #print "firstDown: {} down {} distanceToGo {} playYardLineStart {}".format(firstDownYard, down, distanceToGo, playYardLineStart)



        #previousDown = (down, playYardLineStart-  distanceToGo)

        valueFirstDown = 4.97 -.0565*firstDownYard

        resultValue = -(4.97 -.0565*result)

        if score !=0:
            resultValue = score

        #result = int(play['endYardToEndZone'])

        endType = play['shortDisplayResult']
        #weight = play['homeTeamWeight']

        #if downCount > 4: continue

        if playYardLineStart < 20 or playYardLineStart > 80: continue
        if distanceToGo < 0 or distanceToGo > 25: continue
        if "END"  in endType: continue 
        if down >4 or down < 1: continue

        if down not in dictYardValueStart:
            dictYardValueStart[down] = {}
        if distanceToGo not in dictYardValueStart[down]:
            dictYardValueStart[down][distanceToGo] = []

        dictYardValueStart[down][distanceToGo].append(resultValue - valueFirstDown )



    for down in dictYardValueStart:
        for distanceToGo in dictYardValueStart[down]:
            print "distanceToGo: {} \t distance: {} \t value {}".format(down, distanceToGo, np.average(dictYardValueStart[down][distanceToGo]) )
     #   dictYardValueStartResult[key] = np.average(dictYardValueStart[key],  weights = dictYardValueStartWeights[key])


    return dictYardValueStart, dictYardValueStartResult

dictYardValueStartResult = {}
dictYardValueStart = {}
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)

#yards = []
#values = []
#for i in range(100):
#    yards.append(float(i+1))
#    values.append(float(dictYardValueStartResult[i+1]))
#
#
#
#x= np.arange(100)
#p, res, _, _, _ = np.polyfit(x, values, 1, full=True)
#
#
#_ = plt.plot(x, values, '.', x, p(x), '-')
#


#yfit = np.polyval(p,x)
#
#
#plt(x,values, label='data')
#plt(x,yfit, label='fit')

#plt.scatter(yards,values)

#plt.plot(yards, p[yards], '-')



#plt.show()


#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
#dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)

print dictYardValueStartResult

#n, bins, patches = plt.hist(startYardsArray, 50, normed=1, facecolor='r', alpha=0.75)
#plt.title('Starting Yard Histogram')
#plt.xlabel('Starting Yard')
#plt.ylabel('Count')
##plt.plot(obsWinArray,predWinArray, 'ro')
#plt.savefig('output/startingYard.png')
#
#plt.clf()
#plt.hist2d(startYardsArray, scoreArray, bins=7, norm=LogNorm())
#plt.title('Score result vs start of drive')
#plt.xlabel('Starting Yard')
#plt.ylabel('Score result')
##plt.plot(obsWinArray,predWinArray, 'ro')
#plt.savefig('output/score_v_startingYard.png')#