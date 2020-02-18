
# SIMPLE EXAMPLE 01 - single instance of a LP model (concrete model)

from pyomo.environ import *

"""
	min x1 + 2x2
	st. 3x1 + 4x2 >= 1
	    2x1 + 5x2 >= 2
		x1,x2>=0

From Pyomo Optimization Modeling in Python (2nd Ed, 2017).
ISBN 978-3-319-58821-6 (eBook)
   William E. Hart , Carl D. Laird, Jean-Paul Watson, David L. Woodruff,
   Gabriel A. Hackebeil, Bethany L. Nicholson, John D. Siirola
"""

#
# Create model object
model = ConcreteModel()

# Variable declarations
x1 = model.x1 = Var (within = NonNegativeReals)
x2 = model.x2 = Var (within = NonNegativeReals)

# Constraint declarations
model.con1 = Constraint(expr = 3 * x1 + 4 * x2 >= 1)
model.con2 = Constraint(expr = 2 * x1 + 5 * x2 >= 2)

# Objective Function declaration
model.objfunc = Objective(expr = x1 + 2 * x2)

# Solver call
SolverFactory('glpk').solve(model, tee = True)

# Print results
model.pprint()
