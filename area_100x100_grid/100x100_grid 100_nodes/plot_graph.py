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
		if(numberOfDeadNodesAxis[i]<100):
			ind = i
			break
	return ind+1

listt_1=[]
file_ = 'output_bma_mac100.txt'
with open(file_,'r') as f:
	for line in f:
		listt_1.append(line)

listt_3=[]
file_ = 'output_bee_mac100.txt'
with open(file_,'r') as f:
	for line in f:
		listt_3.append(line)

roundAxis_1 = list(map(int,listt_1[0].strip().split(' ')))
numberOfDeadNodesAxis_1 = list(map(int,listt_1[1].strip().split(' ')))
firstDeadNodeRound_1 = findFirstDeadNodeRound(roundAxis_1,numberOfDeadNodesAxis_1)
lastDeadNodeRound_1 = findLastDeadNodeRound(roundAxis_1,numberOfDeadNodesAxis_1)
roundAxis_1=roundAxis_1[0:firstDeadNodeRound_1//2]+roundAxis_1[firstDeadNodeRound_1//2:6000:65]
numberOfDeadNodesAxis_1=numberOfDeadNodesAxis_1[0:firstDeadNodeRound_1//2]+numberOfDeadNodesAxis_1[firstDeadNodeRound_1//2:6000:65]
roundAxis_1=np.asarray(roundAxis_1)
numberOfDeadNodesAxis_1=np.asarray(numberOfDeadNodesAxis_1)
roundAxis_new_1 = np.linspace(roundAxis_1.min(), roundAxis_1.max(),60000)
numberOfDeadNodesAxis_smooth_1=spline(roundAxis_1,numberOfDeadNodesAxis_1,roundAxis_new_1)
plt.text(firstDeadNodeRound_1-300, 5, firstDeadNodeRound_1)
plt.text(lastDeadNodeRound_1, 105, lastDeadNodeRound_1)
plt.plot(roundAxis_new_1,numberOfDeadNodesAxis_smooth_1,'b',label='BMA MAC')

roundAxis_3 = list(map(int,listt_3[0].strip().split(' ')))
numberOfDeadNodesAxis_3 = list(map(int,listt_3[1].strip().split(' ')))
firstDeadNodeRound_3 = findFirstDeadNodeRound(roundAxis_3,numberOfDeadNodesAxis_3)
lastDeadNodeRound_3 = findLastDeadNodeRound(roundAxis_3,numberOfDeadNodesAxis_3)
roundAxis_3=roundAxis_3[0:firstDeadNodeRound_3//2]+roundAxis_3[firstDeadNodeRound_3//2:6000:110]
numberOfDeadNodesAxis_3=numberOfDeadNodesAxis_3[0:firstDeadNodeRound_3//2]+numberOfDeadNodesAxis_3[firstDeadNodeRound_3//2:6000:110]
roundAxis_3=np.asarray(roundAxis_3)
numberOfDeadNodesAxis_3=np.asarray(numberOfDeadNodesAxis_3)
roundAxis_new_3 = np.linspace(roundAxis_3.min(), roundAxis_3.max(),60000)
numberOfDeadNodesAxis_smooth_3=spline(roundAxis_3,numberOfDeadNodesAxis_3,roundAxis_new_3)
plt.text(firstDeadNodeRound_3-100, 5, firstDeadNodeRound_3)
plt.text(lastDeadNodeRound_3, 105, lastDeadNodeRound_3)
plt.plot(roundAxis_new_3,numberOfDeadNodesAxis_smooth_3,'r',label='BEE MAC')

plt.legend()
plt.xlabel('Number of rounds')
plt.ylabel('Number of Dead Nodes')
plt.title('Graph between number of Dead nodes and number of rounds\n(100x100 grid)')
plt.show()