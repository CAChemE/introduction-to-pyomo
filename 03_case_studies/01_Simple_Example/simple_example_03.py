
# SIMPLE EXAMPLE 03 -  general LP model (concrete model). Load data from file

from pyomo.environ import *

"""
	min sum(i, ci * xi)
	st. sum(i, aij * xi) >= bj   for all j = 1....m
		xi>=0                    for all i = 1...n

From Pyomo Optimization Modeling in Python (2nd Ed, 2017).
ISBN 978-3-319-58821-6 (eBook)
   William E. Hart , Carl D. Laird, Jean-Paul Watson, David L. Woodruff,
   Gabriel A. Hackebeil, Bethany L. Nicholson, John D. Siirola
"""

# Problem data
import simple_example_data as data

# Create model object
model = ConcreteModel()

# Variable declarations
x = model.x = Var (data.I, within = NonNegativeReals)

# Constraint declarations
def con_rule(model, j):
    return sum(data.a[j,i] * x[i] for i in data.I) >= data.b[j]
model.con = Constraint(data.J, rule = con_rule )


# Objective Function declaration
def obj_rule(model):
	return sum(data.c[i] * x[i] for i in data.I)
model.objfunc = Objective(rule = obj_rule)

# Solver call
SolverFactory('glpk').solve(model, tee = True)

# Print results
model.pprint()
