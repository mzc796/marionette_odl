#!/bin/bash
echo "connecting to the remote controller with IP $1"
sudo mn --custom fattree_topo.py --topo mytopo --controller remote,ip=$1,port=6653 --switch ovsk,protocols=OpenFlow13 --mac
