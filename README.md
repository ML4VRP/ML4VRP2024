<img src="logo.png" alt="ML4VRP Logo" width="215">

# ML4VRP Competition Resources

This repository is used for the Machine Learning for Evolutionary Computation - for Vehicle Routing Problems ([ML4VRP](https://sites.google.com/view/ml4vrp)) competition in [GECCO 2024](https://gecco-2024.sigevo.org/Competitions#id_Machine%20Learning%20for%20Evolutionary%20Computation%20-%20Solving%20the%20Vehicle%20Routing%20Problems%20(ML4VRP)). 

<!--This competition aims to serve as a vehicle to bring together the latest developments of machine learning-assisted evolutionary computation for vehicle routing problems (VRPs). The focus of this competition is on solving VRP with Time Window constraints (VRPTW). 

Participants must submit descriptions of the developed algorithms and the produced solutions for the corresponding VRPTW instances. Submissions of the produced solutions for the corresponding VRPTW instances will be evaluated on randomly selected instances from the provided VRPTW instances with an evaluator. The most widely adapted evaluation function, i.e. to minimise the number of vehicles and total travel distance, is used to determine the best machine learning assisted evolutionary algorithms for solving VRPs. The algorithms which produced the best average fitness for solving VRPs will receive the highest score. -->

In this repository, you will find:
- [Problem Instances](#vrps) for the competition
- - [CVRP](#cvrp)
- - [CVRPTW](#cvrptw)
- [Solution Evaluator](#api)

## <a id='vrps'>VRP Problem Instances </a>
### <a id='cvrp'>CVRP </a>
The Uchoa dataset [Uchoa17] is one of the most widely studied CVRP benchmark data sets. This data set covers different instance features, such as depot positioning, customer positioning, demand distribution etc, allowing a comprehensive assessment of algorithm performance. 

The problem instances provided in the competition are the Uchoa CVRP instances with customers ranging from 100 to 400, covering different instance types. The competition will evaluate the submitted solution results using a subset of the provided instances (unknown to the participants before the results are presented).


<details>
<summary><strong>More about instance file format</strong></summary>

The CVRP problem data can be found under the `Instances/CVRP/vrp/` directory. The JSON files corresponding to the problem instances can be found under the `Instances/CVRP/json/` directory. 

Each `.vrp` file and json file is named with respect to its corresponding instance name, e.g.: the files corresponding to problem instance **X-n101-k25** is located at
- `Instances/CVRP/vrp/X-n101-k25.vrp` and 
- `Instances/CVRP/json/X-n101-k25.json`. 

</details>

<details>
<summary><strong>More about instance description</strong></summary>

See the paper [New benchmark instances for the capacitated vehicle routing problem](http://vrp.galgos.inf.puc-rio.br/index.php/en/new-instances) for the detailed instance description.

</details>



### <a id='cvrptw'>CVRPTW </a>
Solomon [Sol87] dataset and Homberger and Gehring [HG99] data set are widely studied CVRPTW benchmark data sets. Both data sets consist of [six types of instances](http://web.cba.neu.edu/~msolomon/problems.htm), i.e., C1, C2, R1, R2, RC1, RC2, which differ with respect to the customers’ geographical locations, vehicle capacity, density and tightness of the time windows. 

<span style="color:red">

The problem instances provided in the competition are taken from two sources, i.e., 
- Solomon [Sol87] dataset of 100 customer problems,
- Homberger and Gehring [HG99] data sets of 200 customer problems and 400 customer problems.

</span>

The provided problem instances provided are randomly selected from these <span style="color:red">three</span> sized problem instances, covering different instance types. The competition will conduct the evaluation of the submitted solution results using a subset of the provided instances (unknown to the participants before the results are presented). 

The problem instances provided in the competition are available to download on <span style="color:red">the folder [Instances](https://github.com/ML4VRP2023/ML4VRP2023/tree/main/Instances)</span> of this repo. All the VRPTW instances can also be found in [CVRPLIB](http://vrp.galgos.inf.puc-rio.br/index.php/en/). 

In addition to the benchmark VRPTW instances, we provide an example problem instance `toy`, locating at 
- `Instances/CVRPTW/txt/Customer6/toy.txt` and 
- `Instances/CVRPTW/json/Customer6/toy.json`. 

<details>
<summary><strong>More about instance file format</strong></summary>

The text files corresponding to the problem instances can be found under the `Instances/CVRPTW/txt/` directory. The JSON files corresponding to the problem instances can be found under the `Instances/CVRPTW/json/` directory. 

Each txt file and json file is named with respect to its corresponding instance name, e.g.: the files corresponding to problem instance **C102** is located at
- `Instances/CVRPTW/txt/C102.txt` and 
- `Instances/CVRPTW/json/C102.json`. 

</details>

<details>
<summary><strong>More about instance description</strong></summary>

See [Solomon's website](http://web.cba.neu.edu/~msolomon/problems.htm) for the detailed instance description.

</details>
 

<!--Below is a description of the format of the text file that defines each problem instance (assuming 100 customers).

```
<Instance name>
<empty line>
VEHICLE
NUMBER     CAPACITY
  K           Q
<empty line>
CUSTOMER
CUST NO.  XCOORD.   YCOORD.    DEMAND   READY TIME  DUE DATE   SERVICE TIME
<empty line>
    0       x0        y1         q0         e0          l0            s0
    1       x1        y2         q1         e1          l1            s1
  ...      ...       ...        ...        ...         ...           ...
  100     x100      y100       q100       e100        l100          s100
```
-->



## <a id='api'>VRP Solution Evaluator </a>
<!--extended from the version used in ML4VRP2023-->

The solution evaluator has been extended from the version utilised in ML4VRP2023, with slight modifications to the syntax. Please keep reading &#x1F60A;

The Python script `evaluator.py` is the solution evaluation program to use. The solution evaluator takes a solution and the corresponding problem instance to
- check feasibility of the solution,
- calculate the objective function value of the solution (following the objective function as stated on the [competition website](https://sites.google.com/view/ml4vrp#h.8tn33nmddfdh)) for feasible solution.

### How to start

Let's prepare the environment and download the resources to work.
1. Download/clone the whole repository. Note the `Instances/` directory where **JSON file format** of the problem instances are essentially needed.
2. Install `Python 3`.
3. Install the [DEAP](https://github.com/deap/deap) framework in Python.
   ```bash
   pip install deap
   ```
4. Prepare the solution files in the specific format as described in the [competition website](https://sites.google.com/view/ml4vrp#h.j2mwimqjm1ge).


### Usage example
Navigating to the repository directory, use the following command in the terminal or command prompt:
```sh
python evaluator.py <problem_type> <instance_name> <path_to_solution_file>
```
Replace <problem_type>, <instance_name>, and <path_to_solution_file> with appropriate values.
- `<problem_type> `must be one of the following: `cvrp` or `cvrptw`.
- `<instance_name>` is the name of the instance you want to evaluate.
- `<path_to_solution_file>` is the path to the solution file you want to evaluate against.

<div class="alert alert-success" style="display: inline-block;">
For additional examples of usage, please refer to the <a href="./quick-start.ipynb">quick-start</a> notebook.
</div>


<!--Below are the examples, however, to maintain clarity and conciseness in this README, I have removed them.
### Example

#### Evaluation of a solution for a CVRP instance
The optimal solution for solving `X-n101-k25` are provided in `Solutions/cvrp` directory, i.e., `BKS-X-n101-k25.txt`.

To evaluate `BKS-X-n101-k25.txt`, run:
```sh
python evaluator.py cvrp X-n101-k25 Solutions/cvrp/BKS-X-n101-k25.txt
```
The output is (similar to) as shown below:
```sh
Problem:  cvrp  Instance name:  X-n101-k25  Solution path:  Solutions/cvrp/BKS-X-n101-k25.txt
File: .../Instances/cvrp/json/X-n101-k25.json exists.
Number of vehicles:  26 , Total distance:  27591 Objective value:  53591
```

#### Evaluation of a solution for a CVRPTW instance
Solutions for solving `toy` are provided in `Solutions/cvrptw` directory. 
- The solution file `toy_solution.txt` gives a feasible solution (in terms of the time window and vehicle capacity constraints).

To evaluate `toy_solution`, run:
```sh
python evaluator.py cvrptw toy Solutions/cvrptw/toy_solution.txt
```
The output is (similar to) as shown below:
```sh
Problem:  cvrptw  Instance name:  toy  Solution path:  Solutions/cvrptw/toy_solution.txt
File: .../Instances/cvrptw/json/toy.json exists.
Number of vehicles:  2 , Total distance:  153.82268590411263 Objective value:  2153.8226859041124
```

#### Evaluation of an infeasible solution
The solution file `toy_solution_infeasible.txt` provides an invalid solution for the example instance `toy`. 
When running:
```sh
python evaluator.py cvrptw toy Solutions/cvrptw/toy_solution_infeasible.txt
```
The infeasible solution cannot pass the feasibility check, thus no objective function value will be returned. The output is (similar to) as shown below:
```sh
Problem:  cvrptw  Instance name:  toy  Solution path:  Solutions/cvrptw/toy_solution_infeasible.txt
File: .../Instances/cvrptw/json/toy.json exists.
invalid capacity
invalid time window: too late to serve customer  6
The solution in infeasible!
```
-->
## File Structure
```
├── Instances/
│   ├── CVRP/
│   │   ├── json/
│   │   │   ├──<Instance name>.json
│   │   │   └── ...
│   │   ├── vrp/
│   │   │   ├──<Instance name>.vrp
│   │   │   └── ...
│   ├── CVRPTW/
│   │   ├── json/
│   │   │   ├──<Instance name>.json
│   │   │   └── ...
│   │   ├── txt/
│   │   │   ├──<Instance name>.txt
│   │   │   └── ...
├── vrp_evaluator/
│   ├── __init__.py
│   ├── core.py
│   └── utils.py
├── evaluator.py
├── Solutions
│   ├── cvrp/
│   │   ├── Instance name of the solution.txt
│   ├── cvrptw/
│   │   ├── toy_solution.txt
│   │   ├── toy_solution_infeasible.txt
├── README.md
└── logo.png
```

## Organisers
Rong Qu,         University of Nottingham, UK, rong.qu@nottingham.ac.uk

Nelishia Pillay, University of Pretoria, South Africa, nelishia.pillay@up.ac.za

Weiyao Meng, University of Nottingham, UK, weiyao.meng2@nottingham.ac.uk

<div class="alert alert-success" style="display: inline-block;">
Please contact <strong> Weiyao</strong> in case of any problems or if you require help for the problem instances and the solution evaluator in this repository.
</div>

## References
[HG99] J. Homberger and H. Gehring, "Two evolutionary metaheuristics for the vehicle routing problem with time windows," INFOR: Information Systems and Operational Research, 37(3):297–318, 1999. [PDF](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=a34e12bf0a30deb56233c26d82a0979987bb6ce4)

[Sol87] M. M. Solomon, "Algorithms for the vehicle routing and scheduling problems with time window constraints," Operations Research, 35(2):254–265, 1987. [PDF](https://www.jstor.org/stable/pdf/170697.pdf?casa_token=ltF2XRa2-nAAAAAA:OV4ClhhdAM_ds_p3-XIzKaz3hDYb9Jy2yHa7-jniGyYLzy2Rg2JC1b-ope2_gtsoQ1eOfFcgeTvtFmGZdPWDACEySwlfASLdRl-mhJRQE4f_6Kc5jJRnYg)

[Uchoa17] Uchoa, E., Pecin, D., Pessoa, A., Poggi, M., Vidal, T., & Subramanian, A. (2017). New benchmark instances for the capacitated vehicle routing problem. European Journal of Operational Research, 257(3), 845-858.