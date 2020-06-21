import copy
import scrt.logic

class TableauSolver:
    @classmethod
    def solve(cls, expression):
        def delta(nodes, exprs):
            if len(nodes) == 0:
                nodes.append([])

            if len(exprs) == 1:
                for node in nodes:
                    node.append(exprs[0])
                return nodes

            elif len(exprs) >= 2:
                ret_nodes = []

                for i in range(len(exprs) - 1):
                    tmp_nodes = [copy.copy(n) for n in nodes]
                    for tmp_node in tmp_nodes:
                        tmp_node.append(exprs[i])
                    ret_nodes += tmp_nodes

                for node in nodes:
                    node.append(exprs[len(exprs) - 1])
                ret_nodes += nodes

                return ret_nodes

        start_expr = copy.deepcopy(expression)

        nodes = [
            [start_expr]
        ]

        while len(nodes) > 0:
            node = nodes.pop()
            print(", ".join([str(expr) for expr in node]))

            new_nodes = []
            atom_values = {}
            is_paradox = False
            is_changed = False

            for expr in node:
                if type(expr) == scrt.logic.LogicalNot:
                    not_expr = expr.target
                    if type(not_expr) == scrt.logic.LogicalNot:
                        delta(new_nodes, [not_expr.target])
                        is_changed = True

                    elif type(not_expr) == scrt.logic.LogicalAnd:
                        delta(new_nodes, [~not_expr.left, ~not_expr.right])
                        is_changed = True

                    elif type(not_expr) == scrt.logic.LogicalOr:
                        delta(new_nodes, [~not_expr.left])
                        delta(new_nodes, [~not_expr.right])
                        is_changed = True

                    elif type(not_expr) == scrt.logic.LogicalImplies:
                        delta(new_nodes, [not_expr.left])
                        delta(new_nodes, [~not_expr.right])
                        is_changed = True

                    elif type(not_expr) == scrt.logic.LogicalAtom:
                        delta(new_nodes, [expr])
                        if not_expr.name in atom_values and atom_values[not_expr.name] is True:
                            is_paradox = True
                            break
                        elif not_expr.name not in atom_values:
                            atom_values[not_expr.name] = False

                    else:
                        raise ValueError()

                elif type(expr) == scrt.logic.LogicalAnd:
                    delta(new_nodes, [expr.left])
                    delta(new_nodes, [expr.right])
                    is_changed = True

                elif type(expr) == scrt.logic.LogicalOr:
                    delta(new_nodes, [expr.left, expr.right])
                    is_changed = True

                elif type(expr) == scrt.logic.LogicalImplies:
                    delta(new_nodes, [~expr.left, expr.right])
                    is_changed = True

                elif type(expr) == scrt.logic.LogicalAtom:
                    delta(new_nodes, [expr])
                    if expr.name in atom_values and atom_values[expr.name] is False:
                        is_paradox = True
                        break
                    elif expr.name not in atom_values:
                        atom_values[expr.name] = True

                else:
                    raise ValueError()

            if is_paradox is False:
                if is_changed is True:
                    for node in new_nodes:
                        print("ADD NODE: " + (", ".join([str(expr) for expr in node])))
                    nodes += new_nodes
                else:
                    return True

            print()
        return False
