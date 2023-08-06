#!/usr/bin/env python3

"""
|===========================|
| Modelisation du cluster   |
| de travail par un graphe. |
|===========================|

* Cela permet de modeliser et de representer
les connection qu'il peut y avoir entre
les differentes machines d'un reseau.
* Cette partie permet de pouvoir optimiser la
repartition des taches en se basant sur la theorie
des graphes.
* De facon generale, avoir une information precise
des machines environante est necessaire pour
pouvoir faire du travail en grappe.
"""

from .basegraph import BaseGraph


__all__ = ["edge", "vertex", "Graph", "BaseGraph"]


class Graph(BaseGraph):
    """
    |===================================|
    | Graphe abstrait mathematique avec |
    | le plus de proprietes possible.   |
    |===================================|


    Example
    -------
    >>> from raisin.graph import *
    >>> g1 = Graph() # graphe modifiable car pas d'arguments
    >>> g1
    Graph()
    >>> g1.add_edges((0, 2), (0, 3), (1, 2))
    >>> g1
    Graph({Edge(Vertex(n=0), Vertex(n=2), n=0), ..., Edge(Vertex(n=1), Vertex(n=2), n=2)})
    >>> g1 = Graph(g1) # graphe fige, mais avec plus de methodes
    >>> g1
    BipartiteGraph({Edge(Vertex(n=0), Vertex(n=2), n=0), ..., Edge(Vertex(n=1), Vertex(n=2), n=2)})
    >>>
    """
    def __new__(cls, *args, **kwargs):
        """
        |========================================|
        | Constructeur qui retourne une instance |
        | de graphe la plus evoluee possible.    |
        |========================================|

        * L'assemblage est fait par une metaclasse.
        """
        graph = super(BaseGraph, cls).__new__(cls)
        graph.__init__(*args, **kwargs)
        return graph
