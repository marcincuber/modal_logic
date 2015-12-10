# Auther: Marcin Cuber
# All rights reserved
__author__ = 'marcincuber'
import syntax

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

    elif psi[0] == 'not' and isinstance(psi[1], tuple) and psi[1][0] == 'or':
        #print psi[0]
        #print psi[1]

        psi1 = ('not', psi[1][1])
        psi1_set = ['not',psi[1][1]]
        if psi[1][1][0] in parsed_constants or psi[1][1][0] in parsed_modalities:
            psi1_set = recursivealpha(psi1)

        psi2 = ('not', psi[1][2])
        psi2_set = [('not', psi[1][2])]
        if psi[1][2][0] in parsed_constants or psi[1][2][0] in parsed_modalities:
            psi2_set = recursivealpha(psi2)
        print "psi1_set + psi2_set", psi1_set + psi2_set
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

    elif psi[0] == 'not' and isinstance(psi[1], tuple) and psi[1][0] == 'or':
        #print psi[0]
        #print psi[1]

        psi1 = ('not', psi[1][1])
        psi1_set = [('not',psi[1][1])]
        if psi[1][1][0] in parsed_constants or psi[1][1][0] in parsed_modalities:
            psi1_set = recursivealpha(psi1)

        psi2 = ('not', psi[1][2])
        psi2_set = [('not',psi[1][2])]
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

