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
    :Modal Logic K4- all transitive frames
'''
"""
Sybmol import
"""
BML = syntax.Language(*syntax.default_ascii)

"""
Arrays to store the number of worlds and sets that correspond to each world
"""
Graphs = [];
Worlds = [1];
Edges = [];
Sets = [];

"""
Input String:
"""

str_psi = "(#p ^ #@t)^ @q"
print(str_psi)

"""
Parsed string into tuple and list
"""
psi = syntax.parse_formula(BML, str_psi)

print "psi      " + str(psi)

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
    set = []
    value_list = graph.node[node]
    #print "here we have: ", value_list, "its size is: ", len(value_list)

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
        #print "here value_list = ", value_list, "for node =", i, "length of list is: ", len(value_list)
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
                #just added!!!
                for graph in Graphs:
                    alpha_node(graph)
'''
    :resolving BETAS given a NODE in graph
'''
def beta_node_solve(graph, node):
    value_list = graph.node[node]
    #print "here value_list = ", value_list, "for node =", i, "length of list is: ", len(value_list)
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
                #dealing with alpha formulaes
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
                #dealing with alpha formulaes
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
                #dealing with alpha formulaes
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
    delta_list = graph.node[node]
    #print "starting delta is: ", delta_list
    for i in range(len(delta_list)-1,-1,-1):
        part1 = delta_list[i][0]
        if part1 == 'diamond':
            sub = delta_list[i]
            part2 = delta_list[i][1]
            new_node= graph.number_of_nodes()+1

            graph.add_edge(node,(new_node)) #adding new world and relation Rxx'
            graph.add_edge((new_node),(new_node)) #adding recursive edge
            #graph.add_edge((new_node),node) #adding symmetric edge

            graph.node[node] = delta_list

            graph.node[new_node] = [part2]
            alpha_node(graph)
            beta_node(graph)
            transitive_gamma_node(graph, new_node)
            alpha_node(graph)
            beta_node(graph)

            previous = graph.predecessors(new_node)
            for num in previous:
                set = graph.node[num];
                for j in range(0,len(set)):
                    if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                        formula = ('not',set[j][1][1])
                        if formula not in graph.node[new_node]:
                            graph.node[new_node].append(formula)
                    elif set[j][0] == 'box':
                        if set[j][1] not in graph.node[new_node]:
                            graph.node[new_node].append(set[j][1])

        elif part1 == 'not' and delta_list[i][1][0] == 'box':
            sub = delta_list[i]
            part2 = ('not', delta_list[i][1][1])
            new_node= graph.number_of_nodes()+1

            graph.add_edge(node,(new_node)) #adding new world and relation Rxx'
            graph.add_edge((new_node),(new_node)) #adding recursive edge
            #graph.add_edge((new_node),node) #adding symmetric edge

            graph.node[node] = delta_list
            #graph.node[node].remove(sub)
            graph.node[new_node] = [part2]
            alpha_node(graph)
            beta_node(graph)
            transitive_gamma_node(graph, new_node)
            alpha_node(graph)
            beta_node(graph)

            previous = graph.predecessors(new_node)
            for num in previous:
                set = graph.node[num];
                for j in range(0,len(set)):
                    if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                        formula = ('not',set[j][1][1])
                        if formula not in graph.node[new_node]:
                            graph.node[new_node].append(formula)
                    elif set[j][0] == 'box':
                        if set[j][1] not in graph.node[new_node]:
                            graph.node[new_node].append(set[j][1])

'''
    :solving gammas at a NODE in graph
'''
def symmetric_gamma_node(graph, node):

    value_list = graph.node[node]
    size = len(value_list)
    index = 0
    for i in range(index,size):
        value = value_list[i]
        if value[0] == 'box':
            formula = value[1]
            #find previous node and add box formula to it
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
                    beta_node_solve(graph,single_node)
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
                                #### do not remove!!!
                                #value_list_single_node_initial.remove(value)
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
                                        elif set[j][0] == 'box':
                                            if set[j][1] not in graph.node[new_node]:
                                                graph.node[new_node].append(set[j][1])
                            elif isinstance(value,tuple) and value[0] == 'not' and value[1][0] == 'box':
                                part = ('not', value[1][1])
                                new_node= graph.number_of_nodes()+1
                                #adding new world
                                graph.add_edge(single_node,(new_node))
                                #adding symmetric edge
                                graph.add_edge((new_node),single_node)
                                #### do not remove!!!
                                #value_list_single_node_initial.remove(value)
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
                                        elif set[j][0] == 'box':
                                            if set[j][1] not in graph.node[new_node]:
                                                graph.node[new_node].append(set[j][1])


        elif value[0] == 'not' and value[1][0] == 'diamond':
            formula = ('not', value[1][1])
            #find previous node and add box formula to it
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
                    beta_node_solve(graph,single_node)
                    final_size = len(graph.node[single_node])
                    #take diff to scan for these new entries
                    diff_size = final_size-initial_size
                    if diff_size > 0:
                        value_list_single_node_initial= graph.node[single_node]
                        value_list_single_node = value_list_single_node_initial[-diff_size:]
                        for value in value_list_single_node:
                            print "last value is", value
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
                                #### do not remove!!!
                                #value_list_single_node_initial.remove(value)
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
                                        elif set[j][0] == 'box':
                                            if set[j][1] not in graph.node[new_node]:
                                                graph.node[new_node].append(set[j][1])

                            elif isinstance(value,tuple) and value[0] == 'not' and value[1][0] == 'box':
                                part = ('not', value[1][1])
                                new_node= graph.number_of_nodes()+1
                                #adding new world
                                graph.add_edge(single_node,(new_node))
                                #adding symmetric edge
                                graph.add_edge((new_node),single_node)
                                #### do not remove!!!
                                #value_list_single_node_initial.remove(value)
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
                                        elif set[j][0] == 'box':
                                            if set[j][1] not in graph.node[new_node]:
                                                graph.node[new_node].append(set[j][1])

def reflexive_gamma_node(graph, node):
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
                if formula not in graph.node[node]:
                    graph.node[node].append(formula)
            elif value[0] == 'not' and value[1][0] == "diamond":
                formula = ('not', value[1][1])
                if formula not in graph.node[node]:
                    graph.node[node].append(formula)
        new_size = len(graph.node[node])
        #print "new size is: ", new_size
        if size == new_size:
            status = 0;
        else:
            diff = new_size - size
            #print diff
            index = len(graph.node[node])-diff
            size = new_size

def transitive_gamma_node(graph, node):
    parent = graph.predecessors(node)
    if node in parent:
        parent.remove(node)
    status = True
    if len(parent) == 0: #check if predecessor exists
        return None
    else:
        previous = graph.predecessors(parent[0])
        if parent[0] in previous:
            previous.remove(parent[0])

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
                            if formula not in graph.node[node]:
                                graph.node[node].append(formula)
                        elif set[i][0] == 'box':
                            if set[i][1] not in graph.node[node]:
                                graph.node[node].append(set[i][1])
                previous = graph.predecessors(previous[0])
                if parent[0] in previous:
                    previous.remove(parent[0])

for graph in Graphs:

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

            reflexive_gamma_node(graph, node)
            remove_dups_graph(graph)

            delta_node_solve(graph,node)
            remove_dups_graph(graph)

            #check if such node already exists
            value_list = graph.node[node]
            current_length = len(graph.nodes())

            for i in range (current_length, current_length-3, -1):
                #print "value for i is: ", i
                if node != i:
                    value_at_previous_node = graph.node[i]
                    # print "value at prev node: ", value_at_previous_node
                    if set(value_list) == set(value_at_previous_node):
                        print "sets are the same!"
                        status = 0
                        break

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
            index_inconsistent.append(i)
        else:
            status == False

index_inconsistent = list(set(index_inconsistent))

# removing inconsistent graphs- models
if index_inconsistent is not []:
    for num in reversed(index_inconsistent):
        del Graphs[num]


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
        '''
        for j in range(1,len(graph.nodes())+1):
            custom_labels[j] = graph.node[j]
            node_colours.append('b')
        '''
        nx.draw(Graphs[i],  node_size=1000, with_labels=True, labels = custom_labels, node_color=node_colours)
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