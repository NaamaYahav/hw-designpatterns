# Put your code here. You can add files if needed.
from collections import defaultdict
import heapq
from builders import *
from outputtypes import *
import random

"""
Minimum Spanning Tree (MST) System using Design Patterns

========================
Overview
========================
This system computes a Minimum Spanning Tree (MST) for a graph using:
- Two input types: adjacency matrix / adjacency list
- Two algorithms: Kruskal and Prim
- Multiple output types: weight, edges, or both

The input type is detected automatically.

========================
Design Patterns
========================

Strategy Pattern:
The algorithm (Kruskal / Prim) is passed as a parameter to mst(),
allowing easy extension without modifying existing code.

Flyweight Pattern:
The MSTBuilder manages the tree structure and stores only the required data
(e.g., weight only or full edges), avoiding unnecessary memory usage.

Factory Pattern:
Each OutputType creates the appropriate builder, separating
the algorithm logic from the output representation.

========================
Design Decisions
========================

- All inputs are converted to a unified edge list representation.
- Duplicate edges in undirected graphs are removed.
- The tree is updated in-place for efficiency.
- Only required data is computed based on the output type.

========================
Extensibility
========================

The system can be easily extended by:
- Adding new algorithms
- Adding new output types
- Supporting additional input formats

========================
Summary
========================

The implementation is modular, efficient, and avoids code duplication,
while supporting multiple configurations as required.
"""

#Seprate function to parse the input graph into a common format (list of edges)
def parse_input(graph):
    if isinstance(graph, list): # Adjacency matrix
        edges=[]
        n=len(graph)
        for i in range(n):
            for j in range(i+1, n):
                if graph[i][j] != 0:
                    if i < j:
                        edges.append((i, j, graph[i][j]))
        return edges
    elif isinstance(graph, dict): # Adjacency list
        edges=[]
        for u in graph:
            for v, w in graph[u]:
                if u < v: 
                    edges.append((u, v, w))
        return edges
    else:
        raise ValueError("Unknown graph format")

def mst(algorithm: callable, graph, outputtype):
    """
    >>> matrix = [
    ... [0,1,3],
    ... [1,0,2],
    ... [3,2,0]
    ... ]

    >>> adj = {
    ... 0: [(1,1),(2,3)],
    ... 1: [(0,1),(2,2)],
    ... 2: [(0,3),(1,2)]
    ... }

    #combinations of algorithm and outputtype:
    >>> mst(kruskal, matrix, Weight)
    3
    >>> mst(kruskal, matrix, Edges)
    [(0, 1, 1), (1, 2, 2)]

    >>> mst(kruskal, adj, Weight)
    3
    >>> mst(kruskal, adj, Edges)
    [(0, 1, 1), (1, 2, 2)]

    >>> mst(prim, matrix, Weight)
    3
    >>> mst(prim, matrix, Edges)
    [(0, 1, 1), (1, 2, 2)]

    >>> mst(prim, adj, Weight)
    3
    >>> mst(prim, adj, Edges)
    [(0, 1, 1), (1, 2, 2)]
    """
    edges = parse_input(graph)
    builder = outputtype.create_binner()
    tree = builder.new_tree()
    algorithm(builder, edges, tree)
    return outputtype.extract(builder, tree)

# Implement Kruskal's algorithm to find the MST
def kruskal(builder: MSTBuilder, edges: list, tree: any):
    parent={}
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]    
    def union(x, y):
        parent[find(x)] = find(y)
    nodes=set()
    for u,v, _ in edges:
        nodes.add(u)
        nodes.add(v)
    for node in nodes:
        parent[node] = node
    for u, v, w in sorted(edges, key=lambda x: x[2]):
        if find(u) != find(v):
            union(u, v)
            builder.add_edge(tree, u, v, w)
    return tree

# Implement Prim's algorithm to find the MST
def prim(builder: MSTBuilder, edges: list, tree: any):
    if not edges:
        return tree
    graph = defaultdict(list)
    nodes = set()
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
        nodes.add(u)
        nodes.add(v)
    start = next(iter(nodes))
    visited = set([start])
    heap = []
    for v, w in graph[start]:
        heapq.heappush(heap, (w, start, v))

    while heap:
        w, u, v = heapq.heappop(heap)
        if v not in visited:
            visited.add(v)
            builder.add_edge(tree, u, v, w)
            for to, weight in graph[v]:
                if to not in visited:
                    heapq.heappush(heap, (weight, v, to))

    return tree

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
