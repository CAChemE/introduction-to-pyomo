"""
*-------------------------------------------------------------------------------
*                           #### MACHINERY PROBLEM ####
*-------------------------------------------------------------------------------


* Source: Grado Ingeniería Química. Universidad de Alicante.
          Asignatura: Simulaicón, optimización y diseño de procesos químicos

"""


"""
 PROBLEM STATMENT:
    A company manufacture four types of machinery. The factory is divided in
    three sections. The first section has available 960 h/week, the second
    1110 h/week and the third 400 h/week. Each machinery unit requires the time
    given in "time_x_section" at each section.
    Determine the number of units of machinery for each type that should be
    manufacture per week to maximize profit.
"""

from pyomo.environ import *


# Create model object
model = ConcreteModel()

# Set declarations
M = model.M = Set(initialize =  ['m1', 'm2', 'm3', 'm4'], ordered = True)
S = model.S = Set(initialize =  ['s1', 's2', 's3'], ordered = True)

# Problem data
profit   = {'m1':  12, 'm2':    8, 'm3':  12, 'm4':17}
max_time = {'s1': 960, 's2': 1110, 's3': 400}

time_x_section = { ('m1','s1'): 6 , ('m1','s2'): 3 , ('m1','s3'): 2,
                   ('m2','s1'): 4 , ('m2','s2'): 3 , ('m2','s3'): 1,
				   ('m3','s1'): 4 , ('m3','s2'): 6 , ('m3','s3'): 2,
				   ('m4','s1'): 8 , ('m4','s2'): 9 , ('m4','s3'): 1}

#time_x_section_data = [ [6, 3,2], [4, 3, 1], [4, 6,2], [8,9,1]]
#time_x_section = {(ii, jj): time_x_section_data[i][j] for i,ii in enumerate(M) for j,jj in enumerate(S)}

# Variable declarations
x = model.x = Var(M, within = PositiveIntegers)


# Constraint declarations
def constraint_rule(model, s):
	return sum( time_x_section[m,s] * x[m] for m in M ) <= max_time[s]
model.constraint = Constraint(S, rule = constraint_rule)

# Objective Function
model.value = Objective( expr = sum( profit[m] * x[m] for m in M),
                         sense = maximize )

# Solver call
solver = SolverFactory('glpk')
results_solver = solver.solve(model, keepfiles = True)


# Print results
model.pprint()



