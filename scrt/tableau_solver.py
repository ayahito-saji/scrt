import copy
import scrt.logic

from graphviz import Graph

class TableauSolver:
    @classmethod
    def solve(cls, expression, graphviz=False, graph_filename='tableau'):

        if graphviz is True:
            graph = Graph(format="png")
            graph.attr("node", color='white')
        else:
            graph = None

        def delta(nodes, exprs, values):
            if len(nodes) == 0:
                nodes.append(([], copy.copy(values)))

            if len(exprs) == 1:
                for node in nodes:
                    node[0].append(exprs[0])
                return nodes

            elif len(exprs) >= 2:
                ret_nodes = []

                for i in range(len(exprs) - 1):
                    tmp_nodes = [(copy.copy(n[0]), copy.copy(n[1])) for n in nodes]
                    for tmp_node in tmp_nodes:
                        tmp_node[0].append(exprs[i])
                    ret_nodes += tmp_nodes

                for node in nodes:
                    node[0].append(exprs[len(exprs) - 1])
                ret_nodes += nodes

                return ret_nodes

        start_expr = copy.deepcopy(expression)

        nodes = [
            ([start_expr], {})
        ]

        no_counter = 0

        while len(nodes) > 0:
            exprs, values = nodes.pop(0)

            new_nodes = []
            is_paradox = False

            for expr in exprs:
                if type(expr) == scrt.logic.LogicalNot:
                    not_expr = expr.target
                    if type(not_expr) == scrt.logic.LogicalAtom:
                        if not_expr.name in values and values[not_expr.name] is True:
                            is_paradox = True
                            break
                        elif not_expr.name not in values:
                            values[not_expr.name] = False

                elif type(expr) == scrt.logic.LogicalAtom:
                    if expr.name in values and values[expr.name] is False:
                        is_paradox = True
                        break
                    elif expr.name not in values:
                        values[expr.name] = True

            # print(", ".join([str(expr) for expr in exprs]), values)

            for expr in exprs:
                if type(expr) == scrt.logic.LogicalNot:
                    not_expr = expr.target
                    if type(not_expr) == scrt.logic.LogicalNot:
                        new_nodes = delta(new_nodes, [not_expr.target], values)

                    elif type(not_expr) == scrt.logic.LogicalAnd:
                        new_nodes = delta(new_nodes, [~not_expr.left, ~not_expr.right], values)

                    elif type(not_expr) == scrt.logic.LogicalOr:
                        new_nodes = delta(new_nodes, [~not_expr.left], values)
                        new_nodes = delta(new_nodes, [~not_expr.right], values)

                    elif type(not_expr) == scrt.logic.LogicalImplies:
                        new_nodes = delta(new_nodes, [not_expr.left], values)
                        new_nodes = delta(new_nodes, [~not_expr.right], values)

                    elif type(not_expr) != scrt.logic.LogicalAtom:
                        raise ValueError()

                elif type(expr) == scrt.logic.LogicalAnd:
                    new_nodes = delta(new_nodes, [expr.left], values)
                    new_nodes = delta(new_nodes, [expr.right], values)

                elif type(expr) == scrt.logic.LogicalOr:
                    new_nodes = delta(new_nodes, [expr.left, expr.right], values)

                elif type(expr) == scrt.logic.LogicalImplies:
                    new_nodes = delta(new_nodes, [~expr.left, expr.right], values)

                elif type(expr) != scrt.logic.LogicalAtom:
                    raise ValueError()

            if is_paradox is False:
                if len(new_nodes) > 0:
                    for new_node in new_nodes:
                        if graphviz is True:
                            graph.edge("\n".join([str(expr) for expr in exprs]), "\n".join([str(expr) for expr in new_node[0]]))
                        # print("ADD NODE: " + (", ".join([str(expr) for expr in new_node[0]])), str(new_node[1]))
                    nodes += new_nodes
                else:
                    if graphviz is True:
                        graph.edge("\n".join([str(expr) for expr in exprs]), "yes")
                        graph.render(graph_filename)
                    return True
            else:
                if graphviz is True:
                    no_counter += 1
                    graph.node("no_"+str(no_counter), "no")
                    graph.edge("\n".join([str(expr) for expr in exprs]), "no_"+str(no_counter))

            # print()
        if graphviz is True:
            graph.render(graph_filename)
        return False
