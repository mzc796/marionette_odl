import json
import sys

def read_nc(argv):
    f = open('data/nodes.json')
    data = json.load(f)
    nodes = data['opendaylight-inventory:nodes']['node']
    num_nodes = len(nodes)
    mac_addr = '00:00:00:00:00:00'
#    print("number of nodes is:",num_nodes)
    for i in range(0, num_nodes):
        node = nodes[i]
        node_cons = node['node-connector']
        num_node_cons = len(node_cons)
        for j in range(0, num_node_cons):
            node_con = node_cons[j]
#            print(node_con['id'])
#            print(argv)
            if node_con['id'] == argv:
                mac_addr = node_con['flow-node-inventory:hardware-address']
#                print(mac_addr)
    return mac_addr

#ans = read_nc(sys.argv[1])
#print(ans)


