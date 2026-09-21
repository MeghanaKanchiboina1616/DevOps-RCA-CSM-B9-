# Research Datasets

This directory contains datasets used by the Context-Aware AI DevOps RCA project.

## RCAEval

RCAEval is used as the primary benchmark dataset for root-cause-analysis experiments.

Official dataset:

https://huggingface.co/datasets/phamquiluan/RCAEval

Official repository:

https://github.com/phamquiluan/RCAEval

The current RCAEval release contains:

- 735 failure cases
- 9 datasets
- 3 benchmark suites: RE1, RE2, RE3
- 3 microservice systems:
  - Online Boutique
  - Sock Shop
  - Train Ticket
- 11 fault types

The complete dataset is approximately 3.44 GB.

## Local installation

The dataset should be downloaded locally using:

```powershell
python research\download_rcaeval.py