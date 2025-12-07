import random
import time

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from asign1a1 import ProblemaAsigna1a1
from recursos import DistribucionRecursos
from mochila import ProblemaMochila
from vendedor import ProblemaVendedor
from tiempo import MedidorTiempo

console = Console()

def ejecutar_analisis():
   # Función principal del módulo: ejecuta el análisis completo de los problemas según el tamaño elegido
    

    # Muestra un panel simple con opciones
    panel = Panel(
        "[bold white]ANÁLISIS DE MÉTODOS[/bold white]\n\n"
        "Seleccione el tamaño del análisis:\n"
        "  [1] Pequeño\n"
        "  [2] Mediano\n"
        "  [3] Grande\n",
        border_style="white",
        box=box.DOUBLE,
        width=60
    )
    console.print(panel)

    # Se pide la opción
    opcion = console.input("Digite una opción (1-3): ")

    # Según la elección definimos los tamaños
    if opcion == "1":
        # Tamaños pequeños
        tamanos = {
            "asignacion": 6,
            "distribucion": 6,
            "mochila": 6,
            "vendedor": 6,
            # Para greedy / RA permite tamaño mayor
            "asignacion_g": 20,
            "distribucion_g": 20,
            "mochila_g": 20,
            "vendedor_g": 20
        }
    elif opcion == "2":
        # Tamaños medianos
        tamanos = {
            "asignacion": 12,
            "distribucion": 12,
            "mochila": 12,
            "vendedor": 12,
            "asignacion_g": 50,
            "distribucion_g": 50,
            "mochila_g": 50,
            "vendedor_g": 50
        }
    else:
        # Tamaños grandes
        tamanos = {
            "asignacion": 20,
            "distribucion": 20,
            "mochila": 20,
            "vendedor": 20,
            "asignacion_g": 100,
            "distribucion_g": 100,
            "mochila_g": 100,
            "vendedor_g": 100
        }

    # Ejecuta el análisis para cada problema
    ejecutar_analisis_asignacion(tamanos)
    ejecutar_analisis_distribucion(tamanos)
    ejecutar_analisis_mochila(tamanos)
    ejecutar_analisis_vendedor(tamanos)

    # Final
    console.print("\n[bold green]Análisis completado.[/bold green]")
    console.input("Presione ENTER para continuar...")



# Analisis problema asignación 1 a 1

def ejecutar_analisis_asignacion(t):
    

    # Mostramos encabezado
    console.print(Panel("Análisis: Asignación ",
                        border_style="white", box=box.DOUBLE))

    # Crea tabla de resultados
    tabla = Table(show_header=True, header_style="bold white", box=box.SIMPLE)
    tabla.add_column("Método")
    tabla.add_column("Tamaño")
    tabla.add_column("Ganancia/Costo")
    tabla.add_column("Factibles")
    tabla.add_column("Tiempo (s)")

    # Genera matriz aleatoria para greedy y RA
    tam_g = t["asignacion_g"]
    matriz_g = [[0] * (tam_g + 1) for _ in range(tam_g + 1)]
    for i in range(1, tam_g + 1):
        for j in range(1, tam_g + 1):
            matriz_g[i][j] = random.randint(0, 300)

    # Ejecuta greedy sobre matriz grande
    timer = MedidorTiempo()
    timer.cargar_tiempo()
    sol = ProblemaAsigna1a1(matriz_g, tam_g).busqueda_greedy()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Greedy", str(tam_g), str(sol.ganancia),
                  "-", formatear_tiempo_segundos(tiempo))

    # Exhaustiva pura → tamaño pequeño
    tam_p = t["asignacion"]
    matriz_p = [[0] * (tam_p + 1) for _ in range(tam_p + 1)]
    for i in range(1, tam_p + 1):
        for j in range(1, tam_p + 1):
            matriz_p[i][j] = random.randint(0, 300)

    timer.cargar_tiempo()
    sol = ProblemaAsigna1a1(matriz_p, tam_p).busqueda_exhaustiva_pura()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Exh. Pura", str(tam_p), str(sol.ganancia),
                  str(sol.soluciones_factibles),
                  formatear_tiempo_segundos(tiempo))

    # RA usando tamaño grande
    timer.cargar_tiempo()
    sol = ProblemaAsigna1a1(matriz_g, tam_g).busqueda_exhaustiva_ra()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Ramificación", str(tam_g), str(sol.ganancia),
                  str(sol.soluciones_factibles),
                  formatear_tiempo_segundos(tiempo))

    console.print(tabla)
    console.input("\nPresione ENTER para continuar...")



# Análisis problema distribución de recursos

def ejecutar_analisis_distribucion(t):
    """Analiza el problema de distribución de recursos."""
    
    console.print(Panel("Análisis: Distribución",
                        border_style="white", box=box.DOUBLE))

    tabla = Table(show_header=True, header_style="bold white", box=box.SIMPLE)
    tabla.add_column("Método")
    tabla.add_column("Tamaño")
    tabla.add_column("Ganancia")
    tabla.add_column("Factibles")
    tabla.add_column("Tiempo (s)")

    # Greedy / RA con tamaño grande
    tam_g = t["distribucion_g"]
    matriz_g = [[0] * (tam_g + 1) for _ in range(tam_g + 1)]
    for i in range(0, tam_g + 1):
        for j in range(1, tam_g + 1):
            matriz_g[i][j] = random.randint(0, 300)

    timer = MedidorTiempo()
    timer.cargar_tiempo()
    sol = DistribucionRecursos(matriz_g, tam_g, tam_g).busqueda_greedy()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Greedy", str(tam_g), str(sol.ganancia), "-",
                  formatear_tiempo_segundos(tiempo))

    # Exhaustiva pura → tamaño pequeño
    tam_p = t["distribucion"]
    matriz_p = [[0] * (tam_p + 1) for _ in range(tam_p + 1)]
    for i in range(0, tam_p + 1):
        for j in range(1, tam_p + 1):
            matriz_p[i][j] = random.randint(0, 300)

    timer.cargar_tiempo()
    sol = DistribucionRecursos(matriz_p, tam_p, tam_p).busqueda_exhaustiva_pura()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Exh. Pura", str(tam_p), str(sol.ganancia),
                  str(sol.soluciones_factibles),
                  formatear_tiempo_segundos(tiempo))

    # RA con tamaño grande
    timer.cargar_tiempo()
    sol = DistribucionRecursos(matriz_g, tam_g, tam_g).busqueda_exhaustiva_ra()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Ramificación", str(tam_g), str(sol.ganancia),
                  str(sol.soluciones_factibles),
                  formatear_tiempo_segundos(tiempo))

    console.print(tabla)
    console.input("\nPresione ENTER para continuar...")



# Análisis problema mochila

def ejecutar_analisis_mochila(t):
    """Analiza el problema de la mochila."""
    
    console.print(Panel("Análisis: Mochila",
                        border_style="white", box=box.DOUBLE))

    tabla = Table(show_header=True, header_style="bold white", box=box.SIMPLE)
    tabla.add_column("Método")
    tabla.add_column("Tamaño")
    tabla.add_column("Beneficio")
    tabla.add_column("Factibles")
    tabla.add_column("Tiempo (s)")

    # Datos para tamaño grande
    tam_g = t["mochila_g"]
    pesos_g = [random.randint(1, 50) for _ in range(tam_g)]
    beneficios_g = [random.randint(1, 300) for _ in range(tam_g)]
    capacidad_g = tam_g * 10

    timer = MedidorTiempo()
    timer.cargar_tiempo()
    sol = ProblemaMochila(pesos_g, beneficios_g, capacidad_g, tam_g).busqueda_greedy()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Greedy", str(tam_g), str(sol.beneficio),
                  "-", formatear_tiempo_segundos(tiempo))

    # Exhaustiva pura → tamaño pequeño
    tam_p = t["mochila"]
    pesos_p = [random.randint(1, 50) for _ in range(tam_p)]
    beneficios_p = [random.randint(1, 300) for _ in range(tam_p)]
    capacidad_p = tam_p * 10

    timer.cargar_tiempo()
    sol = ProblemaMochila(pesos_p, beneficios_p, capacidad_p, tam_p).busqueda_exhaustiva_pura()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Exh. Pura", str(tam_p), str(sol.beneficio),
                  str(sol.soluciones_factibles),
                  formatear_tiempo_segundos(tiempo))

    # RA con tamaño grande
    timer.cargar_tiempo()
    sol = ProblemaMochila(pesos_g, beneficios_g, capacidad_g, tam_g).busqueda_exhaustiva_ra()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Ramificación", str(tam_g), str(sol.beneficio),
                  str(sol.soluciones_factibles),
                  formatear_tiempo_segundos(tiempo))

    console.print(tabla)
    console.input("\nPresione ENTER para continuar...")


# Análisis problema vendedor viajero

def ejecutar_analisis_vendedor(t):
    
    console.print(Panel("Análisis: Vendedor",
                        border_style="white", box=box.DOUBLE))

    tabla = Table(show_header=True, header_style="bold white", box=box.SIMPLE)
    tabla.add_column("Método")
    tabla.add_column("Tamaño")
    tabla.add_column("Costo")
    tabla.add_column("Factibles")
    tabla.add_column("Tiempo (s)")

    # Matriz grande para greedy / RA
    tam_g = t["vendedor_g"]
    matriz_g = [[0] * (tam_g + 1) for _ in range(tam_g + 1)]
    for i in range(1, tam_g + 1):
        for j in range(1, tam_g + 1):
            matriz_g[i][j] = 0 if i == j else random.randint(1, 300)

    timer = MedidorTiempo()
    timer.cargar_tiempo()
    sol = ProblemaVendedor(matriz_g, tam_g).busqueda_greedy()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Greedy", str(tam_g), str(sol.costo), "-",
                  formatear_tiempo_segundos(tiempo))

    # Exhaustiva pura → tamaño pequeño
    tam_p = t["vendedor"]
    matriz_p = [[0] * (tam_p + 1) for _ in range(tam_p + 1)]
    for i in range(1, tam_p + 1):
        for j in range(1, tam_p + 1):
            matriz_p[i][j] = 0 if i == j else random.randint(1, 300)

    timer.cargar_tiempo()
    sol = ProblemaVendedor(matriz_p, tam_p).busqueda_exhaustiva_pura()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Exh. Pura", str(tam_p), str(sol.costo),
                  str(sol.soluciones_factibles),
                  formatear_tiempo_segundos(tiempo))

    # RA → tamaño grande
    timer.cargar_tiempo()
    sol = ProblemaVendedor(matriz_g, tam_g).busqueda_exhaustiva_ra()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Ramificación", str(tam_g), str(sol.costo),
                  str(sol.soluciones_factibles),
                  formatear_tiempo_segundos(tiempo))

    console.print(tabla)
    console.input("\nPresione ENTER para continuar...")



# Función auxiliar para formatear tiempos

def formatear_tiempo_segundos(dic):
    """Convierte el diccionario de tiempo a un número de segundos."""
    s = dic["horas"] * 3600 + dic["minutos"] * 60 + dic["segundos"] + dic["centesimas"] / 100
    return f"{s:.4f}"

