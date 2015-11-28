# Auther: Marcin Cuber
# All rights reserved
__author__ = 'marcincuber'
import syntax
''' deals with intersection: 'and'
    return p1, p2 and removes 'and'
    input.py [('and','p1','p2')]
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
    using list as an input.py
    input.py ~(p1 -> p2)
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
    using list as an input.py
    input.py ~(~(p))
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
        #print "first part= ", psi[0]
        #print "second part= ", psi[1]

        psi1 = (psi[1][1])
        psi1_set = [psi1]
        if psi[1][1][0] in parsed_constants or psi[1][1][0] in parsed_modalities:
            psi1_set = recursivealpha(psi1)

        psi2_set = [('not',psi[1][2])]
        #print "here this first: ", (psi1_set + psi2_set), psi[1][2], psi2_set
        if isinstance(psi[1][2], str):
            psi2_set = [('not',psi[1][2])]
        elif psi[1][2][0] in parsed_constants or psi[1][2][0] in parsed_modalities:
            #print "here we are taking this:", recursivealpha(('not',psi[1][2]))
            psi2_set = recursivealpha(('not',psi[1][2]))

            #print "here this second: ", (psi1_set + psi2_set), psi[1][2], psi2_set
        return (psi1_set + psi2_set)
    #elif psi[0] == 'not' and psi[1][0] == 'diamond' and psi[1][0][0] == 'not':
    #    psi1_set = ('box',[1][0][1])
    #    return psi1_set
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

def recursivealpha2(psi):
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
        #print "first part= ", psi[0]
        #print "second part= ", psi[1]

        psi1 = (psi[1][1])
        psi1_set = [psi1]
        if psi[1][1][0] in parsed_constants or psi[1][1][0] in parsed_modalities:
            psi1_set = recursivealpha(psi1)

        psi2_set = [('not',psi[1][2])]
        #print "here this first: ", (psi1_set + psi2_set), psi[1][2], psi2_set

        if psi[1][2][0] in parsed_constants or psi[1][2][0] in parsed_modalities:
            #print "here we are taking this:", recursivealpha(('not',psi[1][2]))
            psi2_set = recursivealpha(('not',psi[1][2]))

            #print "here this second: ", (psi1_set + psi2_set), psi[1][2], psi2_set
        return psi1_set + psi2_set
    #elif psi[0] == 'not' and psi[1][0] == 'diamond' and psi[1][0][0] == 'not':
    #    psi1_set = ('box',[1][0][1])
    #    return psi1_set
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
        return psi

'''
    :Function finds and removes inconsistent formulas from the list
'''
def inconsistent(psi):
    status = False;
    index = []
    main_list=psi
    for i in range(0,len(psi)):
        for j in range(0,len(psi[i])):
            main = psi[i]
            form = psi[i][j]
            if isinstance(main, str):
                contra = ('not',main)
                if (contra in main_list) and (main in main_list):
                    status = True
                    break
                else:
                    status = False
            elif main[0] == 'not' and main[1][0] == 'or' and isinstance(main[1][1][0], str):
                part = main[1][1][0]
                contra = ('not',part)
                if (contra in main_list) and (part in main_list):
                    status = True
                    break
                else:
                    status = False
            elif main[0] == 'not' and main[1][0] == 'or' and isinstance(main[1][1][1], str):
                part = main[1][1][1]
                contra = ('not',part)
                if (contra in main_list) and (part in main_list):
                    status = True
                    break
                else:
                    status = False

            elif main[0] == 'not' and main[1][0] == 'and' and isinstance(main[1][1][0], str) and isinstance(main[1][1][1], str):
                part1 = main[1][1][0]
                part2 = main[1][1][1]
                contra1 = ('not',part1)
                contra2 = ('not',part2)
                if ((contra1 in main_list) and (part1 in main_list)) or ((contra2 in main_list) and (part2 in main_list)):
                    status = True
                    break
                else:
                    status = False

            elif main[0] == 'not' and main[1][0] == 'imply' and ((isinstance(main[1][1][0], str) or (isinstance(main[1][1][1], str)))):
                part1 = main[1][1][0]
                part2 = main[1][1][1]
                #print "part1:, ", part1, "part2: ", part2
                contra1 = ('not',part1)
                contra2 = ('not',part2)
                if (contra1 in main_list) or (part2 in main_list):
                    status = True
                    break
                else:
                    status = False

    return status