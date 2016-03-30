__author__ = 'marcincuber'
import pytest
from pytest import raises
import sols
import syntax
import graph as gr
import networkx as nx
import Logic_K as l
#import symbols
SET = syntax.Language(*syntax.ascii_setup)
'''
    :testing parser's conversion
'''
@pytest.mark.conver
def test_convert_form1_and():
    str_psi = "(~Bp ^ Dq) "
    psi = syntax.parse_formula(SET, str_psi)
    converted_string = ('and', ('not', ('box', 'p')), ('diamond', 'q'))
    assert psi == converted_string

@pytest.mark.conver
def test_convert_form2_or():
    str_psi = "(DBp V BDq) "
    psi = syntax.parse_formula(SET, str_psi)
    converted_string = ('or', ('diamond', ('box', 'p')), ('box',('diamond', 'q')))
    assert psi == converted_string

@pytest.mark.conver
def test_convert_form3_imply():
    str_psi = "(DBp > BDq) "
    psi = syntax.parse_formula(SET, str_psi)
    converted_string = ('imply', ('diamond', ('box', 'p')), ('box',('diamond', 'q')))
    assert psi == converted_string

#test whether ambigious formulas are reporting error
@pytest.mark.conver
def test_convert_form4_imply():
    str_psi = "(~Bp ^ Dq V s) "
    with raises(Exception) as excinfo:
        syntax.parse_formula(SET, str_psi)
    assert 'Proposition should be in place!' in str(excinfo.value)

'''
    :testing alpha expansion function
'''
#alpha expansion: two formulas
@pytest.mark.alphas
def test_alpha_form1():
    Sets = []
    alpha_expand = [('not', ('box', 'p')), ('diamond', 'q')]
    str_psi = "(~Bp ^ Dq) "
    psi = syntax.parse_formula(SET, str_psi)
    Sets.append(sols.recursivealpha(psi))
    assert Sets[0] == alpha_expand

#alpha expanstion: #alpha expansion: embedded formulas
@pytest.mark.alphas
def test_alpha_form2():
    Sets = []
    alpha_expand = [('not', ('box', ('and', 'p', ('diamond', 'q')))), 's', 'q', ('diamond', 't')]
    str_psi = "(~B(p ^ Dq) ^ (s ^ (q ^ Dt))) "
    psi = syntax.parse_formula(SET, str_psi)
    Sets.append(sols.recursivealpha(psi))
    assert Sets[0] == alpha_expand

'''
    :testing graph functions, expanding a graph(delta,gamma) and number of graphs(beta)
'''
#alpha formulas tested
@pytest.mark.graph
def test_graph_form1():
    Graphs = []
    Sets = []
    G = nx.MultiDiGraph()
    str_psi = "(~Bp ^ Dq) "
    psi = syntax.parse_formula(SET, str_psi)
    Sets.append(sols.recursivealpha(psi))
    gr.create_graph_K(G,Sets)
    Graphs.append(G)
    #check if there is new graph
    assert len(Graphs) == 1
    #check if the graph has correct formula at node 1
    assert G.node[1] == [('not', ('box', 'p')), ('diamond', 'q')]

#alpha, delta and gamma formulas tested
@pytest.mark.graph
def test_graph_form2():
    Graphs = []
    Sets = []
    formulas_in = {}
    formulas_in[1] = []
    G = nx.MultiDiGraph()
    str_psi = "(Bp ^ Dq) "
    psi = syntax.parse_formula(SET, str_psi)
    Sets.append(sols.recursivealpha(psi))
    gr.create_graph_K(G,Sets)
    Graphs.append(G)
    #apply delta expansion
    l.delta_node_solve(G, 1 ,formulas_in)
    #check if node 1 has correct formula
    assert G.node[1] == [('box', 'p'), ('diamond', 'q')]
    #check new node contains expanded delta and gamma formulas
    assert G.node[2] == ['q','p']

#beta formula tested
@pytest.mark.graph
def test_graph_form3():
    l.Graphs = []
    Sets = []
    formulas_in = {}
    formulas_in[1] = []
    G = nx.MultiDiGraph()
    str_psi = "(Bp V Dq)"
    psi = syntax.parse_formula(SET, str_psi)
    Sets.append(sols.recursivealpha(psi))
    gr.create_graph_K(G,Sets)
    l.Graphs.append(G)
    #apply beta expansion
    l.beta_node_solve(G, 1 ,formulas_in)
    #check if there are 2 graphs
    assert len(l.Graphs) == 2
    #check if there are correct formulas in node 1
    assert l.Graphs[1].node[1] == [('diamond', 'q')]
    assert l.Graphs[0].node[1] == [('box', 'p')]

#beta,gamma and delta formulas tested
@pytest.mark.graph
def test_graph_form4():
    l.Graphs = []
    Sets = []
    formulas_in = {}
    formulas_in[1] = []
    G = nx.MultiDiGraph()
    str_psi = "(Bp > (Dq ^ Bt))"
    psi = syntax.parse_formula(SET, str_psi)
    Sets.append(sols.recursivealpha(psi))
    gr.create_graph_K(G,Sets)
    l.Graphs.append(G)
    #apply beta expansion
    l.beta_node_solve(G, 1 ,formulas_in)
    l.delta_node_solve(l.Graphs[0],1,formulas_in)
    l.delta_node_solve(l.Graphs[1],1,formulas_in)
    #check if there are 2 graphs
    assert len(l.Graphs) == 2
    #check node 1 of graph 1 and graph 2
    assert l.Graphs[0].node[1] == [('not',('box', 'p'))]
    assert l.Graphs[1].node[1] == [('diamond', 'q'),('box','t')]
    #check node 2 of graph 1
    assert l.Graphs[0].node[2] == [('not', 'p')]
    #check node 2 of graph 2
    assert l.Graphs[1].node[2] == ['q','t']

@pytest.mark.consist
# False- consistent True- inconsistent
def test_consistent_form1():
    answer = True
    psi = [('and','p', 'q'), ('not', 'q'), 'p']
    result = sols.inconsistent(psi)
    assert answer == result

@pytest.mark.consist
def test_consistent_form2():
    answer = True
    psi = [('not',('or','q', 'p')),  'p']
    result = sols.inconsistent(psi)
    assert answer == result

@pytest.mark.consist
def test_consistent_form3():
    answer = True
    psi = [('not',('imply', 'p', ('not','q'))), ('not','q')]
    result = sols.inconsistent(psi)
    assert answer == result


@pytest.mark.consist
def test_consistent_form4():
    answer = False
    psi = [('not',('or', ('not','p'), 'q')), ('not',('imply','p','q'))]
    result = sols.inconsistent(psi)
    assert answer == result

