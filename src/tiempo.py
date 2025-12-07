"""
tiempo.py

Módulo para medir el tiempo de ejecución de algoritmos.
"""

import time
from typing import Dict

class MedidorTiempo:
    def __init__(self):
        self.tiempo_inicial = 0.0

    def cargar_tiempo(self) -> None:
        self.tiempo_inicial = time.perf_counter()

    def intervalo_tiempo(self) -> Dict[str, int]:
        intervalo = time.perf_counter() - self.tiempo_inicial

        horas, resto = divmod(intervalo, 3600)
        minutos, resto = divmod(resto, 60)
        segundos, resto = divmod(resto, 1)

        centesimas = int(round(resto * 100))

        # En caso de que centésimas redondee a 100
        if centesimas == 100:
            centesimas = 0
            segundos += 1

        return {
            "horas": int(horas),
            "minutos": int(minutos),
            "segundos": int(segundos),
            "centesimas": int(centesimas),
        }

    def formato_tiempo(self, t: Dict[str, int]) -> str:
        return f"{t['horas']:02d}:{t['minutos']:02d}:{t['segundos']:02d},{t['centesimas']:02d}"
