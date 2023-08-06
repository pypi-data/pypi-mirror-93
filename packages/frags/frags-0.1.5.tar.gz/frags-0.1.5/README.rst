Find Recombinations Among Genomes (FRAGS)
=========================================

Find Recombinations Among Genomes (FRAGS) is a software dedicated to analyze recombinations in viral genomes.

.. image:: https://badge.fury.io/py/frags.svg
    :target: https://badge.fury.io/py/frags
    :alt: Pypi repo

.. image:: https://gitlab.pasteur.fr/nmaillet/frags/badges/master/pipeline.svg
    :target: https://gitlab.pasteur.fr/nmaillet/frags/commits/master
    :alt: Build Status

.. image:: https://gitlab.pasteur.fr/nmaillet/frags/badges/master/coverage.svg
    :target: https://gitlab.pasteur.fr/nmaillet/frags/commits/master
    :alt: Coverage Report

.. image:: https://readthedocs.org/projects/frags/badge/?version=latest
    :target: https://frags.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

:note: FRAGS is tested with Gitlab Ci for the following Python version: 3.7 to 3.8
:issues: Please use https://gitlab.pasteur.fr/nmaillet/frags



Overview
========

Find Recombinations Among Genomes (FRAGS), is a standalone software dedicated to identify reads coming from recombination events.

FRAGS is a python tool taking fasta/fastq files of reads as input and one or two reference genomes. It then identifies chimeric reads (reads composed of non-adjacent fragsments, coming either from on one or the two references genomes) and potential breakpoints (insert between fragsments). Optionally, breakpoints can then be Blasted again the host genome, if provided.

Main results are in CSV files. Three CSV files contain respectively results for reads that have fragsments coming from the first reference only, the second reference only or both references. Another CSV file contains headers of reads that did not match anywhere. Finally, three files are produced when using Blast: ``breakpoints.fasta``, containing the breakpoint portions to Blast, ``res_blast.csv`` containing the result of Blast on ``breakpoints.csv`` and ``compressed.fasta``, a compressed version of ``res_blast.csv`` keeping only results of the best e-value/bit-score for each input sequences and produce a fasta-like file.

FRAGS follows the standards for software development with continuous integration on Gitlab (https://gitlab.pasteur.fr/nmaillet/frags) and automatic on-line documentation (https://frags.readthedocs.io/en/latest/).



Installation
============

In order to install FRAGS, you can use **pip**:

.. code-block:: shell

    pip3 install frags

This command installs FRAGS and its Python dependencies.


Usage
=====

From the command line:

.. code-block:: shell

    frags --help
