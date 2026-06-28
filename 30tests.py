import random
import time
import pandas as pd
import tracemalloc
from Dijkstra import dijkstra
from AStar import astar

def generar_grafo_con_coordenadas(num_nodos, densidad=0.2):
    posiciones = {i: (random.randint(0, 500), random.randint(0, 500)) for i in range(num_nodos)}
    grafo = [[None for _ in range(num_nodos)] for _ in range(num_nodos)]
    for i in range(num_nodos):
        for j in range(i + 1, num_nodos):
            if random.random() < densidad:
                peso = random.randint(10, 100)
                grafo[i][j] = peso
                grafo[j][i] = peso
    return grafo, posiciones

def ejecutar_muestreo_masivo(replicaciones=30):
    datos_completos = []
    
    print(f"Iniciando experimento estadístico con {replicaciones} ejecuciones por escala...")
    
    for tamano in [100, 250, 500, 1000]:
        print(f"-> Procesando entorno con {tamano} nodos...")
        
        for i in range(1, replicaciones + 1):
            # Generamos un grafo nuevo y unico en cada una de las 30 corridas
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
            
            # Guardar 
            datos_completos.append({
                'id_muestra': i,
                'Nodos': tamano, 
                'Dijkstra_Tiempo': tiempo_d, 
                'AStar_Tiempo': tiempo_a,
                'Dijkstra_Memoria': pico_memoria_d / 1024,
                'AStar_Memoria': pico_memoria_a / 1024
            })
            
    return pd.DataFrame(datos_completos)

if __name__ == "__main__":
    # Ejecutar 30 pruebas
    df_estadistico = ejecutar_muestreo_masivo(replicaciones=30)
    
    # Exportar a csv resultados_algoritmos.csv
    nombre_archivo = "resultados_algoritmos.csv"
    df_estadistico.to_csv(nombre_archivo, index=False)
    
    print("\nCompletado")
    print(f"Resultados: '{nombre_archivo}'")