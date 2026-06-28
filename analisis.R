# Analisis de resultados para 30 pruebas ejecutadas por cada iteracion con 100, 250, 500 y 1000 nodos

# Leer archivos
datos <- read.csv("resultados_algoritmos.csv")
datos$Nodos <- factor(datos$Nodos)

# Dividir pruebas por cantidad de nodos
data_100 <- subset(datos, Nodos == "100")
data_250 <- subset(datos, Nodos == "250")
data_500 <- subset(datos, Nodos == "500")
data_1000 <- subset(datos, Nodos == "1000")

# Medidas de resumen

print("--- 100 Nodos ---")

print("--- Métricas de Tiempo para Dijkstra ---")
summary(data_100$Dijkstra_Tiempo)
cat("Desviación Estándar:", sd(data_100$Dijkstra_Tiempo), "\n\n")

print("--- Métricas de Tiempo para A* ---")
summary(data_100$AStar_Tiempo)
cat("Desviación Estándar:", sd(data_100$AStar_Tiempo), "\n\n")

print("--- Métricas de Memoria (Pico KB) para Dijkstra ---")
summary(data_100$Dijkstra_Memoria)
cat("Desviación Estándar:", sd(data_100$Dijkstra_Memoria), "\n\n")

print("--- Métricas de Memoria (Pico KB) para A* ---")
summary(data_100$AStar_Memoria)
cat("Desviación Estándar:", sd(data_100$AStar_Memoria), "\n\n")


print("--- 250 Nodos ---")

print("--- Métricas de Tiempo para Dijkstra ---")
summary(data_250$Dijkstra_Tiempo)
cat("Desviación Estándar:", sd(data_250$Dijkstra_Tiempo), "\n\n")

print("--- Métricas de Tiempo para A* ---")
summary(data_250$AStar_Tiempo)
cat("Desviación Estándar:", sd(data_250$AStar_Tiempo), "\n\n")

print("--- Métricas de Memoria (Pico KB) para Dijkstra ---")
summary(data_250$Dijkstra_Memoria)
cat("Desviación Estándar:", sd(data_250$Dijkstra_Memoria), "\n\n")

print("--- Métricas de Memoria (Pico KB) para A* ---")
summary(data_250$AStar_Memoria)
cat("Desviación Estándar:", sd(data_250$AStar_Memoria), "\n\n")


print("--- 500 Nodos ---")

print("--- Métricas de Tiempo para Dijkstra ---")
summary(data_500$Dijkstra_Tiempo)
cat("Desviación Estándar:", sd(data_500$Dijkstra_Tiempo), "\n\n")

print("--- Métricas de Tiempo para A* ---")
summary(data_500$AStar_Tiempo)
cat("Desviación Estándar:", sd(data_500$AStar_Tiempo), "\n\n")

print("--- Métricas de Memoria (Pico KB) para Dijkstra ---")
summary(data_500$Dijkstra_Memoria)
cat("Desviación Estándar:", sd(data_500$Dijkstra_Memoria), "\n\n")

print("--- Métricas de Memoria (Pico KB) para A* ---")
summary(data_500$AStar_Memoria)
cat("Desviación Estándar:", sd(data_500$AStar_Memoria), "\n\n")


print("--- 1000 Nodos ---")

print("--- Métricas de Tiempo para Dijkstra ---")
summary(data_1000$Dijkstra_Tiempo)
cat("Desviación Estándar:", sd(data_1000$Dijkstra_Tiempo), "\n\n")

print("--- Métricas de Tiempo para A* ---")
summary(data_1000$AStar_Tiempo)
cat("Desviación Estándar:", sd(data_1000$AStar_Tiempo), "\n\n")

print("--- Métricas de Memoria (Pico KB) para Dijkstra ---")
summary(data_1000$Dijkstra_Memoria)
cat("Desviación Estándar:", sd(data_1000$Dijkstra_Memoria), "\n\n")

print("--- Métricas de Memoria (Pico KB) para A* ---")
summary(data_1000$AStar_Memoria)
cat("Desviación Estándar:", sd(data_1000$AStar_Memoria), "\n\n")


# Prueba de hipotesis

# H0: mu_Dijkstra - mu_AStar <= 0 (Dijkstra es igual o más rápido que A*)
# H1: mu_Dijkstra - mu_AStar > 0 (Dijkstra tarda más que A*, es decir, A* es más eficiente)

# Evaluamos la diferencia de tiempos usando el t.test de tu formulario (Sección 1.2 / Página 1)

# Usamos muestras independientes (paired = FALSE es el valor por defecto)
t.test(data_1000$Dijkstra_Tiempo, data_1000$AStar_Tiempo, alternative = "greater", conf.level = 0.95)

# P valor menor que alfa se rechaza H0
# Hay suficiente evidencia para afirmar de que A* es mas rapido que Dijkstra