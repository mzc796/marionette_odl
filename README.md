# Artifact on Zenodo
https://doi.org/10.5281/zenodo.12786197

# Video Demo
https://youtu.be/qwHv9tXd-ts

https://youtu.be/R2dOJO3hB1E

# Part 2: Marionette as an Application on OpenDaylight with Fat Tree Topology
Marionette attacks OpenDaylight Calcium (karaf-0.20.1.zip) from a malicious application to alter the topology with the goal of making more flows to an eavesdropping point on an enterprise fat tree topology. Step 1: The Marionette collects nodes and topology information to learn a deceptive topology based on an enterprise fat-tree topology to meet the attack goal. Step 2: The Marionette composes and sends corresponding poisonous flow entries to the networking leading the OpenDaylight controller to discover a deceptive topology as designed in Step 1 independently.


## Virtual Machine Platform
VMware Fusion
## Virtual Machine Summary
Memory: 32GB

Storage: 50GB

CPU: 2 cores, AMD64 Architecture

Installation Disc: ubuntu-22.04.4-desktop-amd64.iso

NOTE: After installation and reboot, please DO NOT select `Install Now` when the `Software Updater` window pops up. Otherwise, it may cause an error of `not enough space` later. High memory and storage are required due to the reinforcement learning algorithm.
## Software Dependencies
1. OpenDaylight Calcium
2. Stable-baselines3==1.7.0
3. Mininet (any version supports OpenFlow v1.3)

## Build and Run OpenDaylight VM
1. Install Python3.9 and stable-baselines3
  ```
  sudo apt-get update
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt-get install python3.9 vim wget net-tools curl
  sudo apt install python3-pip python3.9-distutils
  python3.9 -m pip install --upgrade Pillow
  python3.9 -m pip install networkx matplotlib
  python3.9 -m pip install 'stable-baselines3==1.7.0'
  ```
2. Install and Configure Java
> (1) Install Java
  ```
  sudo apt-get install openjdk-17-jdk
  ```
> (2) Configure JAVA_HOME to /etc/profile

  ```
  sudo vim /etc/profile
  ```
> (3) Add the following to the end of /etc/profile
  ```
  JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
  PATH=$PATH:$HOME/bin:$JAVA_HOME/bin
  export JAVA_HOME
  export JRE_HOME
  export PATH
  ```
> (4) Make JAVE_HOME valid and Test JAVA Version
  ```
  source /etc/profile
  java -version
  ```
3. Install Latest OpenDaylight (Calcium, June 27, 2024)
> (1) Download OpenDaylight Calcium
  ```
  wget https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.20.1/karaf-0.20.1.zip
  ```
>  (2) Extract it to $HOME
  ```
  unzip karaf-0.20.1.zip
  ```
> (3) Configure ODL-0.20.1 Environment
  ```
  cd karaf-0.20.1/bin
  vim setenv
  ```
> (4) Add the following to the setenv file
  
  ```
  export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
  ```
4. Run OpenDaylight and Install OpenFlow Plugins
> (1) Run OpenDaylight
  ```
  sudo ./karaf
  ```
> (2) Install OpenFlow Plugins
  ```
  opendaylight-user@root>feature:install odl-openflowplugin-app-topology-lldp-discovery odl-openflowplugin-app-table-miss-enforcer odl-openflowplugin-flow-services odl-openflowplugin-flow-services-rest odl-openflowplugin-app-topology-manager odl-openflowplugin-app-lldp-speaker
  ```
> (3) Check Listening Ports
>
> Open another terminal
> 
  ```
  sudo lsof -i -P -n | grep LISTEN
  ```
  NOTE: If ```tcp *:6653 (LISTEN)``` and ```tcp *:8181 (LISTEN)``` do not show, shut down OpenDaylight with ```Control+D``` and restart ```sudo ./karaf```

## Build and Run Mininet VM
   
  We build another VM to run Mininet. The Mininet VM use the ODL VM setting but with Memory:4GB, Storage: 50GB

1. Install mininet
  ```
  sudo apt-get update
  sudo apt-get install mininet
  ```
2. Download marionette_odl.zip and extract it to $HOME
   
   NOTE: If you download the code from GitHub and the name is ```marionette_odl-master.zip```, please change the folder name to ```marionette_odl``` after extracting it to $HOME.
   
4. Run Mininet with Customized Topology and Connect to Remote Controller with $IP_ODL
  ``` 
  cd marionette_odl/mininet_fattree
  sudo chmod 774 fattree_mn_run.sh dump_flows.sh
  sudo ./fattree_mn_run.sh $IP_ODL
  ```
  NOTE: The $IP_ODL can be known with the command ```ifconfig``` on OpenDaylight VM.
  
### Utility for Checking Flow Entries 
  ```
  sudo ./dump_flows.sh $sw_id
  ```
  For Example,
  ```
  sudo ./dump_flows.sh s1
  ```
## Marionette Attack
To efficiently demonstrate Marionette with budgeted time (within 5 minutes) and resources (2 core CPU, Memory: 32GB), we give Marionette an easy goal to run the reinforcement learning algorithm to compute an adequate deceptive topology.

In `main.py`, we set the eavesdropping node as node 6 (openflow:7), the expected increased number of eavesdropping flows is 4, the similarity lower bound is 80%, and the degree sequence must remain unchanged after altering the topology.

1. Open another terminal on the OpenDaylight VM
2. Download marionette_odl.zip and extract it to $HOME.
   
   NOTE: If you download the code from GitHub and the name is ```marionette_odl-master.zip```, please change the folder name to ```marionette_odl``` after extracting it to $HOME.
   
3. Run Marionette
  ```
  cd marionette_odl/
  python3.9 main.py
  ```
### Result
  
 After the program is finished, we go to the 'figure' folder. There will be three figures:

  - topo_original.png: The topology discovered by the ODL controller before being poisoned, which is the real topology.

  - RL_topo.png: The Reinforcement Learning produced deceptive topology.

  - topo_deceptive.png: The topology discovered by the ODL controller after being poisoned by Marionette, which is the deceptive topology.

  The RL_topo.png should be the same as topo_deceptive.png, which proves the success of precise link manipulation.
  
### Utility to Reset the Environment

```
python3.9 clear_all.py 36
```

NOTE: `36` is the total number of switches in this fat tree topology

### NOTE: 

1. Because the latest version (e.g. at least after the version of 15.3.0) of OpenDaylight removed the user interface project DLUX and we want to show the changes of the topology easily, we use RESTful API to GET topology in real-time and draw the topology with nodes having fixed positions by scripts.

2. The node indices start from 0 in RL_topo.png but start from 1 in topo_deceptive.png.
3. I recently found some bugs on the OpenDaylight Calcium (karaf-0.20.1.zip). When restarting the ODL with the features installed, the restful URLs (the scripts under `bash` folder) encounter 401 errors. That is the bug of OpenDaylight Calcium, not Marionette. Please consider going back to Step `3` of `Build and Run OpenDaylight VM` and continue.
4. You can also use previous OpenDaylight versions (e.g. 15.3.2). If so, you will need to change the scripts under the `bash` folder. To send flow entries, please change the URLs to this [link](https://docs.opendaylight.org/projects/openflowplugin/en/latest/users/flow-examples.html). For requesting nodes and topology, please change the URLs as `http://$IP_ADDR:8181/restconf/operational/opendaylight-inventory:nodes` and `http://$IP_ADDR:8181/restconf/operational/network-topology:network-topology/topology/flow:1`.
