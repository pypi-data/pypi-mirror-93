# -*- coding: utf-8 -*-

"""An implementation of Reverse Causal Reasoning (RCR) described by [Catlett2013]_.

.. [Catlett2013] ﻿Catlett, N. L., *et al* (2013). `Reverse causal reasoning: applying qualitative causal knowledge to
                 the interpretation of high-throughput data <https://doi.org/10.1186/1471-2105-14-340>`_.
                 BMC Bioinformatics, 14(1), 340.
"""

from collections import defaultdict

import pandas
import scipy.stats
from scipy.special import binom

from pybel import BELGraph
from pybel.constants import CAUSAL_DECREASE_RELATIONS, CAUSAL_INCREASE_RELATIONS, RELATION

__all__ = [
    'run_rcr',
]


def _point_probability(k, n, l, p: float = 0.5):  # noqa:E741
    return binom(n - l, k) * p ** k * (1 - p) ** (n - k - l)


def _concordance(k: int, n: int, m: int, l, p: float = 0.5):  # noqa:E741
    return sum(
        _point_probability(j, n, l, p)
        for j in range(k, min(n - 1, m))
    )


def run_rcr(graph: BELGraph, tag: str = 'dgxp'):
    """Run the reverse causal reasoning algorithm on a graph.

    Steps:

    1. Get all downstream controlled things into map (that have at least 4 downstream things)
    2. calculate population of all things that are downstream controlled

    .. note:: Assumes all nodes have been pre-tagged with data

    :param graph: A BEL graph
    :param tag: The key for the nodes' data dictionaries that corresponds to the integer value for its differential
     expression.
    """
    # Step 1: Calculate the hypothesis subnetworks (just simple star graphs)
    hypotheses = defaultdict(set)
    increases = defaultdict(set)
    decreases = defaultdict(set)

    for u, v, d in graph.edges(data=True):
        hypotheses[u].add(v)

        if d[RELATION] in CAUSAL_INCREASE_RELATIONS:
            increases[u].add(v)

        elif d[RELATION] in CAUSAL_DECREASE_RELATIONS:
            decreases[u].add(v)

    # Step 2: Calculate the matching of the data points to the causal relationships

    #: A dictionary from {tuple controller node: int count of correctly matching observations}
    correct = defaultdict(int)
    #: A dictionary from {tuple controller node: int count of incorrectly matching observations}
    contra = defaultdict(int)
    #: A dictionary from {tuple controller node: int count of ambiguous observations}
    ambiguous = defaultdict(int)
    #: A dictionary from {tuple controller node: int count of missing obvservations}
    missing = defaultdict(int)

    for controller, downstream_nodes in hypotheses.items():
        if len(downstream_nodes) < 4:
            continue  # need enough data to make reasonable calculations!

        for node in downstream_nodes:

            if node in increases[controller] and node in decreases[controller]:
                ambiguous[controller] += 1

            elif node in increases[controller]:
                if graph.nodes[node][tag] == 1:
                    correct[controller] += 1
                elif graph.nodes[node][tag] == -1:
                    contra[controller] += 1

            elif node in decreases[controller]:
                if graph.nodes[node][tag] == 1:
                    contra[controller] += 1
                elif graph.nodes[node][tag] == -1:
                    correct[controller] += 1

            else:
                missing[controller] += 1

    # Step 3: Keep only controller nodes who have 4 or more downstream nodes
    controllers = {
        controller
        for controller, downstream_nodes in hypotheses.items()
        if 4 <= len(downstream_nodes)
    }

    # Step 4: Calculate concordance scores
    concordance_scores = {
        controller: scipy.stats.beta(0.5, correct[controller], contra[controller])
        for controller in controllers
    }

    # Step 5: Calculate richness scores
    # TODO

    # Calculate the population as the union of all downstream nodes for all controllers
    # population = {
    #     node
    #     for controller in controllers
    #     for node in hypotheses[controller]
    # }
    # population_size = len(population)

    # Step 6: Export

    return pandas.DataFrame({
        'contra': contra,
        'correct': correct,
        'concordance': concordance_scores,
    })
