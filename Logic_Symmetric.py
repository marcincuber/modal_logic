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
    :Solving Modal Logic Symmetric - symmetric and NOT reflexive relation
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

str_psi = "(@#s > @t) ^ (@~#p ^ ##@q)"
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

graph.create_graph_symmetric(G,Edges,uniq_Sets)
Graphs.append(G)

#function to remove duplicates from the list
def remove_duplicates(l):
    return list(set(l))

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
    #graph.node[node] = remove_duplicates(set)

'''
    :resolving BETAS given a GRAPH
'''
def beta_node(graph):
    for node in graph.nodes():
        value_list = graph.node[node]
        #print "here value_list = ", value_list, "for node =", i, "length of list is: ", len(value_list)
        for i in range(0,len(value_list)):
            value = value_list[i]

            ###ADD scaning through the list of propositions
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
                #break
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
                #break
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
                #break
'''
    :resolving BETAS given a NODE in graph
'''
def beta_node_solve(graph, node):
    value_list = graph.node[node]
    #print "here value_list = ", value_list, "for node =", i, "length of list is: ", len(value_list)
    for i in range(0,len(value_list)):
        value = value_list[i]
        ###ADD scaning through the list of propositions
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
            #break
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
            #break
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
            #break
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
            #break
        elif value_list[i] == 'or':
            part1 = value_list[i+1]
            part2 = value_list[i+2]
            comp2 = graph.copy()
            graph.node[node] = []
            comp2.node[node] = []
            graph.node[node].append(part1)
            comp2.node[node].append(part2)
            Graphs.append(comp2)
            #break

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
            #adding new world
            graph.add_edge(node,(new_node))
            #adding symmetric edge
            graph.add_edge((new_node),node)
            delta_list.remove(sub)
            graph.node[node] = delta_list
            #graph.node[node].remove(sub)
            graph.node[new_node] = [part2]


            previous = graph.predecessors(new_node)
            for num in previous:
                set = graph.node[num];
                for j in range(0,len(set)):
                    if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                        formula = ('not',set[j][1][1])
                        #print "here print: ", formula
                        graph.node[new_node].append(formula)
                    elif set[j][0] == 'box':
                        graph.node[new_node].append(set[j][1])

        elif part1 == 'not' and delta_list[i][1][0] == 'box':
            sub = delta_list[i]
            part2 = ('not', delta_list[i][1][1])
            new_node= graph.number_of_nodes()+1
            #adding new world
            graph.add_edge(node,(new_node))
            #adding recursive edge
            graph.add_edge((new_node),(node))
            delta_list.remove(sub)
            #print "list is: ", delta_list
            graph.node[node] = delta_list
            #graph.node[node].remove(sub)
            graph.node[new_node] = [part2]

            previous = graph.predecessors(new_node)
            for num in previous:
                set = graph.node[num];
                for j in range(0,len(set)):
                    if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                        formula = ('not',set[j][1][1])
                        #print "here print: ", formula
                        graph.node[new_node].append(formula)

                    elif set[j][0] == 'box':
                        #print "we added: ", (set[j][1]), " to new node: ", new_node
                        graph.node[new_node].append(set[j][1])


'''
    :solving gammas at a NODE in graph
'''
def symmetric_gamma_node(graph, node):

    value_list = graph.node[node]
    size = len(value_list)
    index = 0
    #print "size is: ", len(value_list), value_list
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
                            #print "last value is", value
                            if isinstance(value,tuple) and value[0] == 'box':
                                part = value[1]
                                graph.node[node].append(part)

                            elif isinstance(value,tuple) and value[0] == 'not' and value[1][0] == 'diamond':
                                part = ('not',value[1][1])
                                graph.node[node].append(part)

                            elif isinstance(value, tuple) and value[0] == 'diamond':
                                part = value[1]
                                new_node= graph.number_of_nodes()+1
                                #adding new world
                                graph.add_edge(single_node,(new_node))
                                #adding symmetric edge
                                graph.add_edge((new_node),single_node)
                                value_list_single_node_initial.remove(value)
                                graph.node[single_node] = value_list_single_node_initial
                                graph.node[new_node] = [part]

                                #expand new delta formulae
                                previous = graph.predecessors(new_node)
                                for num in previous:
                                    set = graph.node[num];
                                    for j in range(0,len(set)):
                                        if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                                            formula = ('not',set[j][1][1])
                                            #print "here print: ", formula
                                            graph.node[new_node].append(formula)
                                        elif set[j][0] == 'box':
                                            graph.node[new_node].append(set[j][1])
                            elif isinstance(value,tuple) and value[0] == 'not' and value[1][0] == 'box':
                                part = ('not', value[1][1])
                                new_node= graph.number_of_nodes()+1
                                #adding new world
                                graph.add_edge(single_node,(new_node))
                                #adding symmetric edge
                                graph.add_edge((new_node),single_node)
                                value_list_single_node_initial.remove(value)
                                graph.node[single_node] = value_list_single_node_initial
                                graph.node[new_node] = [part]

                                previous = graph.predecessors(new_node)
                                for num in previous:
                                    set = graph.node[num];
                                    for j in range(0,len(set)):
                                        if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                                            formula = ('not',set[j][1][1])
                                            #print "here print: ", formula
                                            graph.node[new_node].append(formula)
                                        elif set[j][0] == 'box':
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
                                graph.node[node].append(part)
                            elif isinstance(value,tuple) and value[0] == 'not' and value[1][0] == 'diamond':
                                part = ('not',value[1][1])
                                graph.node[node].append(part)
                            elif isinstance(value, tuple) and value[0] == 'diamond':
                                part = value[1]
                                new_node= graph.number_of_nodes()+1
                                #adding new world
                                graph.add_edge(single_node,(new_node))
                                #adding symmetric edge
                                graph.add_edge((new_node),single_node)
                                value_list_single_node_initial.remove(value)
                                graph.node[single_node] = value_list_single_node_initial
                                graph.node[new_node] = [part]

                                previous = graph.predecessors(new_node)
                                for num in previous:
                                    set = graph.node[num];
                                    for j in range(0,len(set)):
                                        if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                                            formula = ('not',set[j][1][1])
                                            #print "here print: ", formula
                                            graph.node[new_node].append(formula)
                                        elif set[j][0] == 'box':
                                            graph.node[new_node].append(set[j][1])

                            elif isinstance(value,tuple) and value[0] == 'not' and value[1][0] == 'box':
                                part = ('not', value[1][1])
                                new_node= graph.number_of_nodes()+1
                                #adding new world
                                graph.add_edge(single_node,(new_node))
                                #adding symmetric edge
                                graph.add_edge((new_node),single_node)
                                value_list_single_node_initial.remove(value)
                                graph.node[single_node] = value_list_single_node_initial
                                graph.node[new_node] = [part]

                                previous = graph.predecessors(new_node)
                                for num in previous:
                                    set = graph.node[num];
                                    for j in range(0,len(set)):
                                        if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                                            formula = ('not',set[j][1][1])
                                            #print "here print: ", formula
                                            graph.node[new_node].append(formula)
                                        elif set[j][0] == 'box':
                                            graph.node[new_node].append(set[j][1])

'''
    :split the main graph into two in case there is a beta formula in the World
'''
number_graph = 1
for graph in Graphs:

    status = 1;
    index = 1;
    print "graph number is: ", number_graph
    alpha_node(graph)
    beta_node(graph)
    alpha_node(graph)
    while status == 1:
        for node in range(index,len(graph.nodes())+1):
            #print "we are at node: ", node
            start_length = len(graph.nodes())

            alpha_node_solve(graph,node)
            remove_dups_graph(graph)

            beta_node_solve(graph, node)
            remove_dups_graph(graph)

            delta_node_solve(graph,node)
            remove_dups_graph(graph)

            symmetric_gamma_node(graph, node)

            if len(graph.nodes()) > 3:
                length = len(graph.nodes())
                node1 = graph.node[length]
                node2 = graph.node[length-1]
                node3 = graph.node[length-2]

                list_of_nodes = []
                if node1 == node2 and node1 == node3 and node2 == node3:
                    for i in range(1,length+1):
                        value_list = graph.node[i]
                        if value_list == node3:
                            list_of_nodes.append(i)
                    delete_list = list_of_nodes[-(len(list_of_nodes)-2):]
                    #print "main list is: ", list_of_nodes
                    #print "delete_list is: ", delete_list
                    for i in delete_list:
                        graph.remove_node(i)
                    connect_list = list_of_nodes[:2]
                    graph.add_edge(connect_list[0], connect_list[1])
                    status = 0
            if len(graph.nodes()) > 20:
                main_node_list = graph.neighbors(1)
                repeat_list = []
                for num in main_node_list:
                    for num2 in main_node_list:
                        if graph.node[num] == graph.node[num2]:
                            if num2 not in repeat_list:
                                repeat_list.append(num2)
                for num in main_node_list:
                    print "what ever"
                    #graph.remove_node(repeat_list[1])
                print repeat_list
                status = 0

            end_length = len(graph.nodes())
            if start_length < end_length:
                diff = end_length - start_length
                index = index+1
            elif index < len(graph.nodes()):
                index = index+1
            else:
                status = 0;
        #print "node is: ", node, " in graph: ", graph

    #remove_dups_graph(graph)
    number_graph +=1




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