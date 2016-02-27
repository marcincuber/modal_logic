__author__ = 'marcincuber'
# -*- coding: utf-8 -*-
"""
    :Modal Logic S4- transitive and reflexive frames
"""
import syntax
import sols
import graph
import networkx as nx
import matplotlib.pyplot as plt
import copy
from collections import OrderedDict

#import symbols
BML = syntax.Language(*syntax.default_ascii)

'''
    :Arrays to store the number of worlds and sets that correspond to each world
'''
Graphs = [] #initilise empty list of graphs
Worlds = [1] #list of worlds with root node
Edges = [] #initilise list storing edges needed to create the graph
Sets = [] #initilise list to store formulas which will be available in each world

graph_formulas = [] #list of dictionaries-used formulas in node for graph
formulas = {} #single dictionary
formulas[1] = [] #first list for node 1
graph_formulas.append(formulas)#add it to list of dictionaries

'''
    :Input String:
'''
str_psi = "(~#(~@(~p ^ @#t) V ~s) ^ (#@#p > @q)) "
print "formula input: ", (str_psi)

'''
    :Parsed string into tuple and list
'''
psi = syntax.parse_formula(BML, str_psi)
Sets.append(sols.recursivealpha(psi))

'''
    :creating graph
    :deleting non unique elements
    :passing data to graph function
'''
G = nx.MultiDiGraph()
uniq_Sets = [list(OrderedDict.fromkeys(l)) for l in Sets]

graph.create_graph_K(G,Edges,uniq_Sets)
Graphs.append(G)

'''
    :functions to remove duplicates from the list
'''
def remove_duplicates(lista):
    return list(set(lista))

def remove_dups_graph(graph):
    for node in graph.nodes():
        value_list = graph.node[node]
        unique_list = remove_duplicates(value_list)
        graph.node[node] = unique_list
'''
    :resolving ALPHAS given a GRAPH
'''
def alpha_node(graph):
    for node in graph.nodes():
        set = []
        value_list = graph.node[node]
        for i in range(0,len(value_list)):
            if isinstance(value_list[i], tuple):
                alpha = sols.recursivealpha(value_list[i])
                if isinstance(alpha[0], tuple):
                    if alpha[0] not in set:
                        set.append(alpha[0])
                        if len(alpha) > 1:
                            if alpha[1] not in set:
                                set.append(alpha[1])
                else:
                    for prop in alpha:
                        if prop not in set:
                            set.append(prop)
            elif isinstance(value_list[i], str):
                if value_list[i] not in set:
                    set.append(value_list[i])
        graph.node[node] = remove_duplicates(set)
'''
    :resolving ALPHAS given a NODE in graph
'''
def alpha_node_solve(graph,node):
    set = [] # array to store expanded alphas
    value_list = graph.node[node]

    for i in range(0,len(value_list)):
        if isinstance(value_list[i], tuple):
            alpha = sols.recursivealpha(value_list[i])
            if isinstance(alpha[0], tuple):
                if alpha[0] not in set:
                    set.append(alpha[0])
                    if len(alpha) > 1:
                        if alpha[1] not in set:
                            set.append(alpha[1])
            else:
                for prop in alpha:
                    if prop not in set:
                        set.append(prop)

        elif isinstance(value_list[i], str):
            if value_list[i] not in set:
                set.append(value_list[i])
    graph.node[node] = set
'''
    :resolving BETAS given a NODE in graph
'''
def beta_node_solve(graph, node, formulas_in):
    value_list = graph.node[node]
    for i in range(0,len(value_list)):
        value = value_list[i]
        if value not in formulas_in[node]:

            if value[0] =='or':
                part1 = value[1]
                part2 = value[2]
                comp2 = graph.copy()
                graph.node[node].remove(value)
                comp2.node[node].remove(value)
                graph.node[node].append(part1)
                comp2.node[node].append(part2)
                Graphs.append(comp2)

                formulas_in[node].append(value)
                copy_formulas_in = copy.deepcopy(formulas_in)
                graph_formulas.append(copy_formulas_in)

                for graph in Graphs:
                    alpha_node(graph)

            elif value_list[i] == 'or':
                part1 = value_list[i+1]
                part2 = value_list[i+2]
                comp2 = graph.copy()
                graph.node[node] = []
                comp2.node[node] = []
                graph.node[node].append(part1)
                comp2.node[node].append(part2)
                Graphs.append(comp2)

                formulas_in[node].append(value)
                copy_formulas_in = copy.deepcopy(formulas_in)
                graph_formulas.append(copy_formulas_in)

                for graph in Graphs:
                    alpha_node(graph)

            elif value[0] == 'not' and value[1][0] == 'and':
                part1 = value[1][1]
                part2 = value[1][2]

                left_part = ('not',part1)
                right_part = ('not',part2)
                comp2 = graph.copy()
                graph.node[node].remove(value)
                comp2.node[node].remove(value)
                graph.node[node].append(left_part)
                comp2.node[node].append(right_part)
                Graphs.append(comp2)

                formulas_in[node].append(value)
                formulas_in[node].append(part1)

                copy_formulas_in = copy.deepcopy(formulas_in)
                copy_formulas_in[node].append(part2)
                graph_formulas.append(copy_formulas_in)

                for graph in Graphs:
                    alpha_node(graph)

            elif value[0] == 'imply':
                part1 = value[1]
                part2 = value[2]
                if part1[0] == 'not':
                    left_part = part1[1]
                else:
                    left_part = ('not',part1)
                comp2 = graph.copy()
                graph.node[node].remove(value)
                comp2.node[node].remove(value)
                graph.node[node].append(left_part)
                comp2.node[node].append(part2)
                Graphs.append(comp2)

                formulas_in[node].append(value)
                copy_formulas_in = copy.deepcopy(formulas_in)
                graph_formulas.append(copy_formulas_in)

                for graph in Graphs:
                    alpha_node(graph)

            elif value_list[i] == 'imply':
                part1 = value_list[i+1]
                part2 = value_list[i+2]
                left_part = ('not',part1)
                comp2 = graph.copy()
                graph.node[node] = []
                comp2.node[node] = []
                graph.node[node].append(left_part)
                comp2.node[node].append(part2)
                Graphs.append(comp2)

                formulas_in.append(value)
                copy_formulas_in = copy.deepcopy(formulas_in)
                graph_formulas.append(copy_formulas_in)

                for graph in Graphs:
                    alpha_node(graph)

'''
    :resolving DELTAS given a NODE in graph
'''
def delta_node_solve(graph, node, formulas_in):
    delta_list = graph.node[node]

    for i in range(len(delta_list)-1,-1,-1):
        part1 = delta_list[i][0]
        if part1 == 'diamond':
            sub = delta_list[i]
            if sub not in formulas_in[node]:
                formulas_in[node].append(sub)
                part2 = delta_list[i][1]
                new_node= graph.number_of_nodes()+1
                graph.add_edge(node,(new_node)) #adding new world and relation Rxx'

                graph.node[node] = delta_list

                graph.node[new_node] = [part2]
                formulas_in[new_node] = []
                alpha_node_solve(graph, node)
                beta_node_solve(graph, node, formulas_in)
                transitive_gamma_node(graph, new_node, formulas_in)
                alpha_node_solve(graph, node)
                beta_node_solve(graph, node, formulas_in)

                previous = graph.predecessors(new_node)
                for num in previous:
                    set = graph.node[num];
                    for j in range(0,len(set)):
                        if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                            formula = ('not',set[j][1][1])
                            if formula not in graph.node[new_node]:
                                graph.node[new_node].append(formula)
                                alpha_node_solve(graph, new_node)
                                beta_node_solve(graph, new_node, formulas_in)
                                reflexive_gamma_node(graph,node,formulas_in)
                        elif set[j][0] == 'box':
                            if set[j][1] not in graph.node[new_node]:
                                graph.node[new_node].append(set[j][1])
                                alpha_node_solve(graph, new_node)
                                beta_node_solve(graph, new_node, formulas_in)
                                reflexive_gamma_node(graph,node,formulas_in)

        elif part1 == 'not' and delta_list[i][1][0] == 'box':
            sub = delta_list[i]
            if sub not in formulas_in[node]:
                formulas_in[node].append(sub)
                part2 = ('not', delta_list[i][1][1])
                new_node= graph.number_of_nodes()+1
                graph.add_edge(node,(new_node)) #adding new world and relation Rxx'

                graph.node[node] = delta_list
                graph.node[new_node] = [part2]
                formulas_in[new_node] = []
                alpha_node_solve(graph, node)
                beta_node_solve(graph, node, formulas_in)
                transitive_gamma_node(graph, new_node, formulas_in)
                alpha_node_solve(graph, node)
                beta_node_solve(graph, node, formulas_in)

                previous = graph.predecessors(new_node)
                for num in previous:
                    set = graph.node[num];
                    for j in range(0,len(set)):
                        if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                            formula = ('not',set[j][1][1])
                            if formula not in graph.node[new_node]:
                                graph.node[new_node].append(formula)
                                alpha_node_solve(graph, new_node)
                                beta_node_solve(graph, new_node, formulas_in)
                                reflexive_gamma_node(graph,node,formulas_in)
                        elif set[j][0] == 'box':
                            if set[j][1] not in graph.node[new_node]:
                                graph.node[new_node].append(set[j][1])
                                alpha_node_solve(graph, new_node)
                                beta_node_solve(graph, new_node, formulas_in)
                                reflexive_gamma_node(graph,node,formulas_in)
        alpha_node_solve(graph, node)
        beta_node_solve(graph, node, formulas_in)
'''
    :solving gammas at a NODE in graph
'''
def reflexive_gamma_node(graph, node, formulas_in):

    value_list = graph.node[node]
    #print "size is: ", len(value_list), value_list
    size = len(graph.node[node])
    status = 1;
    index = 0;
    while status == 1:
        for i in range(index,size):
            value = value_list[i]
            if value[0] == 'box':
                formula = value[1]
                if value not in formulas_in[node]:
                    formulas_in[node].append(value)
                    if formula not in graph.node[node]:
                        graph.node[node].append(formula)

            elif value[0] == 'not' and value[1][0] == "diamond":
                formula = ('not', value[1][1])
                if value not in formulas_in[node]:
                    formulas_in[node].append(value)
                    if formula not in graph.node[node]:
                        graph.node[node].append(formula)

        new_size = len(graph.node[node])

        if size == new_size:
            status = 0;
        else:
            diff = new_size - size
            index = len(graph.node[node])-diff
            size = new_size

def transitive_gamma_node(graph, node, formulas_in):

    parent = graph.predecessors(node)
    status = True
    if len(parent) == 0: #check if predecessor exists
        return None

    else:
        previous = graph.predecessors(parent[0])
        while status == True:
            if len(previous) == 0:
                status = False
                return None
            else:
                for num_node in previous:
                    graph.add_edge(num_node,node)
                    set = graph.node[num_node]
                    for i in range(0,len(set)):
                        if set[i][0] == 'not' and set[i][1][0] == 'diamond':
                            formula = ('not',set[i][1][1])
                            if set[i] not in formulas_in[node]:
                                formulas_in[node].append(set[i])
                                if formula not in graph.node[node]:
                                    graph.node[node].append(formula)
                            alpha_node_solve(graph, node)
                            beta_node_solve(graph,node,formulas_in)
                        elif set[i][0] == 'box':
                            if set[i] not in formulas_in[node]:
                                formulas_in[node].append(set[i])
                                if set[i][1] not in graph.node[node]:
                                    graph.node[node].append(set[i][1])
                            alpha_node_solve(graph, node)
                            beta_node_solve(graph,node,formulas_in)
                previous = graph.predecessors(previous[0])

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""             Main loop iterating over graphs         """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
num_graph = 0
for graph in Graphs:
    #dictionary of nodes: ticked formulas
    formulas_in = graph_formulas[num_graph]

    #initialise loop parameters
    status = 1;
    index = 1;
    #initial solve for alpha
    alpha_node(graph)

    #iterate over all nodes and all formulas inside them
    while status == 1:
        length = len(graph.nodes())+1
        for node in range(index,length):
            #initial number of nodes
            start_length = len(graph.nodes())

            #set internal status to False
            status_inside = False

            #verify whether node exists
            try:
                value_node = graph.node[node]
            except:
                #move on if it does not exists
                status_inside = True
                pass

            #when internal status is true add edge between them
            if status_inside == True:
                pass

            else:
                alpha_node_solve(graph,node)
                beta_node_solve(graph, node, formulas_in)
                reflexive_gamma_node(graph, node, formulas_in)
                alpha_node_solve(graph,node)
                beta_node_solve(graph, node, formulas_in)
                delta_node_solve(graph, node, formulas_in)

                #new variable to store current node
                current_node = node
                #number of node at this stage
                new_num_nodes = len(graph.nodes())

                #deal with new nodes and compare them with existing ones
                if new_num_nodes-current_node > 0:
                    for i in range(new_num_nodes,current_node,-1):
                        #if the last new node is the same as
                        try:
                            if graph.node[current_node] == graph.node[new_num_nodes] and ((current_node,new_num_nodes) in graph.edges()):
                                graph.remove_node(new_num_nodes)
                                new_num_nodes = len(graph.nodes())
                                pass
                            for all_nodes in range(1,new_num_nodes-1):
                                if (graph.node[new_num_nodes]==graph.node[all_nodes]) and ((all_nodes,new_num_nodes) not in graph.edges()):
                                    graph.add_edge(current_node,all_nodes)
                                    graph.remove_node(new_num_nodes)
                                    new_num_nodes = len(graph.nodes())
                                    break
                        except:
                            pass

                        try:
                            temp_node = graph.node[i]
                        except:
                            pass

                        status_inside2 = False
                        for exist in range(1,current_node):
                            if temp_node == graph.node[exist] and temp_node != exist:
                                #if the same node exists set status to true and exit the loop
                                status_inside2 = True
                                break

                        #deal with the node that already exists
                        if status_inside2 == True:
                            #remove the new_node which already exists
                            try:
                                graph.remove_node(i)
                            except:
                                continue
                            #add an edge from the node to existing node
                            graph.add_edge(current_node,exist)
                            #graph.add_edge(i,exist)

                            #get currrent list of nodes in the graph
                            list_of_nodes = graph.nodes()

                            #check nodes that have id > than deleted node and change ids, ids cannot have gaps in numbering
                            new_counter = i
                            temp_value = 0
                            for sig_node in list_of_nodes:
                                #when id of the node is greater than the deleted one deal with it
                                if (sig_node > new_counter+temp_value) and ((new_counter+temp_value) not in list_of_nodes):
                                    #add missing node
                                    try:
                                        graph.add_node(new_counter+temp_value)
                                        #assign set of formulas to a new node
                                        graph.node[new_counter+temp_value] = graph.node[sig_node]
                                    except:
                                        graph.remove_node(new_counter+temp_value)
                                        break

                                    #scan predecessor of the higher node and deal with edges
                                    predecessor = graph.predecessors(sig_node)

                                    for pred in predecessor:
                                        graph.add_edge(pred,new_counter+temp_value)

                                    #after we dealt with edges we can remove the higher order node
                                    graph.remove_node(sig_node)

                                    #get the current list of nodes
                                    list_of_nodes = graph.nodes()

                                    # increment temp_value in case there are more nodes in the list
                                    temp_value += 1
            end_length = len(graph.nodes())
            if start_length < end_length:
                diff = end_length - start_length
                index = index+1
            elif index < len(graph.nodes()):
                index = index+1
            else:
                status = 0;

    #increment number of graph to get correct list with used formulas
    num_graph += 1
    #print "used formulas in each node: ",formulas_in

'''
    :finding inconsistencies in the model
'''
index_inconsistent =[]
for i in range(0,len(Graphs)):
    graph = Graphs[i]
    for node in graph.nodes():
        consistent_list = graph.node[node]
        #print "we are here:", consistent_list
        status = sols.inconsistent(consistent_list)
        if status == True:
            #print "graph: ",i, " is inconsistent"
            index_inconsistent.append(i)
        else:
            status == False
index_inconsistent = list(set(index_inconsistent))
# removing inconsistent graphs- models
if index_inconsistent is not []:
    for num in reversed(index_inconsistent):
        del Graphs[num];

'''
    :display and save as pictures all the exiting graphs in the list
'''
if Graphs == []:
    print "sorry there a no models for the formula below"
    print "your provided formula is: ", (syntax.formula_to_string(psi))
    print "This means that the negation of it : ", "~(",(syntax.formula_to_string(psi)), ") is valid."

else:
    for i in range(0,len(Graphs)):
        graph = Graphs[i]

        custom_labels={}
        node_colours=['y']
        for node in graph.nodes():
            custom_labels[node] = graph.node[node]
            node_colours.append('c')

        #nx.draw(Graphs[i], nx.random_layout(Graphs[i]),  node_size=1500, with_labels=True, labels = custom_labels, node_color=node_colours)
        nx.draw(Graphs[i], nx.circular_layout(Graphs[i]),  node_size=1500, with_labels=True, labels = custom_labels, node_color=node_colours)
        #show with custom labels
        fig_name = "graph" + str(i) + ".png"

         #scaling the graph to fit the figure
        l,r = plt.xlim()
        plt.xlim(l-0.5,r+0.5)
        plt.savefig(fig_name)
        plt.show()

    print "Satisfiable models have been displayed."
    if len(Graphs) == 1:
        print "You have ",len(Graphs), " valid model."
    else:
        print "You have ",len(Graphs), " valid models."
    print "Your provided formula is: ", (syntax.formula_to_string(psi))
    print "Pictures of the graphs have been saves as: graph0.png, graph1.png etc."