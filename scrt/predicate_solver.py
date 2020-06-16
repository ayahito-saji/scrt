import copy
import scrt.predicate_logic
import scrt.logic


class PredicateSolver:
    @classmethod
    def normalize(cls, expr):
        expr = copy.deepcopy(expr)

        def skolemize(clause):
            if type(clause) == scrt.predicate_logic.PredicateCall:
                print(clause)
                for arg in clause.args:
                    if type(arg) is not scrt.predicate_logic.Variable:
                        skolemize(arg)
            elif type(clause) == scrt.predicate_logic.FunctionCall:
                print(clause)
                for arg in clause.args:
                    if type(arg) is not scrt.predicate_logic.Variable:
                        skolemize(arg)
            elif type(clause) == scrt.logic.LogicalNot:
                skolemize(clause.target)
            elif type(clause) == scrt.logic.LogicalAnd:
                skolemize(clause.left)
                skolemize(clause.right)
            elif type(clause) == scrt.logic.LogicalOr:
                skolemize(clause.left)
                skolemize(clause.right)
            elif type(clause) == scrt.logic.LogicalImplies:
                skolemize(clause.left)
                skolemize(clause.right)
            elif type(clause) == scrt.predicate_logic.All:
                skolemize(clause.expression)
            elif type(clause) == scrt.predicate_logic.Exists:
                skolemize(clause.expression)
            else:
                raise Exception("Invalid predicate logical expression ("+str(type(clause))+")")
        skolemize(expr)
