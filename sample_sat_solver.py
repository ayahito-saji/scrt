from scrt.sat_solver import SatSolver

p = SatSolver.atom('p')
q = SatSolver.atom('q')

KB = p >> q
Q = q

print(SatSolver.ask(KB, Q))
