from scrt.predicate_logic import Constant, Variable, All, Exists, Function, Predicate

Tuna = Constant("Tuna")
Jack = Constant("Jack")
Curiosity = Constant("Curiosity")

x = Variable("x")
y = Variable("y")
z = Variable("z")

Cat = Predicate("Cat")
Animal= Predicate("Animal")
Loves = Predicate("Loves", arity=2)
Kills = Predicate("Kills", arity=2)

print(All(x, All(y, Animal(y) >> Loves(x, y)) >> Exists(z, Loves(z, x))))
print(All(x, Exists(y, Animal(y) & Kills(x, y)) >> All(z, Loves(z, x))))
print(All(x, Animal(x) >> Loves(Jack, x)))
print(Kills(Jack, Tuna) | Kills(Curiosity, Tuna))
print(Cat(Tuna))
print(All(x, Cat(x) >> Animal(x)))

print(Kills(Curiosity, Tuna))
