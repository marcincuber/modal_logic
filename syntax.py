# Auther: Marcin Cuber
# All rights reserved
# -*- coding: utf-8 -*-
default_ascii =    [{'p','q','r','s','t','u','v','w','x'},
                    # false, not, or, and, imply
                    ['F', '~', 'V', '^', '>'],
                    # diamond, box
                    ('@', '#'),
                    {('(',')'), ('[',']'), ('{','}')}
                   ]


class Language:
    """
    :modal language consists of:
    :-a set of propositions (one character strings)
    :-a list of constants (list position determines iterpretation)
    :-a modal operator and it's dual (a pair)
    :-a a set of pairs of opening and closing brackets
    """
    def __init__(self, prop = None,
                       constants = None,
                       modality = None,
                       brackets = None):
        if prop == None:
            prop = default_ascii[0]
        self.prop = prop
        if constants == None:
            constants = default_ascii[1]
        self.constants = constants
        if modality == None:
            modality = default_ascii[2]
        self.modality = modality
        if brackets == None:
            brackets = default_ascii[3]
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

def list_tableau(L, formula):
    '''
        :Takes a formula as a string and gives it a tableau form for
        :easier parsing by other functions (e.g. valuation, satisfaction).
    '''

    # Remove whitespace from the formula.
    formula = ''.join(formula.split())
    tableau = []

    # If it's atomic, return.
    if len(formula) == 1:
        if formula in L.prop:
            return L[formula]
        else: raise ValueError("unexpected character; expected a proposition")

    # First partition by subformulas.
    partition = [[]]
    bracket_stack = []
    i = 0 # Index of current subformula/partition.
    for ch in formula:
        partition[i].append(ch)
        if ch in {pair[0] for pair in L.brackets}:
            bracket_stack.append(ch)
        elif ch in {pair[1] for pair in L.brackets}:
            if not (bracket_stack[-1], ch) in L.brackets:
                raise ValueError("mismatched brackets")
            bracket_stack.pop()
            # If the bracket we just popped was the last in the stack,
            # then we are at the end of a subformula.
            if bracket_stack == []:
                i = i + 1
                partition.append([])
        elif bracket_stack == []:
        # If the bracket stack is empty, propositions and 0-place
        # logical constants are get theirl lown partitiony.
        # Likewise for constants of arity >2; they deliminate subformulas.
            if ((ch == L[0]) or # ch is bottom
               ch in L.prop or
               ch in L.constants[2:]): # ch is a 2-place constant
                i = i + 1
                partition.append([])
    partition = partition[:-1]

    # Either we need to remove outter brackets, or a unary operator is
    # the main connective.
    if len(partition) == 1:
        if (partition[0][0], partition[0][-1]) in L.brackets:
            tableau = parse_formula(L, formula[1:-1])
        elif partition[0][0] == L.constants[1] or partition[0][0] in L.modality:
        # partition[0][0] is 1-place (not or a modality)
            tableau = [L[partition[0][0]], parse_formula(L, formula[1:])]
        else:
            raise ValueError("can not partition formula")
    # One of the partitions should be the main connective. Find it,
    # add it to the tableau, and parse the remaning subformulas
    else:
        for sub in partition:
            if (len(sub) == 1 and
                sub[0] in {const for const in (L.constants)}):
                tableau = [L[sub[0]]] + \
                          [parse_formula(L, ''.join(form)) \
                          for form in partition if not form[0] == sub[0]]

    return tableau

def tuple_tableau(form):
    if type(form) == list:
        return tuple(tuple_tableau(sub) for sub in form)
    elif type(form) == str or type(form) == tuple:
        return form
    else:
        print(form)
        raise ValueError("error converting formula list to tuples:")

def get_subformulas(f):
    '''
        :Return the set of all subformulas of f.
    '''

    subforms = {f}
    if len(f) > 1:
        # f has a unary or binary operator: get first operand.
        subforms = subforms.union(get_subformulas(f[1]))
    if len(f) == 3:
        # f has a binary operator: get second operand.
        subforms = subforms.union(get_subformulas(f[2]))
    return subforms

def subformula_close(fset):
    """
    Close fset under subformulas.
    """

    closed_fset = set()
    for f in fset:
        closed_fset = closed_fset.union(get_subformulas(f))
    return closed_fset

def formula_to_string(formula):
    """
    Convert a formula in list format to a string.
    """

    if len(formula) == 1:
        # The formula is atomic.
        string = formula[0]
    else:
        # If the main operator is unary, handle it.

        if len(formula) == 2:
            if formula[0] == 'box':
                string = '[]'
            elif formula[0] == 'diamond':
                string = '<>'
            else:
                string = '~'
        else:
            string = ''

        # Handle the first (and possibly only) operand.
        if len(formula[1]) < 3:
            string += formula_to_string(formula[1])
        else:
            string += '(' + formula_to_string(formula[1]) + ')'

        # If the main operator is binary, handle the remainder of the formula.
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

            # Handle the second operand.
            if len(formula[2]) < 3:
                string += formula_to_string(formula[2])
            else:
                string += '(' + formula_to_string(formula[2]) + ')'

    return string
