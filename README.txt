# Author: Marcin Cuber
# All rights reserved
These are Propositional Modal Logic solvers. I have used tableaux method to derive solutions. We have following logics covered:

K:  completed - Logic_K.py
    no properties

T:  completed - Logic_T.py
    reflexive   []p -> p

K4: completed- Logic_K4.py
    transitive frames

KB: completed - Logic_KB.py
    symmetric   p -> []<>p

B:  completed - Logic_B.py
    symmetric and reflexive

S4: completed - Logic_S4.py
    reflexive and transitive    []p -> [][]p

S5: completed - Logic_S5.py
    reflexive, transitive and symmetric
    S4 + <>p ->[]<>p

How to use:
    1. Download all the .py files
    2. Place them in one folder
    3. Open Logic_?.py with python interpreter where ? corresponds to logic
    4. Using instructions below write formula
    5. Input your formula inside specific file str_psi = "formula"
    6. Run, test and get results
    7. Each graph corresponds to a Kripke model in which the formula is satisfiable

Formula input instructions:
    To input correctly formula
    :Legend:
        AND is represented by the symbol:                ^
        OR is represented by the symbol:                 V
        IMPLICATION is represented by the symbol:        >
        BOX (must) is represented by the symbol:         B
        DIAMOND (possibly) is represented by the symbol: D

    :Example input:
        str_psi = "~(p > Br) ^  (Dp >((DDDs^Bt) V (Bs ^ Dq))) "

        which can be easier visualised as
        ~(p -> []r) ^ (<>p -> ((<><><>s ^ []t) V ([]s ^ <>q)))
    :After writting a formula run Logic_?.py and it will bring the results
    :Do no change the name of the string (str_psi)

No copying of the applications allowed without consent!