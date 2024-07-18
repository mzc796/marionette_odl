import read_config_table as read_table
import trans_topo as topo
import json
import subprocess
import time
import random

def extract_output(link_label, sw1, sw2):
    key = (sw1, sw2)
    if key in link_label:
        value = link_label.get(key)
        src_tp = value.rsplit('------')[0]
    else:
        key = (sw2, sw1)
        value = link_label.get(key)
        src_tp = value.rsplit('------')[1]
    port = src_tp.rsplit(':')[1]
    return port
    
def extract_used_entry_id(sw_id):
    used_id = []
    subprocess.Popen(["bash/req_config_table.sh",sw_id])
    time.sleep(1)
    f = open('data/'+sw_id+'_config_table.json')
    data = json.load(f)
    if 'flow-node-inventory:table' in data:
        tables = data['flow-node-inventory:table']
        num_tables = len(tables)
        flow_id_list = []
        for i in range(0, num_tables):
            flow_dict = {}
            table = tables[i]
            tbl_id = table['id']
            if 'flow' in table:
                flows = table['flow']
                num_flows = len(flows)
                for j in range(0, num_flows):
                    flow = flows[j]
                    flow_id = flow['id']
                    #print("flow_id:"+str(flow_id))
                    used_id.append(flow_id)
    return used_id

def get_avail_entry_id(sw_id):
    entry_id = "0"
    used_id = extract_used_entry_id(sw_id)
    #print("used_ids:"+str(used_id))
    size = len(used_id)
    if size == 0:
        print("there is not a used entry id on "+ sw_id)
        return "1"
    r_int = random.randint(1, 1000)
    for i in range(1, size+1):
        if str(i+r_int) not in used_id:
            entry_id = str(i+r_int)
            #print("find the avail entry_id:"+entry_id)
            break
    return entry_id
    
def extract_fid_prio_exist(sw_tbl_dict, dst_ip, sw_id, avail_en_ids, content, dst_sw, outport):
    entry_id = "0"
    priority = "0"
    exist = 0
#    dst_ip = sw_host_dict.get(dst_sw)
    num_sw = len(sw_tbl_dict)
    reused = 0
    if num_sw != 0:
        table = sw_tbl_dict.get(sw_id)
        if table is not None:
            num_flows = len(table)
            for i in table:
                if table[i].get("match_protocol") == content and table[i].get("dst_addr") == dst_ip:
                    if table[i].get("out_put") == outport:
                        entry_id = str(table[i].get("entry_id"))
                        priority = str(table[i].get("priority"))
                        exist = 1
                        
                    else: #going to overwrite the output port
                        print("going to overwrite the output port")
                        entry_id = str(table[i].get("entry_id"))
                        print(entry_id)
                        priority = str(table[i].get("priority"))
                        reused = 1
                    break
                else:
                    #print("did not find the flow for entry_id "+content+dst_ip+" on "+sw_id)
                    if len(avail_en_ids) == 0:
                    	print("available entry ids are exhausted")
                    	return
                    else:
                    	entry_id = avail_en_ids.pop(0)
                    	priority = "1"  
        else:
            print("no flows on "+sw_id)
            entry_id = avail_en_ids.pop(0)
            priority = "1"
    else:
        print("no sw info yet")
        priority = "1"
        entry_id = avail_en_ids.pop(0)
    return [entry_id,priority,exist, reused, avail_en_ids]

def getpool(A):
    pool = []
    print(A)
    for i in range(0,len(A)):
        c = 0
        for j in range(0,len(A[i])):
            if A[i][j] != 0:
                c += 1
        if c < 3:
            pool.append(i)
    print("pool:")
    print(pool)
    return pool
def get_sw_host_dict(A):
    pool = getpool(A)
    sw_host_dict = {}
    for i in range(0,len(pool)):
        host_name = "Host"+str(i+1)
        host_ip = "10.0.0."+str(i+1)+"/32"
        sw_id = "openflow:"+str(pool[i]+1)+":1"
        sw_host_dict.update({sw_id:host_ip})
    return sw_host_dict

def get_s_t_dict(sw_host_dict, s_t_pairs):
    s_t_dict = {}
    for i in range(0,len(s_t_pairs)):
        s_ip = "10.0.0."+str(s_t_pairs[i][0])+"/32"
        t_ip = "10.0.0."+str(s_t_pairs[i][1])+"/32"
        s_sw_port = [k for k, v in sw_host_dict.items() if v == s_ip][0]
        t_sw_port = [k for k, v in sw_host_dict.items() if v == t_ip][0]
        s_sw_id = s_sw_port.rsplit(":",1)[0]
        t_sw_id = t_sw_port.rsplit(":",1)[0]
        print("s_sw_id")
        print(s_sw_id)
        s_t_ip = s_ip +"-"+t_ip
        s_t_sw = s_sw_id + "-" + t_sw_id
        s_t_dict.update({s_t_ip:s_t_sw})
    return s_t_dict

def sort_flow(table_dict, flow_dict, flow_id):
    for key in table_dict:
        if key in flow_dict.keys():
            pair = (flow_id,table_dict.get(key))
            flow_dict[key].append(pair)
        else:
            value = [(flow_id,table_dict.get(key))]
            flow_dict.update({key:value})
    return flow_dict

def reverse(traceback):
    half = len(traceback)//2
    for i in range(0, half):
        temp = traceback[i]
        traceback[i] = traceback[len(traceback)-1 - i]
        traceback[len(traceback)-1 - i] = temp
    return traceback
    
def create_mal_ins_db(mal_ins_dict,vid_link_map):
    mal_ins_db = {}
    for key in vid_link_map.keys():
        value = vid_link_map.get(key)
        l = value.rsplit("-",1)[0]
        l_node = l.rsplit(":",1)[0]
        l_tp = l.rsplit(":",1)[1]
        link_l = "openflow:"+l_node+",o:"+l_tp
        r = value.rsplit("-",1)[1]
        r_node = r.rsplit(":",1)[0]
        r_tp = r.rsplit(":",1)[1]
        link_r = "openflow:"+r_node+",i:"+r_tp
        print("link_l:")
        print(link_l)
        route = mal_ins_dict.get(link_l)
        if route:
            nx_hop = route[0]
            sw_in = nx_hop[0]
            sw_id = sw_in.rsplit(",",1)[0]
            inport = sw_in.rsplit(",",1)[1]
            if len(route) == 1:
                output = nx_hop[1]
                mal_content = sw_id+","+output
            elif len(route) == 2 and r_node == sw_id:
                output = nx_hop[1]
                mal_content = sw_id+","+output+",vid:"+key+","+inport
            else:
                output = nx_hop[1]
                mal_content = sw_id+","+output+",vid:"+key
                
            mal_ins_db.update({link_l:mal_content})
        else:
            print("fail to find "+link_l+" in mal_ins_dict")
    return mal_ins_db
	    
    '''
def back_trace(A, sw_id, trace, sw_group, sw_host_dict):
    id = int(sw_id.rsplit(':',1)[1]) - 1
    for i in range(0,len(A[id])):
        pre = 'openflow:'+ str(i+1)
        if A[id][i] != 0 and pre in sw_group:
            pair = trace[len(trace)-1]
            inport = str(A[id][i])
            last_updated = (pair[0]+'-'+inport,pair[1])
            trace[len(trace)-1] = last_updated
            pre_out = A[i][id]
            pre_pair = (pre,str(pre_out))
            
            if pre+':'+str(1) in sw_host_dict.keys():
                pre_pair = (pre_pair[0]+'-1',pre_pair[1])
            trace.append(pre_pair)
            print("trace:")
            print(trace)
            #sw_group.remove(pre)
            trace = back_trace(A, pre, trace, sw_group, sw_host_dict)
            break
    print("sw_group size:"+str(len(sw_group)))
    print(sw_group)
    return trace
    #else:
        #print("Error: trace is broken")
        #return sw_group'
        
        '''
        
def mark(path_dict):
    for key in path_dict:
        path_list = path_dict.get(key)
        for i in range(0,len(path_list)):
            m_hop = 'm*'+path_list[i][0]
            path_list[i] = (m_hop,path_list[i][1])
    return path_dict 

def unmark(path_dict, path_key, sw_id, entry_id):
    path_list = path_dict.get(path_key)
    #print("path_list in unmark")
    if len(path_list) == 0:
        return {}
    for i in range(0,len(path_list)):
        #print(path_list[i][0],path_list[i][1])
        if path_list[i][0] == 'm*'+ sw_id and path_list[i][1] == entry_id:
            print("find the entry and going to unmark it")
            um_hop = path_list[i][0].rsplit('*',1)[1]
            print(um_hop)
            path_list[i] = (um_hop,path_list[i][1])
            path_dict.update({path_key:path_list})
    return path_dict
    
def candid_exist(sw_id, sw_group):
    exist = False
    i_return = -1
    print('sw_id in candid_exist:'+sw_id)
    print(sw_group)
    for i in range(0, len(sw_group)):
        if sw_group[i][0] == sw_id:
            exist = True
            i_return = i
            print(i_return)
    return i_return, exist
    
def back_trace(A, trace, sw_group, sw_host_dict, done):
    post = trace[len(trace)-1]
    sw_id = post[0]
    print('sw_id:'+sw_id)
    if done:
        return trace
    i = len(sw_group)
    post_sw_id = int(sw_id.split(':',1)[1]) - 1
    for i in range(0, len(A)):
        candid_sw_id = 'openflow:'+ str(i+1)
        index, exist = candid_exist(candid_sw_id, sw_group)
        if A[i][post_sw_id] != 0 and exist:
            print('candid find')
            print(sw_group[index][1])
            print(A[i][post_sw_id])
            print(index)
            print(sw_group)
            print(sw_group[index])
            if sw_group[index][1] == str(A[i][post_sw_id]):
                pre_sw = 'openflow:'+str(i+1)
                print('openflow:'+str(i+1)+' is a pre')
                post_in = str(A[post_sw_id][i])
                post_updated = (sw_id+'-'+post_in,post[1])
                trace[len(trace)-1] = post_updated
                if pre_sw+':'+str(1) in sw_host_dict.keys():
                    pre_updated = (pre_sw +'-1', sw_group[index][1])
                    done = True
                else:
                    pre_updated = (pre_sw, sw_group[index][1])
                trace.append(pre_updated)
                print(trace)
                trace = back_trace(A, trace, sw_group, sw_host_dict, done)
            else:
                print('openflow:'+str(i+1)+' is a neighbour but not involved')
    return trace
        
#flow_dict:
#{'icmp,10.0.0.9/32': [('openflow:4', '3'), ('openflow:8', '4'), ('openflow:13', '3'), ('openflow:16', '1')], 'arp,10.0.0.9/32': [('openflow:4', '3'), ('openflow:8', '4'), ('openflow:13', '3'), ('openflow:16', '1')], 'icmp,10.0.0.2/32': [('openflow:4', '1'), ('openflow:8', '2'), ('openflow:13', '1'), ('openflow:16', '3')], 'arp,10.0.0.2/32': [('openflow:4', '1'), ('openflow:8', '2'), ('openflow:13', '1'), ('openflow:16', '3')]}

#sw_host_dict
#{'openflow:2:1': '10.0.0.1/32', 'openflow:4:1': '10.0.0.2/32', 'openflow:6:1': '10.0.0.3/32', 'openflow:7:1': '10.0.0.4/32', 'openflow:10:1': '10.0.0.5/32', 'openflow:11:1': '10.0.0.6/32', 'openflow:14:1': '10.0.0.7/32', 'openflow:15:1': '10.0.0.8/32', 'openflow:16:1': '10.0.0.9/32', 'openflow:17:1': '10.0.0.10/32', 'openflow:18:1': '10.0.0.11/32'}
#sw_group in sort path (sw_id, outport)
#[('openflow:4', '3'), ('openflow:8', '4'), ('openflow:13', '3'), ('openflow:16', '1')]

#{'openflow:1,o:2': 'openflow:4,o:3,vid:1i:2', 'openflow:13,o:4': 'openflow:17,o:INPORT,vid:2i:2', 'openflow:4,o:2': 'openflow:1,o:INPORT,vid:3i:2', 'openflow:13,o:1': 'openflow:8,o:2,vid:4i:4', 'openflow:8,o:4': 'openflow:13,o:4,vid:5i:1', 'openflow:17,o:2': 'openflow:13,o:1,vid:6i:4'}

def sort_path(flow_dict, A):
    print(A)
    sw_host_dict = get_sw_host_dict(A)
    print("sw_host_dict")
    print(sw_host_dict)
    path_dict = {}
    trace_dict = {}
    done = False
    for key in flow_dict:
        if '10.0.0.' in key:
            dst_ip = key.split(',',1)[1]
            dst_sw_p = [k for k, v in sw_host_dict.items() if v == dst_ip][0]
            dst_sw = dst_sw_p.rsplit(':',1)[0]
            print("dst:")
            print(dst_ip)
            print(dst_sw)
            sw_group = flow_dict.get(key)
            print('sw_group in sort path')
            print(sw_group)
            last = (dst_sw,str(1))
            trace = [last]
#            sw_group.remove(last)         
            traceback = back_trace(A, trace, sw_group, sw_host_dict, done)
            print('trace in sort-path:')
            print(traceback)
            #reverse traceback
            trace = reverse(traceback)
            trace_dict.update({key:trace})
    return trace_dict



