import numpy
import math
import matplotlib
import matplotlib.pyplot as plt
import csv
from scipy.stats import poisson, norm
import pickle

from teamClass import team

teamDict = pickle.load(open('pickledTeamDict.dat', 'rb'))


for keys in teamDict:
    year = 2017
    week = 10
    elo =  teamDict[keys].returnEloByTime(year, week)
    print elo, teamDict[keys].name