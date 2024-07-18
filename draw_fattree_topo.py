import matplotlib.pyplot as plt
import networkx as nx
import trans_topo as topo
import subprocess
import sys
import time
import math

if len(sys.argv) > 1:
    topo_type = sys.argv[1]
else:
    topo_type = "original"
print(topo_type)
if topo_type != "original":
    process = subprocess.Popen(["bash/req_topo.sh",topo_type])
    process.wait()
topo_info = topo.read_topo(topo_type)
nodes = topo_info.get("node_list")
edges = topo_info.get("link_list")
#G = nx.DiGraph()
G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
#pos = nx.spring_layout(G)
plt.figure()
#nx.spring_layout(G, k = 0.15, iterations = 20)
fixed_positions = {'openflow:1':(18,5),'openflow:2':(15,8),'openflow:3':(12,9),'openflow:4':(13,7),'openflow:5':(14,4),'openflow:6':(11,10),'openflow:7':(10,9),'openflow:8':(10,7),'openflow:9':(12,5),'openflow:10':(13,3),'openflow:11':(10,11),'openflow:12':(2,8),'openflow:13':(10,6),'openflow:14':(7,3),'openflow:15':(12,4),'openflow:16':(6,6),'openflow:17':(8,5),'openflow:18':(8,11)}
fixed_positions = {'openflow:1':(20,30),'openflow:2':(50,30),'openflow:3':(80,30),'openflow:4':(110,30),'openflow:5':(10,20),'openflow:6':(25,20),'openflow:7':(40,20),'openflow:8':(55,20),'openflow:9':(75,20),'openflow:10':(90,20),'openflow:11':(105,20),'openflow:12':(120,20),'openflow:13':(10,10),'openflow:14':(25,10),'openflow:15':(40,10),'openflow:16':(55,10),'openflow:17':(75,10),'openflow:18':(90,10),'openflow:19':(105,10),'openflow:20':(120,10),'openflow:21':(-10,0),'openflow:22':(0,0),'openflow:23':(10,0),'openflow:24':(20,0),'openflow:25':(30,0),'openflow:26':(40,0),'openflow:27':(50,0),'openflow:28':(60,0),'openflow:29':(70,0),'openflow:30':(80,0),'openflow:31':(90,0),'openflow:32':(100,0),'openflow:33':(110,0),'openflow:34':(120,0),'openflow:35':(130,0),'openflow:36':(140,0)}

fixed_nodes = fixed_positions.keys()
pos = nx.spring_layout(G, pos=fixed_positions, fixed = fixed_nodes)
#pos = nx.spring_layout(G,k=5/math.sqrt(G.order()),pos=fixed_positions, fixed=fixed_nodes)
#nx.draw(G, pos = pos, edge_color='black', width=1, linewidths=1, node_size=500, node_color='pink', alpha=0.9, connectionstyle='arc3, rad = 0.1', labels={node: node for node in G.nodes()})

#nx.draw(G, pos = pos, with_labels = True, node_color = 'orange')
nx.draw(G, pos = pos, with_labels = False, node_color = 'orange')
    
    #nx.draw(G, pos = pos, with_labels = True, node_color = 'orange')

link_labels = topo_info.get("link_label")
#edge_labels=dict([(u,v)for u,v in G.edges(data=True)])
#print("label number:"+str(len(link_labels)))
nx.draw_networkx_edge_labels(
    G, pos,
#    edge_labels={('openflow:2', 'openflow:3'): 'AhahahB',('openflow:5','openflow:4'):'hehehe'},
#    edge_labels={(edges[0]): 'AhahahB'},
    edge_labels=link_labels,
    label_pos = 0.7,
    font_color='black',
    font_size = 6
)
plt.axis('off')
#plt.show()
plt.savefig("figure/topo_"+topo_type+".png")
