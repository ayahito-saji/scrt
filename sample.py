from scrt.logic import LogicalAtom

p = LogicalAtom('p')
q = LogicalAtom('q')

expr = p & q

print(expr)
satisfiable, allocation = expr.solve(external_solver='minisat')
