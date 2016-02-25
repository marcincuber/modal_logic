__author__ = 'marcincuber'
import networkx as nx
import matplotlib.pyplot as plt
'''
    :Logic K, T, KB, B, K4, S4, S5- graph initialisation
'''
def create_graph_K(G,nodes,Sets):
    #add edges based on the list of nodes provided
    G.add_edges_from(nodes)

    #dictionary with labels = value assigned to each world
    custom_labels={}
    #dictionary with sizes for each node
    custom_node_sizes={}
    node_colours=['y']

    for i in range(0, len(Sets)):
        #To each label assign correspoding set with formulas
        custom_labels[i+1] = Sets[i]
        G.node[i+1] = Sets[i]
        custom_node_sizes[i+1] = 5000
        node_colours.append('b')

    #draw the graph on circular layout with colours, labels, sizes included.
    nx.draw(G, nx.circular_layout(G), node_list = nodes,node_color=node_colours, labels=custom_labels, node_size=1000, with_labels = True)

    #plot the graph and display the figure
    plt.show()


