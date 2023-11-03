#!/bin/bash

# docker build -t slurm_base_rocky8:21 -f slurm_base/Dockerfile .

docker build -t inojeon/qe_slurm_master_rocky8:21 -f slurm_master/Dockerfile .
docker build -t inojeon/qe_slurm_worker_rocky8:21 -f slurm_worker/Dockerfile .


