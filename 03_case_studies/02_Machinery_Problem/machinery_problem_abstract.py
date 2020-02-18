"""
*-------------------------------------------------------------------------------
*                           #### MACHINERY PROBLEM ####
**------------------------------------------------------------------------------


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
model = AbstractModel()

# Set declarations
model.M = Set(ordered = True)
model.S = Set(ordered = True)

# Parameter declarations
model.profit   = Param(model.M)
model.max_time = Param(model.S)
model.time_x_section = Param(model.M, model.S)

# Variable declarations
model.x = Var(model.M, within = PositiveIntegers)


# Constraint declarations
def constraint_rule(model, s):
 	return sum( model.time_x_section[m,s] * model.x[m] for m in model.M ) <= model.max_time[s]
model.constraint = Constraint(model.S, rule = constraint_rule)

# Objective Function
def obj_rule(model):
    return sum (model.profit[m] * model.x[m] for m in model.M)
model.objfunc = Objective (rule =obj_rule, sense = maximize )


# Solver call
instance = model.create_instance('machinery.dat')
SolverFactory('glpk').solve(instance, tee = True)

# Print results
instance.pprint()

