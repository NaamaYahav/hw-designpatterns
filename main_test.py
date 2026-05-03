# Put your unit-tests here. 
import pytest
from main import *
from outputtypes import *

# Helper functions to check if the edges form a valid tree
def is_acyclic(edges):
    parent = {}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x,y):
        parent[find(x)] = find(y)

    nodes = set()
    for u,v,_ in edges:
        nodes.add(u)
        nodes.add(v)

    for node in nodes:
        parent[node] = node

    for u,v,_ in edges:
        if find(u) == find(v):
            return False
        union(u,v)
    return True

def is_connected(edges):
    nodes = set()
    for u,v,_ in edges:
        nodes.add(u)
        nodes.add(v)
    visited = set()

    def dfs(u):
        visited.add(u)
        for x,y,_ in edges:
            if x == u and y not in visited:
                dfs(y)
            if y == u and x not in visited:
                dfs(x)

    start = next(iter(nodes))
    dfs(start)
    return visited == nodes

def is_graph_connected(graph):
    if not graph:
        return True

    visited = set()

    def dfs(u):
        visited.add(u)
        for v, _ in graph[u]:
            if v not in visited:
                dfs(v)

    start = next(iter(graph))
    dfs(start)

    return len(visited) == len(graph)

#basic test
def test_medium_graph():
    graph = {
        0: [(1,4),(2,1)],
        1: [(0,4),(2,2),(3,5)],
        2: [(0,1),(1,2),(3,8)],
        3: [(1,5),(2,8)]
    }
    assert mst(kruskal, graph, Weight) == 8
    assert mst(prim, graph, Weight) == 8

# Test that both algorithms produce the same weight for the same graph(and that the graph can be represented in both formats)
def test_same_weight_across_algorithms_and_inputs():
    graph = {
        0: [(1,10),(2,6),(3,5)],
        1: [(0,10),(3,15)],
        2: [(0,6),(3,4)],
        3: [(0,5),(1,15),(2,4)]
    }

    matrix = [
        [0,10,6,5],
        [10,0,0,15],
        [6,0,0,4],
        [5,15,4,0]
    ]
    # same algorithm, different input format
    assert mst(kruskal, graph, Weight) == mst(kruskal, matrix, Weight)
    assert mst(prim, graph, Weight) == mst(prim, matrix, Weight)

    # different algorithm, same result
    assert mst(kruskal, graph, Weight) == mst(prim, graph, Weight)
    assert mst(kruskal, matrix, Weight) == mst(prim, matrix, Weight)

# Single node graph should have weight 0 and no edges
def test_single_node():
    graph = {0: []}
    assert mst(kruskal, graph, Weight) == 0
    assert mst(prim, graph, Weight) == 0

# Disconnected graph should have weight 0 and no edges  
def test_disconnected_graph():
    graph = {
        0: [],
        1: [],
        2: []
    }
    assert mst(kruskal, graph, Weight) == 0
    assert mst(prim, graph, Weight) == 0

#Edges correctness
@pytest.mark.parametrize("algo", [kruskal, prim])
def test_edges_match_weight(algo):
    matrix = [
        [0,1,3],
        [1,0,2],
        [3,2,0]
    ]

    edges = mst(algo, matrix, Edges)
    total = sum(w for _,_,w in edges)
    assert total == mst(algo, matrix, Weight)

@pytest.mark.parametrize("algo", [kruskal, prim])
def test_edges_form_valid_tree(algo):
    graph = {
        0: [(1,1),(2,3)],
        1: [(0,1),(2,2)],
        2: [(0,3),(1,2)]
    }

    edges = mst(algo, graph, Edges)

    assert len(edges) == 2          # n-1 edges
    assert is_acyclic(edges)        # no cycles
    assert is_connected(edges)      # connected

#Combined output
@pytest.mark.parametrize("algo", [kruskal, prim])
def test_edges_and_weight_output(algo):
    graph = {
        0: [(1,1),(2,3)],
        1: [(0,1),(2,2)],
        2: [(0,3),(1,2)]
    }

    edges, weight = mst(algo, graph, EdgesAndWeight)

    assert sum(w for _,_,w in edges) == weight
    assert len(edges) == 2
    assert is_acyclic(edges)
    assert is_connected(edges)

# Additional robustness tests
def test_equal_weights_graph():
    graph = {
        0: [(1,1),(2,1)],
        1: [(0,1),(2,1)],
        2: [(0,1),(1,1)]
    }

    assert mst(kruskal, graph, Weight) == 2
    assert mst(prim, graph, Weight) == 2


def test_duplicate_edges_handling():
    graph = {
        0: [(1,1)],
        1: [(0,1)]  # duplicate
    }

    assert mst(kruskal, graph, Weight) == 1
    assert mst(prim, graph, Weight) == 1

# ====random graphs test=====

#Helper function to generate random graphs
def generate_random_graph(n, edge_prob=0.5, max_weight=20):
    """Generate random undirected graph (adjacency list)"""
    graph = {i: [] for i in range(n)}

    for i in range(n):
        for j in range(i+1, n):
            if random.random() < edge_prob:
                w = random.randint(1, max_weight)
                graph[i].append((j, w))
                graph[j].append((i, w))

    return graph


def graph_to_matrix(graph, n):
    """Convert adjacency list to matrix"""
    matrix = [[0]*n for _ in range(n)]
    for u in graph:
        for v, w in graph[u]:
            matrix[u][v] = w
            matrix[v][u] = w
    return matrix

@pytest.mark.parametrize("n", [5, 7, 10])
def test_random_graphs(n):
    for _ in range(10): 
        graph = generate_random_graph(n)

        if not is_graph_connected(graph):
            continue
        
        if all(len(v) == 0 for v in graph.values()):
            continue
        
        w1 = mst(kruskal, graph, Weight)
        w2 = mst(prim, graph, Weight)
        assert w1 == w2
        edges = mst(kruskal, graph, Edges)

        if edges:
            assert len(edges) <= n - 1
            assert is_acyclic(edges)
            assert is_connected(edges)

        matrix = graph_to_matrix(graph, n)

        w11 = mst(kruskal, graph, Weight)
        w22 = mst(kruskal, matrix, Weight)

        assert w11 == w22
        edges = mst(kruskal, graph, Edges)

        if edges:
            assert len(edges) <= n - 1
            assert is_acyclic(edges)
            assert is_connected(edges)
            