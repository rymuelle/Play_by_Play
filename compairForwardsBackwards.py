import numpy
import matplotlib
import matplotlib.pyplot as plt
import csv
from matplotlib.colors import LogNorm


reader = csv.DictReader(open("output_step2.csv"), delimiter = '\t') 

predWinError = []
predWinFastError= []
obsWinArray = []
predWinArray = []
predWinFastArray = []

k = "forwards"
kFast = "forwards + backwards"
forwards = {}


backwards = {}


backwards['ALA'] =  2163.0482658
backwards['UGA'] =  2162.7114333
backwards['ND'] =  2154.87215614
backwards['PSU'] =  2124.98915883
backwards['CLEM'] =  2057.59810272
backwards['TCU'] =  2056.915488
backwards['OSU'] =  2038.34906947
backwards['UCF'] =  1998.70236751
backwards['WIS'] =  1996.3582766
backwards['GT'] =  1988.64609802
backwards['WASH'] =  1981.77777862
backwards['VT'] =  1970.91839986
backwards['MIAMI'] =  1970.73184562
backwards['OKST'] =  1959.33922324
backwards['AUB'] =  1958.75633776
backwards['MSU'] =  1929.28211467
backwards['STAN'] =  1916.64466215
backwards['ISU'] =  1912.47473679
backwards['OKLA'] =  1908.96500626
backwards['MSST'] =  1907.59212434
backwards['ASU'] =  1893.60659305
backwards['NCST'] =  1889.71264905
backwards['MICH'] =  1885.72080213
backwards['IOWA'] =  1862.08345715
backwards['TEX'] =  1854.37776796
backwards['USC'] =  1845.13066234
backwards['FRES'] =  1843.95520796
backwards['LSU'] =  1834.99426253
backwards['FSU'] =  1827.56581488
backwards['WVU'] =  1811.11735368
backwards['WAKE'] =  1810.45174342
backwards['CAL'] =  1804.48230712
backwards['WSU'] =  1800.25009171
backwards['TA&M'] =  1794.1005305
backwards['BC'] =  1788.2382456
backwards['USF'] =  1784.77979393
backwards['SYR'] =  1781.66358353
backwards['LOU'] =  1774.32357578
backwards['IND'] =  1766.82702673
backwards['TTU'] =  1766.57251907
backwards['NW'] =  1766.13377419
backwards['BSU'] =  1765.09713856
backwards['FLA'] =  1764.23550092
backwards['SC'] =  1750.89436529
backwards['UCLA'] =  1743.74631844
backwards['ARIZ'] =  1741.89679324
backwards['TOL'] =  1741.75453934
backwards['MRSH'] =  1741.45131325
backwards['NAVY'] =  1740.8276745
backwards['KSU'] =  1735.56516835
backwards['UTAH'] =  1735.06576183
backwards['PUR'] =  1734.28828931
backwards['MEM'] =  1722.85696479
backwards['MINN'] =  1716.11567319
backwards['FAU'] =  1708.67806991
backwards['SMU'] =  1701.90899748
backwards['UVA'] =  1699.2783522
backwards['PITT'] =  1693.83093475
backwards['NEB'] =  1693.15694414
backwards['MISS'] =  1685.92781441
backwards['DUKE'] =  1684.73667688
backwards['MD'] =  1679.36146197
backwards['NIU'] =  1677.70702861
backwards['UK'] =  1672.19239165
backwards['HOU'] =  1667.64131456
backwards['COLO'] =  1667.07144712
backwards['ORE'] =  1660.10975954
backwards['VAN'] =  1652.19013029
backwards['WMU'] =  1640.78473715
backwards['ARST'] =  1635.75429396
backwards['RUTG'] =  1632.64494948
backwards['UNC'] =  1621.20176941
backwards['TROY'] =  1619.42960461
backwards['CSU'] =  1613.70126367
backwards['EMU'] =  1612.23767381
backwards['SDSU'] =  1610.13783521
backwards['ARK'] =  1606.16291356
backwards['USM'] =  1603.86789682
backwards['UTSA'] =  1603.61752863
backwards['OHIO'] =  1599.53984835
backwards['JMU'] =  1599.03747446
backwards['MIZ'] =  1593.20856739
backwards['TULN'] =  1591.92642568
backwards['BAY'] =  1588.6215418
backwards['APP'] =  1587.41158724
backwards['TLSA'] =  1587.16816438
backwards['TENN'] =  1585.04475806
backwards['ARMY'] =  1580.05936509
backwards['UNM'] =  1578.02768552
backwards['USU'] =  1569.03879047
backwards['TNST'] =  1566.11140877
backwards['WIU'] =  1554.7292732
backwards['UNI'] =  1553.25592654
backwards['LIB'] =  1549.38742125
backwards['WYO'] =  1545.80863585
backwards['LT'] =  1545.14110224
backwards['UNT'] =  1543.03870519
backwards['AFA'] =  1539.96719336
backwards['YSU'] =  1538.22435656
backwards['CIN'] =  1535.98834919
backwards['AKR'] =  1531.144741
backwards['CONN'] =  1529.47302121
backwards['BUFF'] =  1525.39415499
backwards['MER'] =  1524.66491128
backwards['M-OH'] =  1508.66474174
backwards['USA'] =  1507.35025929
backwards['NMSU'] =  1501.41965808
backwards['TEM'] =  1500.17419023
backwards['ILL'] =  1486.43222908
backwards['CMU'] =  1480.80760815
backwards['MTSU'] =  1466.65918809
backwards['WKU'] =  1461.76060517
backwards['NEV'] =  1461.25669843
backwards['HAW'] =  1454.96371119
backwards['FIU'] =  1444.17410584
backwards['STON'] =  1443.88386545
backwards['SDAK'] =  1437.83835852
backwards['UNLV'] =  1431.7932925
backwards['UAB'] =  1427.5459103
backwards['SIU'] =  1426.19506403
backwards['GAST'] =  1424.49578964
backwards['EWU'] =  1422.44887202
backwards['UMASS'] =  1420.54880997
backwards['UNH'] =  1415.06209888
backwards['JVST'] =  1415.02004439
backwards['NOVA'] =  1414.86179737
backwards['UND'] =  1412.49027047
backwards['SAM'] =  1403.44378023
backwards['ULM'] =  1403.09984238
backwards['FUR'] =  1400.34010177
backwards['ODU'] =  1394.47819288
backwards['HC'] =  1390.74058495
backwards['MONT'] =  1369.89398261
backwards['ULL'] =  1369.86700546
backwards['ORST'] =  1362.79333792
backwards['KU'] =  1361.50806409
backwards['IDHO'] =  1360.30591694
backwards['ECU'] =  1358.76238891
backwards['BGSU'] =  1358.04754811
backwards['W&M'] =  1353.00478747
backwards['DEL'] =  1350.52189569
backwards['WEB'] =  1346.5538259
backwards['NICH'] =  1345.46416147
backwards['URI'] =  1342.31868102
backwards['HOW'] =  1340.49393472
backwards['BYU'] =  1340.4317608
backwards['UNCO'] =  1338.42897991
backwards['CCU'] =  1336.11697121
backwards['UCA'] =  1334.29548713
backwards['NCAT'] =  1333.78141372
backwards['CHAT'] =  1325.75204408
backwards['KENT'] =  1321.38169101
backwards['CCSU'] =  1321.29405036
backwards['EKY'] =  1316.12354266
backwards['TOWS'] =  1301.87874656
backwards['IDST'] =  1291.96169928
backwards['MTST'] =  1287.02727924
backwards['BALL'] =  1283.61186034
backwards['EIU'] =  1281.21731993
backwards['RICE'] =  1271.48223669
backwards['SJSU'] =  1268.25494997
backwards['IW'] =  1267.05738749
backwards['CHAR'] =  1265.62759152
backwards['SUU'] =  1260.71238066
backwards['ALBY'] =  1260.14208357
backwards['UCD'] =  1250.06214013
backwards['ALCN'] =  1238.33869431
backwards['UTM'] =  1236.1393374
backwards['PRST'] =  1234.68724685
backwards['INST'] =  1234.11861737
backwards['GASO'] =  1217.35729764
backwards['WAG'] =  1215.4731758
backwards['BCU'] =  1214.00493138
backwards['NWST'] =  1213.78324881
backwards['FOR'] =  1212.24706307
backwards['NAU'] =  1209.88555434
backwards['COLG'] =  1204.86380942
backwards['DSU'] =  1204.41614621
backwards['TXST'] =  1202.38468325
backwards['ACU'] =  1194.91884141
backwards['ALST'] =  1193.5265027
backwards['UTEP'] =  1193.47573338
backwards['SFA'] =  1193.35911658
backwards['HAMP'] =  1189.28285016
backwards['LAM'] =  1185.73482236
backwards['PEAY'] =  1178.75290736
backwards['TNTC'] =  1175.50319706
backwards['ELON'] =  1160.94797313
backwards['CHSO'] =  1158.32941297
backwards['WEBB'] =  1154.61898838
backwards['JKST'] =  1149.33864881
backwards['WCU'] =  1147.02223454
backwards['NCCU'] =  1143.77311249
backwards['GRAM'] =  1141.8809918
backwards['PRE'] =  1137.35283552
backwards['MOST'] =  1124.81608754
backwards['SEMO'] =  1120.42856251
backwards['HBU'] =  1118.5152452
backwards['SAV'] =  1118.05753742
backwards['MURR'] =  1111.63129184
backwards['UAPB'] =  1097.86415794
backwards['VMI'] =  1096.1397869
backwards['FAMU'] =  1090.97947222
backwards['SOU'] =  1082.20098084
backwards['CP'] =  1074.70973023
backwards['MORG'] =  1062.1317129
backwards['SAC'] =  1058.04627442
backwards['AAMU'] =  1002.53326004
 

def get_week(s):
    try:
        int(s)
        return int(s)
    except ValueError:
        return 16

for row in reader:
	if int(row['year']) == 2017  and get_week(week) == 9:
		
		obsWin = float(row['obsWin'])
		
		obsWinArray.append(obsWin)
		


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