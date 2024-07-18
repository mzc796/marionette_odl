#!/usr/bin/python3.9
import poison_link_vlan as po_link
import os
import numpy as np
import trans_topo as topo
import networkx as nx
import subprocess
import time
import math
import read_config_table as flow
import topo_flow_util as tf_util
os.sys.path.insert(1, 'pois_topo_RL')
import bridge as brdg
import RL_model as RL
import utilities as util
import fat_tree_topo_reader as topo_reader

# Collect Topology Information
process = subprocess.Popen(["bash/req_topo.sh","original"])
process.wait()
os.system('python3.9 draw_fattree_topo.py original')
topo_info = topo.read_topo("original")
A = topo_info.get("adj_matrix")

# Initiate Parameters for Reinforcement Learning Model
expect_incr = 4
np.set_printoptions(threshold=np.inf)
num_f = 120
deg_thres = 1
st_list = topo_reader.gen_flows(A, num_f, deg_thres)
vul_node = 6
baseline = util.get_cflow_num(A, st_list, vul_node)
expected_num = baseline + expect_incr
expected_sim = 0.8
step_len = 5
node_num = len(A)
edge_num = util.get_edge_num(A)
action_space_size = math.comb(edge_num*2,2)
max_edge_num = node_num*(node_num-1)//2
project_name = "FatTree"


# Build Reinforcement Learning Model
env = RL.build_env(A,st_list,vul_node,expected_num, expected_sim, step_len, action_space_size, project_name)
reward_thrshd = 1
pois_topo_info = RL.learn_topo(env, reward_thrshd)
print(pois_topo_info)
Ap = pois_topo_info.get("adj_matrix")
util.draw_graph(Ap,"figure/RL_topo")


# Compose and Set Poison
print("Compose and set poison")
poi_link_list = brdg.setPoison(A,Ap)
print("Poi_link_list is")
print(poi_link_list)
vid_link_map, mal_ins_dict = po_link.poison_links(poi_link_list,node_num)
print("malicious insertion dict is:")
print(mal_ins_dict)
print("vlan_id link map is:")
print(vid_link_map)


