"""
Output Types for MST System

========================
Overview
========================
This module defines different output formats for the MST computation.

Each output type:
- Chooses the appropriate builder (data representation)
- Extracts the required result from the constructed tree

========================
Design Pattern
========================

Factory Pattern:
Each OutputType is responsible for creating the correct builder.
This decouples the MST algorithm from the output representation.

========================
Output Types
========================

Weight:
    Returns only the total weight of the MST.
    Uses a lightweight builder that stores only the sum.

Edges:
    Returns the list of edges in the MST.

EdgesAndWeight:
    Returns both:
        (edges, total weight)

========================
Design Decisions
========================

- OutputType controls what data is stored during computation.
- Avoids unnecessary work (e.g., no edges stored if only weight is needed).
- Keeps the algorithm independent of output format.

========================
Summary
========================

This design enables flexible and efficient output handling,
while keeping the system modular and extensible.
"""

from abc import ABC
from builders import *

class MSTOutputType(ABC):
    @classmethod
    def create_binner(cls):
        raise NotImplementedError()

    @classmethod
    def extract(cls, binner, tree):
        raise NotImplementedError()

class Weight(MSTOutputType):

    @classmethod
    def create_binner(cls):
        return BuilderKeepingWeight()

    @classmethod
    def extract(cls, binner, tree):
        return binner.weight(tree)

class Edges(MSTOutputType):

    @classmethod
    def create_binner(cls):
        return BuilderKeepingEdges()

    @classmethod
    def extract(cls, binner, tree):
        return tree[1]

class EdgesAndWeight(MSTOutputType):

    @classmethod
    def create_binner(cls):
        return BuilderKeepingEdges()

    @classmethod
    def extract(cls, binner, tree):
        return (tree[1], binner.weight(tree))