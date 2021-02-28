from ortools.linear_solver import pywraplp

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
    status = model.Solve()
    
    solution = []
    for i in range(set_count):
        solution.append(x[i].solution_value())
    
    return solution
