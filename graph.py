# Auther: Marcin Cuber
# All rights reserved
__author__ = 'marcincuber'
import networkx as nx
import matplotlib.pyplot as plt
'''
    :Logic K, graph with no properties
'''
def create_graph_K(G,nodes,Sets):
    G.add_edges_from(nodes)


    #value assigned to each world
    custom_labels={}
    custom_node_sizes={}
    node_colours=['y']
    custom_node_colours = {}

    for i in range(0, len(Sets)):
        custom_labels[i+1] = Sets[i]
        G.node[i+1] = Sets[i]
        custom_node_sizes[i+1] = 5000
        node_colours.append('b')
    nx.draw(G, nx.circular_layout(G), node_list = nodes,node_color=node_colours, labels=custom_labels, node_size=1000, with_labels = True)

    plt.show()

'''
    :Reflexive graph
'''
def create_graph_T(G,nodes,Sets):
    G.add_edges_from(nodes)
    G.add_edge(1,1)

    #value assigned to each world
    custom_labels={}
    custom_node_sizes={}
    node_colours=['y']
    custom_node_colours = {}

    for i in range(0, len(Sets)):
        custom_labels[i+1] = Sets[i]
        G.node[i+1] = Sets[i]
        custom_node_sizes[i+1] = 5000
        node_colours.append('b')
    nx.draw(G,node_list = nodes,node_color=node_colours, labels=custom_labels, node_size=1000, with_labels = True)

    #plt.savefig("original_graph.png")
    plt.show()
    G_comp = nx.weakly_connected_component_subgraphs(G)

'''
    :Symmetric but Not reflexive graph
'''
def create_graph_symmetric(G,nodes,Sets):
    G.add_edges_from(nodes)

    #value assigned to each world
    custom_labels={}
    custom_node_sizes={}
    node_colours=['y']
    custom_node_colours = {}

    for i in range(0, len(Sets)):
        custom_labels[i+1] = Sets[i]
        G.node[i+1] = Sets[i]
        custom_node_sizes[i+1] = 5000
        node_colours.append('b')
    nx.draw(G,node_list = nodes,node_color=node_colours, labels=custom_labels, node_size=1000, with_labels = True)

    #plt.savefig("original_graph.png")
    plt.show()
    G_comp = nx.weakly_connected_component_subgraphs(G)

'''
    :Logic S5, equivalent relation
'''

def create_graph_S5(G,nodes,Sets):
    G.add_edges_from(nodes)


    #value assigned to each world
    custom_labels={}
    custom_node_sizes={}
    node_colours=['y']
    custom_node_colours = {}
    pos=nx.circular_layout(G)

    for i in range(0, len(Sets)):
        custom_labels[i+1] = Sets[i]
        G.node[i+1] = Sets[i]
        custom_node_sizes[i+1] = 5000
        node_colours.append('b')
    nx.draw(G, nx.circular_layout(G), node_list = nodes,node_color=node_colours, labels=custom_labels, node_size=1000, with_labels = True)

    #plt.savefig("original_graph.png")
    plt.show()

def addedge(edges,world,Worlds):
    #print "here we are adding to world: ",world
    lengthmain = len(Worlds)
    #if edges == []:
    edges.append((world,Worlds[lengthmain-1]))

def addedge2(nodes,worlds):
    #print "here we are adding to world: ",worlds
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

