from draw import*
import random
import math
import time
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.interpolate import spline
import json

def euclid_dist(a1,b1,a2,b2):
	return (math.sqrt((a1-a2)**2+(b1-b2)**2))

def transmissionEnergy(k,d):
	return 50*pow(10,-9)*k+10*pow(10,-12)*(d**2)*k

def recievingEnergy(k):
	return 50*pow(10,-9)*k

def resetAllCH(NodesList,flag):
	for i in range(1,len(NodesList)):
		if(NodesList[i]['isClusterHead']==True and NodesList[i]['isDead']==False):
			x,y=NodesList[i]['location']['x'],NodesList[i]['location']['y']
			if(flag==1):
				draw_vertex('red',x,y)
		NodesList[i]['wantToSendData']=False
		NodesList[i]['isClusterHead']=False
	return NodesList

def convertToNodesList(clusterList):
	NodesList=[]
	NodesList.append([])
	for i in range(len(clusterList)):
		for j in range(len(clusterList[i])):
			NodesList.append(clusterList[i][j])
	return NodesList

def findClusterHeadLocation(cell):
	x_ch,y_ch=0,0
	for i in range(len(cell)):
		if(cell[i]['isClusterHead']==True):
			x_ch,y_ch=cell[i]['location']['x'],cell[i]['location']['y']
			break
	return (x_ch,y_ch)

def maxmDistanceFromCH(cell):
	x_ch,y_ch = findClusterHeadLocation(cell)
	maxDistance = 0
	maxDistanceIndex = -1
	for i in range(len(cell)):
		if(cell[i]['isClusterHead']==False ):
			x,y = cell[i]['location']['x'],cell[i]['location']['y']
			d = euclid_dist(x/4,y/4,x_ch/4,y_ch/4)
			if(d>maxDistance):
				maxDistance = d
				maxDistanceIndex = i
	return maxDistance
    
def findNumberOfDeadNodes(clusterList):
	count_=0
	for i in range(len(clusterList)):
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['isDead']==True):
				count_+=1
				print('Dead Node ID:',clusterList[i][j]['id'])
	return count_

def isAllLessThanThreshold(clusterList):
	flag = True
	for i in range(len(clusterList)):
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['energy']>=clusterList[i][j]['threshold']):
				flag = False
				break
		if(flag==False):
			break
	return flag

def makeDead(clusterList):
	if(isAllLessThanThreshold(clusterList)):
		print("****************** ALL DEAD! **********************")
		for i in range(len(clusterList)):
			for j in range(len(clusterList[i])):
				if(clusterList[i][j]['energy']<clusterList[i][j]['threshold']):
					clusterList[i][j]['isDead'] = True
	return clusterList

def findFirstDeadNodeRound(roundAxis,numberOfDeadNodesAxis):
	ind=0
	for i in range(len(roundAxis)):
		if(numberOfDeadNodesAxis[i]==1):
			ind = i
			break
	return ind

    ###########################################
    #                                         #
    #              SETUP PHASE                #
    #                                         #
    ###########################################

#step 3 (cluster head formation according to the LEACH protocol)
def calculateClusterHead(NodesList,roundNum):
	P=0.125
	x=(P*(roundNum%round(1/P)))
	if(roundNum%(1/P)==0):
		for i in range(1,len(NodesList)):
			NodesList[i]['lastTimeCH'] = -1
	T=(P/(1-x))
	print(T,x)
	count_=0
	flag = True
	n = 1
	cnt = 0
	for i in range(1,len(NodesList)):
		if( (NodesList[i]['lastTimeCH']==-1 and NodesList[i]['isDead']==False) or (NodesList[i]['lastTimeCH']!=-1 and roundNum>=NodesList[i]['lastTimeCH']+(1/P) and NodesList[i]['energy']>=NodesList[i]['threshold'] and NodesList[i]['isDead']==False)):
			random_num=random.random()
			cnt+=1
			if(random_num<=T):
				flag = False
				count_+=1
				NodesList[i]['isClusterHead']=True
				NodesList[i]['lastTimeCH']=roundNum
	print("Total number of candidate for selection:",cnt)
	while(flag==True and cnt!=0):
		print("n: ",n)
		for i in range(1,len(NodesList)):
			if( (NodesList[i]['lastTimeCH']==-1 and NodesList[i]['isDead']==False) or (NodesList[i]['lastTimeCH']!=-1 and roundNum>=NodesList[i]['lastTimeCH']+(1/P) and NodesList[i]['energy']>=NodesList[i]['threshold'])):
				random_num=random.random()
				if(random_num<=T):
					flag = False
					count_+=1
					NodesList[i]['isClusterHead']=True
					NodesList[i]['lastTimeCH']=roundNum
		n+=1
	NodesList[0]=count_
	return NodesList

def clusterFormation(NodesList):
	num_of_cluster=NodesList[0]
	clusterHeads=[]
	nonClusterHeads=[]
	for i in range(1,len(NodesList)):
		if(NodesList[i]['isClusterHead']==True):
			clusterHeads.append(NodesList[i])
		else:
			nonClusterHeads.append(NodesList[i])
	clusterList=[]
	for i in range(num_of_cluster):
		clusterList.append([])
	for i in range(len(clusterList)):
		clusterList[i].append(clusterHeads[i])
	for i in range(len(nonClusterHeads)):
		minDistance=10000000
		minDistanceIndex=(-1,-1)
		for j in range(len(clusterHeads)):
			x_ch,y_ch=clusterHeads[j]['location']['x'],clusterHeads[j]['location']['y']
			x,y=nonClusterHeads[i]['location']['x'],nonClusterHeads[i]['location']['y']
			distance = euclid_dist(x,y,x_ch,y_ch)
			if(distance<minDistance):
				minDistance=distance
				minDistanceIndex=(i,j)
		if(minDistance!=10000000):
			(nonCHIndex,chIndex)=minDistanceIndex
			clusterList[chIndex].append(nonClusterHeads[nonCHIndex])
	return clusterList

# Each CH broadcost advertisement packet so transmission energy will be subtracted from each cluster head
def step4_a(clusterList):
	broadcastingEnergy=transmissionEnergy(800,100*math.sqrt(2)) #changed
	for i in range(len(clusterList)):
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['isClusterHead']==True and clusterList[i][j]['isDead']==False):
				clusterList[i][j]['energy']-=broadcastingEnergy
				if(clusterList[i][j]['energy']<=0):
					clusterList[i][j]['energy']=0
					clusterList[i][j]['isDead']=True
				break
	return clusterList

# Each non cluster head member will recieve that advertisement packets
def step4_b(clusterList):
	num_of_ch=len(clusterList)
	for i in range(len(clusterList)):
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['isClusterHead']==False and clusterList[i][j]['isDead']==False):
				k=100*8 #changed
				clusterList[i][j]['energy']-= num_of_ch*recievingEnergy(k)
				if(clusterList[i][j]['energy']<=0):
					clusterList[i][j]['energy']=0
					clusterList[i][j]['isDead']=True
	return clusterList

# step 5- Each member node will select that CH whose signal strength is strongest.
def step5(clusterList):
	# cluster formation
	return clusterList

# Each member will send the join request to CH
def step6(clusterList):
	for i in range(len(clusterList)):
		num_of_non_ch=0
		x_ch,y_ch=findClusterHeadLocation(clusterList[i])
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['isClusterHead']==False and clusterList[i][j]['isDead']==False):
				x,y = clusterList[i][j]['location']['x'],clusterList[i][j]['location']['y']
				d = euclid_dist(x/4,y/4,x_ch/4,y_ch/4)
				k = 100*8 #changed
				clusterList[i][j]['energy']-=transmissionEnergy(k,d)
				num_of_non_ch+=1
				if(clusterList[i][j]['energy']<=0):
					clusterList[i][j]['energy']=0
					clusterList[i][j]['isDead']=True
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['isClusterHead']==True and clusterList[i][j]['isDead']==False):
				k=100*8 #changed
				clusterList[i][j]['energy']-= num_of_non_ch*recievingEnergy(k)
				if(clusterList[i][j]['energy']<=0):
					clusterList[i][j]['energy']=0
					clusterList[i][j]['isDead']=True
	return clusterList

 # Each cluster head will broadcost a control slot allotment packet in it's own cluster
def step7(clusterList):
	for i in range(len(clusterList)):
		maxDistance = maxmDistanceFromCH(clusterList[i])
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['isClusterHead']==True and clusterList[i][j]['isDead']==False):
				k = 100*8 #changed
				clusterList[i][j]['energy']-=transmissionEnergy(k,maxDistance)
				if(clusterList[i][j]['energy']<=0):
					clusterList[i][j]['energy']=0
					clusterList[i][j]['isDead']=True
				break
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['isClusterHead']==False and clusterList[i][j]['isDead']==False):
				k = 100*8 #changed
				clusterList[i][j]['energy']-=recievingEnergy(k)
				if(clusterList[i][j]['energy']<=0):
					clusterList[i][j]['energy']=0
					clusterList[i][j]['isDead']=True
	return clusterList

 ################################################
 #                                              #
 #          STEADY-STATE PHASE                  #
 #                                              #
 ################################################

# The member of the node which has data will send the control packet to CH in it's own CS
def step8(clusterList):
	for i in range(len(clusterList)):
		count_=0
		total_nodes=0
		x_ch,y_ch = findClusterHeadLocation(clusterList[i])
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['isClusterHead']==False and clusterList[i][j]['isDead']==False):
				total_nodes+=1
			if(clusterList[i][j]['isClusterHead']==False and clusterList[i][j]['isDead']==False and math.floor(random.random()/0.5)==1):
				count_+=1
				x,y = clusterList[i][j]['location']['x'],clusterList[i][j]['location']['y']
				d = euclid_dist(x/4,y/4,x_ch/4,y_ch/4)
				k = 20*8
				clusterList[i][j]['wantToSendData']=True
				clusterList[i][j]['energy']-=transmissionEnergy(k,d)
				if(clusterList[i][j]['energy']<=0):
					clusterList[i][j]['energy']=0
					clusterList[i][j]['isDead']=True
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['isClusterHead']==True and clusterList[i][j]['isDead']==False):
				k = 20*8
				clusterList[i][j]['energy']-= count_*recievingEnergy(k)
				clusterList[i][j]['energy']-= (total_nodes-count_)*recievingEnergy(k)/2
				if(clusterList[i][j]['energy']<=0):
					clusterList[i][j]['energy']=0
					clusterList[i][j]['isDead']=True
	return clusterList

# On the basis of CS recieved , CH will broadcost the TDMA schedule packet
def step9(clusterList):
	for i in range(len(clusterList)):
		maxDistance = maxmDistanceFromCH(clusterList[i])
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['isClusterHead']==True and clusterList[i][j]['isDead']==False):
				k = 100*8 #changed
				clusterList[i][j]['energy']-=transmissionEnergy(k,maxDistance)
				if(clusterList[i][j]['energy']<=0):
					clusterList[i][j]['energy']=0
					clusterList[i][j]['isDead']=True
				break
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['isClusterHead']==False and clusterList[i][j]['isDead']==False ):
				k = 100*8 #changed
				clusterList[i][j]['energy']-=recievingEnergy(k)
				if(clusterList[i][j]['energy']<=0):
					clusterList[i][j]['energy']=0
					clusterList[i][j]['isDead']=True
	return clusterList

# Each member node will send data packet in it's own alloted DS
def step10(clusterList):
	for i in range(len(clusterList)):
		x_ch,y_ch = findClusterHeadLocation(clusterList[i])
		count_=0
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['isClusterHead']==False and clusterList[i][j]['isDead']==False and clusterList[i][j]['wantToSendData']==True):
				x,y=clusterList[i][j]['location']['x'],clusterList[i][j]['location']['y']
				d = euclid_dist(x/4,y/4,x_ch/4,y_ch/4)
				k = 100*8 #changed
				count_+=1
				clusterList[i][j]['energy']-=transmissionEnergy(k,d)
				if(clusterList[i][j]['energy']<=0):
					clusterList[i][j]['energy']=0
					clusterList[i][j]['isDead']=True
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['isClusterHead']==True and clusterList[i][j]['isDead']==False):
				k = 100*8 #changed
				clusterList[i][j]['energy']-= count_*recievingEnergy(k)
				if(clusterList[i][j]['energy']<=0):
					clusterList[i][j]['energy']=0
					clusterList[i][j]['isDead']=True
				break
	return clusterList

# Each cluster head will aggregate the data and send it to the basestation
def step11(clusterList):
	for i in range(len(clusterList)):
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['isClusterHead']==True and clusterList[i][j]['isDead']==False):
				x_ch,y_ch=clusterList[i][j]['location']['x'],clusterList[i][j]['location']['y']
				x,y=base_stn['x'],base_stn['y']
				x,y=0,105
				d = euclid_dist(x_ch/4,y_ch/4,x,y)
				k = 100*8 #changed
				clusterList[i][j]['energy']-=transmissionEnergy(k,d)
				if(clusterList[i][j]['energy']<=0):
					clusterList[i][j]['energy']=0
					clusterList[i][j]['isDead']=True
				break
	return clusterList

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

show_graphics = 0
factor=4
if(show_graphics==1):
	Screen()
	ht()
	title('Grid')
	speed(0)
	draw_grid_without_cell(4)
	draw_base_station('red',-15,50*factor+40,15,50*factor+40,0,50*factor+70,0,50*factor+20)

base_stn={'x':0,'y':50*factor+55,}
X=[]
Y=[]
file_='random_points100.txt'
listt=[]
with open(file_,'r') as f:
	for line in f:
		listt.append(line)

X = list(map(float,listt[0].strip().split(' ')))
Y = list(map(float,listt[1].strip().split(' ')))

NodesList=[]
NodesList.append([])
for i in range(len(X)):
	Node={'id':0,'energy': 0,'location':{'x':0,'y': 0,},'isClusterHead': False,'isDead':False,'threshold':0.1,'lastTimeCH':-1,'wantToSendData':False}
	Node['id']=i+1
	Node['energy']=5
	Node['location']['x']=X[i]
	Node['location']['y']=Y[i]
	Node['isClusterHead']=False
	NodesList.append(Node)

if(show_graphics==1):
	for i in range(len(X)):
		draw_vertex('red',X[i],Y[i])

roundAxis=[]
numberOfDeadNodesAxis=[]
maxRound=6000
for rnd in range(maxRound):
	cnt=0
	NodesList = calculateClusterHead(NodesList,rnd)
	for i in range(1,len(NodesList)):
		if(NodesList[i]['isClusterHead']==True):
			(x,y)=(NodesList[i]['location']['x'],NodesList[i]['location']['y'])
			cnt+=1
			if(show_graphics==1):
				draw_vertex('green',x,y)
	clusterList = clusterFormation(NodesList)
	clusterList = step4_a(clusterList)
	clusterList = step4_b(clusterList)
	clusterList = step5(clusterList)
	clusterList = step6(clusterList)
	clusterList = step7(clusterList)
	total_frames = 20
	for num in range(total_frames):
		clusterList = step8(clusterList)
		clusterList = step9(clusterList)
		clusterList = step10(clusterList)
		clusterList = step11(clusterList)
	clusterList = makeDead(clusterList)
	for i in range(len(clusterList)):
		for j in range(len(clusterList[i])):
			if(clusterList[i][j]['isDead']==True):
				x,y = clusterList[i][j]['location']['x'],clusterList[i][j]['location']['y']
				if(show_graphics==1):
					draw_vertex('black',x,y)
	roundAxis.append(rnd)
	if(len(clusterList)>0):
		NodesList = convertToNodesList(clusterList)
		numberOfDeadNodesAxis.append(findNumberOfDeadNodes(clusterList))
	else:
		numberOfDeadNodesAxis.append(numberOfDeadNodesAxis[-1])
	NodesList = resetAllCH(NodesList,show_graphics)
	print('len:',len(NodesList))
	print('After Round {}:'.format(rnd),cnt)

print(json.dumps(NodesList,indent=4))
print('roundAxis:',roundAxis)
print('numberOfDeadNodesAxis',numberOfDeadNodesAxis)
file_name='output_bma_mac100.txt'
with open(file_name,'w') as f:
	for i in roundAxis:
		f.write(str(i)+' ')
	f.write('\n')
	for i in numberOfDeadNodesAxis:
		f.write(str(i)+' ')
firstDeadRound = findFirstDeadNodeRound(roundAxis,numberOfDeadNodesAxis)
print("Round at which the first node is dead is ",firstDeadRound)

listt_1=[]
file_ = 'output_bma_mac100.txt'
with open(file_,'r') as f:
	for line in f:
		listt_1.append(line)

X1=list(map(int,listt_1[0].strip().split(' ')))
Y1=list(map(int,listt_1[1].strip().split(' ')))
firstDeadNodeRound = findFirstDeadNodeRound(X1,Y1)
lastDeadNodeRound = findLastDeadNodeRound(X1,Y1)
roundAxis=roundAxis[0:firstDeadNodeRound//2]+roundAxis[firstDeadNodeRound//2:6000:65]
numberOfDeadNodesAxis=numberOfDeadNodesAxis[0:firstDeadNodeRound//2]+numberOfDeadNodesAxis[firstDeadNodeRound//2:6000:65]
roundAxis=np.asarray(roundAxis)
numberOfDeadNodesAxis=np.asarray(numberOfDeadNodesAxis)
roundAxis_new = np.linspace(roundAxis.min(), roundAxis.max(),60000)
numberOfDeadNodesAxis_smooth=spline(roundAxis,numberOfDeadNodesAxis,roundAxis_new)
plt.text(firstDeadNodeRound+100, 0, firstDeadNodeRound)
plt.text(lastDeadNodeRound-500, 100, lastDeadNodeRound)
plt.plot(roundAxis_new,numberOfDeadNodesAxis_smooth,'b',label='BMA-MAC')
plt.xlabel('Number of rounds')
plt.ylabel('Number of Dead Nodes')
plt.title('Graph between number of dead nodes and number of rounds\n(100x100 grid)')
plt.legend()
plt.show()
if(show_graphics==1):
	done()

