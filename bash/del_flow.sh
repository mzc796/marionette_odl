#!/bin/bash
curl -u admin:admin -X DELETE "http://localhost:8181/rests/data/opendaylight-inventory:nodes/node=$1/flow-node-inventory:table=$2/flow=$3" -H "content-type: application/json"
