import gurobipy as gp
from gurobipy import *
import functions

def facility_gurobi(facilities, customers):
    try:
        # Create a new model
        m = gp.Model("facility")

        # Create variables 
        #A[c][f] = 1 then Facility f is assign to customer c
        A = [[-1 for x in range(len(facilities))] for y in range(len(customers))]
        F = [0 for x in range(len(facilities))]
        for facility in facilities:
            F[facility.index] = m.addVar(vtype=GRB.BINARY, name=str(facility.index))
            for customer in customers:
                A[customer.index][facility.index] = m.addVar(vtype=GRB.BINARY, name=str(customer.index)+","+str(facility.index))

        # Add constraint: um cliente é atendido por apenas 1 local
        for customer in customers:
            m.addConstr(sum([A[customer.index][f.index] for f in facilities]) == 1, "c"+str(customer.index))

        # Add constraint: a demanda dos clientes pode ser atendida pela capacidade do local
        for facility in facilities:
            m.addConstr(sum([c.demand * A[c.index][facility.index] for c in customers]) <= facility.capacity, "d"+str(facility.index))

        # Add constraint: para dar valores corretos variável F
        for facility in facilities:
            m.addConstr(sum([A[c.index][facility.index] for c in customers]) <= len(customers) * F[facility.index], "f"+str(facility.index))
            

        # Set objective
        m.setObjective(sum([F[f.index] * f.setup_cost for f in facilities]) + sum([sum([A[c.index][f.index] * functions.length(f.location, c.location) for f in facilities]) for c in customers]), GRB.MINIMIZE)

   
        #m.write('model.lp')
        
        #parameters
        m.Params.TimeLimit =60*10
        #m.Params.MIPGap=0.1
    
        # Optimize model
        m.optimize()

        S = [[-1 for x in range(len(facilities))] for y in range(len(customers))]
        for v in m.getVars():
            indexs = v.varName.split(",")
            if(len(indexs)>1):
                S[int(indexs[0])][int(indexs[1])] = int(v.x)
                
        solution = [-1]*len(customers)
        for customer in customers:
            for facility in facilities:
                if(S[customer.index][facility.index] == 1):
                    if(solution[customer.index] != -1):
                        print('The solutions has more than one facility to the same customer.')
                        break;
                    else: solution[customer.index] = facility.index
                    
        return solution
        print('Obj: %g' % m.objVal)

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))
