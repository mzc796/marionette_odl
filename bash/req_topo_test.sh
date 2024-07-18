#!/bin/bash
echo "request topo $1"
curl -s -u admin:admin -X GET "http://$IP_ADDR:8181/restconf/operational/network-topology:network-topology/topology/flow:1" -H "content-type: application/json"
