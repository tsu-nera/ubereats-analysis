#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate ubereats

HOMEDIR=${HOME}/repo/ubereats-analysis

cd ${HOMEDIR}

inv crawl
inv update-premerge
