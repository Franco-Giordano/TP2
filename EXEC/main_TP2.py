import os
from time import sleep
import re

EXTENSIONES_BUSCADAS = (".txt",".md",".py",".c")
RUTA_CODIGO = os.path.join(".",os.path.basename(__file__))
MODOS = ("and:","or:","not:")

AYUDA = """
Se disponen de tres modos de busqueda: AND,OR o NOT. Las coincidencias son aquellos archivos que en su ruta o nombre respeten las condiciones de busqueda. En caso de ser archivos '.txt', '.md', '.py' o '.c' se buscara terminos dentro de los mismos, analizando su contenido.
Introduciendo <comando>: <terminos> se realiza una consulta. Un termino debe coincidir completamente al encontrado para ser contado como valido. DEBE DEJARSE UN ESPACIO LUEGO DE LOS DOS PUNTOS(':')

Busqueda OR:
	Ejecutada con 'OR: <terminos>' o '<terminos>'. Devuelve las rutas de los archivos que coincidan con AL MENOS un termino.

Busqueda AND:
	Ejecutada con 'AND: <terminos>'. Devuelve las rutas de los archivos que coincidan con TODOS los terminos.

Busqueda NOT:
	Ejecutada con 'NOT: <termino>'. Devuelve las rutas de los archivos que NO coinciden con el unico termino dado.
"""

CREDITOS = """TP2 - Catedra Wachenchauzer - Algoritmos y Programacion I - FIUBA 2017
Franco Giordano - 100608
"""




def indexar_archivos():
	"""dsadsa"""
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

			terminos_actuales_sin_basura = [term for term in terminos_actuales if term != ""]
			INDICE_POR_RUTA[ruta_archivo] = terminos_actuales_sin_basura

	INDICE_POR_TERMINO = invertir_diccionario(INDICE_POR_RUTA)
	cantidad_indexados = len(INDICE_POR_RUTA)
	return INDICE_POR_TERMINO,cantidad_indexados



def invertir_diccionario(diccionario):
	''''''
	diccionario_invertido = {}
	for clave, lista in diccionario.items():
		for elemento in lista:
			diccionario_invertido[elemento] = diccionario_invertido.get(elemento, []) + [clave]
	return diccionario_invertido



def terminos_en_archivo(ruta):
	''''''
	with open(ruta) as archivo:
		terminos_del_archivo = []
		for linea in archivo:
			linea_sin_salto = linea.rstrip("\n").lower()
			terminos_linea = re.split("\W+",linea_sin_salto)
			for palabra in terminos_linea:
				terminos_del_archivo += [palabra]

	return remover_repetidos(terminos_del_archivo)

def recibir_comandos():
	""""""
	input_raw = input("> ").lower()
	palabras = input_raw.split()
	modo_elegido = "or:"

	if input_raw.startswith(MODOS):
		modo_elegido = palabras[0]
		palabras.pop(0)

	return modo_elegido,palabras,input_raw

def remover_repetidos(lista):
	''''''
	return list(set(lista))

def decidir_comando_especial(cadena):
	''''''
	if cadena == "/*":
		print("Adios!\n")
		exit()
	elif cadena == "/h":
		print(AYUDA)
	elif cadena == "/c":
		print(CREDITOS)
	else:
		print("Comando no reconocido. ¿Has probado con '/h'?")


def main():
	''''''
	print("Indexando archivos",end="",flush=True)
	sleep(0.5)
	for letra in "...":
		print(letra,flush=True,end="")
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
			for termino in terminos_a_buscar:
				if termino not in indice_invertido:
					break
				rutas_coincidentes = [ruta for ruta in indice_invertido[termino] if ruta in rutas_coincidentes]


		elif modo_busqueda == "not:":
			if not un_solo_term_a_buscar:
				print("La busqueda 'not' recibe un solo termino! Intente nuevamente")
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