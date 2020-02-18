"""
*-------------------------------------------------------------------------------
*                         #### NON SHARP SEPARATION ####
*-------------------------------------------------------------------------------
                                                                Juan Javaloyes
                                                                nov 2019
 -------------------------------------------------------------------------------

* Source: Grado Ingeniería Química. Universidad de Alicante.
          Asignatura: Simulaicón, optimización y diseño de procesos químicos

"""


"""
 PROBLEM STATMENT:

"""

from pyomo.environ import *

# Create model object
model = ConcreteModel(name = "NON SHARP SEPARATION ")

# SETS -------------------------------------------------------------------------
# Components (I)
I = model.I = Set(initialize = ['A', 'B', 'C'], ordered = True, doc = 'components')


# Conventional distillation columns (C)
C = model.C = Set(initialize = ['c1', 'c2', 'c3', 'c4', 'c5'], ordered = True, doc = 'distillation columns')
C0 = model.C0 = Set(initialize = ['c1', 'c2', 'c3'], ordered = True, doc = 'distillation columns')
# ALIAS
II = model.II = SetOf(model.I)

# PARAMETERS -------------------------------------------------------------------
# Feed stream component molar flow {kmol/h}
F0 = {'A': 20, 'B': 30, 'C': 50}

# > Column fixed cost
FC = {'c1': 100, 'c2': 100, 'c3': 100, 'c4': 75, 'c5': 30}

# > Column variable cost
VC = {'c1': 20, 'c2': 10, 'c3': 15, 'c4': 8, 'c5': 5}

# Column Component fraction in distillate
x = { ('c1', 'A'): 0.98, ('c1', 'B'): 0.02, ('c1', 'C'): 0.00,
      ('c2', 'A'): 0.98, ('c2', 'B'): 0.50, ('c2', 'C'): 0.02,
      ('c3', 'A'): 0.98, ('c3', 'B'): 0.98, ('c3', 'C'): 0.02,
      ('c4', 'A'): 1.00, ('c4', 'B'): 0.98, ('c4', 'C'): 0.02,
      ('c5', 'A'): 0.98, ('c5', 'B'): 0.02, ('c5', 'C'): 0.00,
     }


# VARIABLES --------------------------------------------------------------------
# > Continuous Variables
col_cost = model.col_cost = Var(C, domain = NonNegativeReals, doc = 'distillation column c cost')

F = model.F = Var(C, I, domain = NonNegativeReals, doc = 'Feed stream to column c and component i')
D = model.D = Var(C, I, domain = NonNegativeReals, doc = 'Distillate product of column c and component i')
B = model.B = Var(C, I, domain = NonNegativeReals, doc = 'Bottoms product of column c and component i')

S1 = model.S1  = Var(I, domain = NonNegativeReals, doc = 'Feed stream bypass to node A')
S2 = model.S2  = Var(I, domain = NonNegativeReals, doc = 'Feed stream bypass to node B')
S3 = model.S3  = Var(I, domain = NonNegativeReals, doc = 'Feed stream bypass to node C')

ProdA = model.ProdA = Var(I, domain = NonNegativeReals, doc = 'Product stream rich in product A')
ProdB = model.ProdB = Var(I, domain = NonNegativeReals, doc = 'Product stream rich in product B')
ProdC = model.ProdC = Var(I, domain = NonNegativeReals, doc = 'Product stream rich in product C')

# > Binary Variables
y = model.y = Var(C, domain = Binary, doc = '1 if column c is selected. 0 otherwise')

# MODEL CONSTRAINTS EQUATIONS --------------------------------------------------
# I components {A, B, C}
# C columns {c}

# > Global Constraints

  # - Material balance in feed node
def MB_feed_node_rule(model, i):
    return F0[i] == S1[i] + S2[i] + S3[i] + F['c1', i] + F['c2', i] + F['c3', i]
model.MB_feed_node = Constraint(I, rule = MB_feed_node_rule)

#   - Material balance in column c4 node
def MB_feed_column_c4_rule(model, i):
    return F['c4', i] == B['c1', i] + B['c2', i]
model.MB_feed_column_c4 = Constraint(I, rule = MB_feed_column_c4_rule)

#   - Material balance in column c5 node
def MB_feed_column_c5_rule(model, i):
    return F['c5', i] == D['c2', i] + D['c3', i]
model.MB_feed_column_c5 = Constraint(I, rule = MB_feed_column_c5_rule)

#   - Material balance in node A
def MB_node_A_rule(model, i):
    return ProdA[i] == S1[i] + D['c1', i] + D['c5', i]
model.MB_node_A = Constraint(I, rule = MB_node_A_rule)

#   - Material balance in node B
def MB_node_B_rule(model, i):
    return ProdB[i] == S2[i] + D['c4', i] + B['c5', i]
model.MB_node_B = Constraint(I, rule = MB_node_B_rule)

#   - Material balance in node C
def MB_node_C_rule(model, i):
    return ProdC[i] == S3[i] + B['c3', i] + B['c4', i]
model.MB_node_C = Constraint(I, rule = MB_node_C_rule)

#   - Feed Splitter composition equality
# (stream S1)
def splitter_S1_rule(model, i):
    return sum(S1[ii] for ii in II) * F0[i] == sum(F0[ii] for ii in II) * S1[i]
model.splitter_S1 = Constraint(I, rule = splitter_S1_rule)

# (stream S2)
def splitter_S2_rule(model, i):
    return sum(S2[ii] for ii in II) * F0[i] == sum(F0[ii] for ii in II) * S2[i]
model.splitter_S2 = Constraint(I, rule = splitter_S2_rule)

# (stream S3)
def splitter_S3_rule(model, i):
    return sum(S3[ii] for ii in II) * F0[i] == sum(F0[ii] for ii in II) * S3[i]
model.splitter_S3 = Constraint(I, rule = splitter_S3_rule)

# (stream F for c1, c2 and c3)
def splitter_F_rule(model, c, i):
    if (c in ['c1', 'c2', 'c3']):
        return sum(F[c, ii] for ii in II) * F0[i] == sum(F0[ii] for ii in II) * F[c, i]
model.splitter_F = Constraint(C0, I, rule = splitter_F_rule)

#   - Distillation column material balance
def MB_distillation_column_rule(model, c, i):
    return F[c, i] == D[c, i] + B[c, i]
model.MB_distillation_column = Constraint(C, I, rule = MB_distillation_column_rule)

#   - Distillate product stream
def distillate_product_rule(model, c, i):
    return D[c, i] == F[c, i] * x[c, i]
model.distillate_product = Constraint(C, I, rule = distillate_product_rule)


# > Disjunctions (Convex Hull reformulation)
def column_cost_rule(model, c):
    return col_cost[c] == FC[c] * y[c] + VC[c] * sum( D[c, i] for i in I )
model.column_cost = Constraint(C, rule = column_cost_rule)

def column_feed_ub_rule(model, c, i):
    return F[c,i] <= F0[i] * y[c]
model.column_feed_ub = Constraint(C, I, rule = column_feed_ub_rule)


# > Logic Propositions
# Y1 V Y2 V Y3
def logic_proposition_1_rule(model):
    return sum(y[c] for c in C if c in ['c1', 'c2', 'c3']) == 1
model.logic_proposition_1 = Constraint(rule = logic_proposition_1_rule)

# Y1 ==> Y4
def logic_proposition_2_rule(model):
    return y['c1'] - y['c4'] <= 0
model.logic_proposition_2 = Constraint(rule = logic_proposition_2_rule)

# Y1 ==> ¬ Y5
def logic_proposition_3_rule(model):
    return  y['c1'] + y['c5']  <= 1
model.logic_proposition_3 = Constraint(rule = logic_proposition_3_rule)


# OBJECTIVE FUNCTION  ----------------------------------------------------------
def obj_rule(model):
   return sum( col_cost[c] for c in C )
model.obj_rule = Objective (rule = obj_rule, sense = minimize )


# FIXED VALUES -----------------------------------------------------------------
# Product Stream A specifications
ProdA['A'].setlb(0.80 * F0['A'])
ProdA['B'].setub(0.15 * F0['B'])
ProdA['C'].setub(0.05 * F0['C'])

# Product Stream B specifications
ProdB['A'].setub(0.10 * F0['A'])
ProdB['B'].setlb(0.80 * F0['B'])
ProdB['C'].setub(0.10 * F0['C'])

# Product Stream B specifications
ProdC['A'].setub(0.05 * F0['A'])
ProdC['B'].setub(0.10 * F0['B'])
ProdC['C'].setlb(0.80 * F0['C'])

# SOLVER CALL ------------------------------------------------------------------
# > Pyomo solver library
SolverFactory("glpk").solve(model, tee = True)



# Print results
model.pprint()

# > Objective function
print(' ** Objective function: {0:0.3f}  **'.format(model.obj_rule.expr() ))

# > Binary Variable (distillation columns selected)
for c in y:
    if y[c] == 1:
        print(' ** Distillation column {} is selected'.format(c))
