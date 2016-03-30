__author__ = 'marcincuber'
import networkx as nx
import matplotlib.pyplot as plt
import syntax
'''
    :Logic K, T, KB, B, K4, S4, S5- graph initialisation
'''
def create_graph_K(G,Sets):
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
    nx.draw(G, nx.circular_layout(G),node_color=node_colours, labels=custom_labels, node_size=1000, with_labels = True)

    #plot the graph and display the figure
    plt.show()

def final_graphs(Graphs,psi):
    if Graphs == []:
        print "There are no models for the input formula: ", (syntax.formula_to_string(psi))
        print "So the the negation of it : ", "~(",(syntax.formula_to_string(psi)), ") is valid."

    else:
        for i in range(0,len(Graphs)):
            graph = Graphs[i]

            custom_labels={}
            node_colours=['y']
            for node in graph.nodes():
                custom_labels[node] = graph.node[node]
                node_colours.append('c')

            nx.draw(Graphs[i], nx.circular_layout(Graphs[i]),  node_size=1500, with_labels=True, labels = custom_labels, node_color=node_colours)
            #show with custom labels
            fig_name = "graph" + str(i) + ".png"

            plt.savefig(fig_name)
            plt.show()

        print "Satisfiable models have been displayed."
        if len(Graphs) == 1:
            print "You have ",len(Graphs), " valid model."
        else:
            print "You have ",len(Graphs), " valid models."
        print "Your provided formula is: ", (syntax.formula_to_string(psi))
        print "Pictures of the graphs have been saves as: graph0.png, graph1.png etc."