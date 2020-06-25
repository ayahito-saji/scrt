from scrt.logic import LogicalAtom
from scrt.tableau_solver import TableauSolver

p = LogicalAtom('p')
q = LogicalAtom('q')

expr = ~(((p | q) & ~p) >> q)
result = TableauSolver.solve(expr, graphviz=True, graph_filename='tableau')
print(result)
