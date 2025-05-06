# VARIABLES GLOBALES
pos_actual = [] # Lista de posiciones durante la búsqueda 
soluciones = [] # Lista de soluciones encontradas
cadena = "" # Cadena inicial que se quiere transformar
objetivo = "" # Caracter objetivo al que se quiere reducir la cadena
tabla_sustitucion = { # Tabla de sustitución usada para la transformación
    'a': {'a': 'b', 'b': 'b', 'c': 'a', 'd': 'd'},
    'b': {'a': 'c', 'b': 'a', 'c': 'd', 'd': 'a'},
    'c': {'a': 'b', 'b': 'a', 'c': 'c', 'd': 'c'},
    'd': {'a': 'd', 'b': 'c', 'c': 'd', 'd': 'b'}
}

# FUNCIONES

def generar_hijos(cadena_actual : str) -> list:
    """ Genera y devuelve una lista de posibles opciones para el siguiente paso """
    
    hijos = [] # Lista donde se guardarán las posibles transformaciones

    # Itera sobre cada par de caracteres adyacentes en la cadena
    for i in range(len(cadena_actual) - 1):
        c1, c2 = cadena_actual[i], cadena_actual[i + 1]

        # Verificamos si la combinación existe en la tabla de sustitución
        if c1 in tabla_sustitucion and c2 in tabla_sustitucion[c1]:
            nuevo_caracter = tabla_sustitucion[c1][c2]
            # Generamos la nueva cadena
            nueva_cadena = cadena_actual[:i] + nuevo_caracter + cadena_actual[i + 2:]
            # Evitar agregar transformaciones idénticas al original
            if nueva_cadena != cadena_actual and nueva_cadena not in hijos:
                hijos.append(nueva_cadena)

    return hijos  

def es_solucion(candidatos : list) -> bool:
    """ Determina si la lista de candidatos representa una solución válida """
    global objetivo

    return candidatos and len(candidatos[-1]) == 1 and candidatos[-1] == objetivo

def tratar_solucion(candidatos : list, soluciones : list):
    """ Realiza las acciones necesarias cuando se encuentra una solución """
    resultado = candidatos[:]
    if resultado not in soluciones: # Evita agregar soluciones duplicadas
        soluciones.append(resultado)


def backtracking(candidatos : list, soluciones : list, nivel : int = 0):
    """ Esquema para resolver problemas mediante backtracking """
    global pos_actual # Usamos la variable global

    # Caso Base: si se encontró una solución válida
    if es_solucion(candidatos):                                     # (1)
        tratar_solucion(candidatos, soluciones)
        return True
    
    # Generación de posibles hijos (transformaciones siguientes)
    hijos = generar_hijos(candidatos[-1])                           # (2)

    for hijo in hijos:
        candidatos.append(hijo)
        pos_actual.append(hijo)
        backtracking(candidatos, soluciones, nivel + 1)
        candidatos.pop()  # Backtracking: deshacer la elección
        pos_actual.pop()

# CASOS DE PRUEBA

casos_prueba = [
    ("acabada", "d"),
    ("abcda", "d"),
    ("d", "d"),
    ("cccc", "d"),
    ("xyz", "d"),
    ("", "d"),
    ("a", "d"),
    ("abababa", "d")
]

for cadena, objetivo in casos_prueba:
    soluciones = []
    print(f"\nProbando con: {cadena} -> {objetivo}")
    backtracking([cadena], soluciones)
    if soluciones : 
        print(f"Se encontraron {len(soluciones)} soluciones:")
        for i, camino in enumerate(soluciones):
            print(f"Solución {i + 1}: {' → '.join(camino)}")
    else :
        print("No se encontró una forma de reducir la cadena al carácter objetivo")

# TEST

def test_generar_hijos_ejercicio6():

    # Caso 1: caso estándar
    cadena = "acabada"
    hijos1 = generar_hijos(cadena)
    resultado1 = ["aabada", "abbada", "acbada", "acacda", "acabda", "acabad"]
    assert set(hijos1) == set(resultado1) # Comparamos conjuntos para evitar errores por orden

    # Caso 2: caso sin hijos posibles
    cadena = "cccc"
    hijos2 = generar_hijos(cadena)
    assert hijos2 == ["ccc"]

    # Caso 3: caracteres desconocidos
    cadena = "xyz"
    hijos3 = generar_hijos(cadena) # Debería imprimir un aviso
    assert hijos3 == []

def test_es_solucion_ejercicio6():
    global objetivo
    objetivo = "d"

    # Caso 1: el último elemento es el objetivo
    assert es_solucion(["d"])

    # Caso 2: caso donde la cadena no es el objetivo
    assert not es_solucion(["acabada"])

    # Caso 3: la cadena es vacía
    assert not es_solucion([])

def test_tratar_solucion_ejercicio6():
    soluciones = []
    tratar_solucion(["acabada", "acacda", "abcda", "abcd", "bc", "d"], soluciones)
    assert soluciones == [["acabada", "acacda", "abcda", "abcd", "bc", "d"]]

def test_backtracking_ejercicio6():
    global objetivo
    objetivo = "d"

    # Caso 1: caso estándar con solución encontrada
    cadena = "acabada"
    soluciones1 = []
    backtracking([cadena], soluciones1)
    assert soluciones1

    # Caso 2: caso sin solución ´
    cadena = "cccc" 
    soluciones2 = [] 
    backtracking([cadena], soluciones2) 
    assert soluciones2 == [] 
    
    # Caso 3: caso con cadena que es el objetivo 
    cadena = "d" 
    soluciones3 = [] 
    backtracking([cadena], soluciones3) 
    assert soluciones3 == [["d"]]

# TEST DE RENDIMIENTO  

# Test de rendimiento para backtracking con caso pequeño
def test_backtracking_ejercicio6_benchmark(benchmark):
    global objetivo
    objetivo = "d"

    cadena = "acabada"
    soluciones = []

    def backtracking_funcion():
        backtracking([cadena], soluciones)
        assert soluciones  # Verifica que haya soluciones

    benchmark(backtracking_funcion)

# Test de rendimiento para caso sin solución
def test_backtracking_sin_solucion_benchmark(benchmark):
    global objetivo
    objetivo = "d"

    cadena = "cccc"
    soluciones = []

    def backtracking_funcion():
        backtracking([cadena], soluciones)
        assert soluciones == []  # No debería haber soluciones

    benchmark(backtracking_funcion)

# Test de rendimiento para caso donde la cadena ya es el objetivo
def test_backtracking_objetivo_directo_benchmark(benchmark):
    global objetivo
    objetivo = "d"

    cadena = "d"
    soluciones = []

    def backtracking_funcion():
        backtracking([cadena], soluciones)
        assert soluciones == [["d"]]  # La única solución posible

    benchmark(backtracking_funcion)
