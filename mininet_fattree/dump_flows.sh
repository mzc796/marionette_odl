#!/bin/bash
echo "dumping flow rules"
ovs-ofctl -O OpenFlow13 dump-flows $1
