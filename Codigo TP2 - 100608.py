import os
from time import sleep #utilizado como efecto estetico al principio de main()
import re

EXTENSIONES_BUSCADAS = (".txt",".md",".py",".c")
RUTA_CODIGO = os.path.join(".",os.path.basename(__file__))
MODOS = ("and:","or:","not:")

AYUDA = """
Se disponen de tres modos de busqueda: AND,OR o NOT. Las coincidencias son aquellos archivos que en su ruta o nombre respeten las condiciones de busqueda, ignorando mayusculas y minusculas.
En caso de ser archivos '.txt', '.md', '.py' o '.c' se buscara terminos dentro de los mismos, analizando su contenido.
Introduciendo <comando>: <terminos> se realiza una consulta. Un termino debe coincidir completamente al encontrado para ser contado como valido. DEBE DEJARSE UN ESPACIO LUEGO DE LOS DOS PUNTOS(':')

Busqueda OR:
	Ejecutada con 'OR: <terminos>' o '<terminos>'. Devuelve las rutas de los archivos que coincidan con AL MENOS un termino.

Busqueda AND:
	Ejecutada con 'AND: <terminos>'. Devuelve las rutas de los archivos que coincidan con TODOS los terminos.

Busqueda NOT:
	Ejecutada con 'NOT: <termino>'. Devuelve las rutas de los archivos que NO coinciden con el unico termino dado.

Otros comandos especiales: "/*" para salir, "/c" para creditos.
"""

CREDITOS = """TP2 - Catedra Wachenchauzer - Algoritmos y Programacion I - FIUBA 2017
Franco Giordano - 100608
"""




def indexar_archivos():
	"""No recibe nada. Recorre los directorios y todos los subdirectorios desde donde se ejecuta el programa. Si un archivo coincide con EXTENSIONES_BUSCADAS se llamara a terminos_en_archivo.
	Devuelve un diccionario con terminos (palabras) como claves, y rutas de archivos que contengan dicho termino como valores."""
	INDICE_POR_RUTA = {}
	for tupla in os.walk("."):
		ruta_actual = tupla[0]
		archivos_actuales = tupla[2]
		terminos_ruta_actual = re.split("\W+", ruta_actual.lower())
		for nombre_archivo in archivos_actuales:
			ruta_archivo = os.path.join(ruta_actual,nombre_archivo)
			if ruta_archivo == RUTA_CODIGO:
				continue

			terminos_actuales = terminos_ruta_actual + re.split("\W+", nombre_archivo.lower())

			if nombre_archivo.endswith(EXTENSIONES_BUSCADAS):
				terminos_actuales += terminos_en_archivo(ruta_archivo)

			terminos_actuales_sin_vacios = [term for term in terminos_actuales if term != ""]
			terminos_actuales_sin_repetidos = remover_repetidos(terminos_actuales_sin_vacios)
			INDICE_POR_RUTA[ruta_archivo] = terminos_actuales_sin_repetidos

	INDICE_POR_TERMINO = invertir_diccionario(INDICE_POR_RUTA)
	cantidad_indexados = len(INDICE_POR_RUTA)
	return INDICE_POR_TERMINO,cantidad_indexados



def invertir_diccionario(diccionario):
	'''Dado un diccionario, devuelve un nuevo diccionario donde cada clave sera un valor del anterior, y sus valores seran claves del anterior.
	Ej: {"animal": ["perro"], "persona": ["alumno","bombero"]}  ----->  {"perro": ["animal"], "alumno": ["persona"], "bombero": ["persona"]}'''
	diccionario_invertido = {}
	for clave, lista in diccionario.items():
		for elemento in lista:
			diccionario_invertido[elemento] = diccionario_invertido.get(elemento, []) + [clave]
	return diccionario_invertido



def terminos_en_archivo(ruta):
	'''Dada una ruta de un archivo, devuelve los terminos (palabras) que encuentra en el mismo como una lista, ignorando MAYUS/minus y repetidos.'''
	with open(ruta) as archivo:
		terminos_del_archivo = []
		for linea in archivo:
			linea_sin_salto = linea.rstrip("\n").lower()
			terminos_linea = re.split("\W+",linea_sin_salto)
			for palabra in terminos_linea:
				terminos_del_archivo += [palabra]
	return remover_repetidos(terminos_del_archivo)

def recibir_comandos():
	"""Utilizada en main(). Imprime un prompt y recibe un input. Devuelve tres elementos: un elemento de MODOS (correspondiente al elegido), terminos elegidos (palabras), e input original (sin MAYUS/minus)."""
	input_raw = input("> ").lower()
	palabras = input_raw.split()
	modo_elegido = "or:"

	if input_raw.startswith(MODOS):
		modo_elegido = palabras[0]
		palabras.pop(0)

	return modo_elegido,palabras,input_raw

def remover_repetidos(lista):
	'''Dada una lista, devuelve una nueva desordenada sin elementos repetidos.'''
	return list(set(lista))

def obtener_elem_compartidos_entre(lista1, lista2):
	"""Dadas dos listas, encuentra los elementos compartidos en ambas y los devuelve como una nueva lista."""
	return [elemento1 for elemento1 in lista1 if elemento1 in lista2]

def decidir_comando_especial(cadena):
	'''Utilizada en main(). Dada una cadena, decide qué "comando especial" ejecutar (imprimir ayuda, creditos o salir).'''
	if cadena == "/*":
		print("Adios!\n")
		exit()
	elif cadena == "/h":
		print(AYUDA)
	elif cadena == "/c":
		print(CREDITOS)
	else:
		print("Comando no reconocido. ¿Has probado con '/h'?\n")


def main():
	'''Funcion principal del programa.'''
	print("Indexando archivos",end="",flush=True)
	sleep(0.5)
	for punto in "...":
		print(punto,flush=True,end="")
		sleep(0.5)

	indice_invertido,cantidad = indexar_archivos()
	print("\nListo! Se indexaron {} archivos".format(cantidad))
	print("Puedes utlizar '/*' para salir en cualquier momento, '/h' para ayuda o '/c' para creditos\n")

	while True:
		modo_busqueda,terminos_a_buscar,input_raw = recibir_comandos()
		
		if input_raw.startswith("/"):
			decidir_comando_especial(input_raw)
			continue

		rutas_coincidentes = []
		un_solo_term_a_buscar = len(terminos_a_buscar) == 1

		if modo_busqueda == "or:":
			for termino in terminos_a_buscar:
				rutas_coincidentes += indice_invertido.get(termino,[])
		

		elif modo_busqueda == "and:":
			for i,termino in enumerate(terminos_a_buscar):
				if termino not in indice_invertido:
					rutas_coincidentes = []
					break
				if i == 0:
					rutas_coincidentes = indice_invertido[termino]
				rutas_coincidentes = obtener_elem_compartidos_entre(rutas_coincidentes,indice_invertido[termino])

		elif modo_busqueda == "not:":
			if not un_solo_term_a_buscar:
				print("La busqueda 'not' recibe un solo termino! Intente nuevamente\n")
				continue
			rutas_no_validas = indice_invertido.get(terminos_a_buscar[0], [])
			for termino,rutas in indice_invertido.items():
				rutas_coincidentes += rutas
			rutas_coincidentes = [ruta for ruta in rutas_coincidentes if ruta not in rutas_no_validas]

		if rutas_coincidentes == []:
			print("No hay coincidencias\n")
			continue

		rutas_coincidentes = remover_repetidos(rutas_coincidentes)
		for r_coinc in rutas_coincidentes:
			print(r_coinc)
		print()
		
main()