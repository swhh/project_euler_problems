import networkx as nx
import itertools
from collections import defaultdict

"""A common security method used for online banking is to ask the user for three random characters from a passcode. For example, if the passcode was 531278, they may ask for the 2nd, 3rd, and 5th characters; the expected reply would be: 317.

The text file, keylog.txt, contains fifty successful login attempts.

Given that the three characters are always asked for in order, analyse the file so as to determine the shortest possible secret passcode of unknown length."""


"""Approach: Represent digits as nodes in DAG; maintain set of dags consistent with seen logs; 
choose dag with minimum number of nodes and then use topological sort to generate shortest possible secret code
"""


FILE = 'keylog.txt'

TEST_CODE = "531278"
TEST_LOGS = ["317", "518", "278", "512", "537"]
SECOND_TEST_CODE = "4596796"
SECOND_TEST_LOGS = ["497", "696", "967", "579", "459", "969", "976"]


def read_key_log(file):
    with open(file, 'r') as f:
        new_logs = []
        for line in f:
            new_logs.append(line[:-1])
    return new_logs


def add_to_graph(log, dag, a_node=None, b_node=None, c_node=None):
    """Create new graph based on dag that adds new edges and nodes"""
    a, b, c = log
    size = dag.number_of_nodes()
    new_dag = dag.copy()
    i = 1
    if not a_node:
        new_dag.add_node(size + i, num=a)
        a_node = size + i
        i += 1
    if not b_node:
        new_dag.add_node(size + i, num=b)
        b_node = size + i
        i += 1
    if not c_node:
        new_dag.add_node(size + i, num=c)
        c_node = size + i
    new_dag.add_edge(a_node, b_node)
    new_dag.add_edge(b_node, c_node)
    return new_dag


def update_dag(log, dag):
    """Generate any extension of the dag based on log that does not lead to a cycle"""
    new_dags = []
    a, b, c = log
    a_match = [node for node, num in dag.nodes(data='num') if num == a]
    b_match = [node for node, num in dag.nodes(data='num') if num == b]
    c_match = [node for node, num in dag.nodes(data='num') if num == c]
    a_match = a_match if a_match else [None]
    b_match = b_match if b_match else [None]
    c_match = c_match if c_match else [None]

    # case 1 add all new nodes
    new_dag = add_to_graph(log, dag)
    new_dags.append(new_dag)

    for a_node, b_node, c_node in itertools.product(a_match, b_match, c_match):
        if a_node and b_node and c_node:  # case 2 add no new nodes
            # check if three nodes connected already, in which case return list with just old dag;
            if nx.has_path(dag, a_node, b_node) and nx.has_path(dag, b_node, c_node):
                return [dag]
            new_dag = add_to_graph(log, dag, a_node=a_node, b_node=b_node, c_node=c_node)
            if nx.is_directed_acyclic_graph(new_dag):
                new_dags.append(new_dag)
            # case 3 add some new nodes
        if a_node:
            new_dag = add_to_graph(log, dag, a_node=a_node)
            new_dags.append(new_dag)
        if b_node:
            new_dag = add_to_graph(log, dag, b_node=b_node)
            new_dags.append(new_dag)
        if c_node:
            new_dag = add_to_graph(log, dag, c_node=c_node)
            new_dags.append(new_dag)

        if a_node and b_node:
            new_dag = add_to_graph(log, dag, a_node=a_node, b_node=b_node)
            if nx.is_directed_acyclic_graph(new_dag):
                new_dags.append(new_dag)
        if b_node and c_node:
            new_dag = add_to_graph(log, dag, b_node=b_node, c_node=c_node)
            if nx.is_directed_acyclic_graph(new_dag):
                new_dags.append(new_dag)
        if a_node and c_node:
            new_dag = add_to_graph(log, dag, a_node=a_node, c_node=c_node)
            if nx.is_directed_acyclic_graph(new_dag):
                new_dags.append(new_dag)

    return new_dags


def update_dags(log, dags):
    new_dags = []
    for dag in dags:
        new = update_dag(log, dag)
        new_dags.extend(new)
    new_dags.sort(key=nx.number_of_nodes)
    return new_dags[:100]


def min_dag(dags):
    return min(dags, key=nx.number_of_nodes)


def minimum_possible_passcode(logs):
    graph = nx.DiGraph()
    dags = [graph]
    seen_logs = defaultdict(lambda: False)
    for log in logs:
        if not seen_logs[log]:
            dags = update_dags(log, dags)
            seen_logs[log] = True
    dag = min_dag(dags)
    codes = (dag.nodes[node]['num'] for node in nx.topological_sort(dag))
    return ''.join(codes)


def test():
    min_code = minimum_possible_passcode(TEST_LOGS)
    assert min_code == TEST_CODE
    min_code = minimum_possible_passcode(SECOND_TEST_LOGS)
    assert min_code == SECOND_TEST_CODE


if __name__ == '__main__':
    test()
    logs = read_key_log(FILE)
    print(minimum_possible_passcode(logs))












