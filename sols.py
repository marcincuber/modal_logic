__author__ = 'marcincuber'
import syntax
''' deals with intersection: 'and'
    return p1, p2 and removes 'and'
    input [('and','p1','p2')]
    outputs [('p1','p2')]
    alpha formulae
'''
def intersection(tab):
    newtab=[]
    if tab[0] == "and":
        formula1 = tab[1]
        formula2 = tab[2]
        newtab.append(formula1)
        newtab.append(formula2)
    return newtab;

''' deals with negated implication
    using list as an input
    input ~(p1 -> p2)
    outputs [('not','p1'),'q2']
    alpha formulae
'''
def imply2inter(tab):
    newtab = []
    part = tab[1]
    listnot = []
    if tab[0] == "not" and part[0] == "imply":
        formula1 = part[1]
        formula2 = part[2]
        listnot.append('not')
        listnot.append(formula1)
        listnot = tuple(listnot)
        newtab.append(listnot)
        newtab.append(formula2)
    return newtab;

''' dealing with double negation
    using list as an input
    input ~(~(p))
    outputs p
'''

def negation(tab):
    newtab=[]
    part = tab[1]
    if tab[0] == "not" and part[0] == "not":
        formula1 = part[1]
        newtab.append(formula1)
    return newtab
'''removing all double negetation in the formula
'''
def allnegation(tab):
    tableau = []
    for x in range(0, len(tab)):
        if len(tab[x]) > 1:
            #print ("length is: ", len(tab[x]),"at position ", x , "and the value is: ", tab[x])
            if tab[0] == 'not':
                part = negation(tab[x])
            #part = str(part).replace('[','').replace(']','')
                #print "we have this part :", part
    return tableau;

def recursivealpha(psi):
    parsed_constants = ['or', 'and', 'imply', 'not']
    parsed_modalities = ['diamond', 'box']

    # print "Hallo " + str(psi) + " len " + str(len(psi))

    # if psi[0] == 'or':
    #     psi1_set = [psi[1]]
    #     if psi[1] in parsed_constants or psi[1] in parsed_modalities:
    #         psi1_set = recursivealpha(psi[1])
    #
    #     psi2_set = [psi[2]]
    #     if psi[2] in parsed_constants or psi[2] in parsed_modalities:
    #         psi2_set = recursivealpha(psi[2])
    #
    #     return psi1_set + psi2_set

    #print psi[0]
    #print psi[1]

    if psi[0] == 'and':
        psi1_set = [psi[1]]
        if psi[1][0] in parsed_constants or psi[1][0] in parsed_modalities:
            psi1_set = recursivealpha(psi[1])

        psi2_set = [psi[2]]
        if psi[2][0] in parsed_constants or psi[2][0] in parsed_modalities:
            psi2_set = recursivealpha(psi[2])

        # result = []

        # for psi1 in psi1_set:
        #     for psi2 in psi2_set:
        #         result.append(psi1 + psi2)

        return psi1_set + psi2_set

    # elif psi[0] == 'imply':

    elif psi[0] == 'not' and isinstance(psi[1], tuple) and psi[1][0] == 'not':
        #print psi[0]
        #print psi[1]
        result = [psi[1][1]]
        if psi[1][1][0] in parsed_constants or psi[1][1][0] in parsed_modalities:
            result = recursivealpha(psi[1][1])

        return result

    elif psi[0] == 'not' and isinstance(psi[1], tuple) and psi[1][0] == 'imply':
        #print psi[0]
        #print psi[1]

        psi1 = (psi[1][1])
        psi1_set = [psi1]
        if psi[1][1][0] in parsed_constants or psi[1][1][0] in parsed_modalities:
            psi1_set = recursivealpha(psi1)

        psi2_set = ['not',psi[1][2]]
        if psi[1][2][0] in parsed_constants or psi[1][2][0] in parsed_modalities:
            psi2_set = recursivealpha(psi[1][2])

        return psi1_set + psi2_set

    elif psi[0] == 'not' and isinstance(psi[1], tuple) and psi[1][0] == 'or':
        #print psi[0]
        #print psi[1]

        psi1 = ('not', psi[1][1])
        psi1_set = [psi[1][1]]
        if psi[1][1][0] in parsed_constants or psi[1][1][0] in parsed_modalities:
            psi1_set = recursivealpha(psi1)

        psi2 = ('not', psi[1][2])
        psi2_set = [psi[1][2]]
        if psi[1][2][0] in parsed_constants or psi[1][2][0] in parsed_modalities:
            psi2_set = recursivealpha(psi2)

        return psi1_set + psi2_set

    else:
        return [psi]

'''
    :Function finds and removes inconsistent formulas from the list
'''
def inconsistent(psi):
    index = []
    main_list=psi
    for i in range(0,len(psi)):
        for j in range(0,len(psi[i])):
            main = psi[i]
            form = psi[i][j]
            if form[0] == 'not':
                notform = form[1]
                if form and notform in main:
                    #print "inconsistent: ", psi[i][j]
                    #print "following sublist : ", main, " is inconsistent at index: ", i, " of main Set"
                    index.append(i)
                    break
            else:
                notform = ('not', psi[i][j])
                if form and notform in main:
                    #print "inconsistent: ", psi[i][j]
                    #print "following sublist : ", main, " is inconsistent at index: ", i, " of main Set"
                    index.append(i)
                    break
                #else:
                #    print "consistent: ", psi[i][j]

    '''
        :removing lists from main list using index values
        :index corresponds to inconsistent list
        :we scan them in reverse order so that we can delete them without shifting lists
    '''
    for i in reversed(index):
        main_list.pop(i);

    return main_list