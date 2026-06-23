import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import tracemalloc
from Dijkstra import dijkstra
from AStar import astar

def generar_grafo_con_coordenadas(num_nodos, densidad=0.2):
    # Grafos con coordenadas XY con números aleatorios de 0 a 500
    posiciones = {i: (random.randint(0, 500), random.randint(0, 500)) for i in range(num_nodos)}
    
    # Matriz de adyacencia
    grafo = [[None for _ in range(num_nodos)] for _ in range(num_nodos)]
    
    for i in range(num_nodos):
        for j in range(i + 1, num_nodos):
            if random.random() < densidad:
                # Peso de aristas aleatorio de 10 a 100
                peso = random.randint(10, 100)
                grafo[i][j] = peso
                grafo[j][i] = peso
                
    return grafo, posiciones

def comparar_algoritmos():
    datos = []
    
    for tamano in [100, 250, 500]:
        grafo, posiciones = generar_grafo_con_coordenadas(tamano)
        
        inicio_nodo = 0
        fin_nodo = tamano - 1
        
        # Benchmark Dijkstra
        tracemalloc.start()  
        inicio_tiempo = time.perf_counter()
        
        dijkstra(grafo, inicio_nodo, fin_nodo)
        
        tiempo_d = time.perf_counter() - inicio_tiempo
        pico_memoria_d = tracemalloc.get_traced_memory()[1]  
        tracemalloc.stop()   
        
        # Benchmark A*
        tracemalloc.start()
        inicio_tiempo = time.perf_counter()
        
        astar(grafo, inicio_nodo, fin_nodo, posiciones)
        
        tiempo_a = time.perf_counter() - inicio_tiempo
        pico_memoria_a = tracemalloc.get_traced_memory()[1]  
        tracemalloc.stop()
        
        datos.append({
            'Nodos': tamano, 
            'Dijkstra Tiempo (s)': tiempo_d, 
            'A* Tiempo (s)': tiempo_a,
            'Dijkstra Memoria (KB)': pico_memoria_d / 1024,
            'A* Memoria (KB)': pico_memoria_a / 1024
        })
    
    return pd.DataFrame(datos)

if __name__ == "__main__":
    df_resultados = comparar_algoritmos()
    print("\n---------- Resultados ---------- ")
    print(df_resultados.to_string(index=False))

    # Definimos los nodos para usarlos en el eje X de las funciones de dibujo manual
    nodos_x = df_resultados['Nodos'].astype(str).tolist()

    # VENTANA 1: ANALISIS DE TIEMPO DE EJECUCION
    fig1, (ax1_time, ax2_time) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. Graficos de tiempos
    # 1.1 Grafico lineal de tiempos (left)
    df_graficos = df_resultados.set_index('Nodos')
    df_graficos[['Dijkstra Tiempo (s)', 'A* Tiempo (s)']].plot(kind='line', marker='o', ax=ax1_time)
    ax1_time.set_title('Tendencia de Crecimiento Temporal')
    ax1_time.set_ylabel('Tiempo (segundos)')
    ax1_time.set_xlabel('Número de Nodos (V)')
    ax1_time.grid(True)
    ax1_time.legend(['Dijkstra', 'A*'])

    # 1.2 Gráfico bastones de tiempo (right)
    # Separacion bastones
    x_indices = range(len(nodos_x))
    offset = 0.15

    # Bastones Dijkstra
    ax2_time.vlines([x - offset for x in x_indices], ymin=0, ymax=df_resultados['Dijkstra Tiempo (s)'], color='C0', linewidth=2, label='Dijkstra')
    ax2_time.scatter([x - offset for x in x_indices], df_resultados['Dijkstra Tiempo (s)'], color='C0', s=20, zorder=3)

    # Bastones A*
    ax2_time.vlines([x + offset for x in x_indices], ymin=0, ymax=df_resultados['A* Tiempo (s)'], color='C1', linewidth=2, label='A*')
    ax2_time.scatter([x + offset for x in x_indices], df_resultados['A* Tiempo (s)'], color='C1', s=20, zorder=3)

    ax2_time.set_title('Comparación por Bastones de Tiempos')
    ax2_time.set_ylabel('Tiempo (segundos)')
    ax2_time.set_xlabel('Número de Nodos (V)')
    ax2_time.set_xticks(x_indices)
    ax2_time.set_xticklabels(nodos_x)
    ax2_time.grid(axis='y', linestyle='--')
    ax2_time.legend()

    plt.suptitle('Evaluación de Eficiencia Temporal: Dijkstra vs A*', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # VENTANA 2: ANALISIS DE CONSUMO DE MEMORIA RAM (PICO)

    fig2, (ax1_mem, ax2_mem) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 2. Graficos de picos de memoria
    # 2.1 Gráfico Lineal de Memoria (left)
    df_graficos[['Dijkstra Memoria (KB)', 'A* Memoria (KB)']].plot(kind='line', marker='s', linestyle='--', ax=ax1_mem)
    ax1_mem.set_title('Tendencia de Crecimiento Espacial')
    ax1_mem.set_ylabel('Memoria Consumida (KB)')
    ax1_mem.set_xlabel('Número de Nodos (V)')
    ax1_mem.grid(True)
    ax1_mem.legend(['Dijkstra', 'A*'])

    # 2.2 Gráfico de Bastones (Lollipop) de Memoria (left)
    # Bastones Dijkstra
    ax2_mem.vlines([x - offset for x in x_indices], ymin=0, ymax=df_resultados['Dijkstra Memoria (KB)'], color='C0', linewidth=2, label='Dijkstra')
    ax2_mem.scatter([x - offset for x in x_indices], df_resultados['Dijkstra Memoria (KB)'], color='C0', s=20, zorder=3)

    # Bastones A*
    ax2_mem.vlines([x + offset for x in x_indices], ymin=0, ymax=df_resultados['A* Memoria (KB)'], color='C1', linewidth=2, label='A*')
    ax2_mem.scatter([x + offset for x in x_indices], df_resultados['A* Memoria (KB)'], color='C1', s=20, zorder=3)

    ax2_mem.set_title('Comparación por Bastones de Memoria')
    ax2_mem.set_ylabel('Memoria Consumida (KB)')
    ax2_mem.set_xlabel('Número de Nodos (V)')
    ax2_mem.set_xticks(x_indices)
    ax2_mem.set_xticklabels(nodos_x)
    ax2_mem.grid(axis='y', linestyle='--')
    ax2_mem.legend()

    plt.suptitle('Evaluación de Eficiencia Espacial (Memoria RAM): Dijkstra vs A*', fontsize=14, fontweight='bold')
    plt.tight_layout()

    # Mostrar ventanas
    plt.show()