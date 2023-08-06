# -*- coding: utf-8 -*-

"""This class contains an alternate implementation of the PyBEL database manager that only stores graphs in memory."""

from dataclasses import dataclass
from typing import Iterable, List

from pybel import BELGraph


@dataclass
class _Namespace:
    id: int


class DictManager:
    """A dictionary-based implementation of the PyBEL Manager."""

    def __init__(self):
        self.universe = None
        self.networks = {}
        self.disease_to_id = {}
        self.hash_to_node = {}

    def insert_graph(self, graph: BELGraph, **_kwargs):
        """Insert a graph and return the resulting ORM object (mocked)."""
        result = _Namespace(id=len(self.networks))
        self.networks[result.id] = graph
        return result

    def get_graph_by_id(self, network_id: int) -> BELGraph:
        """Get a graph by its identifier."""
        return self.networks[network_id]

    def get_graphs_by_ids(self, network_ids: Iterable[int]) -> List[BELGraph]:
        """Get several graphs by their identifiers."""
        return [
            self.networks[network_id]
            for network_id in network_ids
        ]
