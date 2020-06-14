from scrt.logic import LogicalAtom
from scrt.satsolver import SatSolver

p = LogicalAtom('p')
q = LogicalAtom('q')

expr = (p >> q) & p

print(expr)
result, allocation = SatSolver.solve(expr)
print(result, allocation)
