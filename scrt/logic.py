import scrt.satsolver

class LogicalExpressionBase:
    def __eq__(self, other):
        return type(self) == type(other)

    def __rshift__(self, other):
        return LogicalImplies(self, other)

    def __lshift__(self, other):
        return LogicalImplies(other, self)

    def __and__(self, other):
        return LogicalAnd(self, other)

    def __or__(self, other):
        return LogicalOr(self, other)

    def __invert__(self):
        return LogicalNot(self)

    def solve(self, external_solver=None):
        return scrt.satsolver.SatSolver.solve(self, external_solver)


class LogicalAtom(LogicalExpressionBase):
    def __init__(self, name=""):
        if name == "":
            raise Exception('A logical atom requires name')
        self.name = name

    def __eq__(self, other):
        return super().__eq__(other) and self.name == other.name

    def __str__(self):
        return self.name


class LogicalAnd(LogicalExpressionBase):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return super().__eq__(other) and ((self.left == other.left and self.right == other.right) or (self.left == other.right and self.right == other.left))

    def __str__(self):
        return "(" + str(self.left) + "&" + str(self.right) + ")"

class LogicalOr(LogicalExpressionBase):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return super().__eq__(other) and ((self.left == other.left and self.right == other.right) or (self.left == other.right and self.right == other.left))

    def __str__(self):
        return "(" + str(self.left) + "|" + str(self.right) + ")"

class LogicalImplies(LogicalExpressionBase):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return super().__eq__(other) and (self.left == other.left and self.right == other.right)

    def __str__(self):
        return "(" + str(self.left) + ">>" + str(self.right) + ")"

class LogicalNot(LogicalExpressionBase):
    def __init__(self, target):
        self.target = target

    def __eq__(self, other):
        return super().__eq__(other) and self.target == other.target

    def __str__(self):
        return "(~"+str(self.target)+")"
