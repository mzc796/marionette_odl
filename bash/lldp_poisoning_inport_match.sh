#!/bin/bash
echo "sending lldp inport match to $1, table $2, entry $3, dst $4, in_port $5, outport $6, priority $7"
curl -u admin:admin -X PUT "http://localhost:8181/rests/data/opendaylight-inventory:nodes/node=$1/flow-node-inventory:table=$2/flow=$3" -H "content-type: application/json" -d '{
     "flow-node-inventory:flow": [
         {
             "id": "'$3'",
             "priority": "'$7'",
             "table_id": 0,
             "hard-timeout": 0,
             "match": {
                 "ethernet-match": {
                     "ethernet-source": {
                         "address":"'$4'"
                     }
                 },
	 	 "in-port":"'$5'"
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
                                         "output-node-connector": "'$6'"
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
