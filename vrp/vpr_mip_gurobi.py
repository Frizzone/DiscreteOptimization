import gurobipy as gp
from gurobipy import *
import functions

def vpr_mip_gurobi(customers, vehicle_count):
    try:
        
        # Create a new model
        m = gp.Model("vpr")
        
        #A[v][o][d] = 1 then v is assigned to route o->d, on this direction
        A = [[[-1 for v in range(vehicle_count)] for o in range(len(customers))] for d in range(len(customers))]
            
        # Add constraint: a route o->d need to have 1 vehicles
        # That means for each v in A[v][o][d], sum of all colunms or lines must be 1
        # Excepction for wharehouse 0
        for o in range(1, len(customers)-1):
            m.addConstr(sum([sum([A[v][o][d] for v in range(vehicle_count)]) for d in range(1, len(customers)-1)]) == 1, "ro"+str(o))
        for d in range(1, len(customers)-1):
            m.addConstr(sum([sum([A[v][o][d] for v in range(vehicle_count)]) for o in range(1, len(customers)-1)]) == 1, "rd"+str(d))

        # Add constraint: tour
        # for a vehicle v, ensure the a node a has a input->a->output
        for v in range(vehicle_count):
            for a in range(len(customers)):
                m.addConstr(sum([A[v][input][a] for input in range(len(customers))]) == sum([A[v][a][output] for output in range(len(customers))]), "t"+str(v)+str(a))

        #Add constraint: capacity <= demand
        # for a vehicle v, ensure
        for v in range(vehicle_count):
            m.addConstr(sum(customers[d].demand * [sum([A[v][o][d] for o in range(1, len(customers))])] for d in range(1, len(customers))) <= vehicle_capacity, "c"+str(v))
        
        #Set objective: minimeze the cost of transportation, which is the total distance of all vehicles
        m.setObjective(sum([sum([sum([functions.length(o, d) * A[v][o.index][d.index] for v in range(vehicle_count)]) for o in customers]) for d in customers]), GRB.MINIMIZE)
    
    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))
