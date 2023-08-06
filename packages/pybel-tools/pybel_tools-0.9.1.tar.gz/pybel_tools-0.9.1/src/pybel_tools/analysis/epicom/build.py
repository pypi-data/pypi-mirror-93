# -*- coding: utf-8 -*-

"""Builds the relational database on all graphs with subgraph annotations"""

import logging
import time
from typing import Optional

import pybel
from .algorithm import get_drug_scores
from .models import Score

logger = logging.getLogger(__name__)

NEUROMMSIG_DEFAULT_URL = 'https://arty.scai.fraunhofer.de/artifactory/bel/annotation/neurommsig/neurommsig-1.0.3.belanno'


def get_networks_using_annotation(manager: pybel.Manager, annotation: str):
    """

    :param pybel.manager.Manager manager:
    :param str annotation:
    :return: list[pybel.manager.models.Network]
    """
    raise NotImplementedError


def get_drug_model(manager: pybel.Manager, name: str):
    """

    :param pybel.manager.Manager manager:
    :param str name:
    :return: pybel.manager.models.NamespaceEntry
    """
    raise NotImplementedError


def build_database(manager: pybel.Manager, annotation_url: Optional[str] = None) -> None:
    """Build a database of scores for NeuroMMSig annotated graphs.

    1. Get all networks that use the Subgraph annotation
    2. run on each
    """
    annotation_url = annotation_url or NEUROMMSIG_DEFAULT_URL

    annotation = manager.get_namespace_by_url(annotation_url)

    if annotation is None:
        raise RuntimeError('no graphs in database with given annotation')

    networks = get_networks_using_annotation(manager, annotation)

    dtis = ...

    for network in networks:
        graph = network.as_bel()

        scores = get_drug_scores(graph, dtis)

        for (drug_name, subgraph_name), score in scores.items():
            drug_model = get_drug_model(manager, drug_name)
            subgraph_model = manager.get_annotation_entry(annotation_url, subgraph_name)

            score_model = Score(
                network=network,
                annotation=subgraph_model,
                drug=drug_model,
                score=score
            )

            manager.session.add(score_model)

    t = time.time()
    logger.info('committing scores')
    manager.session.commit()
    logger.info('committed scores in %.2f seconds', time.time() - t)
