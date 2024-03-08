# -*- coding: utf-8 -*-

'''The JSON files are converted from the **text file format** by `text2json.py` Python script from the [iRB-Lab's repository](https://github.com/iRB-Lab/py-ga-VRPTW). See [iRB-Lab's repository](https://github.com/iRB-Lab/py-ga-VRPTW#json-format) for the detailed description of the JSON file format. '''

import os
import io
import fnmatch
from json import load, dump
from . import BASE_DIR


def make_dirs_for_file(path):
    '''gavrptw.uitls.make_dirs_for_file(path)'''
    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass


def guess_path_type(path):
    '''gavrptw.uitls.guess_path_type(path)'''
    if os.path.isfile(path):
        return 'File'
    if os.path.isdir(path):
        return 'Directory'
    if os.path.islink(path):
        return 'Symbolic Link'
    if os.path.ismount(path):
        return 'Mount Point'
    return 'Path'


def exist(path, overwrite=False, display_info=True):
    '''gavrptw.uitls.exist(path, overwrite=False, display_info=True)'''
    if os.path.exists(path):
        if overwrite:
            if display_info:
                print(f'{guess_path_type(path)}: {path} exists. Overwrite.')
            os.remove(path)
            return False
        if display_info:
            print(f'{guess_path_type(path)}: {path} exists.')
        return True
    if display_info:
        print(f'{guess_path_type(path)}: {path} does not exist.')
    return False


def load_instance(json_file):
    '''gavrptw.uitls.load_instance(json_file)'''
    if exist(path=json_file, overwrite=False, display_info=True):
        with io.open(json_file, 'rt', encoding='utf-8', newline='') as file_object:
            return load(file_object)
    return None

def load_solution(filepath):
    with open(filepath, 'r') as file:
        routes = []
        for line in file:
            # split the line into words
            words = line.split(":")[1].split()
            # create a list to store the integers in this line
            integers = []
            # iterate over the words and extract the integers
            for word in words:
                # check if the word is an integer
                if word.isdigit():
                    # convert the word to an integer and add it to the list of integers
                    integers.append(int(word))
            # add the list of integers for this line to the list of lists of integers
            routes.append(integers)
    return routes


def calculate_distance(customer1, customer2):
    '''gavrptw.uitls.calculate_distance(customer1, customer2)'''
    return ((customer1['coordinates']['x'] - customer2['coordinates']['x'])**2 + \
        (customer1['coordinates']['y'] - customer2['coordinates']['y'])**2)**0.5

def cvrp2json(customize=False):
    text_data_dir = os.path.join(BASE_DIR, 'Instances/CVRP','vrp_customize' if customize else 'vrp')
    json_data_dir = os.path.join(BASE_DIR, 'Instances/CVRP', 'json_customize' if customize else 'json')
        
    for text_file in map(lambda text_filename: os.path.join(text_data_dir, text_filename), \
        fnmatch.filter(os.listdir(text_data_dir), '*.vrp')):
        
        json_data = {}
        
        with io.open(text_file, 'rt', encoding='utf-8', newline='') as file_object:
            j = 0; i = 0; lines = [];
            
            line = file_object.readline().strip('\n')
            if line.__contains__("NAME"):
                    ins_name = line.lstrip('NAME : ')
                    json_data['instance_name'] = ins_name
            
            while line:
                lines.append(line)
                line = file_object.readline().strip('\n')

                # <Instance name>

                # <Maximum vehicle number>, <Vehicle capacity>
                if line.__contains__("DIMENSION"):
                    dimension = int(line.lstrip('DIMENSION : '))
                    json_data['max_vehicle_number'] = int(dimension)
                if line.__contains__("CAPACITY"):
                    capacity = int(line.lstrip('CAPACITY : '))
                    json_data['vehicle_capacity'] = float(capacity)

                # Custom number = 0, depart
                # <Custom number>, <X coordinate>, <Y coordinate>, <Demand>

                if line.__contains__("NODE_COORD_SECTION"):
                    line = file_object.readline().strip('\n')
                    while not line.__contains__("DEMAND_SECTION"):

                        if "\t" in line:
                            values = line.strip().split("\t")
                        else:
                            values = line.strip().split(" ")
                        json_data[f'customer_{values[0]}'] = {
                            'coordinates': {
                                'x': float(values[1]),
                                'y': float(values[2]),
                            }
                        }
                        line = file_object.readline().strip('\n')
                if line.__contains__("DEMAND_SECTION"):
                    line = file_object.readline().strip('\n')
                    while not line.__contains__("DEPOT_SECTION"):
                        #a, self.things[i] = line.strip().split(" ")
                        #i = int(a)
                        #line = f.readline().strip('\n')
                        if "\t" in line:
                            values_demand = line.strip().split("\t")
                        else:
                            values_demand = line.strip().split(" ")
                        #json_data[f'customer_{values_demand[0]}'] = {
                            #'demand': float(values_demand[1]),
                        #}
                        json_data[f'customer_{values_demand[0]}']['demand'] = float(values_demand[1])
                        line = file_object.readline().strip('\n')

                depot_id = []
                if line.__contains__("DEPOT_SECTION"):
                    depot_start = file_object.readline().strip('\n')
                    depot_start = int(depot_start.strip())
                    json_data['depart'] = {
                        'coordinates': {
                            'x': json_data[f'customer_{int(depot_start)}']['coordinates']['x'],
                            'y': json_data[f'customer_{int(depot_start)}']['coordinates']['y'],
                        },
                        'demand': json_data[f'customer_{depot_start}']['demand'],
                    }
                    if(depot_start==1):
                        # Create a new dictionary to store the updated data
                        updated_json_data = {}

                        # Flag to indicate if the first customer key has been removed
                        customer_removed = False

                        # Iterate through the keys of the original dictionary
                        for key, value in json_data.items():
                            if key.startswith('customer_'):
                                # Skip 'customer_1'
                                if key == 'customer_1':
                                    customer_removed = True
                                    continue
                                # Extract the index from the key
                                index = int(key.split('_')[1])
                                # Generate the new customer key
                                new_key = f'customer_{index - 1 if customer_removed else index}'
                                # Add the value with the new key to the updated dictionary
                                updated_json_data[new_key] = value
                            else:
                                # For non-customer keys, simply copy them to the updated dictionary
                                updated_json_data[key] = value
                    else:
                        print("Warning: depot issue - instance "+input_path)
                    break

        customers = ['depart'] + [f'customer_{x}' for x in range(1, dimension)]
        #customers = ['depart'] + [f'customer_{x}' for x in range(1, dimension+1)]
        #json_data['distance_matrix'] = [[calculate_distance(json_data[customer1], \
                #json_data[customer2]) for customer1 in customers] for customer2 in customers]
        updated_json_data['distance_matrix'] =[[round(calculate_distance(updated_json_data[customer1], \
                                                                         updated_json_data[customer2])) \
                                                for customer1 in customers] for customer2 in customers]

        #json_file_name = f"{updated_json_data['instance_name']}.json"  
        pathname = text_file[: text_file.rfind(".vrp")] + ".json"
        json_file_name = os.path.basename(pathname)
        
        json_file = os.path.join(json_data_dir, json_file_name)
        print(f'Write to file: {json_file}')
        make_dirs_for_file(path=json_file)
        with io.open(json_file, 'wt', encoding='utf-8', newline='') as file_object:
            dump(updated_json_data, file_object, sort_keys=True, indent=4, separators=(',', ': '))


def cvrptw2json(customize=False):
    text_data_dir = os.path.join(BASE_DIR, 'Instances/CVRPTW','txt_customize' if customize else 'txt')
    json_data_dir = os.path.join(BASE_DIR, 'Instances/CVRPTW', 'json_customize' if customize else 'json')
    
    for text_file in map(lambda text_filename: os.path.join(text_data_dir, text_filename), \
        fnmatch.filter(os.listdir(text_data_dir), '*.txt')):
        json_data = {}
        with io.open(text_file, 'rt', encoding='utf-8', newline='') as file_object:
            for line_count, line in enumerate(file_object, start=1):
                if line_count in [2, 3, 4, 6, 7, 8, 9]:
                    pass
                elif line_count == 1:
                    # <Instance name>
                    json_data['instance_name'] = line.strip()
                elif line_count == 5:
                    # <Maximum vehicle number>, <Vehicle capacity>
                    values = line.strip().split()
                    json_data['max_vehicle_number'] = int(values[0])
                    json_data['vehicle_capacity'] = float(values[1])
                elif line_count == 10:
                    # Custom number = 0, depart
                    # <Custom number>, <X coordinate>, <Y coordinate>,
                    # ... <Demand>, <Ready time>, <Due date>, <Service time>
                    values = line.strip().split()
                    json_data['depart'] = {
                        'coordinates': {
                            'x': float(values[1]),
                            'y': float(values[2]),
                        },
                        'demand': float(values[3]),
                        'ready_time': float(values[4]),
                        'due_time': float(values[5]),
                        'service_time': float(values[6]),
                    }
                else:
                    # <Custom number>, <X coordinate>, <Y coordinate>,
                    # ... <Demand>, <Ready time>, <Due date>, <Service time>
                    values = line.strip().split()
                    json_data[f'customer_{values[0]}'] = {
                        'coordinates': {
                            'x': float(values[1]),
                            'y': float(values[2]),
                        },
                        'demand': float(values[3]),
                        'ready_time': float(values[4]),
                        'due_time': float(values[5]),
                        'service_time': float(values[6]),
                    }
        
        total_customers = 0
        for key in json_data.keys():
            if key.startswith('customer_'):
                total_customers += 1
        customer_num = total_customers
        
        customers = ['depart'] + [f'customer_{x}' for x in range(1, customer_num+1)]
        json_data['distance_matrix'] = [[calculate_distance(json_data[customer1], \
            json_data[customer2]) for customer1 in customers] for customer2 in customers]
        json_file_name = f"{json_data['instance_name']}.json"
        json_file = os.path.join(json_data_dir, json_file_name)
        print(f'Write to file: {json_file}')
        make_dirs_for_file(path=json_file)
        with io.open(json_file, 'wt', encoding='utf-8', newline='') as file_object:
            dump(json_data, file_object, sort_keys=True, indent=4, separators=(',', ': '))