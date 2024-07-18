#!/usr/bin/env python3.9
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import sys

def adj2PA(A):
	row = len(A)
	column = len(A[0])
	for i in range(0,row):
		mark = 0
		for j in range(0,column):
			if A[i][j] != 0:
				mark += 1
				A[i][j] = mark
	return A

def gen_flows(A,num_f, deg_thres):
	node_num = len(A)
	node_deg = {}
	#get the degree info of every node
	for i in range(0,node_num):
		deg = np.count_nonzero(A[i])
		pair = [(str(i), deg)]
		node_deg.update(pair)
	max_deg = 0
	
	#sort nodes based on their degree
	sort_n = dict(sorted(node_deg.items(), key=lambda item:item[1]))
	print("sort_n")
	print(sort_n)
	#put the nodes with degree < deg_thres in the pool
	pool = []
	for key in sort_n:
		if sort_n.get(key) <= deg_thres:
			pool.append(int(key))
	print('pool size:',len(pool))
	print(pool)
	#creat flows
	flows = []
	combination_size = math.comb(len(pool),2)
	print("combination size:",combination_size)
	if num_f >= combination_size:
		print("the number of flows is impossible to get")
		num_f = math.comb(len(pool),2)
		for i in range(0,len(pool)):
			for j in range(i+1,len(pool)):
				sd = [pool[i],pool[j]]
				flows.append(sd)
	else:
		for j in  range(0,num_f):
			j += 1
			if j < num_f:
				random.seed(j)
				sd = random.sample(pool,2)
				if sd not in flows:
					flows.append(sd)
				else:
					j -= 1
	return flows

def gen_fat_tree():
	num_node = 36
	adj = np.zeros((num_node,num_node))
	#layer 1 to 2
	for i in range(0, 2):
		adj[i][4] = 1
		adj[i][6] = 1
		adj[i][8] = 1
		adj[i][10] = 1
		
		adj[4][i] = 1
		adj[6][i] = 1
		adj[8][i] = 1
		adj[10][i] = 1

	for j in range(2,4):
		adj[j][5] = 1
		adj[j][7] = 1
		adj[j][9] = 1
		adj[j][11] = 1

		adj[5][j] = 1
		adj[7][j] = 1
		adj[9][j] = 1
		adj[11][j] = 1
	for i in range(0,4):
		h = 4+i*2
		l = 12+i*2
		for j in range(0,2):
			h = h+j
			adj[h][l] = 1
			adj[h][l+1] = 1
			adj[l][h] = 1
			adj[l+1][h] = 1
	for i in range(0,8):
		h = 12+i
		l = 20+2*i
		adj[h][l] =1
		adj[h][l+1] = 1		
		adj[l][h] =1
		adj[l+1][h] = 1		
	return adj
	
		
			

def read_topo():
	adj = gen_fat_tree()
	#get port_adj_matrix
	PA = adj2PA(adj)
	G = nx.Graph(adj)
	return PA,G

def print_topo(G):
	fix_pos = {0:(20,10), 1:(50,10), 2:(80,10), 3:(110,10),4:(10,0),5:(30,0),6:(40,0),7:(60,0),8:(70,0),9:(90,0),10:(100,0),11:(120,0),12:(10,-10),13:(30,-10),14:(40,-10),15:(60,-10),16:(70,-10),17:(90,-10),18:(100,-10),19:(120,-10),20:(0,-20),21:(10,-20),22:(20,-20),23:(30,-20),24:(35,-20),25:(45,-20),26:(50,-20),27:(60,-20),28:(70,-20),29:(80,-20),30:(85,-20),31:(95,-20),32:(100,-20),33:(110,-20),34:(120,-20),35:(130,-20)}
	fixed_nodes = fix_pos.keys()
	pos = nx.spring_layout(G,k=5/math.sqrt(G.order()),pos=fix_pos, fixed=fixed_nodes)
	#pos = nx.spring_layout(G,k=5/math.sqrt(G.order()))
	nx.draw(G,pos=pos,node_size=150,with_labels=True, node_color='orange')
	plt.show()

def test():
	PA_matrix,G = read_topo()
	num_f = 120
	deg_thres = 1
	flow_pool = gen_flows(PA_matrix, num_f, deg_thres)
	#np.set_printoptions(threshold=np.inf)
	print(PA_matrix)
	print(flow_pool)
	print_topo(G)

#test()
