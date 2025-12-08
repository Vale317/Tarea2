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
        # Búsqueda Greedy: Asigna recursos uno a uno donde dé mayor ganancia marginal.
        
        # Distribución inicial con 0 recursos asignados a cada ítem
        distribucion = [0] * (self.itemes + 1)
        
        # Recursos aún disponibles para asignar
        recursos_restantes = self.recursos_totales
        
        # Ganancia actual (todos con 0 recursos inicialmente)
        ganancia_actual = 0
        for j in range(1, self.itemes + 1):
            ganancia_actual += self.matriz[0][j]
        
        # Mientras haya recursos disponibles
        while recursos_restantes > 0:
            mejor_margen = -1
            mejor_item = 0
            ganancia_incremento = 0
            
            # Buscar el ítem donde un recurso adicional dé mayor ganancia marginal
            for j in range(1, self.itemes + 1):
                recursos_asignados = distribucion[j]
                
                # Solo considerar si podemos asignar más recursos de los disponibles
                if recursos_asignados < self.recursos_totales:
                    # Ganancia actual con recursos_asignados
                    ganancia_actual_j = self.matriz[recursos_asignados][j]
                    
                    # Ganancia con un recurso más
                    ganancia_nueva_j = self.matriz[recursos_asignados + 1][j]
                    
                    # Ganancia marginal de añadir un recurso
                    margen = ganancia_nueva_j - ganancia_actual_j
                    
                    if margen > mejor_margen:
                        mejor_margen = margen
                        mejor_item = j
                        ganancia_incremento = ganancia_nueva_j - ganancia_actual_j
            
            # Si encontramos un ítem donde añadir recursos mejora la ganancia
            if mejor_item > 0 and mejor_margen > 0:
                # Asignar un recurso más al mejor ítem
                distribucion[mejor_item] += 1
                recursos_restantes -= 1
                ganancia_actual += ganancia_incremento
            else:
                # Si no hay mejora, terminar
                break
        
        return SolucionDistribucion(distribucion, ganancia_actual)

    def busqueda_exhaustiva_pura(self) -> SolucionDistribucion:
        # Explora todas las combinaciones posibles de distribución.
        
        # Distribución final con la mejor solución encontrada
        mejor_distribucion = [0] * (self.itemes + 1)
        # Mejor ganancia encontrada
        mejor_ganancia = 0
        # Contador de soluciones factibles evaluadas
        soluciones_factibles = 0

        # Distribución parcial actual
        actual = [0] * (self.itemes + 1)

        def explorar(item: int, recursos_rest: int, ganancia_actual: int):
            nonlocal mejor_ganancia, mejor_distribucion, soluciones_factibles
            
            # Si ya se asignaron recursos a todos los ítems, se evalúa la solución
            if item > self.itemes:
                soluciones_factibles += 1
                # Se actualiza la mejor solución si esta es superior
                if ganancia_actual > mejor_ganancia:
                    mejor_ganancia = ganancia_actual
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
        return SolucionDistribucion(mejor_distribucion, mejor_ganancia, soluciones_factibles)

    def busqueda_exhaustiva_ra(self) -> SolucionDistribucion:
        # Búsqueda con ramificación y acotamiento.
        
        # Mejor solución encontrada
        mejor_distribucion = [0] * (self.itemes + 1)
        mejor_ganancia = 0
        soluciones_factibles = 0

        # Distribución parcial actual
        actual = [0] * (self.itemes + 1)

        def cota_superior(item: int, recursos_rest: int, ganancia_actual: int) -> int:
            # Calcula una cota superior optimista para la ganancia.
            cota = ganancia_actual
            
            # Para cada ítem restante, sumamos la mejor ganancia posible
            for j in range(item, self.itemes + 1):
                mejor = 0
                # Consideramos todas las posibles asignaciones para este ítem
                for r in range(0, min(recursos_rest, self.recursos_totales) + 1):
                    if self.matriz[r][j] > mejor:
                        mejor = self.matriz[r][j]
                cota += mejor
            
            return cota

        def explorar(item: int, recursos_rest: int, ganancia_actual: int):
            nonlocal mejor_ganancia, mejor_distribucion, soluciones_factibles
            
            # Si se asignó a todos los ítems, se evalúa la solución
            if item > self.itemes:
                soluciones_factibles += 1
                if ganancia_actual > mejor_ganancia:
                    mejor_ganancia = ganancia_actual
                    mejor_distribucion[:] = actual[:]
                return

            # Calcular cota para poda
            cota = cota_superior(item, recursos_rest, ganancia_actual)
            
            # Si la cota no puede superar la mejor solución encontrada, se poda
            if cota <= mejor_ganancia:
                return

            # Se generan opciones de asignación ordenadas por ganancia descendente
            opciones = []
            for r in range(0, recursos_rest + 1):
                ganancia_con_r = ganancia_actual + self.matriz[r][item]
                opciones.append((r, ganancia_con_r))
            
            # Ordenar por ganancia descendente (mejores opciones primero)
            opciones.sort(key=lambda x: x[1], reverse=True)

            # Explorar opciones en orden
            for r, ganancia_con_r in opciones:
                # Actualizar distribución actual
                actual[item] = r
                # Explorar recursivamente
                explorar(item + 1, recursos_rest - r, ganancia_con_r)
                # Volver a estado anterior (backtrack)
                actual[item] = 0

        # Arranca la búsqueda desde el ítem 1
        explorar(1, self.recursos_totales, 0)

        # Retorna la mejor solución encontrada
        return SolucionDistribucion(mejor_distribucion, mejor_ganancia, soluciones_factibles)