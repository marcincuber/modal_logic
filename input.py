# Auther: Marcin Cuber
# All rights reserved
'''
    To input correctly formula
    :Legend:
        AND is represented by the symbol:                ^
        OR is represented by the symbol:                 V
        IMPLICATION is represented by the symbol:        >
        BOX (must) is represented by the symbol:         #
        DIAMOND (possibly) is represented by the symbol: @

    :Example input:
        str_psi = "~(p > #r) ^  (@p >((@@@s^#t) V (#s ^ @q))) "

        which can be easier visualised as
        ~(p -> []r) ^ (<>p -> ((<><><>s ^ []t) V ([]s ^ <>q)))
    :After writting a formula run input.py and it will bring the results
    :Do no change the name of the string (str_psi)
'''

'''
    :input string
'''
str_psi = "~(p > #r) ^  (@p >((@@@s^#t) V (#s ^ @q))) "



'''
    :function that passes the input.py string to the executing file
'''
def receive():
    send_string = str_psi
    return send_string
execfile('main_run.py')

