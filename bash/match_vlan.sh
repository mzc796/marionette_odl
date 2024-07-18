#!/bin/bash
echo "matching vlan for $1, table $2, entry_id $3, outport $4, priority$5, vlan_id $6"
curl -u admin:admin -X PUT "http://localhost:8181/rests/data/opendaylight-inventory:nodes/node=$1/flow-node-inventory:table=$2/flow=$3" -H "content-type: application/json" -d '{
     "flow-node-inventory:flow": [
         {
             "id": "'$3'",
             "priority": '$5',
             "table_id": 0,
             "hard-timeout": 0,
             "match": {
             	"vlan-match": {
                    "vlan-id": {
                        "vlan-id-present":true,
                        "vlan-id": "'$6'"
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
                                         "output-node-connector": "'$4'"
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