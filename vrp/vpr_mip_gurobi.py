import gurobipy as gp
from gurobipy import *
import functions

def vpr_mip_gurobi(customers, vehicle_count, vehicle_capacity):
    try:
        
        # Create a new model
        m = gp.Model("vpr")
        
        #A[v][o][d] = 1 then v is assigned to route o->d, on this direction
        A = [[[-1 for d in range(len(customers))] for o in range(len(customers))] for v in range(vehicle_count)]

        #create variables
        for v in range(vehicle_count):
            for o in range(len(customers)):
                for d in range(len(customers)):
                    A[v][o][d] = m.addVar(vtype=GRB.BINARY, name=str(v)+","+str(o)+","+str(d))


        # (2) Add constraint - start/end point: all a vehicles v starts from the depot 0 and end in the depot 0
        m.addConstr(sum([sum([A[v][0][a] for a in range(len(customers))]) for v in range(vehicle_count)]) == vehicle_count, "sl")
        m.addConstr(sum([sum([A[v][a][0] for a in range(len(customers))]) for v in range(vehicle_count)]) == vehicle_count, "sc")
            
        for v in range(vehicle_count):
            a=0
            for a in range(len(customers)):
                # (1) Add constraint flow: ensure that the vehicle route will follow a flow.
                m.addConstr(sum([A[v][input][a] for input in range(len(customers))]) == sum([A[v][a][output] for output in range(len(customers))]), "f"+str(v)+str(a))
                
                # (5) Add constraint flow: one input and one output per node
                m.addConstr(sum([A[v][input][a] for input in range(len(customers))]) <=1 , "fi"+str(v)+str(a))
                m.addConstr(sum([A[v][a][output] for output in range(len(customers))]) <=1 , "fo"+str(v)+str(a))
                
                # (4) avoid loops a->a
                if(a!=0): m.addConstr(A[v][a][a] == 0, "l"+str(v)+str(a))
            
        # Add constraint (3): a route o->d need to have 1 vehicles
        # That means for each v in A[v][o][d], sum of all colunms or lines must be 1
        # Excepction for wharehouse 0
        for o in range(1, len(customers)):
            m.addConstr(sum([sum([A[v][o][d] for v in range(vehicle_count)]) for d in range(1, len(customers))]) == 1, "ro"+str(o))
        for d in range(1, len(customers)):
            m.addConstr(sum([sum([A[v][o][d] for v in range(vehicle_count)]) for o in range(1, len(customers))]) == 1, "rd"+str(d))

        #Add constraint: capacity <= demand
        # for a vehicle v, sum the customers a
        #for v in range(vehicle_count):
        #    m.addConstr(sum([customers[d].demand * sum([A[v][o][d] for o in range(1, len(customers))]) for d in range(1, len(customers))]) <= vehicle_capacity, "c"+str(v))
        
        #Set objective: minimeze the cost of transportation, which is the total distance of all vehicles
        m.setObjective(sum([sum([sum([A[v][o.index][d.index] for v in range(vehicle_count)]) for o in customers]) for d in customers]), GRB.MINIMIZE)

        # Optimize model
        m.write('model.lp')
        m.optimize()
        
        #process the solution output
        S = [[[-1 for d in range(len(customers))] for o in range(len(customers))] for v in range(vehicle_count)]
        for v in m.getVars():
            indexs = v.varName.split(",")
            if(len(indexs)==3):
                S[int(indexs[0])][int(indexs[1])][int(indexs[2])] = int(v.x)
                
        vehicle_tours = []
        for v in range(0, vehicle_count):
            vehicle_tours.append([])
            
            o = -1
            while (o!=0):
                
                if(o==-1): #initialize o in the depot
                    o = 0 
                    vehicle_tours[v].append(customers[o])

                for next in range(len(customers)): #search the next customer
                    if(S[v][o][next]==1):
                        if(next != 0):
                            vehicle_tours[v].append(customers[next])
                            o = next
            
        return vehicle_tours


    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))
