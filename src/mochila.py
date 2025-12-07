from dataclasses import dataclass
from typing import List

@dataclass
class SolucionMochila:
    mochila: List[int]
    beneficio: int
    soluciones_factibles: int = 0


class ProblemaMochila:
    """
    Problema de la mochila 0/1.
    Usa índices desde 1 para que sea compatible con prueba.py.
    """

    def __init__(self, pesos: List[int], beneficios: List[int], capacidad: int, n: int):
        self.pesos = [0] + pesos
        self.beneficios = [0] + beneficios
        self.capacidad = capacidad
        self.n = n

    # -------------------------------------------------------
    # GREEDY: basado en beneficio/peso
    # -------------------------------------------------------
    def busqueda_greedy(self) -> SolucionMochila:
        indices = list(range(1, self.n + 1))
        indices.sort(key=lambda i: self.beneficios[i] / self.pesos[i], reverse=True)

        mochila = [0] * (self.n + 1)
        peso_act = 0
        ben = 0

        for i in indices:
            if peso_act + self.pesos[i] <= self.capacidad:
                mochila[i] = 1
                peso_act += self.pesos[i]
                ben += self.beneficios[i]

        return SolucionMochila(mochila, ben)

    # -------------------------------------------------------
    # EXHAUSTIVA PURA
    # -------------------------------------------------------
    def busqueda_exhaustiva_pura(self) -> SolucionMochila:
        mejor = SolucionMochila(
            mochila=[0] * (self.n + 1),
            beneficio=0,
            soluciones_factibles=0
        )

        mochila = [0] * (self.n + 1)

        def backtrack(i, peso_act, ben_act):
            if i > self.n:
                mejor.soluciones_factibles += 1
                if ben_act > mejor.beneficio:
                    mejor.beneficio = ben_act
                    mejor.mochila = mochila[:]
                return

            # no tomar
            mochila[i] = 0
            backtrack(i + 1, peso_act, ben_act)

            # tomar si cabe
            if peso_act + self.pesos[i] <= self.capacidad:
                mochila[i] = 1
                backtrack(i + 1,
                          peso_act + self.pesos[i],
                          ben_act + self.beneficios[i])
                mochila[i] = 0

        backtrack(1, 0, 0)
        return mejor

    # -------------------------------------------------------
    # RAMIFICACIÓN Y ACOTAMIENTO
    # -------------------------------------------------------
    def busqueda_exhaustiva_ra(self) -> SolucionMochila:
        mejor = SolucionMochila(
            mochila=[0] * (self.n + 1),
            beneficio=0,
            soluciones_factibles=0
        )

        mochila = [0] * (self.n + 1)

        # cota optimista: sumar beneficios de todos los items restantes aunque no quepan
        def calcular_cota(i, ben_actual):
            resto = sum(self.beneficios[j] for j in range(i, self.n + 1))
            return ben_actual + resto

        def backtrack(i, peso_act, ben_act):
            # si superamos la cota, podar
            if calcular_cota(i, ben_act) <= mejor.beneficio:
                return

            if i > self.n:
                mejor.soluciones_factibles += 1
                if ben_act > mejor.beneficio:
                    mejor.beneficio = ben_act
                    mejor.mochila = mochila[:]
                return

            # opción 1: NO tomar
            mochila[i] = 0
            backtrack(i + 1, peso_act, ben_act)

            # opción 2: tomar si cabe
            if peso_act + self.pesos[i] <= self.capacidad:
                mochila[i] = 1
                backtrack(i + 1,
                          peso_act + self.pesos[i],
                          ben_act + self.beneficios[i])
                mochila[i] = 0

        backtrack(1, 0, 0)
        return mejor
