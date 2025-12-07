"""
asign1a1.py

Implementación del problema de Asignación 1 a 1.
"""

from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class SolucionAsigna1a1:
    """Solución al problema de asignación 1 a 1."""
    asignado: List[int]
    ganancia: int
    soluciones_factibles: int = 0


class ProblemaAsigna1a1:
    """Problema de Asignación de 1 a 1."""
    
    def __init__(self, matriz: List[List[int]], tamano: int):
        """
        Inicializa el problema de asignación 1 a 1.
        
        Args:
            matriz: Matriz de ganancias
            tamano: Número de elementos a asignar
        """
        self.matriz = matriz
        self.tamano = tamano
    
    def busqueda_greedy(self) -> SolucionAsigna1a1:
        """
        Búsqueda Greedy: Selecciona la mejor opción local en cada paso.
        
        Returns:
            Solución factible (no necesariamente óptima)
        """
        asignado = [False] * (self.tamano + 1)
        solucion = SolucionAsigna1a1(
            asignado=[0] * (self.tamano + 1),
            ganancia=0
        )
        
        for i in range(1, self.tamano + 1):
            mejor = 1
            while asignado[mejor] and mejor < self.tamano:
                mejor += 1
            
            for j in range(1, self.tamano + 1):
                if (self.matriz[i][j] > self.matriz[i][mejor] and 
                    not asignado[j]):
                    mejor = j
            
            solucion.asignado[i] = mejor
            solucion.ganancia += self.matriz[i][mejor]
            asignado[mejor] = True
        
        return solucion
    
    def busqueda_exhaustiva_pura(self) -> SolucionAsigna1a1:
        """
        Búsqueda Exhaustiva Pura: Explora todas las soluciones posibles.
        
        Returns:
            Solución óptima
        """
        asignado = [False] * (self.tamano + 1)
        asignacion = [0] * (self.tamano + 1)
        ganancia = [0]  # Usar lista para modificar en función anidada
        
        solucion = SolucionAsigna1a1(
            asignado=[0] * (self.tamano + 1),
            ganancia=0,
            soluciones_factibles=0
        )
        
        def asignacion_exhaustiva(item: int):
            """Función recursiva para explorar todas las asignaciones."""
            for i in range(1, self.tamano + 1):
                if not asignado[i]:
                    asignado[i] = True
                    asignacion[item] = i
                    ganancia[0] += self.matriz[item][i]
                    
                    if item == self.tamano:
                        solucion.soluciones_factibles += 1
                        if ganancia[0] > solucion.ganancia:
                            solucion.ganancia = ganancia[0]
                            solucion.asignado = asignacion[:]
                    else:
                        asignacion_exhaustiva(item + 1)
                    
                    asignado[i] = False
                    ganancia[0] -= self.matriz[item][i]
        
        asignacion_exhaustiva(1)
        return solucion
    
    def busqueda_exhaustiva_ra(self) -> SolucionAsigna1a1:
        """
        Búsqueda Exhaustiva con Ramificación y Acotamiento (versión corregida).
        """

        asignado = [False] * (self.tamano + 1)
        asignacion = [0] * (self.tamano + 1)
        ganancia_actual = 0

        mejor = SolucionAsigna1a1(
            asignado=[0] * (self.tamano + 1),
            ganancia=0,
            soluciones_factibles=0
        )

        # Cota optimista: sumar los mejores valores posibles sin considerar conflictos
        def cota_superior(nivel, ganancia_actual):
            cota = ganancia_actual
            for i in range(nivel, self.tamano + 1):
                mejor_local = 0
                for j in range(1, self.tamano + 1):
                    if not asignado[j]:
                        mejor_local = max(mejor_local, self.matriz[i][j])
                cota += mejor_local
            return cota

        def backtrack(i, gan_act):
            nonlocal ganancia_actual

            # poda
            if cota_superior(i, gan_act) <= mejor.ganancia:
                return

            if i > self.tamano:
                mejor.soluciones_factibles += 1
                if gan_act > mejor.ganancia:
                    mejor.ganancia = gan_act
                    mejor.asignado = asignacion[:]
                return

            # probar todas las asignaciones posibles para i
            for j in range(1, self.tamano + 1):
                if not asignado[j]:
                    asignado[j] = True
                    asignacion[i] = j

                    backtrack(i + 1, gan_act + self.matriz[i][j])

                    asignado[j] = False
                    asignacion[i] = 0

        backtrack(1, 0)
        return mejor
