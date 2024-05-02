#!/bin/bash

for exp in "$@" 
do
    for i in {1..1}; do python RecBole/bole_exp.py --model=CKE --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/bole_exp.py --model=CFKG --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/bole_exp.py --model=KGAT --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/bole_exp.py --model=KGCN --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/bole_exp.py --model=KGIN --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/bole_exp.py --model=KGNNLS --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/bole_exp.py --model=KTUP --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/bole_exp.py --model=MKR --dataset=$exp --config_files=config.yaml; done
    for i in {1..1}; do python RecBole/bole_exp.py --model=RippleNet --dataset=$exp --config_files=config.yaml; done

    for i in {1..1}; do python transe_lp.py $exp; done
    for i in {1..1}; do python transe_lp.py $exp; done
    for i in {1..1}; do python transe_lp.py $exp; done
    for i in {1..1}; do python transe_lp.py $exp; done
    for i in {1..1}; do python transe_lp.py $exp; done
    for i in {1..1}; do python transe_lp.py $exp; done
    for i in {1..1}; do python transe_lp.py $exp; done
    for i in {1..1}; do python transe_lp.py $exp; done
    for i in {1..1}; do python transe_lp.py $exp; done
done

