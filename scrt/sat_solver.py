from scrt.minisat import *


class PropLogicBase:
    def __rshift__(self, other):
        return PropLogicExpression('implies', self, other)

    def __lshift__(self, other):
        return PropLogicExpression('implies', other, self)

    def __and__(self, other):
        return PropLogicExpression('and', self, other)

    def __or__(self, other):
        return PropLogicExpression('or', self, other)

    def __invert__(self):
        return PropLogicExpression('not', self)

    def is_paradox(self):
        return SatSolver.paradox(self)

    def solve(self,
              minisat_cmd='minisat',
              input_file_name='',
              output_file_name='',
              clear_files=True
              ):
        return SatSolver.solve(self,
                               minisat_cmd=minisat_cmd,
                               input_file_name=input_file_name,
                               output_file_name=output_file_name,
                               clear_files=clear_files)


class PropLogicAtom(PropLogicBase):
    def __init__(self, name=""):
        if name == "":
            raise Exception('require name')
        self.ope = 'atom'
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class PropLogicExpression(PropLogicBase):
    def __init__(self, ope, *expressions):
        self.ope = ope
        self.expressions = list(expressions)
        if self.ope == "implies" or self.ope == "and" or self.ope == "or":
            if len(self.expressions) != 2:
                raise Exception('invalid expression')
        elif self.ope == "not":
            if len(self.expressions) != 1:
                raise Exception('invalid expression')
        else:
            raise Exception('invalid operation')

    def __str__(self):
        str_expressions = list(map(lambda expression: str(expression), self.expressions))
        if self.ope == "implies":
            return "({0})".format(">>".join(str_expressions))
        elif self.ope == "not":
            return "(~{0})".format(str_expressions[0])
        elif self.ope == "and":
            return "({0})".format("&".join(str_expressions))
        elif self.ope == "or":
            return "({0})".format("|".join(str_expressions))


class SatSolver:
    @classmethod
    def atom(cls, name):
        return PropLogicAtom(name)

    @classmethod
    def solve(cls,
              tree,
              minisat_cmd='minisat',
              input_file_name='',
              output_file_name='',
              clear_files=True):
        solver = MiniSat(minisat_cmd=minisat_cmd,
                         input_file_name=input_file_name,
                         output_file_name=output_file_name,
                         clear_files=clear_files)
        variables = {}

        def convert(node):
            ope = node.ope
            if ope == 'atom':
                if node.name in variables:
                    return variables[node.name]
                else:
                    variable = SatVar()
                    variables[node.name] = variable
                    return variable
            elif ope == 'not':
                x, y = SatVar(), convert(node.expressions[0])
                solver.append((x, y))
                solver.append((-x, -y))
                return x
            elif ope == 'or':
                x, y, z = SatVar(), convert(node.expressions[0]), convert(node.expressions[1])
                solver.append((x, -y))
                solver.append((x, -z))
                solver.append((-x, y, z))
                return x
            elif ope == 'and':
                x, y, z = SatVar(), convert(node.expressions[0]), convert(node.expressions[1])
                solver.append((-x, y))
                solver.append((-x, z))
                solver.append((x, -y, -z))
                return x
            elif ope == 'implies':
                x, y, z = SatVar(), convert(node.expressions[0]), convert(node.expressions[1])
                solver.append((x, y))
                solver.append((x, -z))
                solver.append((-x, -y, z))
                return x

        solver.append((convert(tree),))

        result = solver.solve()
        result_variables = {}

        for key in variables:
            result_variables[key] = solver[variables[key]]

        return result, result_variables

    @classmethod
    def paradox(cls, expression):
        return not cls.solve(expression)[0]

    @classmethod
    def ask(cls, knowledge_base, question):
        if cls.paradox(knowledge_base):
            raise Exception('KnowledgeBase contains paradox')
        tautology = not cls.solve(knowledge_base & (~question))[0]
        if tautology:
            return True
        non_tautology = not cls.solve(knowledge_base & question)[0]
        if non_tautology:
            return False
        return None


if __name__ == "__main__":
    p = SatSolver.atom('p')
    q = SatSolver.atom('q')

    print(SatSolver.solve((p >> q) & p))
