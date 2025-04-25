# VARIABLES GLOBALES
pos_actual = [] # Lista para almacenar posiciones actuales en la cadena
soluciones = [] # Lista de soluciones encontradas
cadena = "" # Cadena de entrada
N = 0 # Longitud objetivo 

# FUNCIONES

def generar_hijos(nivel : int) -> list:
    """ Genera y devuelve una lista de posibles opciones para el siguiente paso. """
    """ Lista de posibles índices """

    global pos_actual, cadena # Uso de las variables globales

    hijos=[] # Lista para almacenar los posibles índices

    if nivel > 0:
        inicio = pos_actual[-1] + 1 # Continuar después del último índice usado
    else:
        inicio = 0 # Iniciar desde el primer índice de la cadena

    for i in range(inicio, len(cadena)):
        hijos.append(i)

    return hijos

def es_solucion(candidatos : list) -> bool:
    """ Determina si la lista de candidatos representa una solución válida. """
    """ Verifica que tien longitud N """

    global N

    return len(candidatos) == N

def tratar_solucion(candidatos : list, soluciones : list):
    """ Realiza las acciones necesarias cuando se encuentra una solución. """
    """ Construye la cadena """

    global cadena

    if not candidatos: # Si no hay candidatos no hay solución válida
        return

    numero = ''
    for i in candidatos: # Construcción de la subsecuencia
        numero += cadena[i]
    if numero not in soluciones: # Evitar duplicados
        soluciones.append(numero)


def backtracking(candidatos : list, soluciones : list, nivel : int = 0) -> bool:
    """ Esquema para resolver problemas mediante backtracking """

    global pos_actual # Uso de la variable global

    # Caso Base: si se encuentra una solución válida
    if es_solucion(candidatos):                                     # (1)
        tratar_solucion(candidatos, soluciones)
        return False # Para que devuelva todas las soluciones posibles
    
    # Generación de posibles hijos (siguientes elementos)
    hijos = generar_hijos(nivel)                                    # (2)

    salir = False
    pos = 0

    # Exploración recursiva
    while pos < len(hijos) and not salir:                           # (3)
        candidatos.append(hijos[pos])
        pos_actual.append(hijos[pos])
        salir = backtracking(candidatos, soluciones, nivel + 1)
        candidatos.pop() # Backtrack: deshacer la elección actual
        pos_actual.pop()
        pos += 1
    return salir

# CASOS DE PRUEBA

casos_prueba = [
    ("", 2),  # Caso vacío
    ("1", 2),  # Cadena de un solo carácter
    ("123", 5),  # N mayor que la longitud de la cadena
    ("12345", 3),  # Caso normal con caracteres distintos
    ("22222", 3),  # Caso con números repetidos
    ("98765", 4),  # Números en orden descendente
    ("1111111111", 3),  # Caso extremo con caracteres repetidos
    ("13579", 2),  # Números impares
    ("24680", 4),  # Números pares
    ("1324354657", 3),  # Patrón no trivial
    ("99999999999999999999", 5),  # Cadena larga para rendimiento
]

for cadena, N in casos_prueba:
    soluciones = []
    pos_actual = []
    print(f"\nProbando con cadena: '{cadena}' y N = {N}")
    backtracking([], soluciones)
    if soluciones:
        print(f"Se encontraron soluciones: {soluciones}")
    else:
        print("No se encontraron soluciones")

# TEST

def test_generar_hijos_ejercicio3():

    global cadena, N

    # Caso 1: caso estándar
    cadena = "12345"
    pos_actual.clear()
    hijos1 = generar_hijos(0)
    resultados1 = [0, 1, 2, 3, 4]
    assert hijos1 == resultados1

    # Caso 2: Nivel mayor que 0
    pos_actual.append(1)
    hijos2 = generar_hijos(1)
    resultados2 = [2, 3, 4]
    assert hijos2 == resultados2

    # Caso 3: cadena vacía
    cadena = ""
    pos_actual.clear
    hijos3 = generar_hijos(0)
    resultados3 = []
    assert hijos3 == resultados3

    # Caso 4: cadena con un solo carácter
    cadena = "1"
    pos_actual.clear()
    hijos4 = generar_hijos(0)
    resultados4 = [0]
    assert hijos4 == resultados4

def test_es_solucion_ejercicio3():

    global N

    # Caso 1: solución válida
    N = 4
    assert es_solucion([0, 1, 2, 3])

    # Caso 2: no es solución
    assert not es_solucion([0, 1, 2])

    # Caso 3: caso vacío
    assert not es_solucion([])

    # Caso 4: caso mínimo N = 1
    N = 1
    assert es_solucion([0])

def test_tratar_solucion_ejercicio3():
    global cadena

    cadena = "115"  # Establece explícitamente la cadena esperada
    soluciones = []
    print(f"Probando con cadena: {cadena}")  # Depuración
    tratar_solucion([0, 1, 2], soluciones)
    resultado = ["115"]
    assert soluciones == resultado

    # Caso 1: guardado de solución nueva
    soluciones = []
    tratar_solucion([0, 1, 2], soluciones)
    resultado = ["115"]
    assert soluciones == resultado

    # Caso 2: la solución repetida no se añade
    tratar_solucion([0, 1, 2], soluciones)
    assert soluciones == resultado

    # Caso 3: candidatos vacíos no generan solución
    soluciones.clear()
    tratar_solucion([], soluciones)
    assert soluciones == []

def test_backtracking_ejercicio3():

    global cadena, N, soluciones, pos_actual

    #Caso 1: caso estándar con solución encontrada
    cadena = "12345"
    N = 3
    soluciones1 = []
    backtracking([], soluciones1)
    resultados1 = ["123", "124", "125", "134", "135", "145", "234", "235", "245", "345"]
    assert sorted(soluciones1) == sorted(resultados1)

    # Caso 2: caso sin solución (N es mayor que la longitud)
    cadena = "12"
    N = 3
    soluciones2 = []
    backtracking([], soluciones2)
    assert soluciones2 == []
    
    # Caso 3: todos los caracteres son iguales
    cadena = "2222"
    N = 2
    soluciones3 = []
    backtracking([], soluciones3)
    resultados3 = ["22"]
    assert sorted(soluciones3) == sorted(resultados3)

    # Caso 4: caso cadena vacía
    cadena = ""
    N = 2
    soluciones4 = []
    backtracking([], soluciones4)
    assert soluciones4 == []