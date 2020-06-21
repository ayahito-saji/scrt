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

        no_counter = 0

        while len(nodes) > 0:
            # print([", ".join([str(expr) for expr in node]) for node in nodes])
            node = nodes.pop(0)

            new_nodes = []
            atom_values = {}
            is_paradox = False
            is_changed = False

            for expr in node:
                if type(expr) == scrt.logic.LogicalNot:
                    not_expr = expr.target
                    if type(not_expr) == scrt.logic.LogicalNot:
                        new_nodes = delta(new_nodes, [not_expr.target])
                        is_changed = True

                    elif type(not_expr) == scrt.logic.LogicalAnd:
                        new_nodes = delta(new_nodes, [~not_expr.left, ~not_expr.right])
                        is_changed = True

                    elif type(not_expr) == scrt.logic.LogicalOr:
                        new_nodes = delta(new_nodes, [~not_expr.left])
                        new_nodes = delta(new_nodes, [~not_expr.right])
                        is_changed = True

                    elif type(not_expr) == scrt.logic.LogicalImplies:
                        new_nodes = delta(new_nodes, [not_expr.left])
                        new_nodes = delta(new_nodes, [~not_expr.right])
                        is_changed = True

                    elif type(not_expr) == scrt.logic.LogicalAtom:
                        new_nodes = delta(new_nodes, [expr])
                        if not_expr.name in atom_values and atom_values[not_expr.name] is True:
                            is_paradox = True
                            break
                        elif not_expr.name not in atom_values:
                            atom_values[not_expr.name] = False

                    else:
                        raise ValueError()

                elif type(expr) == scrt.logic.LogicalAnd:
                    new_nodes = delta(new_nodes, [expr.left])
                    new_nodes = delta(new_nodes, [expr.right])
                    is_changed = True

                elif type(expr) == scrt.logic.LogicalOr:
                    new_nodes = delta(new_nodes, [expr.left, expr.right])
                    is_changed = True

                elif type(expr) == scrt.logic.LogicalImplies:
                    new_nodes = delta(new_nodes, [~expr.left, expr.right])
                    is_changed = True

                elif type(expr) == scrt.logic.LogicalAtom:
                    new_nodes = delta(new_nodes, [expr])
                    if expr.name in atom_values and atom_values[expr.name] is False:
                        is_paradox = True
                        break
                    elif expr.name not in atom_values:
                        atom_values[expr.name] = True

                else:
                    raise ValueError()

            if is_paradox is False:
                if is_changed is True:
                    for new_node in new_nodes:
                        if graphviz is True:
                            graph.edge("\n".join([str(expr) for expr in node]), "\n".join([str(expr) for expr in new_node]))
                        # print("ADD NODE: " + (", ".join([str(expr) for expr in new_node])))
                    nodes += new_nodes
                else:
                    if graphviz is True:
                        graph.edge("\n".join([str(expr) for expr in node]), "yes")
                        graph.render(graph_filename)
                    return True
            else:
                if graphviz is True:
                    no_counter += 1
                    graph.node("no_"+str(no_counter), "no")
                    graph.edge("\n".join([str(expr) for expr in node]), "no_"+str(no_counter))

            # print()
        if graphviz is True:
            graph.render(graph_filename)
        return False
