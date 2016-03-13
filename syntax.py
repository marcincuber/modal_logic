__author__ = 'marcincuber'
# -*- coding: utf-8 -*-
ascii_setup =    [{'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'},
                    # false, not, or, and, imply
                    ['F','~', 'V', '^', '>'],
                    # diamond, box
                    ('D', 'B'),
                    {('(',')'), ('[',']'), ('{','}')}
                   ]

'''
    :General class for modal language
    :we will deal with the following:
    :set of propositions {a,b,...,z}
    :list of constants
    :modal operators and its duals
    :pairs of brackets
'''
class Language:

    def __init__(self, prop = None,
                       constants = None,
                       modality = None,
                       brackets = None):
        if prop == None:
            prop = ascii_setup[0]
        self.prop = prop
        if constants == None:
            constants = ascii_setup[1]
        self.constants = constants
        if modality == None:
            modality = ascii_setup[2]
        self.modality = modality
        if brackets == None:
            brackets = ascii_setup[3]
        self.brackets = brackets


    def __getitem__(self, symbol):

        parsed_constants = ['false', 'not', 'or', 'and', 'imply']
        parsed_modalities = ['diamond', 'box']

        if symbol in self.prop:
            return symbol
        elif symbol in self.constants:
            return parsed_constants[self.constants.index(symbol)]
        elif symbol in self.modality:
            return parsed_modalities[self.modality.index(symbol)]
        else:
            return None

    def __repr__(self):
        return ('language' + '(' + str(self.prop) + ', ' +
                str(self.constants) + ', ' +
                str(self.modality) + ', ' +
                str(self.brackets) + ')')

def parse_formula(L, formula):
    return tuple_tableau(list_tableau(L, formula))

'''
    :Input: formula as a string and turns it into tableau form for easier parsing and evaluation
'''
def list_tableau(L, formula):

    # Remove whitespace
    formula = ''.join(formula.split())
    tableau = []

    # if formula is atomic return it
    if len(formula) == 1:
        if formula in L.prop:
            return L[formula]
        else:
            raise ValueError("Proposition should be in place!")

    # Deal with formula by splitting it and generating subformulas.
    partition = [[]]
    bracket_list = []
    i = 0 #Index of current subformula.
    for part in formula:
        partition[i].append(part)
        if part in {pair[0] for pair in L.brackets}:
            bracket_list.append(part)
        elif part in {pair[1] for pair in L.brackets}:
            if not (bracket_list[-1], part) in L.brackets:
                raise ValueError("brackets are not matching up!")
            bracket_list.pop()
            # check if the bracket removed was the last one, if yes- end of subformula
            if bracket_list == []:
                i = i + 1
                partition.append([])
        elif bracket_list == []:
        # If we have an empty list of brackets we only deal with propositions
            if ((part == L[0]) or # ch is bottom
               part in L.prop or
               part in L.constants[2:]): # ch is a 2-place constant
                i = i + 1
                partition.append([])
    partition = partition[:-1]

    # Delete outer brackets otherwise unary connector is the main connector.
    if len(partition) == 1:
        if (partition[0][0], partition[0][-1]) in L.brackets:
            tableau = parse_formula(L, formula[1:-1])
        elif partition[0][0] == L.constants[1] or partition[0][0] in L.modality:
        # partition[0][0] is in first place- neg or modality
            tableau = [L[partition[0][0]], parse_formula(L, formula[1:])]
        else:
            raise ValueError("Not possible to partition formula")
    # If we get main connector we add it to tablueau and parse the rest ofsubformulas
    else:
        for sub in partition:
            if (len(sub) == 1 and
                sub[0] in {const for const in (L.constants)}):
                tableau = [L[sub[0]]] + \
                          [parse_formula(L, ''.join(form)) \
                          for form in partition if not form[0] == sub[0]]
    return tableau

'''
    :Convert formula to tuples
'''
def tuple_tableau(format):
    if type(format) == list:
        return tuple(tuple_tableau(sub) for sub in format)
    elif type(format) == str or type(format) == tuple:
        return format
    else:
        print(format)
        raise ValueError("Error, formulas couldn't be converted to tuples")

'''
    :Return the set of all subformulas of f.
'''
def get_subformulas(formula):
    subformulas = {formula}
    if len(formula) > 1:
        # Take 1st operand when connector is unary
        subformulas = subformulas.union(get_subformulas(formula[1]))
    if len(formula) == 3:
        # Take 2nd operand when we have binary operator
        subformulas = subformulas.union(get_subformulas(formula[2]))
    return subformulas

'''
    Close fset under subformulas.
'''
def subformula_close(formula_set):
    closed_fset = set()
    for f in formula_set:
        closed_fset = closed_fset.union(get_subformulas(f))
    return closed_fset

'''
    :Turn a input formula (list) into a string format
'''
def formula_to_string(formula):

    if len(formula) == 1:
        # The formula is atomic.
        string = formula[0]
    else:
        # handling unary operators
        if len(formula) == 2:
            if formula[0] == 'box':
                string = '[]'
            elif formula[0] == 'diamond':
                string = '<>'
            else:
                string = '~'
        else:
            string = ''

        # Deal with 1st operand
        if len(formula[1]) < 3:
            string += formula_to_string(formula[1])
        else:
            string += '(' + formula_to_string(formula[1]) + ')'

        # Deal with rest of formula when connector is binary
        if len(formula) == 3:
            # Handle operators
            if formula[0] == 'and':
                string += ' ^ '
            elif formula[0] == 'or':
                string += ' V '
            elif formula[0] == 'imply':
                string += ' -> '
            elif formula[0] == 'box':
                string += ' [] '
            elif formula[0] == 'diamond':
                string+= ' <> '

            # Deal with 2nd operand
            if len(formula[2]) < 3:
                string += formula_to_string(formula[2])
            else:
                string += '(' + formula_to_string(formula[2]) + ')'
    return string
