# Documentación Tarea Programada 2

Universidad de Costa Rica  
Escuela de Ciencias de la Computación e Informática 
CI-0116 Análisis de algoritmos y estructuras de datos - 005
Tarea programada 2
 
Profesor: Braulio Solano Rojas

Autores: 
*Karol Valeria Bolaños Sánchez, C31205*  
*Priscilla López Quesada, C14301*


## Especificaciones del Proyecto

    Se deben aplicar las 3 técnicas de búsqueda para encontrar la solución óptima de los siguientes problemas generales:

    a) Problema de asignación 1 a 1
    b) Problema de distribución de un recurso
    c) Problema de la mochila  
    d) Problema del vendedor

### Requisitos
- Python 3.8+
- Librería rich: `pip install rich`

### Para ejecutar:
    Ubicarse en la carpeta src, y en terminal ingresar el comando "uv run prueba.py".


## Módulos Implementados

    1. asign1a1.py – Problema de Asignación 
    **Tomado del archivo que el profe compartió en clase, lo implementamos de forma a que funcionara con nuestro código. (hicimos algunos ajustes al método de ramificación)

    Clase ProblemaAsigna1a1:
    - Representa el problema de asignar cada elemento `i` a un único elemento `j` maximizando la ganancia total.
    - busqueda_greedy(): Asigna cada `i` al `j` disponible con mayor ganancia local.
    - busqueda_exhaustiva_pura(): Explora todas las permutaciones posibles.
    - busqueda_exhaustiva_ra(): Usa podas con una cota optimista basada en las mejores ganancias restantes.

    Clase SolucionAsigna1a1:
    - Tiene la asignación final, la ganancia total y el contador de soluciones factibles evaluadas.

    2. recursos.py – Problema de Distribución 

    Clase DistribucionRecursos:
    - Distribuye una cantidad limitada de recursos entre varios ítems maximizando la ganancia.
    - busqueda_greedy(): Asigna recursos al ítem con mayor ganancia marginal en cada paso.
    - busqueda_exhaustiva_pura(): Explora todas las combinaciones posibles de distribución.
    - busqueda_exhaustiva_ra(): Ordena decisiones por cota superior y poda ramas no prometedoras.

    Clase SolucionDistribucion:
    - Contiene la distribución final, ganancia total y contador de soluciones factibles.

    3. mochila.py – Problema de la Mochila

    Clase ProblemaMochila:
    - Selecciona un subconjunto de ítems que maximice el beneficio sin exceder la capacidad.
    - busqueda_greedy(): Ordena ítems por relación beneficio/peso y toma mientras haya capacidad.
    - busqueda_exhaustiva_pura(): Evalúa todas las combinaciones binarias de inclusión.
    - busqueda_exhaustiva_ra(): Poda ramas donde la cota optimista (suma de beneficios restantes) no supera la mejor solución.

    Clase SolucionMochila:
    - Contiene la mochila/lista binaria, beneficio total y contador de soluciones factibles.

    4. vendedor.py – Problema del Vendedor 

    Clase ProblemaVendedor:
    - Encuentra el camino más corto que visita cada ciudad exactamente una vez y regresa al origen.
    - busqueda_greedy(): Siempre va a la ciudad más cercana no visitada.
    - busqueda_exhaustiva_pura(): Evalúa todas las permutaciones de ciudades.
    - busqueda_exhaustiva_ra(): Calcula cotas inferiores optimistas y poda ramas que no pueden mejorar la solución.

    Clase SolucionVendedor:
    - Contiene el camino recorrido (en letras), costo total y contador de soluciones factibles.

    5. tiempo.py – Medición de Tiempo
    **Tomado del archivo que el profe compartió en clase, lo implementamos de forma a que funcionara con nuestro código. (hicimos algunos ajustes, como añadir la función divmod)

    Clase MedidorTiempo:
    - Permite medir intervalos de tiempo con precisión de centésimas.
    - cargar_tiempo(): Inicia el cronómetro.
    - intervalo_tiempo(): Devuelve un diccionario con horas, minutos, segundos y centésimas.
    - formato_tiempo(): Formatea el tiempo en `HH:MM:SS,CC`.

    6. prueba.py – Programa Principal 
    **Tomado del archivo que el profe compartió en clase, lo implementamos de forma a que funcionara con nuestro código.

    - Interfaz en consola con la librería Rich.
    - Menú principal para seleccionar el tipo de problema.
    - Submenú para elegir el método de búsqueda.
    - Ingreso de datos.
    - Generación aleatoria de datos.
    - Visualización de matrices cuando el tamaño es ≤ 10.
    - Muestra resultados: solución encontrada, tiempo de ejecución, número de soluciones factibles evaluadas (excepto en Greedy)

    7. analisis.py - Análisis Comparativo
    Este módulo ejecuta pruebas automáticas para comparar Greedy, Exhaustiva Pura y Ramificación y Acotamiento en los cuatro problemas del proyecto. Ejecuta automáticamente tres configuraciones: pequeño, mediano y grande.

    Configuraciones implementadas:
    - Pequeño: Exhaustiva (3 elementos), Greedy/RA (8 elementos)
    - Mediano: Exhaustiva (4 elementos), Greedy/RA (12 elementos)   
    - Grande: Exhaustiva (5 elementos), Greedy/RA (18 elementos)

    *Nota: Se redujeron los tamaños para métodos exhaustivos para evitar tiempos de ejecución excesivos.*

    El módulo genera instancias aleatorias, ejecuta los tres métodos y muestra con Rich:
    - Tiempo de ejecución (segundos)
    - Resultado encontrado
    - Número de soluciones factibles evaluadas (para métodos exhaustivos)

### Generación Aleatoria
- Se activa  cuando el tamaño > 10 para evitar entrada manual extensa.
- Rangos:
  - Ganancias/distancias: 0-299
  - Pesos: 1-50
  - Beneficios: 1-299

## Técnicas de Búsqueda

### 1. Búsqueda Greedy
- **Ventajas**: Muy rápido, fácil de implementar.
- **Desventajas**: No garantiza optimalidad.
- **Complejidad temporal**: Generalmente O(n log n) u O(n²).

### 2. Búsqueda Exhaustiva Pura
- **Ventajas**: Garantiza solución óptima.
- **Desventajas**: Mucha combinatoria, ineficiente para problemas grandes.
- **Complejidad temporal**: O(n!) o O(2^n) según el problema.

### 3. Búsqueda Exhaustiva con Ramificación y Acotamiento
- **Ventajas**: Reduce el espacio de búsqueda, mantiene optimalidad.
- **Desventajas**: Implementación más compleja, eficiencia depende de la cota.
- **Complejidad temporal**: En el peor caso igual que exhaustiva pura, pero normalmente mucho mejor.

## Conclusión

**A la hora de correr el análisis para tamaños grandes, el problema de distribución duró 2413s(40min), así que a pesar de que dura corriéndolo, sí lo corre, ya que no queríamos reducir aún más su tamaño.
Este proyecto implementa y compara tres técnicas de búsqueda  aplicadas a cuatro problemas clásicos. La interfaz  permite experimentar con diferentes tamaños y métodos, facilitando el análisis comparativo entre Greedy, Exhaustiva Pura y Ramificación y Acotamiento.