import numpy
import matplotlib
import matplotlib.pyplot as plt
import csv
from matplotlib.colors import LogNorm


reader = csv.DictReader(open("output_step2.csv"), delimiter = '\t') 
reader = csv.DictReader(open("output_backwards5.csv"), delimiter = '\t') 

predWinError = []
predWinFastError= []
obsWinArray = []
predWinArray = []
predWinFastArray = []

k = 120
kFast = "120 + 80/week"

total = 0
right = 0
alpha = 0
beta = 0
total_fast = 0
right_fast = 0
alpha_fast = 0
beta_fast = 0
for row in reader:
	if int(row['year']) > 2012 :
		predWin = float(row['predWin'])
		predWinFast = float(row['predWinFast'])
		obsWin = float(row['obsWin'])
		predWinError.append( predWin -obsWin)
		predWinFastError.append( predWinFast -obsWin)
		obsWinArray.append(obsWin)
		predWinArray.append(predWin)
		predWinFastArray.append(predWinFast)

		total = total + 1.0
		if((.5-obsWin)*(.5-predWin) > 0):
			right = right + 1
		if  (.5-obsWin) > 0 and (.5-predWin) < 0:
			beta = beta +1
		if  (.5-obsWin) < 0 and (.5-predWin) > 0:
			alpha = alpha +1

		total_fast = total_fast + 1.0
		if((.5-obsWin)*(.5-predWinFast) > 0):
			right_fast = right_fast + 1
		if  (.5-obsWin) > 0 and (.5-predWinFast) < 0:
			beta_fast = beta_fast +1
		if  (.5-obsWin) < 0 and (.5-predWinFast) > 0:
			alpha_fast = alpha_fast +1

print total
print "total games: {}, percent correct: {}, type 1 error: {}, type 2 error: {}".format(total, right/total, alpha/total, beta/total)

print "Fast: total games: {}, percent correct: {}, type 1 error: {}, type 2 error: {}".format(total_fast, right_fast/total_fast, alpha_fast/total_fast, beta_fast/total_fast)



n, bins, patches = plt.hist(predWinError, 50, (-1,1), normed=1, facecolor='g', alpha=0.75)

mu = numpy.mean(predWinError)
sigma = numpy.std(predWinError)




textstr = '$\mu=%.2f$\n$\sigma=%.2f$'%(mu, sigma)

plt.xlabel('predWinError')
plt.ylabel('count')
plt.title('Histogram of slow ELO accuracy')
#plt.axis([0, 25, 0, 0.08])
#plt.savefig('error.png')
print "standard k mean sigma", mu, sigma
#plt.show()
muFast = numpy.mean(predWinFastError)
sigmaFast = numpy.std(predWinFastError)

n, bins, patches = plt.hist(predWinFastError, 50, (-1,1), normed=1, facecolor='r', alpha=0.75)

plt.xlabel('predWinError')
plt.ylabel('count')
plt.title('Histogram of fast ELO accuracy')
plt.text(-.9, 1.1, r'k={} $\mu={},\ \sigma={}$'.format(k,mu,sigma))
plt.text(-.9, 1, r'k={} $\mu={},\ \sigma={}$'.format(kFast,muFast,sigmaFast))

#plt.axis([0, 25, 0, 0.08])
plt.savefig('errorFast.png')
print "standard k mean sigma Fast", muFast, sigmaFast
#plt.show()

plt.clf()
plt.hist2d(obsWinArray, predWinArray, bins=40, norm=LogNorm())
plt.title('observed win percentage vs predicted win percentage for k={}'.format(k))
plt.xlabel('observed win percentage')
plt.ylabel('predicted win percentage')
#plt.plot(obsWinArray,predWinArray, 'ro')
plt.savefig('error2d.png')

plt.clf()
plt.hist2d(obsWinArray, predWinFastArray, bins=40, norm=LogNorm())
plt.title('observed win percentage vs predicted win percentage for k={}'.format(kFast))
plt.xlabel('observed win percentage')
plt.ylabel('predicted win percentage')
#plt.plot(obsWinArray,predWinArray, 'ro')
plt.savefig('error2dFast.png')