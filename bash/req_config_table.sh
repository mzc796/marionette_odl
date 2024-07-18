#!/bin/bash
curl -s -u admin:admin -X GET "http://localhost:8181/rests/data/opendaylight-inventory:nodes/node=$1/flow-node-inventory:table=0" -H "Content-Type: application/json" -o data/$1_config_table.json
