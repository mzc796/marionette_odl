import os
import numpy as np
import math



def locate_real_nx(A, node, port):
    nx = -1
    for i in range(0,len(A[node])):
        if A[node][i] == port:
            nx = i
    if nx == -1:
        print("fail to find the next hop in real topo")
        print(node,port)
    return nx

def get_nx_port(A, node, port):
    nx = -1
    for i in range(0,len(A[node])):
        if A[node][i] == port:
            nx = i
    if nx == -1:
        print("fail to find next hop")
    port = A[nx][node]
    return port

def setPoison(A,Ap):
    poi_link_list=[]
    for i in range(0,len(A)):
        for j in range(0,len(A[0])):
            if Ap[i][j] != 0:
                if A[i][j] != Ap[i][j]:
                    real_nx = locate_real_nx(A, i, Ap[i][j])
                    t1 = str(i+1)+":"+str(Ap[i][j]) #openflow sw index starts from 1 not 0
                    nx_port = get_nx_port(Ap, i, Ap[i][j])
                    t2 = str(j+1)+":"+str(nx_port) #openflow sw index starts from 1 not 0
                    Ap[i][j] = 0
                    Ap[j][i] = 0
                    poi_link = t1 + "-" + t2
                    poi_link_list.append(poi_link)
    return poi_link_list


