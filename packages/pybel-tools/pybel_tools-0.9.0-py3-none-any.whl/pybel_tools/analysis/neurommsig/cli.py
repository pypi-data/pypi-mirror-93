# -*- coding: utf-8 -*-

"""This module contains the CLI to export NeuroMMSig as BEL.

To run, type :code:`python3 -m pybel_tools.analysis.neurommsig` in the command line
"""

import logging
import os

import click

from .export import get_nift_values, mesh_alzheimer, mesh_parkinson, preprocess, write_neurommsig_bel


@click.command()
@click.argument('bms_base')
@click.argument('neurommsig_base')
def main(bms_base, neurommsig_base):
    """Convert the Alzheimer's and Parkinson's disease NeuroMMSig excel sheets to BEL."""
    logging.basicConfig(level=logging.INFO)

    neurommsig_excel_dir = os.path.join(neurommsig_base, 'resources', 'excels', 'neurommsig')

    nift_values = get_nift_values()

    click.echo('Starting Alzheimers')

    ad_path = os.path.join(neurommsig_excel_dir, 'alzheimers', 'alzheimers.xlsx')
    ad_df = preprocess(ad_path)
    with open(os.path.join(bms_base, 'aetionomy', 'alzheimers', 'neurommsigdb_ad.bel'), 'w') as ad_file:
        write_neurommsig_bel(ad_file, ad_df, mesh_alzheimer, nift_values)

    click.echo('Starting Parkinsons')

    pd_path = os.path.join(neurommsig_excel_dir, 'parkinsons', 'parkinsons.xlsx')
    pd_df = preprocess(pd_path)
    with open(os.path.join(bms_base, 'aetionomy', 'parkinsons', 'neurommsigdb_pd.bel'), 'w') as pd_file:
        write_neurommsig_bel(pd_file, pd_df, mesh_parkinson, nift_values)


if __name__ == '__main__':
    main()
