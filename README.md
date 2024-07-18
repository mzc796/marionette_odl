# marionette_odl-0.20.1
We demonstrate Marionette attacking ODL Calcium on a fat tree topology. It starts with collecting network information and learning a deceptive topology, making more flows going to an eavesdropping node. Then Marionette composes and sends poisonous flow entries to make the deceptive topology discovered by the legitimated controller.

# VM Specification
System: ubuntu-22.04.4-desktop-amd64.iso

CPU: 2 cores

Memory: 16GB

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
