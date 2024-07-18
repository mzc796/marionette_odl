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
sudo apt-get install python3.9 vim wget
sudo apt install python3-pip python3.9-distutils
python3.9 -m pip install gym networkx matplotlib

python3.9 -m pip install --upgrade pip
python3.9 -m pip install --upgrade Pillow
python3.9 -m pip install --upgrade pip==22.3.1

python3.9 -m pip install atari-py
python3.9 -m pip install 'stable-baselines3==1.7.0'
python3.9 -m pip install Cmake
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
    JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
    PATH=$PATH:$HOME/bin:$JAVA_HOME/bin
    export JAVA_HOME
    export JRE_HOME
    export PATH
```
### Make JAVE_HOME valid and Test JAVA Version
    source /etc/profile/
    java -version
    
## Install OpenDaylight-15.3.0
### Download OpenDaylight-15.3.0
```
    wget https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/opendaylight/15.3.0/opendaylight-15.3.0.zip
    unzip opendaylight-15.3.0.zip
```
### Configure ODL-15.3.0 Environment
```
cd opendaylight-15.3.0\bin
vim setenv
```
Add the following to the setenv file
```
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
```
