import numpy as np
import random
import os
import networkx as nx 
import matplotlib.pyplot as plt
import math
import random as rnd
import sim_util

def clone(A):
	cloneA = np.zeros((len(A),len(A)),dtype = int)
	for i in range(0,len(A)):
		for j in range(0,len(A)):
			if A[i][j] > 0:
				cloneA[i][j] = A[i][j]
	return cloneA

def get_phi(l):
	phi = np.ones((l,1))
	phi = phi*0.51
	return phi

def get_rand_phi(l):
	phi = np.ones((l,1))
	for i in range(0,l):
		phi[i][0] = rnd.random()
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
				
	
def extract_max(A):
    m_list = []
    for i in range(0,len(A)):
        m = max(A[i])
        m_list.append(m)
    ma = max(m_list)
    return ma

def get_edge_num(A):
    count = 0
    for i in range(0,len(A)):
        for j in range(i,len(A)):
            if A[i][j] != 0:
                count += 1
    return count

def get_cflow_num(A, st_list, vul_node):
    count = 0
    G = nx.Graph(A)
    for i in range(0,len(st_list)):
        src = st_list[i][0]
        dst = st_list[i][1]
        sh_path = nx.shortest_path(G,source=src, target = dst)
        if vul_node in sh_path:
            count += 1
    return count

def draw_graph(A, file_name):
    G = nx.Graph(A)
    fixed_positions = {0:(20,30),1:(50,30),2:(80,30),3:(110,30),4:(10,20),5:(25,20),6:(40,20),7:(55,20),8:(75,20),9:(90,20),10:(105,20),11:(120,20),12:(10,10),13:(25,10),14:(40,10),15:(55,10),16:(75,10),17:(90,10),18:(105,10),19:(120,10),20:(-10,0),21:(0,0),22:(10,0),23:(20,0),24:(30,0),25:(40,0),26:(50,0),27:(60,0),28:(70,0),29:(80,0),30:(90,0),31:(100,0),32:(110,0),33:(120,0),34:(130,0),35:(140,0)}

    fixed_nodes = fixed_positions.keys()
    pos = nx.spring_layout(G,pos=fixed_positions, fixed = fixed_nodes)
    f = plt.figure()
    nx.draw(G, pos = pos, with_labels = True, node_color = 'orange')
    f.savefig(file_name + ".png")

def get_neighbours(A,vul_node):
    neighbours = {}
    for i in range(0,len(A)):
        if A[i][vul_node] != 0:
            key = i #node_id
            value = A[i][vul_node] #port_id
            neighbours.update({key:value}) 
    print("neighbours:")
    print(neighbours)
    return neighbours

def port_switching(A, real_action):
    a = real_action[0]
    b = real_action[1]
    ax = int(a.split('-')[0])
    ay = int(a.split('-')[1])
    bx = int(b.split('-')[0])
    by = int(b.split('-')[1])
    # ax == bx should be true
    temp = 0
    temp = A[ax][ay]
    A[ax][ay] = A[bx][by]
    A[bx][by] = temp
    return A

def two_switching(A, real_action):
    matrix_test = np.zeros((len(A),len(A)))
    for i in range (0, len(A)):
        for j in range(0,len(A)):
            matrix_test[i][j] = A[i][j]
    a = real_action[0]
    b = real_action[1]
    ax = int(a.split('-')[0])
    ay = int(a.split('-')[1])
    bx = int(b.split('-')[0])
    by = int(b.split('-')[1])
    temp = 0
    #switch upper triangle
    temp = matrix_test[ax][by]
    matrix_test[ax][by] = matrix_test[ax][ay]
    matrix_test[ax][ay] = temp
    temp = matrix_test[bx][ay]
    matrix_test[bx][ay] = matrix_test[bx][by]
    matrix_test[bx][by] = temp
    #switch lower triangle
    #because of port info as the matrix element, we need to adjust it before lower triangle switching
    if matrix_test[ay][ax] != matrix_test[by][bx]:
        max_a = max(matrix_test[ay])
        max_b = max(matrix_test[by])
        if max_a > max_b:
            cx = ay
            cy = ax
            dx = by
            dy = bx
        else:
            cx = by
            cy = bx
            dx = ay
            dy = ax
        for i in range(0,len(matrix_test)):
            if matrix_test[cx][i] == matrix_test[dx][dy]:
                temp = matrix_test[cx][cy]
                matrix_test[cx][cy] = matrix_test[cx][i]
                matrix_test[cx][i] = temp
    temp = matrix_test[by][ax]
    matrix_test[by][ax] = matrix_test[ay][ax]
    matrix_test[ay][ax] = temp
    temp = matrix_test[ay][bx]
    matrix_test[ay][bx] = matrix_test[by][bx]
    matrix_test[by][bx] = temp
    #check if the changed graph is connected, if not penalty applied
    G_check = nx.Graph(matrix_test)
    if nx.is_connected(G_check):
        for i in range (0, len(A)):
            for j in range(0,len(A)):
                A[i][j] = matrix_test[i][j]
        is_connected = True
    else:
        is_connected = False
	#check if the adj matrix is still symmetric
    if not check_sym_shape(A):
        print("!!!!not symmetric!!!")
        print(A)
    return A, is_connected

def check_sym_shape(A):
	An = sim_util.normalizeA(A)
	rtol=1e-5
	atol=1e-8
	return np.allclose(An, An.T, rtol=rtol, atol=atol)

def cal_score(st_list, baseline, A, neighbours):
    G = nx.Graph(A)
    sh_path_list = []
    #score = 0 - baseline
    score = 0
    for i in range(0,len(st_list)):
        src = st_list[i][0]
        dst = st_list[i][1]
        sh_path = nx.shortest_path(G,src, dst)
        sh_path_list.append(sh_path)
    for i in range(0,len(sh_path_list)):
        path_len = len(sh_path_list[i])
        for j in range(0,path_len-1):
            test_node = sh_path_list[i][j]
            next_hop = sh_path_list[i][j+1]
            if test_node in list(neighbours.keys()):
                if A[test_node][next_hop] == neighbours[test_node]:
                    score += 1
                    break
    return (score,sh_path_list)

def cal_coverage(st_list, A, neighbours, n_vul):
    G = nx.Graph(A)
    sh_path_list = []
    score = 0
    for i in range(0,len(st_list)):
        src = st_list[i][0]
        dst = st_list[i][1]
        sh_path = nx.shortest_path(G,src, dst)
        sh_path_list.append(sh_path)
    for i in range(0,len(sh_path_list)):
        if sh_path_list[i][0] == n_vul:
            score += 1
        else:
            path_len = len(sh_path_list[i])
            for j in range(0,path_len-1):
                test_node = sh_path_list[i][j]
                next_hop = sh_path_list[i][j+1]
                if test_node in list(neighbours.keys()):
                    if A[test_node][next_hop] == neighbours[test_node]:
                        score += 1
                        break
    return (score,sh_path_list)


     
def create_action_space(A):
        node_num = len(A)
        action_space = []
        sw_space = []
        #iterate non-zero element 
        for i in range(0, node_num):
            for j in range(0, node_num):
                #if adj_matrix[j][i] != 0 & len(sw_space)<=2:
                if A[i][j] != 0:
                    key = str(i)+'-'+str(j)
                    sw_space.append(key)
                    
        #add two_switching actions to the action_space
        for i in range(0,len(sw_space)):
            for j in range(i+1, len(sw_space)):
                ax = sw_space[i].split('-')[0]
                bx = sw_space[j].split('-')[0]
                if ax == bx:
                    continue
                else:
                    pair = (sw_space[i],sw_space[j])
                    action_space.append(pair)
        #add port_switching actions to the action_space
        for i in range(0,node_num):
            port_list = []
            for j in range(0,node_num):
                if A[i][j] != 0:
                    port_list.append(str(i)+'-'+str(j))
            #print(port_list)
            for i in range(0, len(port_list)):
                for j in range(i+1, len(port_list)):
                    pair = (port_list[i],port_list[j])
                    action_space.append(pair)
        return action_space
    
def can_switch(A, sw_action):
        flag = False
        if len(sw_action) != 2:
            print("sw_action format error")
            return False
        position_1 = sw_action[0]
        position_2 = sw_action[1]
        ax = int(position_1.split('-')[0])
        ay = int(position_1.split('-')[1])
        bx = int(position_2.split('-')[0])
        by = int(position_2.split('-')[1])
        #print(ax,ay,bx,by)
        if ax == bx and ay != by:
            flag = True
            info = "port switching"
        elif ax == by or bx == ay or A[ax][by] != 0 or A[bx][ay] != 0:# switching will cause non-zero on the diagnal, illegal switching
            flag = False
            info = "illegal switching"
        else:
            flag = True
            info = "two switching"
        return flag, info

def update_best(best_record, matrix, paths, sim, score):
        for i in range(0,len(matrix)):
            for j in range(0,len(matrix)):
                best_record.get("adj_matrix")[i][j] = matrix[i][j]

        for i in range(0,len(paths)):
            best_record.get("paths")[i] = paths[i]
        #best_record.update({"adj_matrix":matrix})
        #best_record.update({"paths":paths})
        #print("update best:"+str(sim))
        #print(matrix)
        best_record.update({"similarity":sim})
        best_record.update({"score":score})
        return best_record

def num_w_vul(n, paths):
	count = 0
	total = len(paths)
	for i in range(0,total):
		for j in range(0,len(paths[i])):
			if n == paths[i][j]:
				count +=  1
	return count

def get_pool(A):
	node_pool = []
	pool = []
	for i in range(0,len(A)):
		m = max(A[i])
		if m < 3:
			node_pool.append(i)
	for i in range(0,len(node_pool)):
		for j in range(i+1,len(node_pool)):
			st=[node_pool[i],node_pool[j]]
			pool.append(st)
	return pool

def get_rand_st_list(num,pool):
	seed = 1
	rnd.shuffle(pool)
	st_list = []
	for i in range(0,num):
		st_list.append(pool[i])
	return st_list


def get_sh_paths(A,st_list):
	sh_paths = []
	G = nx.Graph(A)
	for i in range(0,len(st_list)):
		src = st_list[i][0]
		dst = st_list[i][1]
		sh_path = nx.shortest_path(G, source = src, target = dst)
		sh_paths.append(sh_path)
	return sh_paths
