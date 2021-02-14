import gurobipy as gp
from gurobipy import *
import functions

def vpr_mip_gurobi(customers, vehicle_count, vehicle_capacity):
    try:
        
        # Create a new model
        m = gp.Model("vpr")
        customer_count = len(customers)
        
        #A[v][o][d] = 1 then v is assigned to route o->d, on this direction
        A = [[[-1 for d in range(customer_count)] for o in range(customer_count)] for v in range(vehicle_count)]
        
        #V[v][c] = when vehicle v is assigned to customer c 
        U = [[-1 for c in range(customer_count)] for v in range(vehicle_count)]
        
        #create variables
        for v in range(vehicle_count):
            for i in range(customer_count):
                U[v][i] = m.addVar(lb=0.0, ub=vehicle_capacity - customers[i].demand, vtype=GRB.CONTINUOUS, name=str(v)+"/"+str(i))
                for j in range(customer_count):
                    A[v][i][j] = m.addVar(vtype=GRB.BINARY, name=str(v)+","+str(i)+","+str(j))
        
        for v in range(vehicle_count):
            #(2) Add constraint - start/end point: all a vehicles v starts from the depot 0 and end in the depot 0
            m.addConstr(sum([sum([A[v][i][j] for i in range(customer_count)]) for j in range(customer_count)]) <= (customer_count + 1) * sum([A[v][0][j] for j in range(customer_count)]), "Starting point v="+str(v))

            for c in range(customer_count):
                # (1) Add constraint flow: Vehicle leaves node that it enters - Ensure that the number of times a vehicle enters a node is equal to the number of times it leaves that node
                m.addConstr(sum([A[v][i][c] for i in range(customer_count)]) == sum([A[v][c][i] for i in range(customer_count)]), "input has output v,c="+str(v)+str(c))
                
                # (5) Add constraint flow: one input and one output per node
                #m.addConstr(sum([A[v][i][c] for i in range(customer_count)]) <=1 , "one input per node v,c="+str(v)+str(c))
                #m.addConstr(sum([A[v][c][j] for j in range(customer_count)]) <=1 , "one output per node v,c="+str(v)+str(c))
                
                # (4) avoid loops a->a
                #if(a!=0): 
                m.addConstr(A[v][c][c] == 0, "loop v,c="+str(v)+str(c))
                
            
        # Add constraint (3): a route o->d need to have 1 vehicles
        # That means for each v in A[v][o][d], sum of all colunms or lines must be 1
        # Excepction for wharehouse 0
        for i in range(1, customer_count):
            m.addConstr(sum([sum([A[v][i][j] for v in range(vehicle_count)]) for j in range(customer_count)]) == 1, "one vehicle per node input c="+str(i))
        #for j in range(1, customer_count):
        #    m.addConstr(sum([sum([A[v][i][j] for v in range(vehicle_count)]) for i in range(customer_count)]) == 1, "one vehicle per node output c="+str(d))
        
        
        # Add constraint (6): subtour elimination constraints - MTZ constraints
        for v in range(vehicle_count):
            for i in range(customer_count):
                for j in range(customer_count):
                    if(i!=j and j!=0 and i!=0): m.addConstr(U[v][i] - U[v][j] >= customers[j].demand - vehicle_capacity * (1 - A[v][i][j]), "subtour v,i,j="+str(v)+str(i)+str(j))

        #Add constraint: capacity <= demand
        # for a vehicle v, sum the customers a
        for v in range(vehicle_count):
            m.addConstr(sum([customers[j].demand * sum([A[v][i][j] for i in range(1, customer_count)]) for j in range(1, customer_count)]) <= vehicle_capacity, "c"+str(v))
        
        #Set objective: minimeze the cost of transportation, which is the total distance of all vehicles
        m.setObjective(sum([sum([sum([functions.length(o, d) * A[v][o.index][d.index] for v in range(vehicle_count)]) for o in customers]) for d in customers]), GRB.MINIMIZE)

        # Optimize model
        m.write('model.lp')
        m.optimize()
        
        #process the solution output
        S = [[[-1 for d in range(customer_count)] for o in range(customer_count)] for v in range(vehicle_count)]
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

                for next in range(customer_count): #search the next customer
                    if(S[v][o][next]==1):
                        if(next != 0):
                            vehicle_tours[v].append(customers[next])
                            o = next
            
        return vehicle_tours


    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))



def vpr_mip_gurobi2(customers, vehicle_count, vehicle_capacity):
    try:
        
        # Create a new model
        m = gp.Model("vpr")
        customer_count = len(customers)
        
        #A[v][o][d] = 1 then v is assigned to route o->d, on this direction
        A = [[[-1 for d in range(customer_count)] for o in range(customer_count)] for v in range(vehicle_count)]
        
        #V[v][c] = when vehicle v is assigned to customer c 
        U = [[-1 for c in range(customer_count)] for v in range(vehicle_count)]
        
        #create variables
        for v in range(vehicle_count):
            for i in range(customer_count):
                U[v][i] = m.addVar(lb=0.0, ub=vehicle_capacity - customers[i].demand, vtype=GRB.CONTINUOUS, name=str(v)+"/"+str(i))
                for j in range(customer_count):
                    A[v][i][j] = m.addVar(vtype=GRB.BINARY, name=str(v)+","+str(i)+","+str(j))
        
        # (1) Vehicle leaves node that it enters - Ensure that the number of times a vehicle enters a node is equal to the number of times it leaves that node
        for v in range(vehicle_count):
            for c in range(customer_count):
                m.addConstr(sum([A[v][i][c] for i in range(customer_count)]) == sum([A[v][c][i] for i in range(customer_count)]), "1="+str(v)+str(c))
            
        # (2): Ensure that every node is entered once
        for i in range(1, customer_count):
            m.addConstr(sum([sum([A[v][i][j] for v in range(vehicle_count)]) for j in range(customer_count)]) == 1, "2="+str(i))
        
        
        # (3): Every vehicle leaves the depot
        for v in range(vehicle_count):
                m.addConstr(sum([A[v][0][j] for j in range(1, customer_count)]) == 1, "3="+str(v)+str(c))

        
        # (4) Capacity constraint
        for v in range(vehicle_count):
            m.addConstr(sum([customers[j].demand * sum([A[v][i][j] for i in range(1, customer_count)]) for j in range(1, customer_count)]) <= vehicle_capacity, "4="+str(v))
        
        
        # (5): subtour elimination constraints - MTZ constraints
        for v in range(vehicle_count):
            for i in range(customer_count):
                for j in range(customer_count):
                    if(i!=j and j!=0 and i!=0): m.addConstr(U[v][i] - U[v][j] >= customers[j].demand - vehicle_capacity * (1 - A[v][i][j]), "5="+str(v)+str(i)+str(j))

 
        #Set objective: minimize the cost of transportation, which is the total distance of all vehicles
        m.setObjective(sum([sum([sum([functions.length(o, d) * A[v][o.index][d.index] for v in range(vehicle_count)]) for o in customers]) for d in customers]), GRB.MINIMIZE)

        # Optimize model
        m.write('model.lp')
        m.optimize()
        
        #process the solution output
        S = [[[-1 for d in range(customer_count)] for o in range(customer_count)] for v in range(vehicle_count)]
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

                for next in range(customer_count): #search the next customer
                    if(S[v][o][next]==1):
                        if(next != 0):
                            vehicle_tours[v].append(customers[next])
                            o = next
            
        return vehicle_tours


    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))
