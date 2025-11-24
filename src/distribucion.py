from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class SolucionDistribucion:
    pass

class ProblemaDistribucion:

    def _init_(self, matriz: List[List[int]], tamano: int):
        pass

    def busqueda_greedy(self) -> SolucionDistribucion:
        pass

    def busqueda_exhaustiva_pura(self) -> SolucionDistribucion:
        pass

    def busqueda_exhaustiva_ra(self)-> SolucionDistribucion:
        pass