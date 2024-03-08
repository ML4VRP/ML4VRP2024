# -*- coding: utf-8 -*-

'''gavrptw/core.py'''

import os
import random
from deap import base, creator, tools
from . import BASE_DIR
from .utils import load_instance, load_solution

def ind2route(individual, instance):
    route = []
    # Initialize a sub-route
    sub_route = []
    vehicle_load = 0
    last_customer_id = 0
    sub=[]
    for sub in individual:
        sub_route = []
        for customer_id in sub:
            sub_route.append(customer_id)
        if sub_route != []:
            # Save current sub-route before return if not empty
            route.append(sub_route)
    return route

def eval_cvrp(individual, instance, unit_cost=1.0, init_cost=0):
    feasibility = 1
    total_cost = 0
    route = ind2route(individual, instance)
    num_routes = len(route)
    num_customers = len(instance['distance_matrix'])-1
    num_customer_counter = 0
    # check feasibility - number of vehicles
    if(instance['max_vehicle_number'] < num_routes):
        feasibility = 0
        print("invalid number of routes")    
    vehicle_capacity = instance['vehicle_capacity']
    for sub_route in route:
        #print(sub_route)
        
        sub_route_distance = 0
        last_customer_id = 0
        
        vehicle_load = 0
        for customer_id in sub_route:
            # check feasibility - capacity 
            demand = instance[f'customer_{customer_id}']['demand'] # get vehicle load
            updated_vehicle_load = vehicle_load + demand # update vehicle load
            if (updated_vehicle_load > vehicle_capacity): # check capacity
                feasibility = 0
                print("invalid capacity")
                        
            # Calculate section distance
            distance = instance['distance_matrix'][last_customer_id][customer_id]
            # Update sub-route distance
            sub_route_distance = sub_route_distance + distance
            
            # Update last customer ID
            last_customer_id = customer_id

            vehicle_load = updated_vehicle_load
                
            # Update last customer ID
            last_customer_id = customer_id
            num_customer_counter=num_customer_counter+1

        # Calculate transport cost
        sub_route_distance = sub_route_distance + instance['distance_matrix'][last_customer_id][0]
        sub_route_transport_cost = init_cost + unit_cost * sub_route_distance
        # Obtain sub-route cost
        sub_route_cost = sub_route_transport_cost
        # Update total cost
        total_cost = total_cost + sub_route_cost
        #total_cost = total_cost + round(sub_route_cost,1)
    total_cost = round(total_cost, 1)
    fitness = 1000*num_routes + total_cost
    # check feasibility - number of customers
    if(num_customer_counter!=num_customers):
        feasibility = 0
        print("invalid number of customers: ", num_customer_counter)
    return (feasibility, fitness, num_routes, total_cost)

def eval_cvrptw(individual, instance, unit_cost=1.0, init_cost=0, wait_cost=0, delay_cost=0):
    feasibility = 1
    total_cost = 0
    route = ind2route(individual, instance)
    num_routes = len(route)
    num_customers = len(instance['distance_matrix'])-1
    num_customer_counter = 0
    # check feasibility - number of vehicles
    if(instance['max_vehicle_number'] < num_routes):
        feasibility = 0
        print("invalid number of routes")    
    vehicle_capacity = instance['vehicle_capacity']
    for sub_route in route:
        #print(sub_route)
        sub_route_time_cost = 0
        sub_route_distance = 0
        last_customer_id = 0
        elapsed_time = 0
        vehicle_load = 0
        for customer_id in sub_route:
            # check feasibility - capacity 
            demand = instance[f'customer_{customer_id}']['demand'] # get vehicle load
            updated_vehicle_load = vehicle_load + demand # update vehicle load
            if (updated_vehicle_load > vehicle_capacity): # check capacity
                feasibility = 0
                print("invalid capacity")
            
            # check feasibility - time window: arrive too late to start serve -- due date
            # get location time window
            ready_time = instance[f'customer_{customer_id}']['ready_time']
            service_time = instance[f'customer_{customer_id}']['service_time']
            depart_due_time = instance[f'customer_{customer_id}']['due_time']
            travel_time = instance['distance_matrix'][last_customer_id][customer_id]
            arrive_time = elapsed_time + instance['distance_matrix'][last_customer_id][customer_id] # arrive & ready to serve
            # update elapsed time - arrive at the current location, not start service
            updated_elapsed_time = elapsed_time + travel_time
            if(arrive_time < ready_time): # arrive too early
                updated_elapsed_time = ready_time
            # elif(arrive_time>=ready_time) and (arrive_time<=depart_due_time):
            #     updated_elapsed_time = updated_elapsed_time
            elif(arrive_time>depart_due_time):
                feasibility = 0
                print("invalid time window: too late to serve customer ", customer_id)
            updated_elapsed_time = updated_elapsed_time + service_time

            # Calculate section distance
            distance = instance['distance_matrix'][last_customer_id][customer_id]
            # Update sub-route distance
            sub_route_distance = sub_route_distance + distance
            # Calculate time cost
            # arrival_time = elapsed_time + distance
            # time_cost = wait_cost * max(instance[f'customer_{customer_id}']['ready_time'] - \
            #     arrival_time, 0) + delay_cost * max(arrival_time - \
            #     instance[f'customer_{customer_id}']['due_time'], 0)
            # Update sub-route time cost
            # sub_route_time_cost = sub_route_time_cost + time_cost
            # Update elapsed time
            # elapsed_time = arrival_time + instance[f'customer_{customer_id}']['service_time']
            
            # Update last customer ID
            last_customer_id = customer_id

            vehicle_load = updated_vehicle_load
            elapsed_time = updated_elapsed_time
                
            # Update last customer ID
            last_customer_id = customer_id
            num_customer_counter=num_customer_counter+1

        # Calculate transport cost
        sub_route_distance = sub_route_distance + instance['distance_matrix'][last_customer_id][0]
        sub_route_transport_cost = init_cost + unit_cost * sub_route_distance
        # Obtain sub-route cost
        #sub_route_cost = sub_route_time_cost + sub_route_transport_cost
        sub_route_cost = sub_route_transport_cost
        # Update total cost
        total_cost = total_cost + sub_route_cost
        #total_cost = total_cost + round(sub_route_cost,1)
    total_cost = round(total_cost, 1)
    fitness = 1000*num_routes + total_cost
    # check feasibility - number of customers
    if(num_customer_counter!=num_customers):
        feasibility = 0
        print("invalid number of customers: ", num_customer_counter)
    return (feasibility, fitness, num_routes, total_cost)

#run_solution_evaluator(problem_type = problem, instance_name=instance_name, solution_path=solution_path)
def run_solution_evaluator(problem_type, instance_name, solution_path, export_csv=False, customize_data=False):
    
    if customize_data:
        #json_data_dir = os.path.join(BASE_DIR, 'Instances', 'json_customize','Customer'+str(instance_size))
        json_data_dir = os.path.join(BASE_DIR, 'Instances', problem_type,'json_customize')
    else:
        #json_data_dir = os.path.join(BASE_DIR, 'Instances', 'json','Customer'+str(instance_size))
        json_data_dir = os.path.join(BASE_DIR, 'Instances', problem_type,'json')
    json_file = os.path.join(json_data_dir, f'{instance_name}.json')
    instance = load_instance(json_file=json_file)
    if instance is None:
        return
    
    ind_size = 25
    unit_cost = 1.0
    init_cost = 0.0
    wait_cost = 0.0
    delay_cost = 0.0
    feasibility = 1
    creator.create('FitnessMax', base.Fitness, weights=(1.0, ))
    creator.create('Individual', list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    # Attribute generator
    toolbox.register('indexes', random.sample, range(1, ind_size + 1), ind_size)
    # Structure initializers
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    # Operator registering
    # 'cvrp', 'cvrptw'
    if(problem_type=='cvrptw'):
        toolbox.register('evaluate', eval_cvrptw, instance=instance, unit_cost=unit_cost, \
                         init_cost=init_cost, wait_cost=wait_cost, delay_cost=delay_cost)
    else:
        toolbox.register('evaluate', eval_cvrp, instance=instance, unit_cost=unit_cost, \
                         init_cost=init_cost)
    #toolbox.register('evaluate', eval_vrptw, instance=instance, unit_cost=unit_cost, \
        #init_cost=init_cost, wait_cost=wait_cost, delay_cost=delay_cost)
    
    solution = load_solution(solution_path)
    feasibility, objvalue, nv, td = toolbox.evaluate(solution)
    return (feasibility, objvalue, nv, td)
