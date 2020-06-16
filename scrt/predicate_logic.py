import scrt.logic


class Constant:
    def __init__(self, name=""):
        if name == "":
            raise Exception("A predicate logical constant requires name")
        self.name = name

    def __str__(self):
        return self.name


class Variable:
    def __init__(self, name=""):
        if name == "":
            raise Exception("A predicate logical variable requires name")
        self.name = name

    def __str__(self):
        return self.name


class Function:
    def __init__(self, name="", arity=1, str='formal'):
        if name == "":
            raise Exception("A predicate logical function requires name")
        self.name = name
        self.arity = arity
        self.str = str

    def __call__(self, *args):
        if len(args) != self.arity:
            raise Exception("Number of arguments don't match arity of function (arity: " + str(self.arity) + ")")
        return FunctionCall(self, args)

    def __str__(self):
        return self.name


class FunctionCall:
    def __init__(self, function=None, args=None):
        self.function = function
        self.args = args

    def __str__(self):
        if self.function.str == "formal":
            return self.function.name + "(" + ",".join([str(arg) for arg in self.args]) + ")"
        elif self.function.str == "natural":
            val = self.function.name
            for arg in self.args:
                val.replace('*', str(arg))
            return "("+val+")"


class Predicate:
    def __init__(self, name="", arity=1, str='formal'):
        if name == "":
            raise Exception("A predicate logical predicate requires name")
        self.name = name
        self.arity = arity
        self.str = str

    def __call__(self, *args):
        if len(args) != self.arity:
            raise Exception("Number of arguments don't match arity of function (arity: " + str(self.arity) + ")")
        return PredicateCall(self, args)

    def __str__(self):
        return self.name


class PredicateCall(scrt.logic.LogicalExpressionBase):
    def __init__(self, predicate=None, args=None):
        self.predicate = predicate
        self.args = args

    def __str__(self):
        if self.predicate.str == "formal":
            return self.predicate.name + "(" + ",".join([str(arg) for arg in self.args]) + ")"
        elif self.predicate.str == "natural":
            val = self.predicate.name
            for arg in self.args:
                val = val.replace('*', str(arg))
            return "("+val+")"


class All(scrt.logic.LogicalExpressionBase):
    def __init__(self, variable, expression):
        if type(variable) != Variable:
            raise Exception("A predicate logical universal instantiation requires variable")
        self.variable = variable
        self.expression = expression

    def __str__(self):
        return "∀" + str(self.variable) + str(self.expression)


class Exists(scrt.logic.LogicalExpressionBase):
    def __init__(self, variable, expression):
        if type(variable) != Variable:
            raise Exception("A predicate logical universal instantiation requires variable")
        self.variable = variable
        self.expression = expression

    def __str__(self):
        return "∃" + str(self.variable) + str(self.expression)
