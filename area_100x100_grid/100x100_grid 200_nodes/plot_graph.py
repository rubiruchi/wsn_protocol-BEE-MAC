import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.interpolate import spline
import matplotlib.patches as mpatches

def findFirstDeadNodeRound(roundAxis,numberOfDeadNodesAxis):
	ind=0
	for i in range(len(roundAxis)):
		if(numberOfDeadNodesAxis[i]>=1):
			ind = i
			break
	return ind

def findLastDeadNodeRound(roundAxis,numberOfDeadNodesAxis):
	ind = 0
	for i in range(len(roundAxis)-1,0,-1):
		if(numberOfDeadNodesAxis[i]<200):
			ind = i
			break
	return ind+1

listt_1=[]
file_ = 'output_bma_mac200.txt'
with open(file_,'r') as f:
	for line in f:
		listt_1.append(line)

'''listt_2=[]
file_ = 'output_ldc_mac200.txt'
with open(file_,'r') as f:
	for line in f:
		listt_2.append(line)'''

listt_3=[]
file_ = 'output_bee_mac200.txt'
with open(file_,'r') as f:
	for line in f:
		listt_3.append(line)

roundAxis_1 = list(map(int,listt_1[0].strip().split(' ')))
numberOfDeadNodesAxis_1 = list(map(int,listt_1[1].strip().split(' ')))
firstDeadNodeRound_1 = findFirstDeadNodeRound(roundAxis_1,numberOfDeadNodesAxis_1)
lastDeadNodeRound_1 = findLastDeadNodeRound(roundAxis_1,numberOfDeadNodesAxis_1)
roundAxis_1=roundAxis_1[0:firstDeadNodeRound_1//2]+roundAxis_1[firstDeadNodeRound_1//2:6000:60]
numberOfDeadNodesAxis_1=numberOfDeadNodesAxis_1[0:firstDeadNodeRound_1//2]+numberOfDeadNodesAxis_1[firstDeadNodeRound_1//2:6000:60]
roundAxis_1=np.asarray(roundAxis_1)
numberOfDeadNodesAxis_1=np.asarray(numberOfDeadNodesAxis_1)
roundAxis_new_1 = np.linspace(roundAxis_1.min(), roundAxis_1.max(),60000)
numberOfDeadNodesAxis_smooth_1=spline(roundAxis_1,numberOfDeadNodesAxis_1,roundAxis_new_1)
plt.text(firstDeadNodeRound_1-300, 10, firstDeadNodeRound_1)
plt.text(lastDeadNodeRound_1, 210, lastDeadNodeRound_1)
plt.plot(roundAxis_new_1,numberOfDeadNodesAxis_smooth_1,'b',label='BMA MAC')

'''roundAxis_2 = list(map(int,listt_2[0].strip().split(' ')))
numberOfDeadNodesAxis_2 = list(map(int,listt_2[1].strip().split(' ')))
firstDeadNodeRound_2 = findFirstDeadNodeRound(roundAxis_2,numberOfDeadNodesAxis_2)
lastDeadNodeRound_2 = findLastDeadNodeRound(roundAxis_2,numberOfDeadNodesAxis_2)
roundAxis_2=roundAxis_2[0:firstDeadNodeRound_2//2]+roundAxis_2[firstDeadNodeRound_2//2:6000:65]
numberOfDeadNodesAxis_2=numberOfDeadNodesAxis_2[0:firstDeadNodeRound_2//2]+numberOfDeadNodesAxis_2[firstDeadNodeRound_2//2:6000:65]
roundAxis_2=np.asarray(roundAxis_2)
numberOfDeadNodesAxis_2=np.asarray(numberOfDeadNodesAxis_2)
roundAxis_new_2 = np.linspace(roundAxis_2.min(), roundAxis_2.max(),60000)
numberOfDeadNodesAxis_smooth_2=spline(roundAxis_2,numberOfDeadNodesAxis_2,roundAxis_new_2)
plt.text(firstDeadNodeRound_2+100, 0, firstDeadNodeRound_2)
plt.text(lastDeadNodeRound_2, 190, lastDeadNodeRound_2)
plt.plot(roundAxis_new_2,numberOfDeadNodesAxis_smooth_2,'g',label='LDC MAC')'''

roundAxis_3 = list(map(int,listt_3[0].strip().split(' ')))
numberOfDeadNodesAxis_3 = list(map(int,listt_3[1].strip().split(' ')))
firstDeadNodeRound_3 = findFirstDeadNodeRound(roundAxis_3,numberOfDeadNodesAxis_3)
lastDeadNodeRound_3 = findLastDeadNodeRound(roundAxis_3,numberOfDeadNodesAxis_3)
roundAxis_3=roundAxis_3[0:firstDeadNodeRound_3//2]+roundAxis_3[firstDeadNodeRound_3//2:6000:55]
numberOfDeadNodesAxis_3=numberOfDeadNodesAxis_3[0:firstDeadNodeRound_3//2]+numberOfDeadNodesAxis_3[firstDeadNodeRound_3//2:6000:55]
roundAxis_3=np.asarray(roundAxis_3)
numberOfDeadNodesAxis_3=np.asarray(numberOfDeadNodesAxis_3)
roundAxis_new_3 = np.linspace(roundAxis_3.min(), roundAxis_3.max(),60000)
numberOfDeadNodesAxis_smooth_3=spline(roundAxis_3,numberOfDeadNodesAxis_3,roundAxis_new_3)
plt.text(firstDeadNodeRound_3-100, 10, firstDeadNodeRound_3)
plt.text(lastDeadNodeRound_3, 210, lastDeadNodeRound_3)
plt.plot(roundAxis_new_3,numberOfDeadNodesAxis_smooth_3,'r',label='BEE MAC')

plt.legend()
plt.xlabel('Number of rounds')
plt.ylabel('Number of Dead Nodes')
plt.title('Graph between number of Dead nodes and number of rounds\n(100x100 grid)')
plt.show()