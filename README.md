# marionette_odl-0.20.1
We demonstrate Marionette attacking ODL Calcium on a fat tree topology. It starts with collecting network information and learning a deceptive topology, making more flows going to an eavesdropping node. Then Marionette composes and sends poisonous flow entries to make the deceptive topology discovered by the legitimated controller.

# VM Specification
System: ubuntu-22.04.4-desktop-amd64.iso

CPU: 2 cores

Memory: 32GB

Hard disk: 50GB

# Systerm Preparation

## Install Python3.9 and stable-baselines3
```
sudo apt-get update
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get install python3.9 vim wget net-tools
sudo apt install python3-pip python3.9-distutils
python3.9 -m pip install --upgrade Pillow
python3.9 -m pip install networkx matplotlib
python3.9 -m pip install 'stable-baselines3==1.7.0'
```
## Install Java
```
sudo apt-get install openjdk-17-jdk
```
### Configure JAVA_HOME and IP_ADDR to /etc/profile
```
sudo vim /etc/profile
```
Add the following to the end of /etc/profile
```
JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
PATH=$PATH:$HOME/bin:$JAVA_HOME/bin
export JAVA_HOME
export JRE_HOME
export PATH
```
### Make JAVE_HOME valid and Test JAVA Version
```
source /etc/profile/
java -version
```
## Install Latest OpenDaylight (Calcium, June 27, 2024)
### Download OpenDaylight Calcium
```
wget https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.20.1/karaf-0.20.1.zip
unzip karaf-0.20.1.zip
```
### Configure ODL-0.20.1 Environment
```
cd karaf-0.20.1\bin
vim setenv
```
Add the following to the setenv file
```
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
```
### Run OpenDaylight
```
sudo ./karaf
```
### Install OpenFlow Plugins
```
opendaylight-user@root>feature:install odl-openflowplugin-app-topology-lldp-discovery odl-openflowplugin-app-table-miss-enforcer odl-openflowplugin-flow-services odl-openflowplugin-flow-services-rest odl-openflowplugin-app-topology-manager odl-openflowplugin-app-lldp-speaker
```
### Check Listening Ports
```
sudo lsof -i -P -n | grep LISTEN
```
If ```tcp *:6653 (LISTEN)``` and ```tcp *:8181 (LISTEN)``` do not show, shut down OpenDaylight with ```Control+D``` and restart ```sudo ./karaf```

## Prepare Mininet
We build another VM to run Mininet, Memory:4GB, Hard disk:20GB

### Install mininet
```
sudo apt-get update
sudo apt-get install mininet
```
### Run Mininet with Customized Topology and Connect with Remote Controller with Ip Address $IP
``` 
cd Mininet_FatTree
sudo ./fattree_mn_run.sh $IP
```
### Check Flow Entries
```
sudo ./dump_flows.sh $sw_id
```
For Example,
```
sudo ./dump_flows.sh s1
```
## Marionette Attack
Open another terminal on OpenDaylight VM
Download marionette_odl-0.20.1.zip
Unzip it in the home folder.
```
cd marionette_odl-0.20.1
python3.9 main.py
```
In order to efficiently demonstrate Marionette, we give the Marionette an easy goal to run a Reinforcement Learning algorithm to compute an adequate deceptive topology.
We set the eavesdropping node as node 6 (openflow:7), the expected increased number of eavesdropping flows is 4, and the degree sequence must remain unchanged after altering the topology.
After the program is finished, we go to the 'figure' folder. There will be three figures.

- topo_original.png: The topology discovered by the ODL controller before being poisoned, which is the real topology.

- RL_topo.png: The Reinforcement Learning produced deceptive topology.

- topo_deceptive.png: The topology discovered by the ODL controller after being poisoned by Marionette, which is the deceptive topology.

The RL_topo.png should be the same as topo_deceptive.png, which proves the success of precise link manipulation.

NOTE: 

(1) Because the latest version (e.g. at least after the version of 15.3.0) of OpenDaylight removed the user interface project DLUX and we want to show the changes of the topology easily, we use RESTful API to GET topology in real-time and draw the topology with nodes having fixed positions by scripts.

(2) The node indices start from 0 in RL_topo.png but start from 1 in topo_deceptive.png. 
