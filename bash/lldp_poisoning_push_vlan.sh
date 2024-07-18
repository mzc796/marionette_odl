#!/bin/bash
echo "pushing vlan of lldp for $1, table $2, entry_id $3, dst $4, outport $5, priority$6, vlan_id $7"
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
                                     "push-vlan-action": {
                                         "ethernet-type": 33024
                                     }
                                 },
                                 {
                                     "order": 1,
                                     "set-field": {
                                         "vlan-match": {
                                         	"vlan-id":{
                                         		"vlan-id-present":true,
                                         		"vlan-id":"'$7'"
                                         	}
                                         }
                                     }
                                 },
                                 {
                                     "order": 2,
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
