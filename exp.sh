#!/bin/bash

for exp in "$@" 
do
    for i in {1..1}; do python RecBole/run_recbole.py --model=CKE --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/run_recbole.py --model=CFKG --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/run_recbole.py --model=KGAT --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/run_recbole.py --model=KGCN --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/run_recbole.py --model=KGIN --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/run_recbole.py --model=KGNNLS --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/run_recbole.py --model=KTUP --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/run_recbole.py --model=MKR --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/run_recbole.py --model=RippleNet --dataset=$exp --config_files=config.yaml; done
done

