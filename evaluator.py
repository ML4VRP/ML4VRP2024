#!/usr/bin/env python
# coding: utf-8

# In[2]:


# -*- coding: utf-8 -*-

'''sample_C1_4_3.py'''

from vrp_evaluator.core import run_solution_evaluator
import sys

#main(problem_type=param_1,instance_name=param_2, solution_path=param_3)
def main(problem_type, instance_name, solution_path):
    '''main()'''
    #solution = "Solution/Customer"+str(instance_size)+"/"+instance_name+".txt"
    
    feasibility, objective, nv, td = run_solution_evaluator(problem_type = problem_type, instance_name=instance_name, solution_path=solution_path)
    if(feasibility == 1):
        print("Number of vehicles: ", nv, ", Total distance: ", td, "Objective value: ", objective)
    else:
        print("The solution in infeasible!")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Error: Please provide arguments as stated in README.")
        sys.exit()
    param_1 = sys.argv[1] # problem type: cvrp or cvrptw
    param_2 = sys.argv[2] # instance id
    param_3 = sys.argv[3]
    
    # need to check problem type input correct or not
    param_1_convert = param_1.lower()
    if not param_1_convert in ['cvrp', 'cvrptw']:
        print("Error: Please give the correct problem type, i.e., 'cvrp' or 'cvrptw'")
        sys.exit()
    
    # check instance name
    #if not param_2.isdigit():
        #print("Error: The instance size must be an integer.")
        #sys.exit()
    
    # check whether input instance name is correct
    if param_2 not in param_3:
        print("Error: Wrong instance name or solution name.")
        sys.exit()
   
    # check whether input instance name is correct
    if param_1 not in param_3:
        print("Error: Wrong problem type or solution path.")
        sys.exit()
    
    # check solution path
    if not param_3.endswith(".txt"):
        print("Error: The solution path must end with '.txt'.")
        sys.exit()
    
    #print('Instance size: ', param_1, " Instance name: ",param_2, " Solution path: ",param_3)
    print('Problem: ', param_1_convert, " Instance name: ",param_2, " Solution path: ",param_3)
    #main(instance_size=param_1,instance_name=param_2, solution_path=param_3)
    main(problem_type=param_1_convert, instance_name=param_2, solution_path=param_3)
