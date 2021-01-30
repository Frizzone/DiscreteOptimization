from ortools.sat.python import cp_model


def ORToolsSolver(edges, node_count):
    
    model = cp_model.CpModel()

    num_colors = node_count

    nodeColors = []
    for node in range(node_count):
        nodeColors.append(model.NewIntVar(0, num_colors, str(node)))

    max_color = model.NewIntVar(0, num_colors, 'max_color')

    #restrição de max_color = max(nodeColors)
    model.AddMaxEquality(max_color, nodeColors)
    
    #adicionar restrições de nós adjacentes
    # se aresta(n1,n2) então nodeColor(n1) != nodeColor(n2)
    for e in edges:
        model.Add(nodeColors[e[0]] != nodeColors[e[1]])
        #usar AllDifferent para melhorar tempo

    # symmetry breaking
    # model.Add(nodeColors[0] == 1);
    # model.Add(nodeColors[1] <= 2);
    #for i in range(num_colors):
    #    model.Add(nodeColors[i] <= i+1)

    #função objetivo =  minimizar(max_color)
    model.Minimize(max_color)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)

        
    solution = []
    for node in range(node_count): solution.append(solver.Value(nodeColors[node]))

    return solution
