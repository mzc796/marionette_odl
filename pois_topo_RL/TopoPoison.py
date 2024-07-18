#!/usr/bin/env python

import gym
from gym import Env
from gym.spaces import Discrete, Box, Dict, Tuple, MultiBinary, MultiDiscrete

#import helper
import numpy as np
import random
import os
import networkx as nx 
import matplotlib.pyplot as plt

#import stable baselines stuff
from stable_baselines3 import PPO, DQN, A2C
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
import os
import utilities as util
import sim_util as sim_util


class TopoPoisoningEnv(Env):
    def __init__(self, vul_node, node_num, action_space_size, max_degree, sh_paths, path_num, adj_matrix, ori_adj_matrix, st_list, neighbours, baseline, expectation, best_topo, expected_sim, step_len,proj_name):
        self.vul_node = vul_node
        #initiate random paths
        self.st_list = st_list
        self.ori_adj_matrix = ori_adj_matrix
        self.baseline = baseline
        self.neighbours = neighbours
        self.sh_path_list = sh_paths
        self.step_length = step_len
        self.expectation = expectation
        self.init_step_len = step_len
        self.init_best_topo = best_topo
        self.init_baseline = baseline
        self.init_sh_paths = sh_paths
        self.expected_sim = expected_sim
        self.action_space = Discrete(action_space_size)
        self.observation_space = Box(low=0,high=max_degree,shape=(node_num,node_num), dtype=int)
        self.state = adj_matrix #(recent topo, gained number of eavesdropped flows)
        self.p_name = proj_name
        self.best = {"adj_matrix":best_topo, "paths":sh_paths, "similarity": -1, "score": baseline}
    
    def step(self, action):
        self.step_length -= 1
        done = False
        reward = 0
        score = 0
        info = {}
        sim = 0
        is_connected = False
        score, self.sh_path_list = util.cal_coverage(self.st_list, self.state, self.neighbours, self.vul_node)
        valid_action_space = util.create_action_space(self.state)
        if action < len(valid_action_space):
            real_action = valid_action_space[action]
            flag, msg = util.can_switch(self.state, real_action)
            if flag and score < self.expectation:
                info = {msg}
                if msg == "two switching":
                    self.state, is_connected = util.two_switching(self.state, real_action)
                    if is_connected: # the graph after two switching is still connected
                        score, self.sh_path_list = util.cal_coverage(self.st_list, self.state, self.neighbours, self.vul_node)
                else:
                    self.state = util.port_switching(self.state, real_action)
                    score, self.sh_path_list = util.cal_coverage(self.st_list, self.state, self.neighbours, self.vul_node)
            
            sim = sim_util.EOverlap(self.ori_adj_matrix, self.state)
        #when eavedropping
        if sim >= self.expected_sim and score >= self.expectation:
            reward = 1
            self.best = util.update_best(self.best, self.state, self.sh_path_list, sim, score)
            #v_num = util.num_w_vul(self.vul_node,self.sh_path_list)
           # if score > self.best.get("score") and sim >= self.best.get("similarity"):
            #    reward = 20
             #   self.best = util.update_best(self.best, self.state, self.sh_path_list, sim, score)
        else:
            reward = -1
        if self.step_length <= 0 or reward > 0:
            done = True
        return self.state, reward, done, {}
        
    def render(self):
        pass
    def reset(self):
        ori_adj_clone = util.clone(self.ori_adj_matrix)
        self.state = ori_adj_clone
        self.step_length = self.init_step_len
        #self.best = {"adj_matrix":self.init_best_topo, "paths":self.init_sh_paths, "similarity": -1, "score": self.init_baseline}
        return self.state




