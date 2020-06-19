import copy
import scrt.predicate_logic
import scrt.logic


class PredicateSolver:
    @classmethod
    def skolemize(cls, expr):
        # simplify
        bounded_table = {}

        def simplify(clause):
            nonlocal bounded_table

            if type(clause) == scrt.predicate_logic.Variable:
                if clause.name in bounded_table:
                    bounded_table[clause.name] = True
                return clause
            elif type(clause) == scrt.predicate_logic.PredicateCall:
                for arg in clause.args:
                    simplify(arg)
                return clause
            elif type(clause) == scrt.predicate_logic.FunctionCall:
                for arg in clause.args:
                    simplify(arg)
                return clause
            elif type(clause) == scrt.logic.LogicalNot:
                target = simplify(clause.target)
                return scrt.logic.LogicalNot(target)
            elif type(clause) == scrt.logic.LogicalAnd:
                left = simplify(clause.left)
                right = simplify(clause.right)
                return scrt.logic.LogicalAnd(left, right)
            elif type(clause) == scrt.logic.LogicalOr:
                left = simplify(clause.left)
                right = simplify(clause.right)
                return scrt.logic.LogicalOr(left, right)
            elif type(clause) == scrt.logic.LogicalImplies:
                left = simplify(clause.left)
                right = simplify(clause.right)
                return scrt.logic.LogicalImplies(left, right)
            elif type(clause) == scrt.predicate_logic.All:
                if clause.variable.name in bounded_table:
                    raise Exception("Variable '" + clause.variable.name + "' is already bounded.")

                bounded_table[clause.variable.name] = False
                expression = simplify(clause.expression)
                tmp = bounded_table[clause.variable.name]
                del bounded_table[clause.variable.name]
                if tmp:
                    return scrt.predicate_logic.All(clause.variable, expression)
                else:
                    return expression
            elif type(clause) == scrt.predicate_logic.Exists:
                if clause.variable.name in bounded_table:
                    raise Exception("Variable '" + clause.variable.name + "' is already bounded.")

                bounded_table[clause.variable.name] = False
                expression = simplify(clause.expression)
                tmp = bounded_table[clause.variable.name]
                del bounded_table[clause.variable.name]
                if tmp:
                    return scrt.predicate_logic.Exists(clause.variable, expression)
                else:
                    return expression
        expr = simplify(expr)

        # sigma
        var_counter = 0
        skolem_func_counter = 0
        convert_table = {}
        bounded_table = {}

        def sigma(clause, reverse, all_symbols):
            nonlocal var_counter
            nonlocal skolem_func_counter
            nonlocal convert_table
            nonlocal bounded_table

            if type(clause) == scrt.predicate_logic.PredicateCall:
                args = []
                for arg in clause.args:
                    if type(arg) is scrt.predicate_logic.FunctionCall:
                        args.append(sigma(arg, reverse, all_symbols))
                    elif type(arg) is scrt.predicate_logic.Variable:
                        if arg.name in bounded_table:
                            args.append(bounded_table[arg.name])
                        else:
                            if arg.name not in convert_table:
                                var_counter += 1
                                convert_table[arg.name] = scrt.predicate_logic.Variable("x" + str(var_counter))
                            args.append(convert_table[arg.name])
                    elif type(arg) is scrt.predicate_logic.Constant:
                        args.append(arg)
                    else:
                        raise Exception("Invalid predicate logical expression ("+str(type(clause))+")")

                return scrt.predicate_logic.PredicateCall(clause.predicate, args)

            elif type(clause) == scrt.predicate_logic.FunctionCall:
                args = []
                for arg in clause.args:
                    if type(arg) is scrt.predicate_logic.FunctionCall:
                        args.append(sigma(arg, reverse, all_symbols))
                    elif type(arg) is scrt.predicate_logic.Variable:
                        if arg.name in bounded_table:
                            args.append(bounded_table[arg.name])
                        else:
                            if arg.name not in convert_table:
                                var_counter += 1
                                convert_table[arg.name] = scrt.predicate_logic.Variable("x" + str(var_counter))
                            args.append(convert_table[arg.name])
                    elif type(arg) is scrt.predicate_logic.Constant:
                        args.append(arg)
                    else:
                        raise Exception("Invalid predicate logical expression ("+str(type(clause))+")")

                return scrt.predicate_logic.FunctionCall(clause.function, args)
            elif type(clause) == scrt.logic.LogicalNot:
                target = sigma(clause.target, reverse + 1, all_symbols)
                return scrt.logic.LogicalNot(target)

            elif type(clause) == scrt.logic.LogicalAnd:
                left = sigma(clause.left, reverse, all_symbols)
                right = sigma(clause.right, reverse, all_symbols)
                return scrt.logic.LogicalAnd(left, right)

            elif type(clause) == scrt.logic.LogicalOr:
                left = sigma(clause.left, reverse, all_symbols)
                right = sigma(clause.right, reverse, all_symbols)
                return scrt.logic.LogicalOr(left, right)

            elif type(clause) == scrt.logic.LogicalImplies:
                left = sigma(clause.left, reverse + 1, all_symbols)
                right = sigma(clause.right, reverse, all_symbols)
                return scrt.logic.LogicalImplies(left, right)

            elif type(clause) == scrt.predicate_logic.All:
                if clause.variable.name in bounded_table:
                    raise Exception("Variable '" + clause.variable.name + "' is already bounded.")

                if reverse % 2 == 0:
                    var_counter += 1
                    bounded_table[clause.variable.name] = scrt.predicate_logic.Variable("x"+str(var_counter))
                    tmp_all_symbols = copy.deepcopy(all_symbols) | {"x"+str(var_counter)}
                    expression = sigma(clause.expression, reverse, tmp_all_symbols)
                else:
                    skolem_func_counter += 1
                    bounded_table[clause.variable.name] = SkolemFunctionCall("σ" + str(skolem_func_counter), all_symbols)
                    expression = sigma(clause.expression, reverse, all_symbols)

                del bounded_table[clause.variable.name]
                return expression

            elif type(clause) == scrt.predicate_logic.Exists:
                if clause.variable.name in bounded_table:
                    raise Exception("Variable '" + clause.variable.name + "' is already bounded.")

                if reverse % 2 == 1:
                    var_counter += 1
                    bounded_table[clause.variable.name] = scrt.predicate_logic.Variable("x" + str(var_counter))
                    tmp_all_symbols = copy.deepcopy(all_symbols) | {"x" + str(var_counter)}
                    expression = sigma(clause.expression, reverse, tmp_all_symbols)
                else:
                    skolem_func_counter += 1
                    bounded_table[clause.variable.name] = SkolemFunctionCall("σ" + str(skolem_func_counter), all_symbols)
                    expression = sigma(clause.expression, reverse, all_symbols)

                del bounded_table[clause.variable.name]
                return expression

            else:
                raise Exception("Invalid predicate logical expression ("+str(type(clause))+")")
        return sigma(expr, False, set())

    @classmethod
    def cnf_convert(cls, expr):
        # TODO スコーレム化された述語論理式exprをCNF化する
        return expr

    @classmethod
    def normalize(cls, expr):
        expr = cls.skolemize(expr)
        expr = cls.cnf_convert(expr)
        return expr


class SkolemFunctionCall:
    def __init__(self, name=None, dependent_variables=None):
        self.name = name
        self.dependent_variables = dependent_variables

    def __str__(self):
        if len(self.dependent_variables) > 0:
            return self.name + "(" + ",".join([str(variable) for variable in self.dependent_variables]) + ")"
        else:
            return self.name
