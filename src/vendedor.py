from typing import List
from dataclasses import dataclass


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
        self.matriz = matriz
        # Número de ciudades
        self.tamano = tamano
        # Diccionario para convertir número de ciudad → letra (1→a, 2→b, ...)
        self.ciudad_a_letra = {i: chr(96 + i) for i in range(1, tamano + 1)}
        
    def busqueda_greedy(self) -> SolucionVendedor:
        # Cream una solución con camino de tamaño tamano+1 (para usar índices 1..n)
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

            # Elege la ciudad más cercana disponible
            mejor_ciudad = None
            mejor_dist = float("inf")

            # Recorre todas las ciudades posibles
            for ciudad in range(1, self.tamano + 1):
                # Solo ciudades no visitadas y con distancia válida
                if not visitadas[ciudad] and self.matriz[ciudad_actual][ciudad] > 0:
                    if self.matriz[ciudad_actual][ciudad] < mejor_dist:
                        mejor_dist = self.matriz[ciudad_actual][ciudad]
                        mejor_ciudad = ciudad

            # Si por algún motivo no hay arista válida, toma la primera no visitada
            if mejor_ciudad is None:
                for ciudad in range(1, self.tamano + 1):
                    if not visitadas[ciudad]:
                        mejor_ciudad = ciudad
                        mejor_dist = self.matriz[ciudad_actual][ciudad]
                        break

            # Marca ciudad como visitada
            visitadas[mejor_ciudad] = True
            # Guarda letra en el camino
            solucion.camino[nivel] = self.ciudad_a_letra[mejor_ciudad]
            # Suma costo del movimiento
            solucion.costo += mejor_dist
            # Mueve ciudad actual
            ciudad_actual = mejor_ciudad

        # Regresa a la ciudad inicial (1)
        solucion.costo += self.matriz[ciudad_actual][1]

        return solucion

    def busqueda_exhaustiva_pura(self) -> SolucionVendedor:

        # Crea solución con costo infinito
        solucion = SolucionVendedor(
            camino=[""] * (self.tamano + 1),
            costo=float("inf"),
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
                ultima = camino[self.tamano]
                total = costo_actual + self.matriz[ultima][1]
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
                if not visitadas[ciudad] and self.matriz[actual][ciudad] > 0:

                    # Marca movimiento
                    visitadas[ciudad] = True
                    camino[nivel + 1] = ciudad
                    costo_actual += self.matriz[actual][ciudad]

                    # Recursiva al siguiente nivel
                    backtrack(nivel + 1)

                    # Deshace movimiento (backtrack)
                    costo_actual -= self.matriz[actual][ciudad]
                    visitadas[ciudad] = False

        # Ejecutamos backtracking
        backtrack(1)

        # Convierte camino numérico en letras
        for i in range(1, self.tamano + 1):
            solucion.camino[i] = self.ciudad_a_letra[mejor_camino[i]]

        return solucion

    def busqueda_exhaustiva_ra(self) -> SolucionVendedor:

        # Crea solución inicial
        solucion = SolucionVendedor(
            camino=[""] * (self.tamano + 1),
            costo=float("inf"),
            soluciones_factibles=0
        )

        mejor_camino = [0] * (self.tamano + 1)
        visitadas = [False] * (self.tamano + 1)
        visitadas[1] = True

        camino = [0] * (self.tamano + 1)
        camino[1] = 1

        costo_actual = 0

        # Calcula cota inferior optimista
        def cota_inferior(nivel: int):
            cota = costo_actual
            actual = camino[nivel]

            # Mínimo costo saliendo del nodo actual
            minimo = float("inf")
            for c in range(1, self.tamano + 1):
                if not visitadas[c] and self.matriz[actual][c] > 0:
                    minimo = min(minimo, self.matriz[actual][c])
            if minimo < float("inf"):
                cota += minimo

            # Mínima arista de cada ciudad no visitada
            for c in range(1, self.tamano + 1):
                if not visitadas[c]:
                    mini = float("inf")
                    for d in range(1, self.tamano + 1):
                        if d != c and self.matriz[c][d] > 0:
                            mini = min(mini, self.matriz[c][d])
                    if mini < float("inf"):
                        cota += mini

            return cota

        # Función de backtracking con poda
        def branch_bound(nivel: int):
            nonlocal costo_actual, solucion

            # Si llega al final
            if nivel == self.tamano:
                ultima = camino[self.tamano]
                total = costo_actual + self.matriz[ultima][1]
                solucion.soluciones_factibles += 1

                # Mejora la solución si aplica
                if total < solucion.costo:
                    solucion.costo = total
                    for i in range(1, self.tamano + 1):
                        mejor_camino[i] = camino[i]
                return

            # Ciudad actual
            actual = camino[nivel]

            # Construye lista de opciones
            opciones = []
            for ciudad in range(1, self.tamano + 1):
                if not visitadas[ciudad] and self.matriz[actual][ciudad] > 0:
                    opciones.append((ciudad, self.matriz[actual][ciudad]))

            # Ordena por distancia ascendente
            opciones.sort(key=lambda x: x[1])

            # Explora opciones
            for ciudad, dist in opciones:
                visitadas[ciudad] = True
                camino[nivel + 1] = ciudad
                costo_actual += dist

                # Poda si la cota no mejora
                if cota_inferior(nivel + 1) < solucion.costo:
                    branch_bound(nivel + 1)

                # Deshace
                costo_actual -= dist
                visitadas[ciudad] = False

        # Ejecutamos B&B (Branch and Bound o Ramificación y Acotamiento)
        branch_bound(1)

        # Convierte mejor camino encontrado a letras
        for i in range(1, self.tamano + 1):
            solucion.camino[i] = self.ciudad_a_letra[mejor_camino[i]]

        return solucion