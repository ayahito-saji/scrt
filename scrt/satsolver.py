import uuid
import os
import subprocess
import copy
import scrt.logic

class SatSolver:
    @classmethod
    def solve(cls, expression, external_solver=None):
        cnf, atom_number, named_atoms = cls.tseitin_convert(expression)

        if external_solver == None:
            satisfiable, allocation = cls.dpll(cnf)
        else:
            file_name = str(uuid.uuid4())
            input_file_name = file_name + '.cnf'
            output_file_name = file_name + '.out'

            with open(input_file_name, 'w') as fp:
                fp.write('p cnf ' + str(atom_number) + ' ' + str(len(cnf)) + '\n' + '\n'.join([' '.join([str(j) for j in i]) + ' 0' for i in cnf]))

            try:
                subprocess.check_output(external_solver + ' ' + input_file_name + ' ' + output_file_name, shell=True)
            except:
                os.remove(input_file_name)
                raise Exception("An error has occurred in command '" + external_solver + "', please check whether external solver is installed correctly or not.")

            with open(output_file_name, 'r') as fp:
                satisfiable = output_file.readline().rstrip() == 'SATISFIABLE'
                allocation = set([int(r) for r in output_file.readline().split()[:1]])

            os.remove(input_file_name)
            os.remove(output_file_name)

        if satisfiable == True:
            allocation = dict([(name, True if id in allocation else False) for (name, id) in named_atoms.items()])
            return True, allocation
        else:
            return False, None


    @classmethod
    def tseitin_convert(cls, expression):
        atom_counter = 0
        named_atoms = {}

        def tau(clause):
            nonlocal atom_counter
            nonlocal named_atoms

            if type(clause) == scrt.logic.LogicalAtom:
                if not clause.name in named_atoms:
                    atom_counter += 1
                    named_atoms[clause.name] = atom_counter
                return named_atoms[clause.name], []

            elif type(clause) == scrt.logic.LogicalNot:
                atom_counter += 1
                x = atom_counter
                y, Y = tau(clause.target)
                return x, [{x, y}, {-x, -y}] + Y

            elif type(clause) == scrt.logic.LogicalAnd:
                atom_counter += 1
                x = atom_counter
                y, Y = tau(clause.left)
                z, Z = tau(clause.right)
                return x, [{-x, y}, {-x, z}, {x, -y, -z}] + Y + Z

            elif type(clause) == scrt.logic.LogicalOr:
                atom_counter += 1
                x = atom_counter
                y, Y = tau(clause.left)
                z, Z = tau(clause.right)
                return x, [{x, -y}, {x, -z}, {-x, y, z}] + Y + Z

            elif type(clause) == scrt.logic.LogicalImplies:
                atom_counter += 1
                x = atom_counter
                y, Y = tau(clause.left)
                z, Z = tau(clause.right)
                return x, [{x, y}, {x, -z}, {-x, -y, z}] + Y + Z

        x, X = tau(expression)
        return [{x}] + X, atom_counter, named_atoms

    @classmethod
    def dpll(cls, cnf):
        stack = [(set(), cnf)]

        while len(stack) > 0:
            allocation, cnf = stack.pop()

            # unit-rule
            unit_targets = []
            for clause in cnf:
                if len(clause) == 1:
                    unit_targets.append(list(clause)[0])
            allocation = allocation | set(unit_targets)
            i = 0
            while i < len(cnf):
                is_deleted = False
                for unit_target in unit_targets:
                    if unit_target in cnf[i]:
                        is_deleted = True
                        break
                    elif -unit_target in cnf[i]:
                        cnf[i].remove(-unit_target)
                if is_deleted == True:
                    cnf.pop(i)
                else:
                    i += 1

            if len(cnf) == 0:
                return True, allocation

            is_unsatisfiable = False
            for clause in cnf:
                if len(clause) == 0:
                    is_unsatisfiable = True
                    break
            if is_unsatisfiable == True:
                continue

            v = list(cnf[0])[0]
            # the case if v is true
            allocation_v_is_true = copy.copy(allocation) | { v }
            cnf_v_is_true = copy.deepcopy(cnf)

            i = 0
            while i < len(cnf_v_is_true):
                if v in cnf_v_is_true[i]:
                    cnf_v_is_true.pop(i)
                else:
                    if -v in cnf_v_is_true[i]:
                        cnf_v_is_true[i].remove(-v)
                    i += 1
            stack.append((allocation_v_is_true, cnf_v_is_true))

            # the case if v is false
            allocation_v_is_false = copy.copy(allocation) | { -v }
            cnf_v_is_false = copy.deepcopy(cnf)

            i = 0
            while i < len(cnf_v_is_false):
                if -v in cnf_v_is_false[i]:
                    cnf_v_is_false.pop(i)
                else:
                    if v in cnf_v_is_false[i]:
                        cnf_v_is_false[i].remove(v)
                    i += 1

            stack.append((allocation_v_is_false, cnf_v_is_false))
        return False, None
