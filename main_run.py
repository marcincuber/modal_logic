# Auther: Marcin Cuber
# All rights reserved
import syntax
import sols
import graph
import networkx as nx
import matplotlib.pyplot as plt
import input

from collections import OrderedDict

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
str_psi = "(@q^(@p > ~##r)) ^  (@p V (#s ^ @q))"# ^ (@s ^ @@#t)"
#str_psi = input.receive()
print(str_psi)

"""
Parsed string into tuple and list
"""
psi = syntax.parse_formula(BML, str_psi)

print "psi      " + str(psi)

#print "result === ", sols.recursivealpha(psi)

Sets.append(sols.recursivealpha(psi))

'''
    :recursively deal with all delta formulaes
    :formulas with following structure: <> p, ~[]p (diamond(p), not(box(p))
'''

def recursivedelta(psi,world):
    parsed_constants = ['or', 'and', 'imply', 'not']
    parsed_modalities = ['diamond', 'box']

    if psi[0] == 'diamond':
        result = [psi[1]]
        #if psi[1][0] in parsed_constants or psi[1][0] in parsed_modalities:
        #    result = recursivedelta(psi[1])
        graph.addworld(Worlds);
        Sets[world-1].remove(psi);

        graph.addedge(Edges,world,Worlds);
        Sets.append(result);
        #print "final results: ", result
        return result

    elif psi[0] == 'not' and isinstance(psi[1], tuple) and psi[1][0] == 'box':
        #print " we are here"
        psi1 = ('not', psi[1][1])
        result = [psi1]
        #if psi[1][1][0] in parsed_constants or psi[1][1][0] in parsed_modalities:
        #    result = recursivedelta(psi1,Worlds[0])
        graph.addworld(Worlds);
        Sets[world-1].remove(psi);

        graph.addedge(Edges,world,Worlds);
        Sets.append(result)
        return result

#print "sets " + str(Sets[0])

# initial expansion of the original formula in the main world
for set in reversed(Sets[0]):
    recursivedelta(set, Worlds[0])
# checking world by world and expanding existing diamond in all other worlds
def recexp():
    i = 1
    while i > 0:
        if len(Sets[i]) == 0:
            i+=1;
        else:

            for j in range(len(Sets[i])-1,-1,-1):
                #print "j= ",j, " i = ", i
                try:
                    Sets[i]
                except:
                    i = -1;
                    break;
                #print "we take: ", Sets[i][j], "and: ", Worlds[i]
                recursivedelta(Sets[i][j],Worlds[i])
            i+=1
        try:
            Worlds[i+1];
        except IndexError:
        #next index does not exist
        #break
            try:
                Sets[i][0];
            except IndexError:
                i = -1



'''
    :recursively deal with all gamma formulaes
    :formulas with following structure: ~<> p, ~<>p (box(p), not(diamond(p))
'''
def recursivegamma(psi,world):
    parsed_constants = ['or', 'and', 'imply', 'not']
    parsed_modalities = ['diamond', 'box']
    if psi[0] == 'box':
        result = psi[1]
        #print "box form: ", result
        if psi[1][0] in parsed_constants or psi[1][0] in parsed_modalities:
            #print "first check", psi
            for i in range(0,len(Sets)-1):
                if Edges[i][0] == 1:
                    value= Edges[i][1]
                    #print "here we adding", Sets[value-1], result
                    Sets[value-1].append(result)
        else:
            for i in range(0,len(Sets)-1):
                if Edges[i][0] == 1:
                    value= Edges[i][1]
                    #print "here we adding", Sets[value-1], result
                    Sets[value-1].append(result)
            #Sets[world-1].remove(psi);
        return result

    elif psi[0] == 'not' and isinstance(psi[1], tuple) and psi[1][0] == 'diamond':

        psi1 = ('not', psi[1][1])
        result = psi1
        if psi[1][1][0] in parsed_constants or psi[1][1][0] in parsed_modalities:
            #result = recursivegamma(psi1,world)
            #print "first check", psi
            for i in range(0,len(Sets)-1):
                if Edges[i][0] == 1:
                    value= Edges[i][1]
                    Sets[value-1].append(result)
        #for i in range(1,len(Sets)):
        #    Sets[i].append(result)
        Sets[world-1].remove(psi);
        return result

for set in reversed(Sets[0]):
    #print "set is: ", set
    recursivegamma(set,Worlds[0])

recexp()


#print "formula with incosistencies: ", Sets
#remove = sols.inconsistent(Sets)
#print "formula without: ", remove, " worlds: ", Worlds

'''
    :creating graph
    :deleting non unique elements
    :passing data to graph function
'''
'''
    :test edges and sets
'''
G = nx.DiGraph()
uniq_Sets = [list(OrderedDict.fromkeys(l)) for l in Sets]
'''
print "sets:" ,Sets
print "edges: ",Edges
print "worlds: ",Worlds
'''
graph.create_graph2(G,Edges,uniq_Sets)
#graph.create_graph2(G,Edges2,Sets2)

G_comp = nx.weakly_connected_component_subgraphs(G)
#add the initial graph to the list of graphs
for comp in G_comp:
    Graphs.append(comp);

def alpha_node(value_list):
    set = []
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
                #print "priting alpha", alpha, tuple(alpha)

                #set.append(sols.recursivealpha(value_list[i]))
            elif isinstance(value_list[i], str):
                set.append(value_list[i])
    return set
def delta_node(graph, delta_list):
    global counter
    for i in range(len(delta_list)-1,-1,-1):
        part1 = delta_list[i][0]
        if part1 == 'diamond':
            sub = delta_list[i];
            part2 = delta_list[i][1]
            new_node= graph.number_of_nodes()+1
            graph.add_edge(node,(new_node))
            #print part1, graph.node[node]
            graph.node[node].remove(sub)
            graph.node[new_node] = [part2]
            counter +=1;
        elif part1 == 'not' and delta_list[i][1][0] == 'box':
            sub = delta_list[i];
            part2 = ('not', delta_list[i][1][1])
            new_node= graph.number_of_nodes()+1
            graph.add_edge(node,(new_node))
            graph.node[node].remove(sub)
            graph.node[new_node] = [part2]
            counter +=1;

def beta_node(graph):
    for node in graph.nodes():
        value_list = graph.node[node]
        #print "here value_list = ", value_list, "for node =", i, "length of list is: ", len(value_list)
        for i in range(0,len(value_list)):
            value = value_list[i]
            #print "inside value is: ", value
            ###ADD scaning trough the list of propositions
            if value[0] =='or':
                part1 = value[1]
                part2 = value[2]
                comp2 = graph.copy()
                graph.node[node].remove(value)
                comp2.node[node].remove(value)
                graph.node[node].append(part1)
                comp2.node[node].append(part2)
                Graphs.append(comp2)
                break
            elif value[0] == 'not' and value[0][0] == 'and':
                part1 = value[1]
                part2 = value[2]
                left_part = ('not',part1)
                right_part = ('not',part2)
                comp2 = graph.copy()
                graph.node[node].remove(value)
                comp2.node[node].remove(value)
                graph.node[node].append(left_part)
                comp2.node[node].append(right_part)
                Graphs.append(comp2)
                break
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
                break

'''
    :split the main graph into two in case there is a beta formula in the World
'''
for graph in Graphs:
    beta_node(graph)

def solvegraph(graph_input):
    global counter
    #dealing with alpha formulaes
    for node in graph_input.nodes():
        alpha_list = graph_input.node[node]
        set = alpha_node(alpha_list)
        graph_input.node[node] = set

    #dealing with delta formulaes - diamond and not box
    for node in graph_input.nodes():
        delta_list = graph_input.node[node]
        for set in delta_list:
            if set[0] == 'diamond' or (set[0] == 'not' and set[1][0] == 'box'):
                delta_node(graph_input,delta_list)
        counter += counter

    for i in range(0,counter):
        for node in graph_input.nodes():
            delta_list = graph_input.node[node]
            delta_node(graph_input,delta_list)
            counter += counter
    counter = 0;

     #dealing with beta formulaes box and not diamond
    #beta_node(graph)

    #dealing with gamma formulaes box and not diamond
    for node in graph.nodes():
        gamma_list = graph.node[node]
        neighbors = graph.neighbors(node)
        for i in range(0,len(gamma_list)):
            part1 = gamma_list[i]

            if isinstance(part1, tuple) and part1[0] == 'box':
                part2 = gamma_list[i][1]
                for num in neighbors:
                    graph.node[num].append(part2)

            elif isinstance(part1, tuple) and part1[0] == 'not' and part1[1][0] == 'diamond':
                part2 = gamma_list[i][1][1]
                sub = ('not',part2)
                for num in neighbors:
                    graph.node[num].append(sub)
                    print graph.node[num]
    #delta again test
    for node in graph.nodes():
        delta_list = graph.node[node]
        delta_node(delta_list)
        counter += counter

    #dealing with beta formulaes box and not diamond
    #beta_node(graph)

'''
    :now we dealt with all the formulas in our main-original graph we can now deal with all graphs one by one
    :graphs are stored as classes in Graphs list
    :for each graph we are going to determine if they are satisfiable, if yes expand them, if not delete
'''

counter = 0; #how many new worlds were added
for graph in Graphs:
    #dealing with alpha formulaes
    for node in graph.nodes():
        alpha_list = graph.node[node]
        set = alpha_node(alpha_list)
        graph.node[node] = set

    #dealing with delta formulaes - diamond and not box
    for node in graph.nodes():
        delta_list = graph.node[node]
        delta_node(graph, delta_list)
        counter += counter
    for i in range(0,counter):
        for node in graph.nodes():
            delta_list = graph.node[node]
            delta_node(graph, delta_list)
            counter += counter
    counter = 0;

     #dealing with beta formulaes box and not diamond
    beta_node(graph)

# checking the consistency of the formulas for existing graphs
index_inconsistent =[]
for i in range(0,len(Graphs)):
    graph = Graphs[i]
    for node in graph.nodes():
        consistent_list = graph.node[node]
        status = sols.inconsistent(consistent_list)
        if status == True:
            #print "graph: ",i, " is inconsistent"
            index_inconsistent.append(i)
        else:
            status == False
#print index_inconsistent
# removing inconsistent graphs- models
if index_inconsistent is not []:
    for num in reversed(index_inconsistent):
        del Graphs[num];

for graph in Graphs:
    #alpha
    for node in graph.nodes():
        alpha_list = graph.node[node]
        set = alpha_node(alpha_list)
        graph.node[node] = set
    #dealing with gamma formulaes box and not diamond
    '''
    for node in graph.nodes():
        gamma_list = graph.node[node]
        neighbors = graph.neighbors(node)
        for i in range(0,len(gamma_list)):
            part1 = gamma_list[i]

            if isinstance(part1, tuple) and part1[0] == 'box':
                part2 = gamma_list[i][1]
                for num in neighbors:
                    graph.node[num].append(part2)

            elif isinstance(part1, tuple) and part1[0] == 'not' and part1[1][0] == 'diamond':
                part2 = gamma_list[i][1][1]
                sub = ('not',part2)
                for num in neighbors:
                    graph.node[num].append(sub)
                    print graph.node[num]
    '''
    #delta
    for node in graph.nodes():
        delta_list = graph.node[node]
        for i in range(len(delta_list)-1,-1,-1):
            part1 = delta_list[i][0]
            if part1 == 'diamond':
                sub = delta_list[i];
                part2 = delta_list[i][1]
                new_node= graph.number_of_nodes()+1
                graph.add_edge(node,(new_node))
            #print part1, graph.node[node]
                graph.node[node].remove(sub)
                graph.node[new_node] = [part2]
                counter +=1;
                #scan backwards
                #print "this node was added", graph.node[new_node]
                previous = graph.predecessors(new_node)
                for num in previous:
                    set = graph.node[num];
                    for j in range(0,len(set)-1):
                        if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                            formula = ('not',set[j][1][1])
                            graph.node[new_node].append(formula)
                        elif set[j][0] == 'box':
                            graph.node[new_node].append(set[j][1])


            elif part1 == 'not' and delta_list[i][1][0] == 'box':
                sub = delta_list[i];
                part2 = ('not', delta_list[i][1][1])
                new_node= graph.number_of_nodes()+1
                graph.add_edge(node,(new_node))
                graph.node[node].remove(sub)
                graph.node[new_node] = [part2]
                counter +=1;


                previous = graph.predecessors(new_node)
                for num in previous:
                    set = graph.node[num];
                    for j in range(0,len(set)-1):
                        if set[j][0] == 'not' and set[j][1][0] == 'diamond':
                            formula = ('not',set[j][1][1])
                            graph.node[new_node].append(formula)
                        elif set[j][0] == 'box':
                            graph.node[new_node].append(set[j][1])

    for node in graph.nodes():
        gamma_list = graph.node[node]
        neighbors = graph.neighbors(node)
        for i in range(0,len(gamma_list)):
            part1 = gamma_list[i]

            if isinstance(part1, tuple) and part1[0] == 'box':
                part2 = gamma_list[i][1]
                for num in neighbors:
                    graph.node[num].append(part2)

            elif isinstance(part1, tuple) and part1[0] == 'not' and part1[1][0] == 'diamond':
                part2 = gamma_list[i][1][1]
                sub = ('not',part2)
                for num in neighbors:
                    graph.node[num].append(sub)
                    print graph.node[num]
#finding inconsistencies in the model
index_inconsistent =[]
for i in range(0,len(Graphs)):
    graph = Graphs[i]
    for node in graph.nodes():
        consistent_list = graph.node[node]
        status = sols.inconsistent(consistent_list)
        if status == True:
            #print "graph: ",i, " is inconsistent"
            index_inconsistent.append(i)
        else:
            status == False
#print index_inconsistent
# removing inconsistent graphs- models
if index_inconsistent is not []:
    for num in reversed(index_inconsistent):
        del Graphs[num];


    #dealing with beta formulaes box and not diamond
    #beta_node(graph)

'''
    :display and save as pictures all the exiting graphs in the list
'''


if Graphs == []:
    print "sorry there a no models for the input.py formula"
    print "your provided formula is: ", (syntax.formula_to_string(psi))
    print "if you provided a negation of the formula that means: ", "~(",(syntax.formula_to_string(psi)), ") is valid."

else:
    for i in range(0,len(Graphs)):
        graph = Graphs[i]
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