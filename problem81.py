import heapq
from collections import defaultdict

FILE = 'matrix.txt'


def dijkstra(graph, source):
    distance_so_far = defaultdict(lambda: float('inf'))
    final_distance = dict()
    heap = [(0, source)]
    distance_so_far[source] = 0
    seen = {0}
    while len(heap) > 0:
        distance, smallest = heapq.heappop(heap)
        final_distance[smallest] = distance
        for neighbor in graph[smallest].keys():
            new_dist = distance + graph[smallest][neighbor]
            if new_dist < distance_so_far[neighbor]:
                distance_so_far[neighbor] = new_dist
                heapq.heapify(heap)
            if neighbor not in seen:
                seen.add(neighbor)
                heapq.heappush(heap, (distance_so_far[neighbor], neighbor))

    return final_distance


def read_matrix(file):
    with open(file) as f:
        graph = defaultdict(dict)
        for i, line in enumerate(f):
            row = [int(num) for num in line[:-1].split(',')]
            if not i:
                graph[0][1] = row[0]
            for j, num in enumerate(row):
                node = len(row) * i + j
                if j:
                    graph[node][node + 1] = num
                if i:
                    graph[node + 1 - len(row)][node + 1] = num
    return graph


def minimal_path_sum(graph):
    distances = dijkstra(graph, 0)
    target = max(graph.keys())
    return distances[target]


if __name__ == '__main__':
    graph = read_matrix(FILE)
    print(minimal_path_sum(graph))

