import subprocess
import read_config_table as read_table
import sys

def clear_table(argv):
    print(argv)
    flow_id_list = read_table.read_flow_id(argv)
    num_flows = len(flow_id_list)
#    print(num_flows)
    for i in range(0, num_flows):
        flow_id = flow_id_list[i]
        print(flow_id)
        subprocess.Popen(["bash/del_flow.sh",argv,str(0),flow_id])

#if len(sys.argv) > 1:
 #   clear_table(sys.argv[1])
#clear_table("openflow:18")

