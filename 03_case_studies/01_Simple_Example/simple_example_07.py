
# SIMPLE EXAMPLE 06 -  general LP model (abstract model).

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


# Create model object
model = AbstractModel()

# Set declarations
model.I = Set(doc = 'set of variables')
model.J = Set(doc = 'set of constraints')

# Parameter declarations
model.a = Param(model.J, model.I)
model.b = Param(model.J)
model.c = Param(model.I)


# Variable declarations
model.x = Var (model.I, within = NonNegativeReals)

# Constraint declarations
def con_rule(model, j):
    return sum(model.a[j,i] * model.x[i] for i in model.I) >= model.b[j]
model.con = Constraint(model.J, rule = con_rule )


# Objective Function declaration
def obj_rule(model):
	return sum(model.c[i] * model.x[i] for i in model.I)
model.objfunc = Objective(rule = obj_rule)

# Solver call
instance = model.create_instance('abstract.dat')
SolverFactory('glpk').solve(instance, tee = True)

# Print results
instance.pprint()
