from typing import List
from dataclasses import dataclass


@dataclass
class SolucionDistribucion:
    # Lista donde distribucion[j] indica cuántas unidades del recurso se asignan al ítem j
    distribucion: List[int]
    # Ganancia total obtenida con esa asignación
    ganancia: int
    # Cantidad de soluciones factibles evaluadas (para búsquedas exhaustivas)
    soluciones_factibles: int = 0


class DistribucionRecursos:
    # Clase que implementa el problema de distribución de un recurso.

    def __init__(self, matriz: List[List[int]], recursos_totales: int, itemes: int):
        # Matriz de ganancias donde matriz[i][j] es la ganancia total asignando i recursos al ítem j
        self.matriz = matriz
        # Cantidad total de recursos disponibles para distribuir
        self.recursos_totales = recursos_totales
        # Número total de ítems sobre los cuales se distribuyen recursos
        self.itemes = itemes

    def busqueda_greedy(self) -> SolucionDistribucion:
       #En cada ítem, se elige la cantidad de recursos que dé mayor ganancia marginal.
       
        # Distribución inicial con 0 recursos asignados
        distribucion = [0] * (self.itemes + 1)
        # Ganancia total acumulada
        ganancia_total = 0
        # Recursos disponibles en cada paso
        recursos_restantes = self.recursos_totales

        # Se procesa cada ítem uno por uno
        for j in range(1, self.itemes + 1):
            # Valor inicial del mejor incremento marginal encontrado
            mejor_margen = -1
            # Cantidad de recursos a asignar al ítem j
            mejor_asignacion = 0

            # Se prueban todas las posibles cantidades que se pueden asignar al ítem actual
            for r in range(0, recursos_restantes + 1):
                # Ganancia total si se asignan r recursos
                ganancia_r = self.matriz[r][j]
                # Ganancia actual asignando 0 recursos
                ganancia_actual = self.matriz[0][j]
                # Ganancia marginal = cuánto mejora respecto a no asignar nada
                margen = ganancia_r - ganancia_actual

                # Se guarda la mejor opción encontrada
                if margen > mejor_margen:
                    mejor_margen = margen
                    mejor_asignacion = r

            # Se asignan los recursos seleccionados al ítem
            distribucion[j] = mejor_asignacion
            # Se suma su ganancia total
            ganancia_total += self.matriz[mejor_asignacion][j]
            # Se reducen los recursos restantes
            recursos_restantes -= mejor_asignacion

        # Devuelve la solución greedy sin contador de factibles
        return SolucionDistribucion(distribucion, ganancia_total)

    def busqueda_exhaustiva_pura(self) -> SolucionDistribucion:
        
        #Explora TODAS las combinaciones posibles de distribución. Busca la asignación con mayor ganancia total.
    
        # Distribución final con la mejor solución encontrada
        mejor_distribucion = [0] * (self.itemes + 1)
        # Mejor ganancia encontrada
        mejor_ganancia = [0]
        # Contador de soluciones factibles evaluadas
        soluciones_factibles = [0]

        # Distribución parcial actual
        actual = [0] * (self.itemes + 1)

        def explorar(item: int, recursos_rest: int, ganancia_actual: int):
            # Si ya se asignaron recursos a todos los ítems, se evalúa la solución
            if item > self.itemes:
                soluciones_factibles[0] += 1
                # Se actualiza la mejor solución si esta es superior
                if ganancia_actual > mejor_ganancia[0]:
                    mejor_ganancia[0] = ganancia_actual
                    mejor_distribucion[:] = actual[:]
                return

            # Para el ítem actual, se prueban todas las cantidades de recursos posibles
            for r in range(0, recursos_rest + 1):
                # Se asignan r recursos al ítem actual
                actual[item] = r
                # Ganancia total del ítem actual con r recursos
                nueva_ganancia = ganancia_actual + self.matriz[r][item]
                # Se pasa al siguiente ítem disminuyendo los recursos restantes
                explorar(item + 1, recursos_rest - r, nueva_ganancia)

        # Arranca la exploración desde el ítem 1
        explorar(1, self.recursos_totales, 0)

        # Devuelve la mejor solución encontrada
        return SolucionDistribucion(mejor_distribucion, mejor_ganancia[0], soluciones_factibles[0])

    def busqueda_exhaustiva_ra(self) -> SolucionDistribucion:
        # Ordena las decisiones por mayor cota y poda ramas que no pueden superar la mejor solución.
        
        # Mejor solución encontrada
        mejor_distribucion = [0] * (self.itemes + 1)
        mejor_ganancia = [0]
        soluciones_factibles = [0]

        # Distribución parcial actual
        actual = [0] * (self.itemes + 1)

        def cota_superior(item: int, recursos_rest: int, ganancia_actual: int) -> int:
            # La cota consiste en sumar la mejor ganancia posible de cada ítem restante
            cota = ganancia_actual
            for j in range(item, self.itemes + 1):
                mejor = 0
                # Se busca la mejor ganancia posible con los recursos disponibles
                for r in range(0, recursos_rest + 1):
                    if self.matriz[r][j] > mejor:
                        mejor = self.matriz[r][j]
                cota += mejor
            return cota

        def explorar(item: int, recursos_rest: int, ganancia_actual: int):
            # Si se asignó a todos los ítems, se evalúa la solución
            if item > self.itemes:
                soluciones_factibles[0] += 1
                if ganancia_actual > mejor_ganancia[0]:
                    mejor_ganancia[0] = ganancia_actual
                    mejor_distribucion[:] = actual[:]
                return

            # Se generan todas las opciones posibles de asignación
            opciones = []
            for r in range(0, recursos_rest + 1):
                # Ganancia si asigno r recursos al ítem actual
                ganancia_r = ganancia_actual + self.matriz[r][item]
                # Cota para ordenar y podar
                cota = cota_superior(item + 1, recursos_rest - r, ganancia_r)
                opciones.append((r, ganancia_r, cota))

            # Ordenar por cota descendente (mejores opciones primero)
            opciones.sort(key=lambda x: x[2], reverse=True)

            # Explorar opciones en orden
            for r, ganancia_r, cota in opciones:
                # Si la cota no puede superar la mejor solución encontrada, se poda
                if cota < mejor_ganancia[0]:
                    break
                # Se asignan r recursos
                actual[item] = r
                # Se continúa explorando
                explorar(item + 1, recursos_rest - r, ganancia_r)

        # Arranca la búsqueda desde el ítem 1
        explorar(1, self.recursos_totales, 0)

        # Retorna la mejor solución encontrada
        return SolucionDistribucion(mejor_distribucion, mejor_ganancia[0], soluciones_factibles[0])