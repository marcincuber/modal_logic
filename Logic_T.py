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
    :Solving Modal Logic T - reflexive
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
#str_phi = "(#p ^ (@r ^ ~(r > #q)))^~@q"
#str_psi = "@r^((@#@p ^ @#q) > @(p ^ q))"
str_psi = "@p ^ ##@s"
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
G = nx.DiGraph()
uniq_Sets = [list(OrderedDict.fromkeys(l)) for l in Sets]

graph.create_graph_T(G,Edges,uniq_Sets)

print G.selfloop_edges()
print G.nodes()
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
    :resolving DELTAS given a GRAPH
'''
def delta_node(graph):
    for node in graph.nodes():
        delta_list = graph.node[node]

        for i in range(len(delta_list)-1,-1,-1):
            part1 = delta_list[i][0]
            if part1 == 'diamond':
                sub = delta_list[i];
                part2 = delta_list[i][1]
                new_node= graph.number_of_nodes()+1
                #adding new world
                graph.add_edge(node,(new_node))
                #adding recursive edge
                graph.add_edge((new_node),(new_node))
                delta_list.remove(sub)
                graph.node[node] = delta_list
                #graph.node[node].remove(sub)
                graph.node[new_node] = [part2]

                #scan backwards
                #print "this node was added", graph.node[new_node]
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
                sub = delta_list[i];
                part2 = ('not', delta_list[i][1][1])
                new_node= graph.number_of_nodes()+1
                #adding new world
                graph.add_edge(node,(new_node))
                #adding recursive edge
                graph.add_edge((new_node),(new_node))
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
                            #print "we added: ", (set[j][1]), " to new node: ", new_node
                            graph.node[new_node].append(set[j][1])


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
            #adding recursive edge
            graph.add_edge((new_node),(new_node))
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
            graph.add_edge((new_node),(new_node))
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
    :solving gammas at first node for a graph
'''
def reflexive_gamma(graph):
    for node in graph.nodes():
        value_list = graph.node[node]
        #print "size is: ", len(value_list), value_list
        size = len(graph.node[node])
        status = 1;

        index = 0;
        while status == 1:
            for i in range(index,size):
                value = value_list[i]
                #print "we have value: ", value, " for i = ", i
                if value[0] == 'box':
                    formula = value[1]
                    #print "here print: ", formula
                    graph.node[node].append(formula)

                elif value[0] == 'not' and value[1][0] == "diamond":
                    formula = ('not', value[1][1])
                    graph.node[node].append(formula)
                    #print "we added: ", (formula), " to new node: ", node
            new_size = len(graph.node[node])
            #print "new size is: ", new_size
            if size == new_size:
                status = 0;
            else:
                diff = new_size - size
                #print diff
                index = len(graph.node[node])-diff
                size = new_size
'''
    :solving gammas at a NODE in graph
'''
def reflexive_gamma_node(graph, node):

    value_list = graph.node[node]
    #print "size is: ", len(value_list), value_list
    size = len(graph.node[node])
    status = 1;
    index = 0;
    while status == 1:
        for i in range(index,size):
            value = value_list[i]
            #print "we have value: ", value, " for i = ", i
            if value[0] == 'box':
                formula = value[1]
                #print "here print: ", formula
                graph.node[node].append(formula)

            elif value[0] == 'not' and value[1][0] == "diamond":
                formula = ('not', value[1][1])
                graph.node[node].append(formula)
                #print "we added: ", (formula), " to new node: ", node
        new_size = len(graph.node[node])
        #print "new size is: ", new_size
        if size == new_size:
            status = 0;
        else:
            diff = new_size - size
            #print diff
            index = len(graph.node[node])-diff
            size = new_size
'''
    :split the main graph into two in case there is a beta formula in the World
'''
number_graph = 1
for graph in Graphs:

    status = 1;
    index = 1;
    print "graph number is: ", number_graph

    while status == 1:
        for node in range(index,len(graph.nodes())+1):
            #print "we are at node: ", node
            start_length = len(graph.nodes())

            alpha_node_solve(graph,node)
            remove_dups_graph(graph)

            beta_node_solve(graph, node)
            remove_dups_graph(graph)

            reflexive_gamma_node(graph,node)
            remove_dups_graph(graph)

            delta_node_solve(graph,node)
            remove_dups_graph(graph)

            end_length = len(graph.nodes())
            if start_length < end_length:
                diff = end_length - start_length
                #print "difference is :", diff, len(graph.nodes())
                index = index+1;
            else:
                status = 0;
        #print "node is: ", node, " in graph: ", graph

    remove_dups_graph(graph)
    number_graph +=1


'''
    :now we dealt with all the formulas in our main-original graph we can now deal with all graphs one by one
    :graphs are stored as classes in Graphs list
    :for each graph we are going to determine if they are satisfiable, if yes expand them, if not delete
'''
'''
for i in range(0,3):
    for graph in Graphs:

        #dealing with alpha formulaes
        alpha_node(graph)

    for graph in Graphs:
        #dealing with beta formulaes
        beta_node(graph)

#for i in range(0,5):
    for graph in Graphs:
    #dealing with delta and gamma formulaes
        delta_node(graph)
        remove_dups_graph(graph)

'''
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
        #print "graph: ", i, " has following selfloops ",graph.selfloop_edges()
        #print graph.nodes()
        #print graph.node[1]
        custom_labels={}
        node_colours=['y']
        for j in range(1,len(graph)+1):
            custom_labels[j] = graph.node[j]
            node_colours.append('b')
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