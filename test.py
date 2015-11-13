import syntax
import sols
import graph
import networkx as nx
import matplotlib.pyplot as plt

from collections import OrderedDict

"""
Sybmol import
"""
BML = syntax.Language(*syntax.default_ascii)

"""
Arrays to store the number of worlds and sets that correspond to each world
"""
Graphs = [1];
Worlds = [1];
Edges = [];
Sets = [];

"""
Input String:
"""
#str_phi = "(#p ^ (@r ^ ~(r > #q)))^~@q"
str_psi = "((@r ^ t) ^ ~(@@s > @~s)) ^ (#r ^ @~r)"# ^ (@s ^ @@#t)"
print(str_psi)

"""
Parsed string into tuple and list
"""
psi = syntax.parse_formula(BML, str_psi)

print "psi      " + str(psi)
print "result === ", sols.recursivealpha(psi)

print "psi =", psi


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
        print " we are here"
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
                print "j= ",j, " i = ", i
                try:
                    Sets[i]
                except:
                    i = -1;
                    break;
                print "we take: ", Sets[i][j], "and: ", Worlds[i]
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

recexp()

'''
    :recursively deal with all gamma formulaes
    :formulas with following structure: ~<> p, ~<>p (box(p), not(diamond(p))
'''
def recursivegamma(psi,world):
    parsed_constants = ['or', 'and', 'imply', 'not']
    parsed_modalities = ['diamond', 'box']
    if psi[0] == 'box':
        result = psi[1]
        print "box form: ", result
        if psi[1][0] in parsed_constants or psi[1][0] in parsed_modalities:
            print "first check", psi
            #if psi[1][0] == "diamond":
            #    print "we we are", result
            #    recexp();
                #result = recursivedelta(result,world)

            #     Sets[world-1].remove(psi);
            #     result = recursivedelta(psi[1],Worlds[1])
            # else:
            #Sets[world-1].remove(psi);
            #result = recursivegamma(psi[1],world)

        for i in range(0,len(Sets)-1):
            if Edges[i][0] == 1:
                value= Edges[i][1]
                print "here we adding", Sets[value-1], result
                Sets[value-1].append(result)
        Sets[world-1].remove(psi);
        return result

    elif psi[0] == 'not' and isinstance(psi[1], tuple) and psi[1][0] == 'diamond':

        psi1 = ('not', psi[1][1])
        result = psi1
        if psi[1][1][0] in parsed_constants or psi[1][1][0] in parsed_modalities:
            #result = recursivegamma(psi1,world)
            print "first check", psi
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
print len(Sets[1])

recexp()

'''
i = 1
print num_of_worlds, len(Worlds)
while i < num_of_worlds:
    #print "we are here", i, Worlds[i]
    try:
        Worlds[i+1];
    except IndexError:
        #next index does not exist
        break
    print len(Sets[i])
    if len(Sets[i]) == 0:
        i+=1;
    else:
        for j in range(0,len(Sets[i])):
            #print "we take: ", Sets[i][j], "and: ", Worlds[i]
            i +=1;
            recursivedelta(Sets[i][j],Worlds[i])
'''

#test = [[('not', ('box', 'p')), ('box', 'p'), ('not', 'q'), ('q'), ('diamond', 'r')], [('or', ('p', 'q')),('not',('or',('p','q')))],['not',('or', ('p', 'q'))],['r', 'q']]




#print "formula with incosistencies: ", Sets
#remove = sols.inconsistent(Sets)
#print "formula without: ", remove, " worlds: ", Worlds

'''
    :creating graph
    :deleting non unique elements
    :passing data to graph function
'''
G = nx.DiGraph()
uniq_Sets = [list(OrderedDict.fromkeys(l)) for l in Sets]
print "sets:" ,Sets
print "edges: ",Edges
print "worlds: ",Worlds
graph.create_graph(G,Edges,uniq_Sets)

# H = G.copy();
#G = nx.DiGraph()
#uniq_Sets = [list(OrderedDict.fromkeys(l)) for l in Sets]
#graph.create_graph(G,Worlds,uniq_Sets)
#H = G.copy();