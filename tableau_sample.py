from scrt.logic import LogicalAtom
from scrt.tableau_solver import TableauSolver

p = LogicalAtom('p')
q = LogicalAtom('q')

expr = (p >> q) & p

print(expr)
result, allocation = TableauSolver.solve(expr)
print(result, allocation)
