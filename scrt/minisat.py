import uuid
import os
import subprocess


class MiniSat(object):
    def __init__(self, minisat_cmd='minisat', input_file_name='', output_file_name='', clear_files=True):
        self.minisat_cmd = minisat_cmd

        self.uuid = str(uuid.uuid4())
        if input_file_name == '':
            input_file_name = self.uuid + '.cnf'
        if output_file_name == '':
            output_file_name = self.uuid + '.out'
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name

        self.clear_files = clear_files
        self.clauses = []
        self.unique_variable_names = {}
        self.unique_variable_name_cnt = 1
        self.result = []

    def append(self, var):
        if not isinstance(var, tuple):
            raise Exception("'clause' should be tuple.")
        for v in var:
            if not isinstance(v, SatVarBase):
                raise Exception("Illegal variable type.")
            if v.name not in self.unique_variable_names:
                self.unique_variable_names[v.name] = self.unique_variable_name_cnt
                self.unique_variable_name_cnt += 1
        self.clauses.append(var)

    def to_num(self, name):
        return str(self.unique_variable_names[name])

    def solve(self):
        input_file = open(self.input_file_name, 'w')
        num_variables = len(self.unique_variable_names)
        num_clauses = len(self.clauses)
        input_file.write("p cnf %d %d\n" % (num_variables, num_clauses))
        for clause in self.clauses:
            write_var = ''
            for e in clause:
                if isinstance(e, SatVar):
                    write_var += self.to_num(e.name) + ' '
                if isinstance(e, SatVarInv):
                    write_var += '-' + self.to_num(e.name) + ' '
            input_file.write(write_var + '0\n')
        input_file.close()

        cmd = self.minisat_cmd + ' ' + self.input_file_name + ' ' + self.output_file_name

        try:
            subprocess.check_output(cmd, shell=True)
        except:
            pass

        output_file = open(self.output_file_name, 'r')
        output_file.readline()
        result = output_file.readline().split()
        for r in result[:-1]:
            self.result.append(int(r))

        if self.clear_files:
            os.remove(self.input_file_name)
            os.remove(self.output_file_name)

        if len(result) == 0:
            return False
        return True

    def __getitem__(self, clause):
        if not isinstance(clause, SatVarBase):
            raise Exception('Type Error')
        index = int(self.to_num(clause.name)) - 1
        if index >= len(self.result):
            return None
        if self.result[index] < 0:
            return False
        return True

    def view(self):
        if len(self.result) == 0:
            print("UNSATISFIABLE")
            return
        print("SATISFIABLE")
        p = ''
        for r in self.result:
            p += str(r >= 0) + ', '
        print(p[:-2])


class SatVarBase(object):
    def __init__(self, name=None):
        self.name = id(self)
        if name is not None:
            self.name = name


class SatVar(SatVarBase):
    def __neg__(self):
        return SatVarInv(self.name)


class SatVarInv(SatVarBase):
    def __neg__(self):
        return SatVar(self.name)


if __name__ == '__main__':
    solver = MiniSat()
    a = SatVar()
    b = SatVar()
    solver.append((-a, -b))
    solver.append((a, -b))
    solver.append((-a, b))
    solver.append((a, b))
    satisfy = solver.solve()
    if satisfy:
        print("SATISFIABLE")
    else:
        print("UNSATISFIABLE")
