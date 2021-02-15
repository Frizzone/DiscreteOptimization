import gurobipy as gp
from gurobipy import *
import functions

#model https://how-to.aimms.com/Articles/332/332-Formulation-CVRP.html
#subtour https://how-to.aimms.com/Articles/332/332-Miller-Tucker-Zemlin-formulation.html
def vpr_mip_gurobi(customers, vehicle_count, vehicle_capacity):
    try:
        
        # Create a new model
        m = gp.Model("vpr")
        customer_count = len(customers)
        
        #A[v][o][d] = 1 then v is assigned to route o->d, on this direction
        A = [[[0 for d in range(customer_count)] for o in range(customer_count)] for v in range(vehicle_count)]
        
        #V[v][c] = when vehicle v is assigned to customer c 
        U = [[0 for c in range(customer_count)] for v in range(vehicle_count)]
        
        #create variables
        for v in range(vehicle_count):
            for i in range(customer_count):
                U[v][i] = m.addVar(lb=customers[i].demand, ub=vehicle_capacity, vtype=GRB.CONTINUOUS, name=str(v)+"/"+str(i))
                for j in range(customer_count):
                    if(i!=j): A[v][i][j] = m.addVar(vtype=GRB.BINARY, name=str(v)+","+str(i)+","+str(j))
        
        # (1) Vehicle leaves node that it enters - Ensure that the number of times a vehicle enters a node is equal to the number of times it leaves that node
        for v in range(vehicle_count):
            for j in range(customer_count):
                m.addConstr(sum([A[v][i][j] for i in range(customer_count) if i!=j]) == sum([A[v][j][i] for i in range(customer_count) if i!=j ]), "(1)v,c="+str(v)+","+str(j))
            
        # (2): Ensure that every node is entered once
        for i in range(1, customer_count):
            m.addConstr(sum([sum([A[v][i][j] for v in range(vehicle_count)]) for j in range(customer_count) if i!=j]) == 1, "(2)c="+str(i))
        
        
        # (3): Every vehicle leaves the depot
        for v in range(vehicle_count):
                m.addConstr(sum([A[v][0][j] for j in range(1, customer_count)]) == 1, "(3)v="+str(v))

        
        # (4) Capacity constraint
        for v in range(vehicle_count):
            m.addConstr(sum([customers[j].demand * sum([A[v][i][j] for i in range(customer_count) if i!=j]) for j in range(customer_count) if i!=j]) <= vehicle_capacity, "(4)v="+str(v))
        
        
        # (5): subtour elimination constraints - MTZ constraints
        for v in range(vehicle_count):
            for i in range(customer_count):
                for j in range(customer_count):
                    if(i!=j and i!=0 and j!=0): m.addConstr(U[v][i] - U[v][j] >= customers[j].demand - vehicle_capacity * (1 - A[v][i][j]), "(5)v,i,j="+str(v)+str(i)+str(j))
                    #ui - uj - Q(A[v][i][j]) >= qj - Q
                    #=0 : ui-uj => qj - Q
                    #=1: ui-uj >= qj
 
        #Set objective: minimize the cost of transportation, which is the total distance of all vehicles
        m.setObjective(sum([sum([sum([functions.length(i, j) * A[v][i.index][j.index] for v in range(vehicle_count)]) for i in customers if i!=j]) for j in customers if i!=j]), GRB.MINIMIZE)

        # Optimize model
        m.write('model.lp')
        m.optimize()
        
        #process the solution output
        S = [[[-1 for d in range(customer_count)] for o in range(customer_count)] for v in range(vehicle_count)]
        SV = [['-1' for d in range(customer_count)] for o in range(customer_count)]
        for v in m.getVars():
            indexs = v.varName.split(",")
            if(len(indexs)==3):
                S[int(indexs[0])][int(indexs[1])][int(indexs[2])] = int(v.x)
                if(int(v.x) ==1): SV[int(indexs[1])][int(indexs[2])] = "v" + indexs[0]
                
        for c in range(customer_count):
            print(SV[c])
                
        vehicle_tours = []
        for v in range(vehicle_count):
            vehicle_tours.append([])
            
            o = -1
            finish = False
            while (not finish):
                
                if(o==-1): #initialize o in the depot
                    o = 0 
                    vehicle_tours[v].append(customers[o])

                for next in range(customer_count): #search the next customer
                    if(S[v][o][next]==1):
                        if(next != 0):
                            vehicle_tours[v].append(customers[next])
                            o = next
                        elif(o != next): 
                            vehicle_tours[v].append(customers[0])
                            finish = True;
            
        return vehicle_tours


    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))
