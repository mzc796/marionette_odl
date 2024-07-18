import clear_table as clear_table
import sys

num_nodes = int(sys.argv[1])
#num_nodes = 5
for i in range(0,num_nodes):
    print(str(i+1))
    clear_table.clear_table("openflow:"+str(i+1))
