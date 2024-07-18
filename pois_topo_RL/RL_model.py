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
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
import os
import utilities as util
import sim_util as sim_util
import TopoPoison as TopoPoison
import timeit

#Work well on Python3.9 but not Python3.10, compatible errors happen

def build_env(A,st_list, vul_node, expected_num, expected_sim, step_len, action_space_size, project_name):
    ori_A = util.clone(A)
    best_topo = util.clone(A)
    node_num = len(A)
    undir_edge_num = util.get_edge_num(A)
    max_edge_num = node_num*(node_num-1)//2
    max_degree = util.extract_max(A)
    path_num = len(st_list)
    sh_paths = util.get_sh_paths(A,st_list)
    neighbours = util.get_neighbours(A, vul_node)
    baseline = util.get_cflow_num(A,st_list,vul_node)
    env = TopoPoison.TopoPoisoningEnv(vul_node,node_num,action_space_size,max_degree, sh_paths, path_num, A, ori_A, st_list, neighbours, baseline, expected_num, best_topo, expected_sim, step_len, project_name)
    
    env = Monitor(env)
#    check_env(env)
    return env

def learn_topo(env, reward_thrshd):
    start = timeit.default_timer()
    #save_path = os.path.join('TrainingV1', 'Saved Models')
    #log_path = os.path.join('TrainingV1','logs')
    #model = DQN('MlpPolicy', env, verbose=1, tensorboard_log=log_path)
    model = DQN('MlpPolicy', env, verbose=1)
    stop_callback = StopTrainingOnRewardThreshold(reward_threshold=1, verbose=1)
    eval_callback = EvalCallback(env,
                             callback_on_new_best=stop_callback,
                             eval_freq=10000,
                             verbose=1)                  
    model.learn(total_timesteps=1000, callback=eval_callback)
    model_name = 'fattree_2switches'
    #topo_poison_path = os.path.join('TrainingV1','saved_models', model_name)
    #model.save(topo_poison_path)
    best_record = env.best
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    return best_record
    
