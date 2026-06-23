import heapq

def dijkstra(graph, start, end):
    n = len(graph)
    distances = [float('inf')] * n
    distances[start] = 0
    previous_vertices = [-1] * n
    
    queue = [(0, start)]
    visited = set()

    while queue:
        curr_dist, curr_vertex = heapq.heappop(queue)
        
        if curr_vertex in visited:
            continue
        visited.add(curr_vertex)
        
        if curr_vertex == end:
            break

        for neighbor, weight in enumerate(graph[curr_vertex]):
            if weight is not None and neighbor not in visited:
                distance = curr_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_vertices[neighbor] = curr_vertex
                    heapq.heappush(queue, (distance, neighbor))

    path, curr_vertex = [], end
    while curr_vertex != -1:
        path.append(curr_vertex)
        curr_vertex = previous_vertices[curr_vertex]
    path.reverse()
    
    return distances[end], path