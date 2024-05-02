# Rich_KGRS

This is the code and data of experiments for paper "The Effect of Semantic Knowledge Graph Richness on Embedding Based Recommender Systems"

The data could be downloaded via [https://zenodo.org/records/11102893](https://zenodo.org/records/11102893)


Before running the experiemnts, you should to make sure put all the `*.ckpt` files and all the decompressed `exp*` folders into correct path as following:
```
.
├── knowledge_graph/
│   ├── *.ttl (put .ttl files from downloaded data here)
│   └── ...
├── ontologies/
│   └── full_ontologies/
│       └── all ontologies
├── knowledge_graph_generator/
│   └── code to generate KGs
├── RecBole/
│   └── data/ (put exp1-7 folder files from downloaded data here)/
│       ├── exp1/
│       │   ├── exp1.inter
│       │   ├── exp1.item
│       │   ├── exp1.kg
│       │   ├── exp1.link
│       │   └── exp1.user
│       └── ...
├── OpenKE/ (put .ckpt files from downloaded data here)/
│   ├── *.ckpt/
│   │   └── benchmark/ (put decompressed benchmark folder here)/
│   │       ├── exp1/
│   │       │   ├── entity2id.txt
│   │       │   ├── relation2id.txt
│   │       │   └── train2id.txt
│   │       └── ...
│   └── ...
├── ml-1m/
├── mappings/
└── ...
```

## Experiments

### Prepare

Conda is recommended as the python environment for experiments.
```
conda create -n RichKGRS python=3.9
conda activate RichKGRS
pip install -r RecBole/requirements.txt
pip install -r requirements.txt
mv config.yaml RecBole/
mv bole_exp.py RecBole/
```

### Preprocess
To clone RecBole and OpenKE
```
git submodule update --init --recursive
```

### Run

```
source exp.sh
```