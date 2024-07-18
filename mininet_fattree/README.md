# Mininet_FatTree
The scripts of this repository builds a FatTree topology for the Marionette project

## Install mininet
```
sudo apt-get update
sudo apt-get install mininet
```
## Run Mininet with Customized Topology
``` 
cd Mininet_FatTree
sudo ./fattree_mn_run.sh
```
## Check Flow Entries
```
sudo ./dump_flows.sh $sw_id
```
For Example,
```
sudo ./dump_flows.sh s1
```
