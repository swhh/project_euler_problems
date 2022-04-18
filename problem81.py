import heapq
from collections import defaultdict

FILE = 'matrix.txt'

TEST_MATRIX = '131,673,234,103,18,201,96,342,965,150,630,803,746,422,111,537,699,497,121,956,805,732,524,37,331'


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
            row = (int(num) for num in line[:-1].split(',') if num != '')

    return graph


def minimal_path_sum(graph):
    distances = dijkstra(graph, 0)
    target = max(graph.keys())
    return distances[target]


def test():
    test_matrix = [int(num) for num in TEST_MATRIX.split(',')]
    test_graph = defaultdict(dict)

    for i, num in enumerate(test_matrix):
        if not i:
            test_graph[0][1] = num
        if i:
            test_graph[i][i + 1] = num
        if i > 4:
            test_graph[i - 4][i + 1] = num
    assert minimal_path_sum(test_graph) == 2472


if __name__ == '__main__':
    test()
    graph = read_matrix(FILE)
    print(minimal_path_sum(graph))

