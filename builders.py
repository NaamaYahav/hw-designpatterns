"""
MST Builder Module

========================
Overview
========================
This module defines the builders used to construct the MST.

A builder manages how the tree is represented and updated
during the execution of an MST algorithm.

========================
Design Pattern
========================

Flyweight Pattern:
The builder controls the internal representation of the tree
and ensures that only the required data is stored.

Different builders store different levels of information,
allowing efficient memory usage.

========================
Builders
========================

BuilderKeepingWeight:
    Stores only the total weight of the MST.
    Does not keep edge information.

BuilderKeepingEdges:
    Stores both:
        - Total weight
        - List of edges

========================
Design Decisions
========================

- The tree is updated in-place for efficiency.
- The weight is stored in a mutable structure ([0]) to allow shared updates.
- The algorithm interacts only with the builder interface,
  without knowing how the data is stored.

========================
Summary
========================

This design separates the MST algorithm from the data representation,
allowing flexible and efficient computation based on the required output.
"""

from abc import ABC, abstractmethod

class MSTBuilder(ABC):

    @abstractmethod
    def new_tree(self):
        pass

    @abstractmethod
    def add_edge(self, tree, u, v, w):
        pass

    @abstractmethod
    def weight(self, tree):
        pass
    
class BuilderKeepingWeight(MSTBuilder):

    def new_tree(self):
        return ([0] , None) 

    def add_edge(self, tree, u, v, w):
        tree[0][0] += w

    def weight(self, tree):
        return tree[0][0]
    
class BuilderKeepingEdges(MSTBuilder):

    def new_tree(self):
        return ([0], [])  # weight, edges

    def add_edge(self, tree, u, v, w):
        weight, edges = tree
        weight[0] += w
        edges.append((u, v, w))  # inplace!

    def weight(self, tree):
        return tree[0][0]