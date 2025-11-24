import time
from typing import Dict

class MedicionTiempo:

    def _init_(self):
        self.tiempo_inicial: float = 0.0
        self.tiempo_final: float = 0.0

    def cargar_tiempo(self) -> None:
        # Guarda el tiempo actual como inicial.
        pass

    def intervalo_timpo(self) -> Dict[str, int]:
        # Calcula el interalo de tiempo transcurrido, devuler hora, con minutos, segundos y centésimas.
        pass

    def formato_tiempo(self, tiempo: Dict[str, int]) -> str:
        # Reescribe el tiempo en unacadena legible. devuelve un string de forma: hh:mm:ss,cc
        pass
