# marionette_odl-0.20.1
We demonstrate Marionette attacking ODL Calcium on a fat tree topology. It starts with collecting network information and learning a deceptive topology, making more flows going to an eavesdropping node. Then Marionette composes and sends poisonous flow entries to make the deceptive topology discovered by the legitimated controller.

# VM Specification
Memory 32GB
# Systerm Preparation

## Install Python3.9
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.9
sudo apt install python3-pip
sudo apt install python3.9-distutils
python3.9 -m pip install gym networkx matplotlib

python3.9 -m pip install --upgrade pip
python3.9 -m pip install --upgrade Pillow
python3.9 -m pip install --upgrade pip==22.3.1

python3.9 -m pip install atari-py

python3.9 -m pip install 'stable-baselines3==1.7.0'
python3.9 -m pip install Cmake

## Install Java
  $ sudo apt-get install openjdk-17-jdk

### Configure JAVA_HOME and IP_ADDR to /etc/profile/
  $ sudo gedit /etc/profile
    JAVA_HOME=/usr/lib/jvm/java-1.17.0-openjdk-arm64
    PATH=$PATH:$HOME/bin:$JAVA_HOME/bin
    export JAVA_HOME
    export JRE_HOME
    export PATH
    IP_ADDR = "The Ipv4 address used to connect to Mininet"
    export IP_ADDR
### Make JAVE_HOME valid and Test JAVA Version
    source /etc/profile/
    java -version
