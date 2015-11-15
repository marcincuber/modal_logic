__author__ = 'marcincuber'
import networkx as nx
import matplotlib.pyplot as plt

def create_graph(G,nodes,Sets):
    G.add_edges_from(nodes)

    #value assigned to each world
    custom_labels={}
    custom_node_sizes={}
    node_colours=['y']

    for i in range(0, len(Sets)):
        custom_labels[i+1] = Sets[i]
        custom_node_sizes[i+1] = 5000
        if i < len(Sets):
            node_colours.append('b')

    nx.draw(G,labels=custom_labels,node_list = nodes,node_color=node_colours, node_size=custom_node_sizes.values())
    #show with custom labels
    plt.show()
    #plt.savefig("path.png")
def create_graph2(G,nodes,Sets):
    G.add_edges_from(nodes)

    #value assigned to each world
    custom_labels={}
    custom_node_sizes={}
    node_colours=['y']
    custom_node_colours = {}

    for i in range(0, len(Sets)):
        custom_labels[i+1] = Sets[i]
        custom_node_sizes[i+1] = 5000
        node_colours.append('b')
    nx.draw(G,node_list = nodes,node_color=node_colours, labels=custom_labels, node_size=1000, with_labels = True)
    plt.savefig("original_graph.png")
    plt.show()
    G_comp = nx.weakly_connected_component_subgraphs(G)

    i = 1;
    custom_number = 1;
    for comp in G_comp:
        print len(comp)
        print comp.edges()
        print comp.nodes()
        dictfilt = lambda x, y: dict([(i,x[i]) for i in x if i in set(y) ])
        #wanted_keys = (range(custom_number,custom_number + len(comp)))
        newdict = dictfilt(custom_labels, comp.nodes())

        node_colours2 = node_colours[0:len(comp)+1]
        node_colours3 = ['b','y','b','b']
        #print node_colours_custom
        if i == 2:
           #node_colours_custom = node_colours[0:len(comp)]
           nx.draw(comp, node_color=node_colours3,  node_size=1000, with_labels=True, labels = newdict)

        else:
            nx.draw(comp, node_color=node_colours2,  node_size=1000, with_labels=True, labels = newdict)
        #show with custom labels
        fig_name = "graph" + str(i) + ".png"
        plt.savefig(fig_name)
        plt.show()
        custom_number += len(comp)
        i += 1

def addedge(edges,world,Worlds):
    #print "here we are adding to world: ",world
    lengthmain = len(Worlds)
    #if edges == []:
    edges.append((world,Worlds[lengthmain-1]))

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
