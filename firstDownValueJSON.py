import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import json
import numpy as np
import math




startYardsArray = []
scoreArray = []
with open("firstDownValue.txt", 'r') as f:
    datastore = json.load(f)

possibleScores = [3,6,7,8, -2, -6, -7, -8, 0]

badYards = [100, 0]

dictYardValueStart = {}
dictYardValueStartWeights = {}


#{u'homeIsOffense': -1, u'startDown': 1, u'endDown': 3, u'driveEnd': 21, u'deltaScore': 0, u'driveValue': 0, u'startYards': 18}
def loopOverDrives(dictYardValueStart,dictYardValueStartResult, datastore):
    dictYardValueStart = {}
    for count, drive in  enumerate(datastore):

        #print drive
        score = int(drive['deltaOffenseScore'])

        startYards = int(drive['yardsToEndzoneFPStart']) # driveLastYardLine #int(drive['startYards'])
      
        endYards = int(drive['endYard'])

        yardsGained = int(drive['yards'])

        result = int(drive['endYardToEndZone'])

        endType = drive['shortDisplayResult']
        weight = drive['homeTeamWeight']

        if "END"  in endType: continue 
        #remove bad cases
        if startYards > 101 or startYards < 1:
            continue
        #if endYards > 101 or endYards < 0:
        #    continue
        if score not in possibleScores:
            continue
        
        #print "past cuts"

        if startYards not in dictYardValueStartResult:
            dictYardValueStartResult[startYards] = 0
        #if 100-endYards not in dictYardValueStartResult:
        #    dictYardValueStartResult[100-endYards] = 0

        value = score

        if score ==0 and result in dictYardValueStartResult:
            value = -dictYardValueStartResult[result]



       # if startYards in badYards: continue
        if startYards not in dictYardValueStart:
             dictYardValueStart[startYards] = []
             dictYardValueStartWeights[startYards] = []
        if startYards in dictYardValueStart:
            dictYardValueStart[startYards].append(value)
            dictYardValueStartWeights[startYards].append(weight)
            #print startYardsStr, value



    for key in dictYardValueStart:
        print "YardStart: {} value: {}".format(key, np.average(dictYardValueStart[key]) )
        dictYardValueStartResult[key] = np.average(dictYardValueStart[key],  weights = dictYardValueStartWeights[key])


    return dictYardValueStart, dictYardValueStartResult

dictYardValueStartResult = {}
dictYardValueStart = {}
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)
dictYardValueStart, dictYardValueStartResult = loopOverDrives(dictYardValueStart, dictYardValueStartResult, datastore)

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