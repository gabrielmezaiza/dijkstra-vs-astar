import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import tracemalloc
import networkx as nx
from Dijkstra import dijkstra
from AStar import astar

def generar_grafo_con_coordenadas(num_nodos, densidad=0.005):
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

def visualizar_ruta(grafo_matriz, posiciones, ruta):
    G = nx.Graph()
    num_nodos = len(grafo_matriz)
    
    # Añadir nodos
    for i in range(num_nodos):
        G.add_node(i, pos=posiciones[i])
        
    # Añadir aristas
    for i in range(num_nodos):
        for j in range(i + 1, num_nodos):
            if grafo_matriz[i][j] is not None:
                G.add_edge(i, j)
                
    pos = nx.get_node_attributes(G, 'pos')
    
    plt.figure(figsize=(12, 10)) 
    
    # Imprimir nodos y aristas
    nx.draw(G, pos, node_size=15, node_color='teal', edge_color='gray', alpha=0.3, with_labels=False)
    
    # Imprimir ruta
    if ruta and len(ruta) > 0:
        ruta_edges = [(ruta[i], ruta[i+1]) for i in range(len(ruta)-1)]
        nx.draw_networkx_nodes(G, pos, nodelist=ruta, node_size=40, node_color='indianred')
        nx.draw_networkx_edges(G, pos, edgelist=ruta_edges, edge_color='indianred', width=2.5)
        
        # Indicar nodo inicial y final
        nx.draw_networkx_nodes(G, pos, nodelist=[ruta[0]], node_size=120, node_color='mediumseagreen', edgecolors='none')
        nx.draw_networkx_nodes(G, pos, nodelist=[ruta[-1]], node_size=120, node_color='sandybrown', edgecolors='none')
        
    # Titulo
    plt.title("Camino más corto encontrado (1000 Nodos)", fontsize=16, fontweight='bold', pad=20)
    
    # Leyenda
    import matplotlib.lines as mlines
    inicio_legend = mlines.Line2D([], [], color='white', marker='o', markerfacecolor='mediumseagreen', markeredgecolor='none', markersize=10, label='Inicio')
    fin_legend = mlines.Line2D([], [], color='white', marker='o', markerfacecolor='sandybrown', markeredgecolor='none', markersize=10, label='Fin')
    ruta_legend = mlines.Line2D([], [], color='indianred', linewidth=2.5, label='Ruta Óptima')
    plt.legend(handles=[inicio_legend, fin_legend, ruta_legend], loc='upper right')
    
    plt.tight_layout() # Ajustar margenes
    plt.show()
    
def comparar_algoritmos():
    datos = []
    # Para cada tamano de nodos
    for tamano in [100, 250, 500, 1000]:
        print(f"Procesando grafo de {tamano} nodos...")
        grafo, posiciones = generar_grafo_con_coordenadas(tamano, densidad=0.005)
        
        inicio_nodo = 0
        fin_nodo = tamano - 1
        
        # Benchmark Dijkstra
        tracemalloc.start()  
        inicio_tiempo = time.perf_counter()
        
        _, ruta_d = dijkstra(grafo, inicio_nodo, fin_nodo)
        
        tiempo_d = time.perf_counter() - inicio_tiempo
        pico_memoria_d = tracemalloc.get_traced_memory()[1]  
        tracemalloc.stop()   
        
        # Benchmark A*
        tracemalloc.start()
        inicio_tiempo = time.perf_counter()
        
        _, ruta_a = astar(grafo, inicio_nodo, fin_nodo, posiciones)
        
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

        # Graficar caso 1000 nodos
        if tamano == 1000:
            print("Generando visualización de 1000 nodos (esto puede tardar unos segundos)...")
            visualizar_ruta(grafo, posiciones, ruta_a)
    
    return pd.DataFrame(datos)

if __name__ == "__main__":
    df_resultados = comparar_algoritmos()
    print("\n---------- Resultados ---------- ")
    print(df_resultados.to_string(index=False))

    fig, (ax_time, ax_mem) = plt.subplots(1, 2, figsize=(14, 5))
    df_graficos = df_resultados.set_index('Nodos')
    
    # 1. Gráfico de Tiempos
    df_graficos[['Dijkstra Tiempo (s)', 'A* Tiempo (s)']].plot(kind='line', marker='o', linewidth=2, ax=ax_time)
    ax_time.set_title('Tendencia de Crecimiento Temporal', fontweight='bold')
    ax_time.set_ylabel('Tiempo (segundos)')
    ax_time.set_xlabel('Número de Nodos (V)')
    ax_time.grid(True, linestyle='--', alpha=0.7)
    
    # 2. Gráfico de Memoria
    df_graficos[['Dijkstra Memoria (KB)', 'A* Memoria (KB)']].plot(kind='line', marker='s', linestyle='--', linewidth=2, ax=ax_mem)
    ax_mem.set_title('Tendencia de Crecimiento Espacial (RAM)', fontweight='bold')
    ax_mem.set_ylabel('Memoria Consumida (KB)')
    ax_mem.set_xlabel('Número de Nodos (V)')
    ax_mem.grid(True, linestyle='--', alpha=0.7)

    plt.suptitle('Evaluación de Eficiencia: Dijkstra vs A*', fontsize=16, fontweight='bold', y=1.05)
    plt.tight_layout()
    plt.show()