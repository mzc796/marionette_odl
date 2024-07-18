#!/bin/bash
curl -u admin:admin -X GET "http://localhost:8181/rests/data/opendaylight-inventory:nodes?content=nonconfig" -H "content-type: application/json" -o data/nodes.json
