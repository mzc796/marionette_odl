import json
import subprocess
import time

def read_flow_id(sw_id):
    subprocess.Popen(["bash/req_config_table.sh", sw_id])
    time.sleep(1)
    f = open('data/'+sw_id+'_config_table.json')
    data = json.load(f)
    flow_id_list = []
    if 'flow-node-inventory:table' in data:
        tables = data['flow-node-inventory:table']
        num_tables = len(tables)
        for i in range(0, num_tables):
            table = tables[i]
            if 'flow' in table:
                flows = table['flow']
                num_flows = len(flows)
                for j in range(0, num_flows):
                    flow = flows[j]
                    if '#U' not in flow['id']:
                        flow_id = flow['id']
                        flow_id_list.append(flow_id)
                    #print(flow_id)
            else:
                continue
    return flow_id_list

def read_priority(sw_id, entr_id):
    subprocess.Popen(["bash/req_config_table.sh", sw_id])
    time.sleep(1)
    f = open('data/'+sw_id+'_config_table.json')
    data = json.load(f)
    tables = data['flow-node-inventory:table']
    num_tables = len(tables)
    flow_id_list = []
    priority = 0
    for i in range(0, num_tables):
        table = tables[i]
        if 'flow' in table:
            flows = table['flow']
            num_flows = len(flows)
            for j in range(0, num_flows):
                flow = flows[j]
                if flow['id'] == entr_id:
                    priority = flow['priority']
                    print(priority)
        else:
            continue
    return priority

def read_mtch_act(sw_id):
    subprocess.Popen(["bash/req_config_table.sh", sw_id])
    time.sleep(1)
    f = open('data/'+sw_id+'_config_table.json')
    data = json.load(f)
    tables = data['flow-node-inventory:table']
    num_tables = len(tables)
    mtch_act_list = {}
    for i in range(0, num_tables):
        table = tables[i]
        if 'flow' in table:
            flows = table['flow']
            num_flows = len(flows)
            for j in range(0, num_flows):
                flow = flows[j]
                match = flow['match']
                match_json = json.dumps(match)
                '''
                if 'ipv4-destination' in match and flow['cookie'] != 2:
                    dst_ip = match['ipv4-destination']
                    pro_id = match['ip-match']['ip-protocol']
                    if pro_id == 1:
                        protocol = 'icmp'
                    elif pro_id == 6:
                        protocol = 'tcp'
                    elif pro_id == 17:
                        protocol = 'upd'
                    else:
                        protocol = str(pro_id)
                    mtch = protocol +','+ dst_ip
                    print(mtch)
                elif 'arp-target-transport-address' in match:
                    dst_ip = match['arp-target-transport-address']
                    mtch = "arp,"+dst_ip
                elif 'ethernet-match' in match:
                    if match['ethernet-match']['ethernet-type'] == str(35020):
                        src_addr = match['ethernet-match']['ethernet-source']
                        mtch = 'lldp,'+ src_addr
                    else:
                    
                        mtch = 'ether-match,'+ str(match['ethernet-match']['ethernet-type'])
                else:
                    mtch = 'undefined_match'
                '''
                actions = flow['instructions']['instruction'][0]['apply-actions']['action']
                for i in range(0,len(actions)):
                    action = actions[i]
                    if 'output-action' in action:
                        outport = action['output-action']['output-node-connector']
                        act = sw_id+',o:'+outport
                        mtch_act_list.update({match_json:act})
                    #else:
                        #print("no output-action found for this flow entry with match:" + match_json + " but the action is " + str(action))
        else:
            continue
    return mtch_act_list

def read_legitimate_mtch_act(sw_id):
    subprocess.Popen(["bash/req_config_table.sh", sw_id])
    time.sleep(1)
    f = open('data/'+sw_id+'_config_table.json')
    data = json.load(f)
    tables = data['flow-node-inventory:table']
    num_tables = len(tables)
    mtch_act_list = {}
    for i in range(0, num_tables):
        table = tables[i]
        if 'flow' in table:
            flows = table['flow']
            num_flows = len(flows)
            for j in range(0, num_flows):
                flow = flows[j]
                cookie = flow['cookie']
                #if cookie == 999:
                    #print("found a pois-flow entry")
                #elif cookie == 1000:
                    #print("found a mal-flow entry")
                if cookie != 999 and cookie != 1000:
                    match = flow['match']
                    match_json = json.dumps(match)
                    actions = flow['instructions']['instruction'][0]['apply-actions']['action']
                    for i in range(0,len(actions)):
                        action = actions[i]
                        if 'output-action' in action:
                            outport = action['output-action']['output-node-connector']
                            act = sw_id+',o:'+outport
                            mtch_act_list.update({match_json:act})
                        #else:
                            #print("no output-action found for this flow entry with match:" + match_json + " but the action is " + str(action))
        else:
            continue
    return mtch_act_list
    
    
#print(read_mtch_act("openflow:3"))

