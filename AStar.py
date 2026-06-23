import heapq
import math

def heuristic(nodo_actual, nodo_destino, posiciones):
    x1, y1 = posiciones[nodo_actual]
    x2, y2 = posiciones[nodo_destino]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def astar(graph, start, end, posiciones):
    num_nodos = len(graph)
    f_score = {node: float('inf') for node in range(num_nodos)}
    f_score[start] = heuristic(start, end, posiciones)

    frontier = [(f_score[start], start)]
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == end:
            break

        for neighbor, distance in enumerate(graph[current]):
            if distance is None:
                continue

            new_cost = cost_so_far[current] + distance
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, end, posiciones)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    path = [end]
    while path[-1] != start:
        try:
            path.append(came_from[path[-1]])
        except:
            break
    path.reverse()

    return cost_so_far.get(end, 0), path