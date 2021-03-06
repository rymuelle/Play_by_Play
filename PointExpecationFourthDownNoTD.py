import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import json

import numpy as np

import math



startYardsArray = []
scoreArray = []
with open("jsonOutput.txt", 'r') as f:
    datastore = json.load(f)

possibleScores = [3,6,7,8, -2, -6, -7, -8, 0]

badYards = [100, 0, 65]

dictYardValueStart = {}


#{u'homeIsOffense': -1, u'startDown': 1, u'endDown': 3, u'driveEnd': 21, u'deltaScore': 0, u'driveValue': 0, u'startYards': 18}
def loopOverDrives(dictYardValueStart,dictYardValueStartResult, datastore):
    dictYardValueStart = {}
    for count, drive in  enumerate(datastore):

        score = int(drive['deltaScore'])
        startYards = int(drive['startYards']) # driveLastYardLine #int(drive['startYards'])
      
        endDown = int(drive['endDown'])
        endYards = int(drive['driveEnd'])
        driveLastYardLine = int(drive['driveLastYardLine'])
        yardsGained = int(drive['yardsGained'])
        result = int(drive['driveEnd'])
        value = float(drive['driveValue'])


        if score > 3: continue
        if endDown <4: continue
        #flip the field for offense
        if drive['homeIsOffense'] == 1:
        #if (yardsGained*(startYards - driveLastYardLine)) < 0: #or yardsGained+(startYards - endYards) <0:
            startYards = 100 - startYards
          
            endYards = 100 -endYards
            result = 100 - result
            driveLastYardLine = 100-driveLastYardLine

        # remove bad cases
        if startYards > 100 or startYards < 0:
            continue
        if endYards > 100 or endYards < 0:
            continue
        if score not in possibleScores:
            continue
        #print yardsGained, (startYards - endYards)
        # cut out bad drives
        #if score > 3  and  driveLastYardLine !=100: continue

        if not(drive['startDown'] == 1): continue
        if score not in possibleScores : continue

        if driveLastYardLine not in dictYardValueStartResult:
            dictYardValueStartResult[driveLastYardLine] = 0
        if 100-endYards not in dictYardValueStartResult:
            dictYardValueStartResult[100-endYards] = 0

        if score ==0:
            value = -(4.95 - .0535*(100-endYards))# dictYardValueStartResult[100-endYards]

        #print value, startYards, driveLastYardLine, endYards

        if driveLastYardLine in badYards: continue
        if driveLastYardLine not in dictYardValueStart:
             dictYardValueStart[driveLastYardLine] = []
        if driveLastYardLine in dictYardValueStart:
            dictYardValueStart[driveLastYardLine].append(value)
            #print startYardsStr, value



    for key in dictYardValueStart:
        print "YardStart: {} value: {}".format(key, np.mean(dictYardValueStart[key]) )
        dictYardValueStartResult[key] = np.mean(dictYardValueStart[key])


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