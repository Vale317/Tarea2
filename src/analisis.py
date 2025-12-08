import random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt

from asign1a1 import ProblemaAsigna1a1
from recursos import DistribucionRecursos
from mochila import ProblemaMochila
from vendedor import ProblemaVendedor
from tiempo import MedidorTiempo

console = Console()

def ejecutar_analisis():
    """Función principal del módulo: ejecuta el análisis completo"""
    
    # Muestra un panel simple (como en la versión original)
    console.clear()
    panel = Panel(
        "[bold white]ANÁLISIS Y COMPARACIÓN DE MÉTODOS[/bold white]\n\n"
        "Se ejecutarán análisis para tamaños pequeños, medianos y grandes.\n"
        "Para métodos exhaustivos se usan tamaños reducidos para evitar tiempos excesivos.",
        border_style="white",
        box=box.DOUBLE,
        width=80
    )
    console.print(panel)
    
   # Pedir ENTER para continuar (igual que en prueba.py)
    respuesta = Prompt.ask("\nPresione ENTER para continuar o 'q' para salir", default="", show_default=False)
    
    # Si el usuario presiona 'q' o cualquier letra (no ENTER), salir
    if respuesta.lower() == 'q' or (len(respuesta) > 0 and respuesta.lower() != ''):
        return
    
    # Configuraciones de tamaño (mejoradas para evitar bloqueos)
    configuraciones = [
        {"nombre": "pequeño", "exhaustivo": 3, "otros": 8},
        {"nombre": "mediano", "exhaustivo": 4, "otros": 12},
        {"nombre": "grande", "exhaustivo": 5, "otros": 18}
    ]
    
    # Ejecutar análisis para cada configuración
    for config in configuraciones:
        ejecutar_analisis_por_tamano(config)
    
    console.print("\n[bold green]Análisis completado.[/bold green]")
    Prompt.ask("\nPulse ENTER para continuar")

def ejecutar_analisis_por_tamano(config):
    """Ejecuta análisis para una configuración específica"""
    
    console.clear()
    console.print(Panel(f"[bold white]Análisis - Tamaño {config['nombre']}[/bold white]", 
                       border_style="white", box=box.DOUBLE))
    
    # Analizar los 4 problemas
    ejecutar_analisis_asignacion(config)
    ejecutar_analisis_distribucion(config)
    ejecutar_analisis_mochila(config)
    ejecutar_analisis_vendedor(config)
    
    if config["nombre"] != "grande":
        console.print("\n[dim]Presione ENTER para continuar con el siguiente tamaño...[/dim]")
        Prompt.ask("")

def ejecutar_analisis_asignacion(config):
    # Analiza el problema de asignación 1 a 1.
    
    console.print("\n[bold cyan]1. Problema de Asignación[/bold cyan]")
    
    # Tabla mejorada (similar estilo a prueba.py)
    tabla = Table(show_header=True, header_style="bold white", box=box.SIMPLE)
    tabla.add_column("Método", style="cyan")
    tabla.add_column("Tamaño", justify="center")
    tabla.add_column("Ganancia", justify="right")
    tabla.add_column("Soluciones", justify="right")
    tabla.add_column("Tiempo (s)", justify="right")
    
    # Generar matriz para greedy/RA (tamaño grande)
    tam_g = config["otros"]
    matriz_g = [[0] * (tam_g + 1) for _ in range(tam_g + 1)]
    for i in range(1, tam_g + 1):
        for j in range(1, tam_g + 1):
            matriz_g[i][j] = random.randint(0, 299)
    
    # Greedy con tamaño grande
    timer = MedidorTiempo()
    timer.cargar_tiempo()
    sol = ProblemaAsigna1a1(matriz_g, tam_g).busqueda_greedy()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Greedy", str(tam_g), str(sol.ganancia),
                  "-", formatear_tiempo_segundos(tiempo))
    
    # Exhaustiva pura con tamaño pequeño (evita bloqueo)
    tam_p = config["exhaustivo"]
    matriz_p = [[0] * (tam_p + 1) for _ in range(tam_p + 1)]
    for i in range(1, tam_p + 1):
        for j in range(1, tam_p + 1):
            matriz_p[i][j] = random.randint(0, 299)
    
    timer.cargar_tiempo()
    sol = ProblemaAsigna1a1(matriz_p, tam_p).busqueda_exhaustiva_pura()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Exh. Pura", str(tam_p), str(sol.ganancia),
                  str(sol.soluciones_factibles),
                  formatear_tiempo_segundos(tiempo))
    
    # Ramificación y acotamiento con tamaño grande
    timer.cargar_tiempo()
    sol = ProblemaAsigna1a1(matriz_g, tam_g).busqueda_exhaustiva_ra()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Ramificación", str(tam_g), str(sol.ganancia),
                  str(sol.soluciones_factibles),
                  formatear_tiempo_segundos(tiempo))
    
    console.print(tabla)

def ejecutar_analisis_distribucion(config):
    #Analiza el problema de distribución de recursos.
    
    console.print("\n[bold cyan]2. Distribución[/bold cyan]")
    
    tabla = Table(show_header=True, header_style="bold white", box=box.SIMPLE)
    tabla.add_column("Método", style="cyan")
    tabla.add_column("Tamaño", justify="center")
    tabla.add_column("Ganancia", justify="right")
    tabla.add_column("Soluciones", justify="right")
    tabla.add_column("Tiempo (s)", justify="right")
    
    # Greedy / RA con tamaño grande
    tam_g = config["otros"]
    matriz_g = [[0] * (tam_g + 1) for _ in range(tam_g + 1)]
    for i in range(0, tam_g + 1):
        for j in range(1, tam_g + 1):
            if i == 0:
                matriz_g[i][j] = 0
            else:
                # Ganancia incremental (más realista)
                matriz_g[i][j] = matriz_g[i-1][j] + random.randint(0, 50)
    
    timer = MedidorTiempo()
    timer.cargar_tiempo()
    sol = DistribucionRecursos(matriz_g, tam_g, tam_g).busqueda_greedy()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Greedy", f"{tam_g}/{tam_g}", str(sol.ganancia), "-",
                  formatear_tiempo_segundos(tiempo))
    
    # Exhaustiva pura → tamaño pequeño (evita bloqueo)
    tam_p = config["exhaustivo"]
    matriz_p = [[0] * (tam_p + 1) for _ in range(tam_p + 1)]
    for i in range(0, tam_p + 1):
        for j in range(1, tam_p + 1):
            if i == 0:
                matriz_p[i][j] = 0
            else:
                matriz_p[i][j] = matriz_p[i-1][j] + random.randint(0, 50)
    
    timer.cargar_tiempo()
    sol = DistribucionRecursos(matriz_p, tam_p, tam_p).busqueda_exhaustiva_pura()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Exh. Pura", f"{tam_p}/{tam_p}", str(sol.ganancia),
                  str(sol.soluciones_factibles),
                  formatear_tiempo_segundos(tiempo))
    
    # RA con tamaño grande
    timer.cargar_tiempo()
    sol = DistribucionRecursos(matriz_g, tam_g, tam_g).busqueda_exhaustiva_ra()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Ramificación", f"{tam_g}/{tam_g}", str(sol.ganancia),
                  str(sol.soluciones_factibles),
                  formatear_tiempo_segundos(tiempo))
    
    console.print(tabla)

def ejecutar_analisis_mochila(config):
    # Analiza el problema de la mochila.
    
    console.print("\n[bold cyan]3. Mochila[/bold cyan]")
    
    tabla = Table(show_header=True, header_style="bold white", box=box.SIMPLE)
    tabla.add_column("Método", style="cyan")
    tabla.add_column("Tamaño", justify="center")
    tabla.add_column("Beneficio", justify="right")
    tabla.add_column("Soluciones", justify="right")
    tabla.add_column("Tiempo (s)", justify="right")
    
    # Datos para tamaño grande (greedy/RA)
    tam_g = config["otros"]
    pesos_g = [random.randint(1, 20) for _ in range(tam_g)]
    beneficios_g = [random.randint(10, 100) for _ in range(tam_g)]
    capacidad_g = sum(pesos_g) // 2  # Capacidad razonable
    
    timer = MedidorTiempo()
    timer.cargar_tiempo()
    sol = ProblemaMochila(pesos_g, beneficios_g, capacidad_g, tam_g).busqueda_greedy()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Greedy", str(tam_g), str(sol.beneficio),
                  "-", formatear_tiempo_segundos(tiempo))
    
    # Exhaustiva pura → tamaño pequeño (evita bloqueo)
    tam_p = config["exhaustivo"]
    pesos_p = [random.randint(1, 20) for _ in range(tam_p)]
    beneficios_p = [random.randint(10, 100) for _ in range(tam_p)]
    capacidad_p = sum(pesos_p) // 2
    
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

def ejecutar_analisis_vendedor(config):
    # Analiza el problema del vendedor viajero.
    
    console.print("\n[bold cyan]4. Vendedor[/bold cyan]")
    
    tabla = Table(show_header=True, header_style="bold white", box=box.SIMPLE)
    tabla.add_column("Método", style="cyan")
    tabla.add_column("Tamaño", justify="center")
    tabla.add_column("Costo", justify="right")
    tabla.add_column("Soluciones", justify="right")
    tabla.add_column("Tiempo (s)", justify="right")
    
    # Matriz grande para greedy / RA
    tam_g = config["otros"]
    matriz_g = [[0] * (tam_g + 1) for _ in range(tam_g + 1)]
    for i in range(1, tam_g + 1):
        for j in range(1, tam_g + 1):
            if i == j:
                matriz_g[i][j] = 0
            elif i < j:
                matriz_g[i][j] = random.randint(1, 299)
                matriz_g[j][i] = matriz_g[i][j]  # Simétrica
    
    timer = MedidorTiempo()
    timer.cargar_tiempo()
    sol = ProblemaVendedor(matriz_g, tam_g).busqueda_greedy()
    tiempo = timer.intervalo_tiempo()
    tabla.add_row("Greedy", str(tam_g), str(sol.costo), "-",
                  formatear_tiempo_segundos(tiempo))
    
    # Exhaustiva pura → tamaño pequeño (evita bloqueo)
    tam_p = config["exhaustivo"]
    matriz_p = [[0] * (tam_p + 1) for _ in range(tam_p + 1)]
    for i in range(1, tam_p + 1):
        for j in range(1, tam_p + 1):
            if i == j:
                matriz_p[i][j] = 0
            elif i < j:
                matriz_p[i][j] = random.randint(1, 299)
                matriz_p[j][i] = matriz_p[i][j]
    
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

def formatear_tiempo_segundos(dic):
    # Convierte el diccionario de tiempo a un número de segundos.
    s = dic["horas"] * 3600 + dic["minutos"] * 60 + dic["segundos"] + dic["centesimas"] / 100
    return f"{s:.4f}"