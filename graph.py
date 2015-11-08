__author__ = 'marcincuber'
import networkx as nx
import matplotlib.pyplot as plt

def create_graph(G,nodes,Sets):
    #create an empty graph
    #G.add_node('1')
    #add edges depending on array nodes
    #for i in range(0, len(nodes)):
    #    G.add_edge('1',str(nodes[i]))
    G.add_edges_from(nodes)

    #value assigned to each world
    custom_labels={}
    custom_node_sizes={}
    node_colours=['y']
    #for i in range(0, len(Sets)):
    #    custom_labels[str(i+1)] = Sets[i]
    #    custom_node_sizes[str(i+1)] = 5000
    for i in range(0, len(Sets)):
        custom_labels[i+1] = Sets[i]
        custom_node_sizes[i+1] = 5000
        if i < len(Sets):
            node_colours.append('b')

    #draw the graph
    #nx.draw_networkx(G, pos=None, arrows=True, with_labels=True,labels=custom_labels,node_list = custom_node_sizes.keys(), node_size=custom_node_sizes.values())

    nx.draw(G,labels=custom_labels,node_list = nodes,node_color=node_colours, node_size=custom_node_sizes.values())
    #show with custom labels
    plt.show()
    plt.savefig("path.png")

def addedge(edges,world,Worlds):
    #print "here we are adding to world: ",world
    lengthmain = len(Worlds)
    #if edges == []:
    edges.append((world,Worlds[lengthmain-1]))
    #else:
    #    length=len(edges)
    #    newedge = edges[length-1][1] + 1
    #    edges.append((world,newedge))

def addedge2(nodes,worlds):
    print "here we are adding to world: ",worlds
    if nodes == []:
        nodes.append((worlds,2))
    else:
        length=len(nodes)
        newedge = nodes[length-1][1] + 1
        nodes.append((worlds,newedge))

def addworld(nodes):
    length=len(nodes)
    newworld = nodes[length-1] + 1
    nodes.append(newworld)
