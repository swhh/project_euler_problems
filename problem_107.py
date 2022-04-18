import heapq
from collections import defaultdict, namedtuple


FILE = 'network.txt'
"""The following undirected network consists of seven vertices and twelve edges with a total weight of 243.


The same network can be represented by the matrix below.

    	A	B	C	D	E	F	G
A	-	16	12	21	-	-	-
B	16	-	-	17	20	-	-
C	12	-	-	28	-	31	-
D	21	17	28	-	18	19	23
E	-	20	-	18	-	-	11
F	-	-	31	19	-	-	27
G	-	-	-	23	11	27	-
However, it is possible to optimise the network by removing some edges and still ensure that all points on the network remain connected. The network which achieves the maximum saving is shown below. It has a weight of 93, representing a saving of 243 − 93 = 150 from the original network."""

TEST_GRAPH = {0: {1: 16, 2: 12, 3: 21}, 1: {0: 16, 3: 17, 4: 20}, 2: {0: 12, 3: 28, 5: 31},
              3: {0: 21, 1: 17, 2: 28, 4: 18, 5: 19, 6: 23},
               4: {1: 20, 3: 18, 6: 11}, 5: {2: 31, 3: 19, 6: 27}, 6: {3: 23, 4: 11, 5: 27}}

Vertex = namedtuple('Vertex', ('key', 'node'))


def read_graph(file):
    """Return graph from matrix in file"""
    with open(file) as f:
        graph = defaultdict(dict)
        for i, line in enumerate(f):
            for j, weight in enumerate(line[:-1].split(',')):
                if weight != '-':
                    graph[i][j] = int(weight)
    return graph


def graph_total_weight(graph):
    return sum(sum(neighbours.values()) for neighbours in graph.values()) / 2


def generate_heap(graph):
    heap = []
    for vertex in graph.keys():
        weight = float('inf') if vertex else 0
        node = Vertex(weight, vertex)
        heap.append(node)
    heapq.heapify(heap)
    return heap


def min_span_tree_max_saving(graph):
    """Return max saving from graph based on minimum spanning tree"""
    graph_weight = graph_total_weight(graph)
    min_span_tree_weight = 0
    remaining_nodes = generate_heap(graph)
    node_map = {node.node: node.key for node in remaining_nodes}
    seen = set()

    while True:
        least_node = heapq.heappop(remaining_nodes)
        if least_node.key == float('inf'):
            break
        if least_node.node in seen:
            continue
        seen.add(least_node.node)
        min_span_tree_weight += least_node.key
        for neighbour in graph[least_node.node].keys():
            if neighbour not in seen:
                weight = graph[least_node.node][neighbour]
                if weight < node_map[neighbour]:
                    node_map[neighbour] = weight
                    heapq.heappush(remaining_nodes, Vertex(weight, neighbour))

    return int(graph_weight - min_span_tree_weight)


def test():
    total_weight = graph_total_weight(TEST_GRAPH)
    max_saving = min_span_tree_max_saving(TEST_GRAPH)
    assert total_weight == 243
    assert max_saving == 150


if __name__ == '__main__':
    test()
    graph = read_graph(FILE)
    print(min_span_tree_max_saving(graph))


