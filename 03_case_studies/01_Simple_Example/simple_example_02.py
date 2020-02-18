# SIMPLE EXAMPLE 02 - general LP model (concrete model)

from pyomo.environ import *

"""
	min x1 + 2x2
	st. 3x1 + 4x2 >= 1
	    2x1 + 5x2 >= 2
		x1,x2>=0

	min sum(i, ci * xi)
	st. sum(i, aij * xi) >= bj   for all j = 1....m
		xi>=0                    for all i = 1...n

From Pyomo Optimization Modeling in Python (2nd Ed, 2017).
ISBN 978-3-319-58821-6 (eBook)
   William E. Hart , Carl D. Laird, Jean-Paul Watson, David L. Woodruff,
   Gabriel A. Hackebeil, Bethany L. Nicholson, John D. Siirola
"""

# Problem data
I = [1,2] # variables
J = [1,2] # constraints

a = {(1,1):3, (1,2):4, (2,1):2, (2,2):5} # constraint coefficients
b = {1:1, 2:2}                           # constraint constant terms
c = {1:1, 2:2}                           # objective function coefficients


# Create model object
model = ConcreteModel()

# Variable declarations
x = model.x = Var (I, within = NonNegativeReals)

# Constraint declarations
def con_rule(model, j):
    return sum(a[j,i] * x[i] for i in I) >= b[j]
model.con = Constraint(J, rule = con_rule )


# Objective Function declaration
def obj_rule(model):
	return sum(c[i] * x[i] for i in I)
model.objfunc = Objective(rule = obj_rule)

# Solver call
SolverFactory('glpk').solve(model, tee = True)

# Print results
model.pprint()
