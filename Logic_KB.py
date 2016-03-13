__author__ = 'marcincuber'
# -*- coding: utf-8 -*-
"""
    :Modal Logic KB- symmetric frames
"""
import syntax
import sols
import graph
import networkx as nx
import matplotlib.pyplot as plt
import copy
import time
from collections import OrderedDict


#import symbols
SET = syntax.Language(*syntax.ascii_setup)

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
str_psi = "(~B~D(BDu ^ DDt) ^ (~B~Dp ^ DBDs)) ^ B~s "
#str_psi = "#~@(#@u ^ @@t) > ( ~#~@p ^ @#@s)"
#str_psi = "(@(@r > @#t)) ^ (##@p)"
print "formula input: ", (str_psi)

'''
    :Parsed string into tuple and list
'''
psi = syntax.parse_formula(SET, str_psi)
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
                for j in alpha:
                    if isinstance(j, tuple):
                        if j not in set:
                            set.append(j)
                    else:
                        for prop in alpha:
                            set.append(prop)
            elif isinstance(value_list[i], str):
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
            for j in alpha:
                if isinstance(j, tuple):
                    if j not in set:
                        set.append(j)
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
                copy_formulas_in = copy.deepcopy(formulas_in)
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
                graph.add_edge((new_node), node) #add symmetric edge

                graph.node[node] = delta_list

                graph.node[new_node] = [part2]
                formulas_in[new_node] = []
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
                        elif set[j][0] == 'box':
                            if set[j][1] not in graph.node[new_node]:
                                graph.node[new_node].append(set[j][1])
                                alpha_node_solve(graph, new_node)
                                beta_node_solve(graph, new_node, formulas_in)

        elif part1 == 'not' and delta_list[i][1][0] == 'box':
            sub = delta_list[i]
            if sub not in formulas_in[node]:
                formulas_in[node].append(sub)
                part2 = ('not', delta_list[i][1][1])
                new_node= graph.number_of_nodes()+1
                graph.add_edge(node,(new_node)) #adding new world and relation Rxx'
                graph.add_edge((new_node), node) #add symmetric edge

                graph.node[node] = delta_list
                graph.node[new_node] = [part2]
                formulas_in[new_node] = []
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
                        elif set[j][0] == 'box':
                            if set[j][1] not in graph.node[new_node]:
                                graph.node[new_node].append(set[j][1])
                                alpha_node_solve(graph, new_node)
                                beta_node_solve(graph, new_node, formulas_in)

'''
    :solving gammas at a NODE in graph
'''
def symmetric_gamma_node(graph, node, formulas_in):

    value_list = graph.node[node]
    size = len(value_list)
    index = 0
    for i in range(index,size):
        value = value_list[i]
        if value[0] == 'box':
            formula = value[1]
            if value not in formulas_in[node]:
                formulas_in[node].append(value)
                try:
                    graph.successors(node)
                except:
                    break
                next_node = graph.successors(node)
                #print "before loop, next node is: ", next_node, " from node ", node
                for single_node in next_node:
                    if single_node < node:
                        #take the initial size of list to check whether it expanded
                        initial_size = len(graph.node[single_node])
                        if formula not in graph.node[single_node]:
                            graph.node[single_node].append(formula)

                        alpha_node_solve(graph,single_node)
                        beta_node_solve(graph,single_node, formulas_in)

                        final_size = len(graph.node[single_node])
                        #take diff to scan for these new entries
                        diff_size = final_size-initial_size
                        if diff_size > 0:
                            value_list_single_node_initial= graph.node[single_node]
                            value_list_single_node = value_list_single_node_initial[-diff_size:]
                            for value in value_list_single_node:
                                #print "last value is", value
                                if isinstance(value,tuple) and value[0] == 'box':
                                    part = value[1]
                                    if part not in graph.node[node]:
                                        graph.node[node].append(part)

                                elif isinstance(value,tuple) and value[0] == 'not' and value[1][0] == 'diamond':
                                    part = ('not',value[1][1])
                                    if part not in graph.node[node]:
                                        graph.node[node].append(part)

                                elif isinstance(value, tuple) and value[0] == 'diamond':
                                    part = value[1]
                                    new_node= graph.number_of_nodes()+1
                                    #adding new world
                                    graph.add_edge(single_node,(new_node))
                                    #adding symmetric edge
                                    graph.add_edge((new_node),single_node)

                                    formulas_in[new_node] = []
                                    graph.node[single_node] = value_list_single_node_initial
                                    graph.node[new_node] = [part]

                                    #expand new delta formulae
                                    previous = graph.predecessors(new_node)
                                    for num in previous:
                                        set = graph.node[num];
                                        for j in range(0,len(set)):
                                            if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                                                formula = ('not',set[j][1][1])
                                                if formula not in graph.node[new_node]:
                                                    graph.node[new_node].append(formula)
                                                    alpha_node_solve(graph,new_node)
                                                    beta_node_solve(graph,new_node, formulas_in)
                                            elif set[j][0] == 'box':
                                                if set[j][1] not in graph.node[new_node]:
                                                    graph.node[new_node].append(set[j][1])
                                                    alpha_node_solve(graph,new_node)
                                                    beta_node_solve(graph,new_node, formulas_in)
                                elif isinstance(value,tuple) and value[0] == 'not' and value[1][0] == 'box':
                                    part = ('not', value[1][1])
                                    new_node= graph.number_of_nodes()+1
                                    #adding new world
                                    graph.add_edge(single_node,(new_node))
                                    #adding symmetric edge
                                    graph.add_edge((new_node),single_node)

                                    formulas_in[new_node] = []
                                    graph.node[single_node] = value_list_single_node_initial
                                    graph.node[new_node] = [part]

                                    previous = graph.predecessors(new_node)
                                    for num in previous:
                                        set = graph.node[num];
                                        for j in range(0,len(set)):
                                            if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                                                formula = ('not',set[j][1][1])
                                                if formula not in graph.node[new_node]:
                                                    graph.node[new_node].append(formula)
                                                    alpha_node_solve(graph,new_node)
                                                    beta_node_solve(graph,new_node, formulas_in)
                                            elif set[j][0] == 'box':
                                                if set[j][1] not in graph.node[new_node]:
                                                    graph.node[new_node].append(set[j][1])
                                                    alpha_node_solve(graph,new_node)
                                                    beta_node_solve(graph,new_node, formulas_in)

                alpha_node_solve(graph, node)
                beta_node_solve(graph, node, formulas_in)
                delta_node_solve(graph, node, formulas_in)

        elif value[0] == 'not' and value[1][0] == 'diamond':
            formula = ('not', value[1][1])
            if value not in formulas_in[node]:
                formulas_in[node].append(value)
                try:
                    graph.successors(node)
                except:
                    break
                next_node = graph.successors(node)

                for single_node in next_node:
                    if single_node < node:
                        #take the initial size of list to check whether it expanded
                        initial_size = len(graph.node[single_node])
                        if formula not in graph.node[single_node]:
                            graph.node[single_node].append(formula)
                        alpha_node_solve(graph, single_node)
                        beta_node_solve(graph, single_node, formulas_in)
                        final_size = len(graph.node[single_node])

                        #take diff to scan for these new entries
                        diff_size = final_size-initial_size
                        if diff_size > 0:
                            value_list_single_node_initial= graph.node[single_node]
                            value_list_single_node = value_list_single_node_initial[-diff_size:]
                            for value in value_list_single_node:

                                if isinstance(value,tuple) and value[0] == 'box':
                                    part = value[1]
                                    if part not in graph.node[node]:
                                        graph.node[node].append(part)
                                elif isinstance(value,tuple) and value[0] == 'not' and value[1][0] == 'diamond':
                                    part = ('not',value[1][1])
                                    if part not in graph.node[node]:
                                        graph.node[node].append(part)
                                elif isinstance(value, tuple) and value[0] == 'diamond':
                                    part = value[1]
                                    new_node= graph.number_of_nodes()+1
                                    #adding new world
                                    graph.add_edge(single_node,(new_node))
                                    #adding symmetric edge
                                    graph.add_edge((new_node),single_node)

                                    formulas_in[new_node] = []
                                    graph.node[single_node] = value_list_single_node_initial
                                    graph.node[new_node] = [part]

                                    previous = graph.predecessors(new_node)
                                    for num in previous:
                                        set = graph.node[num];
                                        for j in range(0,len(set)):
                                            if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                                                formula = ('not',set[j][1][1])
                                                #print "here print: ", formula
                                                if formula not in graph.node[new_node]:
                                                    graph.node[new_node].append(formula)
                                                    alpha_node_solve(graph,new_node)
                                                    beta_node_solve(graph,new_node, formulas_in)
                                            elif set[j][0] == 'box':
                                                if set[j][0] not in graph.node[new_node]:
                                                    graph.node[new_node].append(set[j][1])
                                                    alpha_node_solve(graph,new_node)
                                                    beta_node_solve(graph,new_node, formulas_in)

                                elif isinstance(value,tuple) and value[0] == 'not' and value[1][0] == 'box':
                                    part = ('not', value[1][1])
                                    new_node= graph.number_of_nodes()+1
                                    #adding new world
                                    graph.add_edge(single_node,(new_node))
                                    #adding symmetric edge
                                    graph.add_edge((new_node),single_node)

                                    formulas_in[new_node] = []
                                    graph.node[single_node] = value_list_single_node_initial
                                    graph.node[new_node] = [part]

                                    previous = graph.predecessors(new_node)
                                    for num in previous:
                                        set = graph.node[num];
                                        for j in range(0,len(set)):
                                            if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                                                formula = ('not',set[j][1][1])
                                                #print "here print: ", formula
                                                if formula not in graph.node[new_node]:
                                                    graph.node[new_node].append(formula)
                                                    alpha_node_solve(graph,new_node)
                                                    beta_node_solve(graph,new_node, formulas_in)
                                            elif set[j][0] == 'box':
                                                if set[j][0] not in graph.node[new_node]:
                                                    graph.node[new_node].append(set[j][1])
                                                    alpha_node_solve(graph,new_node)
                                                    beta_node_solve(graph,new_node, formulas_in)
                alpha_node_solve(graph, node)
                beta_node_solve(graph, node, formulas_in)
                delta_node_solve(graph, node, formulas_in)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""             Main loop iterating over graphs         """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def main():
    num_graph = 0
    for graph in Graphs:
        formulas_in = graph_formulas[num_graph]
        status = 1;
        index = 1;
        alpha_node(graph)
        while status == 1:
            for node in range(index,len(graph.nodes())+1):

                start_length = len(graph.nodes())

                alpha_node_solve(graph,node)

                beta_node_solve(graph, node, formulas_in)

                delta_node_solve(graph, node, formulas_in)

                symmetric_gamma_node(graph, node, formulas_in)

                delta_node_solve(graph, node, formulas_in)

                alpha_node_solve(graph,node)

                beta_node_solve(graph, node, formulas_in)

                delta_node_solve(graph, node, formulas_in)

                symmetric_gamma_node(graph, node, formulas_in)

                end_length = len(graph.nodes())
                if start_length < end_length:
                    diff = end_length - start_length
                    index = index+1
                elif index < len(graph.nodes()):
                    index = index+1
                else:
                    status = 0;
        num_graph += 1

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

            nx.draw(Graphs[i], nx.spring_layout(Graphs[i]),  node_size=1500, with_labels=True, labels = custom_labels, node_color=node_colours)
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

t0 = time.clock()
main()
print ((time.clock() - t0), " seconds process time")