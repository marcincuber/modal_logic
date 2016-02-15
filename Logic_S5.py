# Author: Marcin Cuber
# All rights reserved
import syntax
import sols
import graph
import networkx as nx
import matplotlib.pyplot as plt
import input

from collections import OrderedDict

'''
    :Modal Logic K- no restrictions on the frame
'''
"""
Sybmol import
"""
BML = syntax.Language(*syntax.default_ascii)

'''
Arrays to store the number of worlds and sets that correspond to each world
'''
Graphs = [];
Worlds = [1];
Edges = [];
Sets = [];


'''
Input String:
'''

str_psi = "(~#@s ^ ##t) > #(#p > @r)"
#print(str_psi)

'''
Parsed string into tuple and list
'''
psi = syntax.parse_formula(BML, str_psi)

#print "psi      " + str(psi)

Sets.append(sols.recursivealpha(psi))

'''
    :creating graph
    :deleting non unique elements
    :passing data to graph function
'''
G = nx.MultiDiGraph()
uniq_Sets = [list(OrderedDict.fromkeys(l)) for l in Sets]
print "formula: ", uniq_Sets
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
                    set.append(alpha[0])
                    if len(alpha) > 1:
                        set.append(alpha[1])
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

            #print "alpha value is:", alpha
            if isinstance(alpha[0], tuple):
                set.append(alpha[0])
                if len(alpha) > 1:
                    set.append(alpha[1])
            else:
                for prop in alpha:
                    set.append(prop)

        elif isinstance(value_list[i], str):
            set.append(value_list[i])
'''
    :resolving BETAS given a GRAPH
'''
def beta_node(graph):
    for node in graph.nodes():
        value_list = graph.node[node]
        for i in range(0,len(value_list)):
            value = value_list[i]

            if value[0] =='or':
                part1 = value[1]
                part2 = value[2]
                comp2 = graph.copy()
                graph.node[node].remove(value)
                comp2.node[node].remove(value)
                graph.node[node].append(part1)
                comp2.node[node].append(part2)

                Graphs.append(comp2)
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
                for graph in Graphs:
                    alpha_node(graph)

            elif value[0] == 'imply':
                part1 = value[1]
                part2 = value[2]
                left_part = ('not',part1)
                comp2 = graph.copy()
                graph.node[node].remove(value)
                comp2.node[node].remove(value)
                graph.node[node].append(left_part)
                comp2.node[node].append(part2)

                Graphs.append(comp2)
                for graph in Graphs:
                    alpha_node(graph)
'''
    :resolving BETAS given a NODE in graph
'''
def beta_node_solve(graph, node):
    value_list = graph.node[node]
    for i in range(0,len(value_list)):
        value = value_list[i]
        if value[0] =='or':
            part1 = value[1]
            part2 = value[2]
            comp2 = graph.copy()
            graph.node[node].remove(value)
            comp2.node[node].remove(value)
            graph.node[node].append(part1)
            comp2.node[node].append(part2)
            Graphs.append(comp2)
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
            for graph in Graphs:
                alpha_node(graph)

        elif value[0] == 'imply':
            part1 = value[1]
            part2 = value[2]
            left_part = ('not',part1)
            comp2 = graph.copy()
            graph.node[node].remove(value)
            comp2.node[node].remove(value)
            graph.node[node].append(left_part)
            comp2.node[node].append(part2)
            Graphs.append(comp2)
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

        elif value_list[i] == 'or':
            part1 = value_list[i+1]
            part2 = value_list[i+2]
            comp2 = graph.copy()
            graph.node[node] = []
            comp2.node[node] = []
            graph.node[node].append(part1)
            comp2.node[node].append(part2)
            Graphs.append(comp2)

'''
    :resolving DELTAS given a NODE in graph
'''
def delta_node_solve(graph,node):
    alpha_node(graph)
    beta_node(graph)
    delta_list = graph.node[node]
    for i in range(len(delta_list)-1,-1,-1):
        part1 = delta_list[i][0]
        if part1 == 'diamond':
            sub = delta_list[i]
            part2 = delta_list[i][1]
            part2_alpha = sols.recursivealpha(part2)
            print "part2_alpha: ", part2_alpha
            status = False
            for point in graph.nodes():
                value_list = graph.node[point]
                print "values at node: ", value_list
                if part2 in value_list or part2_alpha in value_list or part2_alpha == value_list:
                    status = True
                    break;
            if status == False:
                new_node= graph.number_of_nodes()+1
                graph.node[node] = delta_list
                graph.node[new_node] = [part2]
            alpha_node(graph)
            beta_node(graph)


        elif part1 == 'not' and delta_list[i][1][0] == 'box':
            sub = delta_list[i]
            part2 = ('not', delta_list[i][1][1])
            part2_alpha = sols.recursivealpha(part2)
            status = False
            for point in graph.nodes():
                value_list = graph.node[point]
                if part2 in value_list or part2_alpha in value_list or part2_alpha == value_list:
                    status = True
                    break;
            if status == False:
                new_node= graph.number_of_nodes()+1
                graph.node[node] = delta_list
                graph.node[new_node] = [part2]
            alpha_node(graph)
            beta_node(graph)

'''
    : solving all gammas by creating a seperate list
'''
def gamma_node_solve(graph,node):
    gamma_list = []
    current_list = graph.node[node]
    for i in range(len(current_list)-1,-1,-1):
        part1 = current_list[i][0]
        if part1 == 'box':
            sub = current_list[i]
            part2 = current_list[i][1]
            gamma_list.append(part2)
            current_list.remove(sub)
            graph.node[node] = current_list
            alpha_node(graph)

            if part2[0] == 'diamond':
                gamma_list.remove(part2)
                part_delta = part2[1]
                status_in = False

                for point in graph.nodes():
                    value_list = graph.node[point]
                    if part_delta in value_list:
                        status_in = True
                        break;
                if status_in == False:
                    new_node= graph.number_of_nodes()+1
                    graph.node[new_node] = [part_delta]
            elif part2[0] == 'not' and part2[1][0] == 'box':
                gamma_list.remove(part2)
                part_delta = ('not', part2[1])
                status_in = False
                for point in graph.nodes():
                    value_list = graph.node[point]
                    if part_delta in value_list:
                        status_in = True
                        break;
                if status_in == False:
                    new_node= graph.number_of_nodes()+1
                    graph.node[new_node] = [part_delta]
                alpha_node(graph)
                beta_node(graph)

            #dealing with betas in case they were nested inside gamma
            elif (part2[0] == 'or') or (part2[0] == 'not' and part2[1][0]=='and') or (part2[0] == 'imply'):
                gamma_list.remove(part2)
                for point in graph.nodes():
                    value_list = graph.node[point]
                    if part2 not in value_list:
                        value_list.append(part2)
                alpha_node(graph)
                beta_node(graph)


        elif part1 == 'not' and current_list[i][1][0] == 'diamond':
            sub = current_list[i]
            part2 = ('not', current_list[i][1][1])
            gamma_list.append(part2)
            current_list.remove(sub)

            #current_list.append(part2)
            graph.node[node] = current_list
            alpha_node(graph)
            if part2[0] == 'diamond':
                gamma_list.remove(part2)
                part_delta = part2[1]
                status_in = False
                for point in graph.nodes():
                    value_list = graph.node[point]
                    if part_delta in value_list:
                        status_in = True
                        break;
                if status_in == False:
                    new_node= graph.number_of_nodes()+1
                    graph.node[new_node] = [part_delta]
            elif part2[0] == 'not' and part2[1][0] == 'box':
                gamma_list.remove(part2)
                part_delta = ('not', part2[1])
                status_in = False
                for point in graph.nodes():
                    value_list = graph.node[point]
                    if part_delta in value_list:
                        status_in = True
                        break;
                if status_in == False:
                    new_node= graph.number_of_nodes()+1
                    graph.node[new_node] = [part_delta]
                alpha_node(graph)
                beta_node(graph)
    return gamma_list

for graph in Graphs:
    gamma_list = []
    status = 1;
    index = 1;
    alpha_node(graph)
    beta_node(graph)
    alpha_node(graph)

    while status == 1:
        for node in range(index,len(graph.nodes())+1):
            start_length = len(graph.nodes())

            alpha_node_solve(graph,node)
            remove_dups_graph(graph)

            beta_node_solve(graph, node)
            remove_dups_graph(graph)

            delta_node_solve(graph,node)
            remove_dups_graph(graph)

            gamma_list_temp = gamma_node_solve(graph,node)
            if gamma_list_temp != [] and gamma_list_temp not in gamma_list:
                gamma_list += gamma_list_temp



            delta_node_solve(graph,node)
            remove_dups_graph(graph)

            for gamma in gamma_list:
                print "single gamma is: ", gamma

                for point in graph.nodes():
                    value_list = graph.node[point]
                    if gamma not in value_list:
                        value_list.append(gamma)

            end_length = len(graph.nodes())
            if start_length < end_length:
                diff = end_length - start_length
                index = index+1
            elif index < len(graph.nodes()):
                index = index+1
            else:
                status = 0;




#finding inconsistencies in the model
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
            node_colours.append('b')

        nx.draw(Graphs[i],nx.circular_layout(Graphs[i]),  node_size=1000, with_labels=True, labels = custom_labels, node_color=node_colours)
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

