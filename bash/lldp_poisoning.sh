#!/bin/bash
echo "sending lldp to $1, table $2, entry $3, ether_src $4, outport $5, priority $6"
curl -u admin:admin -X PUT "http://localhost:8181/rests/data/opendaylight-inventory:nodes/node=$1/flow-node-inventory:table=$2/flow=$3" -H "content-type: application/json" -d '{
     "flow-node-inventory:flow": [
         {
             "id": "'$3'",
             "priority": "'$6'",
             "table_id": 0,
             "hard-timeout": 0,
             "match": {
                 "ethernet-match": {
                     "ethernet-source": {
                         "address":"'$4'"
                     }
                 }
             },
             "cookie": 999,
             "flow-name": "flow1",
             "instructions": {
                 "instruction": [
                     {
                         "order": 0,
                         "apply-actions": {
                             "action": [
                                 {
                                     "order": 0,
                                     "output-action": {
                                         "output-node-connector": "'$5'"
                                     }
                                 }
                             ]
                         }
                     }
                 ]
             },
             "idle-timeout": 0
         }
      ]
 }'
