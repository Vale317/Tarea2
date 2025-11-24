from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class SolucionAsignacion:
    pass

class ProblemaAsignacion:

    def _init_(self, matriz: List[List[int]], tamano: int):
        pass

    def busqueda_greedy(self) -> SolucionAsignacion:
        pass

    def busqueda_exhaustiva_pura(self) -> SolucionAsignacion:
        pass

    def busqueda_exhaustiva_ra(self)-> SolucionAsignacion:
        pass