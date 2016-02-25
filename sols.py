__author__ = 'marcincuber'
# -*- coding: utf-8 -*-
'''
    :psi is our parsed formula in tableaux format
    :for each formula in the list deal with all alphas formulas
    :return a list which does not contain any alpas to deal with
'''
def recursivealpha(psi):
    #define constants and modalities
    parsed_constants = ['or', 'and', 'imply', 'not']
    parsed_modalities = ['diamond', 'box']

    #deal with formulas which have AND in the first position
    #scan formulas recursiverly until all formulas are dealt with
    if psi[0] == 'and':
        psi1_set = [psi[1]]
        if psi[1][0] in parsed_constants or psi[1][0] in parsed_modalities:
            psi1_set = recursivealpha(psi[1])

        psi2_set = [psi[2]]
        if psi[2][0] in parsed_constants or psi[2][0] in parsed_modalities:
            psi2_set = recursivealpha(psi[2])

        return psi1_set + psi2_set

    #deal with formulas which contain double negations
    elif psi[0] == 'not' and isinstance(psi[1], tuple) and psi[1][0] == 'not':
        result = [psi[1][1]]
        if psi[1][1][0] in parsed_constants or psi[1][1][0] in parsed_modalities:
            result = recursivealpha(psi[1][1])

        return result

    #deal with formulas with NOT(IMPLY,A,B) in which we return negated B and A
    elif psi[0] == 'not' and isinstance(psi[1], tuple) and psi[1][0] == 'imply':
        psi1 = (psi[1][1])
        psi1_set = [psi1]
        if psi[1][1][0] in parsed_constants or psi[1][1][0] in parsed_modalities:
            psi1_set = recursivealpha(psi1)

        psi2_set = [('not',psi[1][2])]
        if isinstance(psi[1][2], str):
            psi2_set = [('not',psi[1][2])]
        elif psi[1][2][0] in parsed_constants or psi[1][2][0] in parsed_modalities:
            psi2_set = recursivealpha(('not',psi[1][2]))

        return (psi1_set + psi2_set)

    #deal with formulas with NOT(OR,A,B) in which we return negated B and negated A
    elif psi[0] == 'not' and isinstance(psi[1], tuple) and psi[1][0] == 'or':
        psi1 = ('not', psi[1][1])
        psi1_set = ['not',psi[1][1]]
        if psi[1][1][0] in parsed_constants or psi[1][1][0] in parsed_modalities:
            psi1_set = recursivealpha(psi1)

        psi2 = ('not', psi[1][2])
        psi2_set = [('not', psi[1][2])]
        if psi[1][2][0] in parsed_constants or psi[1][2][0] in parsed_modalities:
            psi2_set = recursivealpha(psi2)

        return psi1_set + psi2_set

    #if there are formulas which are not alphas, just add them to the list
    else:
        return [psi]

'''
    :Function finds and removes inconsistent formulas from the list
'''
def inconsistent(psi):
    #initialise status to be false psi meaning that psi is consistent
    status = False;
    main_list=psi
    for i in range(0,len(psi)):
        for j in range(0,len(psi[i])):
            #we assign each formula from the list to a variable main
            main = psi[i]

            if isinstance(main, str):
                contra = ('not',main)
                if (contra in main_list) and (main in main_list):
                    status = True
                    break

            elif main[0] == 'not' and main[1][0] == 'or' and isinstance(main[1][1][0], str):
                part = main[1][1][0]
                contra = ('not',part)
                if (contra in main_list) and (part in main_list):
                    status = True
                    break

            elif main[0] == 'not' and main[1][0] == 'or' and isinstance(main[1][1][1], str):
                part = main[1][1][1]
                contra = ('not',part)
                if (contra in main_list) and (part in main_list):
                    status = True
                    break
            elif main[0] == 'imply' and isinstance(main[1][0], str):
                prop = main[1][0]
                if (prop in main_list):
                    status = True
                    break

            elif main[0] == 'imply' and isinstance(main[1][1], str):
                prop = main[1][1]
                contra = ('not', prop)
                if (contra in main_list):
                    status = True
                    break
    return status

