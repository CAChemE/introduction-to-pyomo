# ===================================================================== #
#                     SUDOKU PROBLEM                                    #
# ===================================================================== #
import logging
from pyomo.environ import *
import pandas as pd

'''
Se trata de resolver un sudoku. Así, a las bravas.
'''

## LECTURA DE DATOS
# Leemos los datos que tan bonitamente ordenados vienen en el excel
data_sudoku = pd.read_excel('sudoku_data_1.xlsx', index_col = 0)
row = data_sudoku.index.tolist()
col = data_sudoku.columns.tolist()

## DEFINICIÓN DEL MODELO
# Usaremos un modelo concreto
m = ConcreteModel()

## SETS
# Tendremos un set para las columnas y otro para las filas, así como
# uno que indica qué numero debe usarse.
r = m.r = Set(initialize = row, ordered = True, doc = 'Indica la fila')
c = m.c = Set(initialize = col, ordered = True, doc = 'Indica la columna')
k = m.k = Set(initialize = [1,2,3,4,5,6,7,8,9], ordered = True, doc = 'Indica el número')

# También necesitaremos un set que relacione las celdillas 3x3. Para crearlo que
# crear una serie de bloques. Hay nueve.
b = m.b = Set(initialize = ['b'+str(i+1) for i in range(9)], ordered = True, doc = 'Bloques')
# Creamos ahora el mapeado
mapping = {
    'b1':('r1','r2','r3'),
    'b2':('r1','r2','r3'),
    'b3':('r1','r2','r3'),

    'b4':('r4','r5','r6'),
    'b5':('r4','r5','r6'),
    'b6':('r4','r5','r6'),

    'b7':('r7','r8','r9'),
    'b8':('r7','r8','r9'),
    'b9':('r7','r8','r9'),
}
# Creamos el set de relación y añadimos valores.
br = m.br = Set(within = b*r, ordered = True, doc = 'Relaciones de sets: Bloques - Filas')
for s in mapping:
    for ss in mapping[s]:
        br.add((s,ss))
# Hacemos lo mismo con el de columnas
mapping2 = {
    'b1':('c1','c2','c3'),
    'b2':('c4','c5','c6'),
    'b3':('c7','c8','c9'),

    'b4':('c1','c2','c3'),
    'b5':('c4','c5','c6'),
    'b6':('c7','c8','c9'),

    'b7':('c1','c2','c3'),
    'b8':('c4','c5','c6'),
    'b9':('c7','c8','c9'),    
}
bc = m.bc = Set(within = b*c, ordered = True, doc = 'Relaciones de sets: Bloques - Columnas')
for s in mapping2:
    for ss in mapping2[s]:
        bc.add((s,ss))

# Tenemos que unir estos dos sets también en uno triple.
brc = m.brc = Set(within = b*r*c, ordered = True)
for s in br:
    for ss in bc:
        if s[0] == ss[0]:
            brc.add((s[0],s[1],ss[1]))



## PARAMETERS
# El primer parámetro son los datos que nos da el sudoku. Para esto, lo
# creamos usando un diccionario.
givens = {}
for i in r:
    for j in c:
        givens[i,j] = data_sudoku.at[i,j]
# Vamos a usar estos datos a continuación para fijar unas binarias. No se introducen
# al modelo como parámetros.

## VARIABLES
# Hay que crear unas binarias. Las binarias dependerán de tres sets. La fila, la columna,
# y el número.
y = m.y = Var(r,c,k, domain = Binary)

# Ahora tenemos que fijar las que sepamos ya que están. Esto lo hacemos con givens.
for i in r:
    for j in c:
        for z in k:
            value = int(givens[i,j] == z)
            if value == 1:
                y[i,j,z].fix(1)
for i in y:
    if y[i].value != None:
        print(y[i], ' esta fija en: ', y[i].value)

## RESTRICCIONES
# Se crean las restricciones necesarias.
# - R1: Solo un valor por fila.
def R1(m, rr, kk):
    return sum(y[rr,cc,kk] for cc in c) == 1
m.R1 = Constraint(r,k, rule = R1, doc = 'Las filas no deben repetir números')
# - R2: Solo un valor por columna.
def R2(m, cc, kk):
    return sum(y[rr,cc,kk] for rr in r) == 1
m.R2 = Constraint(c,k, rule = R2, doc = 'Las columnas no deben repetir números')
# - R3: Cada celda del sudoku debe tener un numerito dentro
def R3(m, rr, cc):
    return sum(y[rr,cc,kk] for kk in k) ==1
m.R3 = Constraint(r,c, rule = R3, doc = 'Cada celda debe tener su número')
# - R4: En cada bloque 3x3 solo debe haber el mismo número una vez
def R4(m, bb, kk):
    return sum(y[rr,cc,kk] for rr in r for cc in c if (bb,rr,cc) in brc) == 1
m.R4 = Constraint(b,k, rule = R4, doc = 'Los bloques 3x3 no deben repetir números')

## FUNCIÓN OBJETIVO
# No es necesario una. Se crea una dummy.
m.OBJ = Objective(expr = 1)

## VERBATIM DE RESOLUCIÓN
from pyomo.opt import SolverFactory
opt = SolverFactory('glpk')
results = opt.solve(m)
results.write()

## LOGGING
# Se crea el logger y se da el nivel
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Se crea el formateador
formatter = logging.Formatter('%(message)s')
# Se crea lo que tratará el archivo y se le asigna el formateador
file_handler = logging.FileHandler(__file__[:-3] + '_Logging.log', mode='w')
file_handler.setFormatter(formatter)
# Se empieza a añadir cosas
logger.addHandler(file_handler)

# Creamos una función para acelerarlo:
def archivar(x, tipo='constraint'):
    parrafo = '\n{0}: {1} ----------------\n'.format(x, x.doc)
    for i in x:
        if tipo == 'constraint':
            parrafo += '\n{0}'.format(x[i].expr)
        elif tipo == 'parameter':
            parrafo += '\n{0} = {1}'.format(i, x[i])
        elif tipo == 'variable':
            parrafo += '\n{0} = {1}'.format(i, x[i].value)
        elif tipo == 'binaria':
            if x[i].value == 1:
                parrafo += '\n{0} = {1}'.format(i, x[i].value)
    return parrafo

logger.info(results)
logger.info('\n========== OBJECTIVE FUNCTION ==========')
logger.info(m.OBJ.expr)
logger.info('\nEl valor de la función objetivo es: ')
logger.info(m.OBJ.expr())
logger.info('========================================')
logger.info('\n============== CONSTRAINTS ==============')
logger.info(archivar(m.R1))
logger.info(archivar(m.R2))
logger.info(archivar(m.R3))
logger.info(archivar(m.R4))
logger.info('=========================================')
logger.info('\n==================================== VARIABLES ====================================')
logger.info(archivar(m.y, tipo='binaria'))
logger.info('===================================================================================')

## GRABAMOS EL SUDOKU RESUELTO
resuelto = data_sudoku[:]
for i in m.y:
    fila = i[0]
    columna = i[1]
    numero = i[2]
    if m.y[i].value == 1:
        resuelto.loc[fila, columna] = numero

print(resuelto)
resuelto.to_excel('sudoku_resuelto.xlsx')