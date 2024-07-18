#!/bin/bash
echo "request topo $1"
echo $IP_ADDR
curl -s -u admin:admin -X GET "http://localhost:8181/rests/data/network-topology:network-topology?content=nonconfig" -H "content-type: application/json" -o data/topology_$1.json
