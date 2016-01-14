# Author: Marcin Cuber
# All rights reserved
This is a Propositional Modal Logic solver for following logics:

K: has been completed - Logic_K.py can be used to test formulas
    no properties
T: completed - Logic_T.py
    reflexive   []p -> p
KB: Logic_Symmetric- almost completed
    symmetric   p -> []<>p
B: not started
    symmetric and reflexive
S4: not started
    reflexive and transitive    []p -> [][]p
S5: not started
    reflexive, transitive and symmetric
    S4 + <>p ->[]<>p
S4.3: not started
    same as S4 but additionally linear



How to use:
    1. Download all the .py files
    2. Place them in one folder
    3. Open Logic_?.py with python interpreter where ? corresponds to logic
    4. Read some simple instructions in input.py
    5. Input your formula
    6. Run, test and get results
    7. And graphs (valid models)

I have used tableaux method to derive the solutions.


No copying or reusing of applications is allowed!!!