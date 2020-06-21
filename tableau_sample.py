from scrt.logic import LogicalAtom
from scrt.tableau_solver import TableauSolver

p = LogicalAtom('p')
q = LogicalAtom('q')
r = LogicalAtom('r')
s = LogicalAtom('s')


expr = (~p) & (p | q) & (p | ~r | s) & (~q | r | s) & (p | ~q | r | s)

result = TableauSolver.solve(expr, graphviz=True)
print(result)
