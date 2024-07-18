import numpy as np
import random
import os
import networkx as nx 
import matplotlib.pyplot as plt
#import utilities as util
import math

def get_phi(l):
	phi = np.ones((l,1))
	phi = phi*0.51
	return phi

def get_rand_phi(l):
	phi = np.ones((l,1))
	for i in range(0,l):
		random.seed(i)
		phi[i][0] = random.random()
	return phi

def get_ac(h):
	temp1 = 4 * h ** 2
	temp2 = 1 - temp1
	a = temp1 / temp2
	c = 2 * h / temp2
	return a,c

def get_h(c1,c2):
	temp1 = c1 ** 2 + 4 * c2
	temp2 = -c1 + math.sqrt(temp1)
	temp3 = temp2 / (8*c2)
	h = math.sqrt(temp3)
	return h

def get_c1(D):
	c1 = 2
	for i in range(0,len(D)):
		c1 += D[i][i]
	return c1

def get_c2(D):
	c2 = -1
	for i in range(0,len(D)):
		temp = D.item(i,i) ** 2
		c2 += temp
	return c2

def get_deg_matrix(A):
	D = np.zeros((len(A),len(A)), dtype = int)
	for i in range(0,len(A)):
		for j in range(0,len(A)):
			if A.item(i,j) > 0:
				D[i][i] += 1
	return D
	
def normalizeA(A):
    An = np.zeros((len(A),len(A)),dtype = int)
    for i in range(0,len(A)):
        for j in range(0,len(A)):
            if A.item(i,j) > 0:
                An[i][j] = 1 
    return An

def checkIdentical(A,B):
    flag = False
    if len(A) != len(B):
        print("input error, two matrices don't have the same size")
        return False
    for i in range(0,len(A)):
        for j in range(0,len(A)):
            if A[i][j] != B[i][j]:
                flag = False
                #print(i,j)
    return True

def getCliqueAdj(l):
    ones = np.ones((l,l),dtype = int)
    iden = np.identity(l,dtype = int)
    clique = np.subtract(ones,iden)
    #print(clique)
    return clique

def cal_belief(A, phi):
    h_h = 0.001
    a,c = get_ac(h_h)
    #print(a)
    #print(c)
    I = np.identity(len(A), dtype = int)
    DA = get_deg_matrix(A)
    TA = I + a*DA - c*A
    inv_TA = np.linalg.inv(TA)
    bA = np.dot(inv_TA,phi)
    return bA

def cal_simvec(A):
    h_h = 0.001
    a,c = get_ac(h_h)
    #print(c)
    a = c ** 2
    #print(a)
    I = np.identity(len(A), dtype = int)
    DA = get_deg_matrix(A)
    TA = I + a*DA - c*A
    inv_TA = np.linalg.inv(TA)
    return inv_TA

def cal_rootEDist(sA,sB):
    ss = 0
    for i in range(0,len(sA)):
        for j in range(0, len(sA[i])):
            temp1 = (np.sqrt(sA[i][j])-np.sqrt(sB[i][j])) ** 2
            ss += temp1
    d = np.sqrt(ss)
    return d


def cal_nEDist(bA,bB,bC,phi):
    ss = 0
    for i in range(0,len(bA)):
        temp1 = (bA[i] - bB[i]) ** 2
        temp2 = (bC[i] - phi[i]) ** 2
        temp3 = temp1 / temp2
        ss += temp3
    d = np.sqrt(ss)
    return d

def cal_sim (d):
    sim = 1/(1+d)
    return sim

def RFaBP(A,B):
	An = normalizeA(A)
	Bn = normalizeA(B)
	C = getCliqueAdj(len(A))
	phi = get_rand_phi(len(A))
	bA = cal_belief(An, phi)
	bB = cal_belief(Bn, phi)
	bC = cal_belief(C, phi)
	#print(bA)
	#print(bB)
	#print(bC)
	d = cal_nEDist(bA,bB,bC,phi)
	sim = cal_sim(d)
	#print(sim)
	return sim

def FaBP(A,B):
	An = normalizeA(A)
	Bn = normalizeA(B)
	C = getCliqueAdj(len(A))
	phi = get_phi(len(A))
	bA = cal_belief(An, phi)
	bB = cal_belief(Bn, phi)
	bC = cal_belief(C, phi)
	#print(bA)
	#print(bB)
	#print(bC)
	d = cal_nEDist(bA,bB,bC,phi)
	sim = cal_sim(d)
	#print(sim)
	return sim

def RFaBP_rEDist(A,B):
	An = normalizeA(A)
	Bn = normalizeA(B)
	phi = get_rand_phi(len(A))
	bA = cal_belief(An, phi)
	bB = cal_belief(Bn, phi)
	#print(bA)
	#print(bB)
	d = cal_rootEDist(bA,bB)
	sim = cal_sim(d)
	#print(sim)
	return sim

def FaBP_rEDist(A,B):
	An = normalizeA(A)
	Bn = normalizeA(B)
	phi = get_phi(len(A))
	bA = cal_belief(An, phi)
	bB = cal_belief(Bn, phi)
	#print(bA)
	#print(bB)
	d = cal_rootEDist(bA,bB)
	sim = cal_sim(d)
	#print(sim)
	return sim


def DeltaCon(A,B):
	An = normalizeA(A)
	Bn = normalizeA(B)
	sA = cal_simvec(An)
	sB = cal_simvec(Bn)
	d = cal_rootEDist(sA,sB)
	sim = cal_sim(d)
	return sim

def EOverlap(A,B):
	same = 0
	edge_num = 0
	for i in range(0,len(A)):
		for j in range(0,len(A[i])):
			if A[i][j] != 0:
				edge_num += 1
				if A[i][j] == B[i][j]:
					same += 1
	sim = same/edge_num
	return sim

def SequenceSim(A,B):
	s = ""
	Al = s.join(s.join(map(str,sub)) for sub in A.tolist())
	Bl = s.join(s.join(map(str,sub)) for sub in B.tolist())
	k = 3
	same = 0
	for i in range(0,len(Al)-k+1):
		value1 = ""
		value2 = ""
		for j in range(0,k):
			value1 += Al[i+j]
			value2 += Bl[i+j]
		if value1 == value2:
			same += 1
	sim = same/(len(Al)-k+1)
	return sim
