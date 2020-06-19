from scrt.predicate_logic import Constant, Variable, All, Exists, Function, Predicate
from scrt.predicate_solver import PredicateSolver

Tuna = Constant("Tuna")
Jack = Constant("Jack")
Curiosity = Constant("Curiosity")

a = Constant("a")
b = Constant("b")

w = Variable("w")
x = Variable("x")
y = Variable("y")
z = Variable("z")

Cat = Predicate("Cat")
Animal = Predicate("Animal")
Loves = Predicate("Loves", arity=2)
Kills = Predicate("Kills", arity=2)

fol_expr = All(x, All(y, Animal(y) >> Loves(x, y)) >> Exists(z, Loves(z, x)))
fol_expr = All(z, Exists(y, Exists(x, Cat(y) & Cat(x)) >> Cat(x)))
print(PredicateSolver.normalize(fol_expr))
print(fol_expr)
# print(All(x, Exists(y, Animal(y) & Kills(x, y)) >> All(z, Loves(z, x))))
# print(All(x, Animal(x) >> Loves(Jack, x)))
# print(Kills(Jack, Tuna) | Kills(Curiosity, Tuna))
# print(Cat(Tuna))
# print(All(x, Cat(x) >> Animal(x)))

# print(Kills(Curiosity, Tuna))

P = Predicate("P", arity=2)
Q = Predicate("Q", arity=1)
R = Predicate("R", arity=1)

# fol_expr = (Exists(x, P(x)) >> ~(All(x, Q(x, y) | ~All(y, P(y))))) & R(x)
# fol_expr = Exists(x, All(y, All(z, Exists(w, P(x, y, z, w)))))
fol_expr = Exists(x, P(x, y) >> Q(a))
print(fol_expr)
print(PredicateSolver.normalize(fol_expr))
