#!/usr/bin/python3.9
import matplotlib.pyplot as plt
import networkx as nx
import trans_topo as topo
import subprocess
import read_src_mac as r_mac
import topo_flow_util as tf_util
import os
import time

def extract_l_outport(links, src, dst):
    key = (src,dst)
    if key in links:
        value = links.get(key)
        src_tp = value.split('------')[0]
    else:
        key = (dst,src)
        value = links.get(key)
        src_tp = value.split('------')[1]
    port = src_tp.split(':')[1]
    return port
    
def extract_r_inport(links, src, dst):
    key = (src,dst)
    #print("ex inport:key:")
    #print(key)
    if key in links:
        value = links.get(key)
        dst_tp = value.split('------')[1]
    else:
        key = (dst,src)
        value = links.get(key)
        dst_tp = value.split('------')[0]

    inport = dst_tp.split(':')[1]
    #print(inport)
    return inport

def extract_entry_id(eid_list,index):
    eid = eid_list[index]
    eid_list[index] = eid + 1
    eid_str = str(eid + 50)
    return eid_str

def find_nx_hop(topo,src):
    links = topo.get("link_list_w_tp")
    #print(links)
    nx_hp = "temp"
    for i in links:
        l = i[0]
        r = i[1]
        if l == src:
            nx_hp = r
        elif r == src:
            nx_hp = l
        else:
            continue
    if nx_hp == "temp":
        print("fail to find next hop")
    return nx_hp

def poison_link(eid_list, src, dst, mal_ins_dict, vid):
    topo_info = topo.read_topo("original")
    edges = topo_info.get("link_list")
    links = topo_info.get("link_label")
    G = nx.Graph()
    G.add_edges_from(edges)
    print("src is "+src+", dst is "+dst)
    table_id = 0
    src_eth = r_mac.read_nc(src)
    src_node = src.rsplit(':',1)[0]
    dst_node = dst.rsplit(':',1)[0]
    src_tp = src.rsplit(':',1)[1]
    dst_tp = dst.rsplit(':',1)[1]
    sub_src = find_nx_hop(topo_info,src)
    key = src_node+',o:'+src_tp
    print("sub_src is:")
    print(sub_src)
    if sub_src == "temp":
    	return
    sub_src_node = sub_src.rsplit(':',1)[0]
    sub_dst = find_nx_hop(topo_info,dst)
    if sub_dst == "temp":
    	return
    sub_dst_node = sub_dst.rsplit(':',1)[0]
    print("sub_dst is:")
    print(sub_dst)
    skip_flag = 0
    if nx.shortest_path_length(G, source = sub_src_node, target = sub_dst_node) <= nx.shortest_path_length(G, source = sub_src_node, target = dst_node):
        p = nx.shortest_path(G, source = sub_src_node, target = sub_dst_node)
        p.append(dst_node)
        # do not need to go forward and back to ajust port number of the last hop
        skip_flag = 1
    else:
        p = nx.shortest_path(G, source=sub_src_node, target=dst_node)
    print("sub path is:")
    print(p)
    path_len=len(p)
    pois_list = []
    priority = "2"
    for j in range(0, path_len - 1):
        sw = p[j]
        sw_index = sw[9:]
        #entry_id = extract_entry_id(eid_list, int(sw_index)-1)
        entry_id = tf_util.get_avail_entry_id(sw)
        if j == 0 and path_len == 2 and skip_flag:
            outport = extract_l_outport(links,p[j],p[j+1])
            inport_mtch = extract_r_inport(links,src_node,sub_src_node)
            subprocess.Popen(["bash/lldp_poisoning.sh",sw,str(table_id),entry_id,src_eth,outport,priority])
        elif j == 0:
            if p[j+1] == src_node:
                print("it is going back to the src, the output should be in_port")
                outport = "INPORT"
            else:
                outport = extract_l_outport(links,p[j],p[j+1])
            inport_mtch = extract_r_inport(links, src_node, sub_src_node)
            subprocess.Popen(["bash/lldp_poisoning_push_vlan.sh",sw,str(table_id),entry_id,src_eth,outport,priority,vid])
        
        elif j == path_len - 2 and skip_flag:
            inport_mtch = extract_r_inport(links, p[j-1],p[j])
            outport = extract_l_outport(links,p[j],p[j+1])
            subprocess.Popen(["bash/pop_vlan.sh",sw,str(table_id),entry_id, outport, priority, vid])
        else:
            inport_mtch = extract_r_inport(links, p[j-1],p[j])
            outport = extract_l_outport(links,p[j],p[j+1])
            subprocess.Popen(["bash/match_vlan.sh",sw,str(table_id),entry_id, outport, priority, vid])
        # store info for malicious insertion
        sub_key = sw +',i:' + str(inport_mtch)
        mal_ins = (sub_key,'o:'+outport)
        pois_list.append(mal_ins)
    if not skip_flag:
        if path_len > 1: 
            outport = extract_r_inport(links,p[path_len-2],p[path_len-1])
        else:
            outport = extract_r_inport(links,src_node,p[path_len-1])
        if dst_tp != outport:
            sw = p[path_len-1]
            #entry_id = extract_entry_id(eid_list,int(sw[9:])-1)
            entry_id = tf_util.get_avail_entry_id(sw)
            if path_len > 1:
                subprocess.Popen(["bash/match_vlan.sh",sw,str(table_id),entry_id,dst_tp,priority, vid])
            else:
                subprocess.Popen(["bash/lldp_poisoning_m_inport_push_vlan.sh",sw,str(table_id),entry_id,src_eth,outport,dst_tp,priority,vid])
            # store info for malicious insertion
            sub_key = sw +'-' + str(outport)
            mal_ins = (sub_key,dst_tp)
            pois_list.append(mal_ins)
                
            nx_hop = find_nx_hop(topo_info,dst)
            sw = nx_hop.rsplit(':',1)[0]
            #entry_id = extract_entry_id(eid_list,int(sw[9:])-1)
            entry_id = tf_util.get_avail_entry_id(sw)
            outport = "INPORT"
            subprocess.Popen(["bash/pop_vlan.sh",sw,str(table_id),entry_id,outport, priority, vid]) 
            # store info for malicious insertion, key: sw + outport
            sub_key = sw +'-' + str(outport)
            mal_ins = (sub_key,outport)
            pois_list.append(mal_ins)
        else:
            print("This is not a poisoning link case but a real link case. Should not happen")
    mal_ins_dict[key] = pois_list     
    return mal_ins_dict
    

def poison_links(link_list, node_num):
    #initialize state
    vid_link_map = create_vid_link_map(link_list)
    mal_ins_dict = {}
    eid_list = []
    for i in range(node_num):
        eid_list.append(0)
    #subprocess.Popen(["bash/req_topo.sh","original"])
    #time.sleep(1)
    subprocess.Popen(["bash/req_nodes.sh"])
    time.sleep(1)
    for key in vid_link_map.keys():
        link = vid_link_map.get(key)
        s = link.rsplit("-")[0]
        t = link.rsplit("-")[1]
        s_name = "openflow:"+s
        t_name = "openflow:"+t
        mal_ins_dict = poison_link(eid_list,s_name,t_name, mal_ins_dict, key)
        time.sleep(1)

    print("malicious insertion dict is:")
    print(mal_ins_dict)
    pois_list = mal_ins_dict.get('openflow:4:2')
    time.sleep(5)
    subprocess.Popen(["bash/req_topo.sh","deceptive"])
    time.sleep(5)
    os.system('python3.9 draw_fattree_topo.py deceptive')
    return vid_link_map, mal_ins_dict

def create_vid_link_map(links):
    vid_link_map = {}
    for i in range(0,len(links)):
        vid = str(2*i+1)
        link = links[i]
        vid_link_map.update({vid:link})
    
        vid = str(2*i+2)
        s = links[i].rsplit("-")[0]
        t = links[i].rsplit("-")[1]
        rev_link = t+"-"+s
        vid_link_map.update({vid:rev_link})
    return vid_link_map
    


