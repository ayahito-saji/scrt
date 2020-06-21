from scrt.logic import LogicalAtom
from scrt.tableau_solver import TableauSolver

A = LogicalAtom('A')
B = LogicalAtom('B')
C = LogicalAtom('C')
D = LogicalAtom('D')
E = LogicalAtom('E')

expr = (A & C & B & ~B)

result = TableauSolver.solve(expr)
print(result)
