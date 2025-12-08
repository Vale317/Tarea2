from typing import List
from dataclasses import dataclass
import math


@dataclass
class SolucionVendedor:
    # Lista del camino recorrido en letras (a, b, c, ...)
    camino: List[str]
    # Costo total del recorrido
    costo: int
    # Cantidad de soluciones factibles evaluadas
    soluciones_factibles: int = 0


class ProblemaVendedor:

    def __init__(self, matriz: List[List[int]], tamano: int):
        # Matriz de distancias entre ciudades
        # Usamos un valor grande para representar "sin camino"
        INF = 10**9
        self.matriz = []
        for i in range(tamano + 1):
            fila = []
            for j in range(tamano + 1):
                if i == 0 or j == 0:
                    fila.append(0)
                elif i == j:
                    fila.append(0)
                elif matriz[i][j] == 0:  # 0 representa "sin camino"
                    fila.append(INF)
                else:
                    fila.append(matriz[i][j])
            self.matriz.append(fila)
        
        # Número de ciudades
        self.tamano = tamano
        # Diccionario para convertir número de ciudad → letra (1→a, 2→b, ...)
        self.ciudad_a_letra = {i: chr(96 + i) for i in range(1, tamano + 1)}
        
    def busqueda_greedy(self) -> SolucionVendedor:
        # Búsqueda Greedy: En cada paso, selecciona la ciudad más cercana no visitada.
        INF = 10**9
        
        # Creamos una solución con camino de tamaño tamano+1 (para usar índices 1..n)
        solucion = SolucionVendedor(
            camino=[""] * (self.tamano + 1),
            costo=0
        )

        # Empieza en la ciudad 1
        ciudad_actual = 1
        solucion.camino[1] = self.ciudad_a_letra[1]

        # Marca las ciudades visitadas
        visitadas = [False] * (self.tamano + 1)
        visitadas[1] = True

        # Recorre todas las ciudades restantes
        for nivel in range(2, self.tamano + 1):
            # Elige la ciudad más cercana disponible
            mejor_ciudad = None
            mejor_dist = INF

            # Recorre todas las ciudades posibles
            for ciudad in range(1, self.tamano + 1):
                # Solo ciudades no visitadas y con distancia válida (no INF)
                if not visitadas[ciudad] and self.matriz[ciudad_actual][ciudad] < INF:
                    if self.matriz[ciudad_actual][ciudad] < mejor_dist:
                        mejor_dist = self.matriz[ciudad_actual][ciudad]
                        mejor_ciudad = ciudad

            # Si no hay camino válido, intentamos cualquier ciudad no visitada
            if mejor_ciudad is None:
                for ciudad in range(1, self.tamano + 1):
                    if not visitadas[ciudad]:
                        mejor_ciudad = ciudad
                        # Busca la mejor distancia disponible (puede ser INF)
                        for otra_ciudad in range(1, self.tamano + 1):
                            if not visitadas[otra_ciudad] and ciudad != otra_ciudad:
                                if self.matriz[ciudad_actual][otra_ciudad] < INF:
                                    mejor_dist = self.matriz[ciudad_actual][otra_ciudad]
                                    break
                        if mejor_dist == INF:
                            # Asume una distancia grande si no hay conexión
                            mejor_dist = 1000
                        break
            
            if mejor_ciudad is None:
                # Si aún no hay ciudad, creamos una ruta artificial
                for ciudad in range(1, self.tamano + 1):
                    if not visitadas[ciudad]:
                        mejor_ciudad = ciudad
                        mejor_dist = 1000  # Distancia artificial
                        break

            # Marca ciudad como visitada
            visitadas[mejor_ciudad] = True
            # Guarda letra en el camino
            solucion.camino[nivel] = self.ciudad_a_letra[mejor_ciudad]
            # Suma costo del movimiento
            solucion.costo += mejor_dist
            # Mueve ciudad actual
            ciudad_actual = mejor_ciudad

        # Regresa a la ciudad inicial (1) si hay camino
        if self.matriz[ciudad_actual][1] < INF:
            solucion.costo += self.matriz[ciudad_actual][1]
        else:
            # Si no hay camino de regreso, usa distancia artificial
            solucion.costo += 1000

        return solucion

    def busqueda_exhaustiva_pura(self) -> SolucionVendedor:
        #Búsqueda Exhaustiva Pura: Explora todas las rutas posibles.
        INF = 10**9
        
        # Crea solución con costo infinito
        solucion = SolucionVendedor(
            camino=[""] * (self.tamano + 1),
            costo=INF,
            soluciones_factibles=0
        )

        # Camino numérico definitivo
        mejor_camino = [0] * (self.tamano + 1)

        # Estados de visitas
        visitadas = [False] * (self.tamano + 1)
        visitadas[1] = True

        # Camino actual numérico
        camino = [0] * (self.tamano + 1)
        camino[1] = 1

        # Costo parcial del camino
        costo_actual = 0

        # Función recursiva de backtracking puro
        def backtrack(nivel: int):
            nonlocal costo_actual, solucion

            # Si completa todas las ciudades
            if nivel == self.tamano:
                # Calcula costo total (incluyendo regreso al inicio)
                ultima = camino[self.tamano]
                costo_regreso = self.matriz[ultima][1]
                
                if costo_regreso < INF:  # Solo si hay camino de regreso
                    total = costo_actual + costo_regreso
                    solucion.soluciones_factibles += 1

                    # Verifica si es la mejor solución
                    if total < solucion.costo:
                        solucion.costo = total
                        for i in range(1, self.tamano + 1):
                            mejor_camino[i] = camino[i]
                return

            # Ciudad actual
            actual = camino[nivel]

            # Intenta ir a cualquier ciudad no visitada
            for ciudad in range(1, self.tamano + 1):
                if not visitadas[ciudad] and self.matriz[actual][ciudad] < INF:
                    # Marca movimiento
                    visitadas[ciudad] = True
                    camino[nivel + 1] = ciudad
                    costo_actual += self.matriz[actual][ciudad]

                    # Llama recursivamente al siguiente nivel
                    backtrack(nivel + 1)

                    # Deshace movimiento (backtrack)
                    costo_actual -= self.matriz[actual][ciudad]
                    visitadas[ciudad] = False

        # Ejecutamos backtracking
        backtrack(1)

        # Convierte camino numérico en letras
        for i in range(1, self.tamano + 1):
            solucion.camino[i] = self.ciudad_a_letra[mejor_camino[i]]

        # Si no se encontró solución factible, usa greedy como fallback
        if solucion.costo == INF:
            return self.busqueda_greedy()

        return solucion

    def busqueda_exhaustiva_ra(self) -> SolucionVendedor:
        # Búsqueda Exhaustiva con Ramificación y Acotamiento.
        INF = 10**9
        
        # Crea solución inicial
        solucion = SolucionVendedor(
            camino=[""] * (self.tamano + 1),
            costo=INF,
            soluciones_factibles=0
        )

        mejor_camino = [0] * (self.tamano + 1)
        visitadas = [False] * (self.tamano + 1)
        visitadas[1] = True

        camino = [0] * (self.tamano + 1)
        camino[1] = 1

        costo_actual = 0

        # Calcula cota inferior optimista usando el algoritmo de los mínimos
        def cota_inferior(nivel: int) -> float:
            #Calcula una cota inferior optimista para el costo restante.
            cota = costo_actual
            actual = camino[nivel]

            # 1. Costo mínimo desde la ciudad actual a una no visitada
            if nivel < self.tamano:
                min_salida = INF
                for c in range(1, self.tamano + 1):
                    if not visitadas[c] and self.matriz[actual][c] < min_salida:
                        min_salida = self.matriz[actual][c]
                if min_salida < INF:
                    cota += min_salida
                else:
                    cota += 1000  # Valor grande si no hay conexión

            # 2. Suma de las aristas mínimas de entrada de cada ciudad no visitada
            # (excepto la primera que ya tiene entrada fija)
            for c in range(1, self.tamano + 1):
                if not visitadas[c]:
                    min_entrada = INF
                    for d in range(1, self.tamano + 1):
                        if d != c and self.matriz[d][c] < min_entrada:
                            min_entrada = self.matriz[d][c]
                    if min_entrada < INF:
                        cota += min_entrada
                    else:
                        cota += 1000  # Valor grande si no hay conexión

            return cota

        # Función de backtracking con poda
        def branch_bound(nivel: int):
            nonlocal costo_actual, solucion

            # Si llega al final
            if nivel == self.tamano:
                ultima = camino[self.tamano]
                costo_regreso = self.matriz[ultima][1]
                
                if costo_regreso < INF:  # Solo si hay camino de regreso
                    total = costo_actual + costo_regreso
                    solucion.soluciones_factibles += 1

                    # Mejora la solución si aplica
                    if total < solucion.costo:
                        solucion.costo = total
                        for i in range(1, self.tamano + 1):
                            mejor_camino[i] = camino[i]
                return

            # Ciudad actual
            actual = camino[nivel]

            # Construye lista de opciones válidas
            opciones = []
            for ciudad in range(1, self.tamano + 1):
                if not visitadas[ciudad] and self.matriz[actual][ciudad] < INF:
                    opciones.append((ciudad, self.matriz[actual][ciudad]))

            # Si no hay opciones válidas, termina esta rama
            if not opciones:
                return

            # Ordena por distancia ascendente (estrategia "best-first")
            opciones.sort(key=lambda x: x[1])

            # Explora opciones
            for ciudad, dist in opciones:
                visitadas[ciudad] = True
                camino[nivel + 1] = ciudad
                costo_actual += dist

                # Calcula cota y poda si no puede mejorar la mejor solución
                cota = cota_inferior(nivel + 1)
                if cota < solucion.costo:
                    branch_bound(nivel + 1)

                # Deshace
                costo_actual -= dist
                visitadas[ciudad] = False

        # Ejecutamos B&B (Branch and Bound o Ramificación y Acotamiento)
        branch_bound(1)

        # Si no se encontró solución factible, usa greedy como fallback
        if solucion.costo == INF:
            return self.busqueda_greedy()

        # Convierte mejor camino encontrado a letras
        for i in range(1, self.tamano + 1):
            solucion.camino[i] = self.ciudad_a_letra[mejor_camino[i]]

        return solucion