import json
import sys
import numpy as np

def read_topo(topo_type):
    f = open('data/topology_'+topo_type+'.json')
    data = json.load(f)
    topo_info = {}
    network_topo = data['network-topology:network-topology']
    topology = network_topo['topology'][0]
    nodes = topology['node']
    num_nodes = len(nodes)
    adj_matrix = np.zeros((num_nodes,num_nodes),dtype = int)
    node_list = []
#    mac_addr = '00:00:00:00:00:00'
    print("number of nodes is:",num_nodes)
    for i in range(0, num_nodes):
        node = nodes[i]
        node_id = node['node-id']
        node_list.append(node_id)
#        print(node_id)
#    print(node_list)
    topo_info.update({"node_list":node_list})
    links = topology['link']
    num_links = len(links)
    link_list = []
    link_set = set()
    link_str_list = []
    link_tp_list = []
    link_tp_dict = {}
    for j in range(0, num_links):
            link = links[j]
            src_node = link['source']['source-node']
            dst_node = link['destination']['dest-node']
            src_tp = link['source']['source-tp']
            dst_tp = link['destination']['dest-tp']
            src_index = int(src_node.rsplit(":",1)[1])-1
            dst_index = int(dst_node.rsplit(":",1)[1])-1
            stp_index = int(src_tp.rsplit(":",1)[1])
            dtp_index = int(dst_tp.rsplit(":",1)[1])
            adj_matrix[src_index][dst_index] = stp_index
            adj_matrix[dst_index][src_index] = dtp_index
            link_item = [src_node,dst_node]
            link_tp_item = [src_tp,dst_tp]
            link_list.append(link_item)
            key = (src_node,dst_node)
            #str_value = src_tp +"--"+ dst_tp
            str_value = (src_node,dst_node)
           # print("set_v")
           # print(set_value)
            value = src_tp[9:]+"------"+dst_tp[9:]
            link_tp_dict.update({key:value})
            link_tp_list.append(link_tp_item)
            link_str_list.append(str_value)
            link_set.add(str_value)
#    print(link_list)
#    print(len(link_list))
#    print(len(link_tp_dict))
#    print(link_tp_list)
#    print(adj_matrix)
    topo_info.update({"link_list":link_list})
    topo_info.update({"link_list_w_tp":link_tp_list})
    topo_info.update({"link_label":link_tp_dict})
    topo_info.update({"link_str_list":link_str_list})
    topo_info.update({"link_set":link_set})
    topo_info.update({"adj_matrix":adj_matrix})
#    temp = topo_info.get("node_list")
#    print("****")
#    print(temp)
#            print(node_con['id'])
#            print(argv)
#            if node_con['id'] == argv:
#                mac_addr = node_con['flow-node-inventory:hardware-address']
#                print(mac_addr)
    return topo_info

#ans = read_topo("original")
#print(ans)


