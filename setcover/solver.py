#!/usr/bin/python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Carleton Coffrin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from collections import namedtuple
from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp

Set = namedtuple("Set", ['index', 'cost', 'items'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    item_count = int(parts[0])
    set_count = int(parts[1])
    
    sets = []
    for i in range(1, set_count+1):
        parts = lines[i].split()
        sets.append(Set(i-1, int(parts[0]), map(int, parts[1:])))


    

    # build a trivial solution
    # pick add sets one-by-one until all the items are covered
    #solution = setcover_CP_cpsatsolver(sets, set_count, item_count)
    solution = setcover_MIP_SCIPsolver(sets, set_count, item_count)
    coverted = set()
    
    for s in sets:
        coverted |= set(s.items)
        if len(coverted) >= item_count:
            break
        
    # calculate the cost of the solution
    obj = sum([s.cost*solution[s.index] for s in sets])

    # prepare the solution in the specified output format
    output_data = str(obj) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys


def setcover_CP_cpsatsolver(sets, set_count, item_count):
    model = cp_model.CpModel()

    #matriz de cobertura s
    # s i j = 1 se existe a cobertura do set i para o item j
    s = []
    for i in range(set_count):
        s.append([])
        items = list(sets[i].items)
        for j in range(item_count):
            try: 
                items.index(j)
                s[i].append(1) 
            except ValueError: s[i].append(0)
        

    #xi=1 se i for selecionado
    x = [model.NewIntVar(0, 1, str(i)) for i in range(set_count)]

    #restrição de cada item esta coberto por pelo menos uma set
    c = []
    for j in range(item_count):
        c.append(model.Add(sum(x[i] * s[i][j] for i in range(set_count)) >= 1))

    #minimizar custo*xi
    model.Minimize(sum([sets[i].cost * x[i] for i in range(set_count)]))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 600.0
    status = solver.Solve(model)
    
    solution = []
    for i in range(set_count):
        solution.append(solver.Value(x[i]))
    
    return solution

def setcover_MIP_SCIPsolver(sets, set_count, item_count):
    model = pywraplp.Solver.CreateSolver('SCIP')

    #matriz de cobertura s
    # s i j = 1 se existe a cobertura do set i para o item j
    s = []
    for i in range(set_count):
        s.append([])
        items = list(sets[i].items)
        for j in range(item_count):
            try: 
                items.index(j)
                s[i].append(1) 
            except ValueError: s[i].append(0)
        

    #xi=1 se i for selecionado
    x = [model.IntVar(0, 1, str(i)) for i in range(set_count)]

    #restrição de cada item esta coberto por pelo menos uma set
    c = []
    for j in range(item_count):
        c.append(model.Add(sum(x[i] * s[i][j] for i in range(set_count)) >= 1))

    #minimizar custo*xi
    model.Minimize(sum([sets[i].cost * x[i] for i in range(set_count)]))
    model.
    status = model.Solve()
    
    solution = []
    for i in range(set_count):
        solution.append(x[i].solution_value())
    
    return solution



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/sc_6_1)')

