from scrt.logic import LogicalAtom

p = LogicalAtom('p')
q = LogicalAtom('q')

expr = p & ~p

print(expr)
satisfiable, allocation = expr.solve()
print(satisfiable, allocation)
