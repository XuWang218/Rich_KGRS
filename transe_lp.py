import torch
from ranx import Qrels, Run, evaluate
import csv
import networkx as nx
from itertools import combinations
from OpenKE.openke.data import TrainDataLoader
from OpenKE.openke.module.model import TransE
from tqdm import tqdm
import sys

assert len(sys.argv) == 2, "Please provide the experiment name as an argument (e.g. exp1)"

class GetOutOfLoop( Exception ):
    pass

def triple_score(h, r, t):
    norm = torch.norm(h + r - t, p=2)
    return norm.item()

def path_score(triples, triple_score_dict):
    path_score = 0.0
    for triple in triples:
        path_score += triple_score_dict(triple)
    path_score /= len(triples)
    return path_score

def get_highest_path_with_score(g:nx.Graph, h, t, index, triple_score_dict):
    max_score = -1000000.0
    max_path = []
    for path in nx.all_simple_paths(g, source=h, target=t, cutoff=3):
        try:
            tuple_pairs = list(combinations(path, 2))
            triples = []
            for pair in tuple_pairs:
                e1, e2 = pair
                if (e1, e2) in index:
                    triples.append((e1, index[(e1, e2)], e2))
                elif (e2, e1) in index:
                    triples.append((e2, index[(e2, e1)], e1))
                else:
                    raise GetOutOfLoop
            score = path_score(triples, triple_score_dict)
            if score > max_score:
                max_score = score
                max_path = path
        except GetOutOfLoop:
            continue            
    return max_path, max_score

exp = str(sys.argv[1])
kg_path = f"./OpneKE/benchmarks/{exp}/train2id.txt"
ent2id_path = f"./OpneKE/benchmarks/{exp}/entity2id.txt"
rel2id_path = f"./OpneKE/benchmarks/{exp}/relation2id.txt"
rating_path = "./ml-1m/ratings.dat"
movie_path = "./ml-1m/movies.dat"

train_dataloader = TrainDataLoader(
		in_path = f"./OpneKE/benchmarks/{exp}/", 
		nbatches = 100,
		threads = 6, 
		sampling_mode = "normal", 
		bern_flag = 1, 
		filter_flag = 1, 
		neg_ent = 25,
		neg_rel = 0)

transe = TransE(
		ent_tot = train_dataloader.get_ent_tot(),
		rel_tot = train_dataloader.get_rel_tot(),
		dim = 100,
		p_norm = 1, 
		norm_flag = True)

transe.load_checkpoint(f'./OpneKE/transe_{exp}.ckpt')
entity_embeddings = transe.ent_embeddings
relation_embeddings = transe.rel_embeddings

g = nx.DiGraph()

triple_score_dict = {}
index = {}
with open(kg_path, 'r') as f:
    reader = csv.reader(f,delimiter='\t')
    length = int(next(reader)[0])
    pb = tqdm(total=length,desc="Precomputing triple scores")
    for row in reader:
        s, o, p = row
        key = (s, o)
        index[key]=p
        s_emb = entity_embeddings(torch.tensor([int(s)], dtype=torch.long)).squeeze(0)
        o_emb = entity_embeddings(torch.tensor([int(o)], dtype=torch.long)).squeeze(0)
        p_emb = relation_embeddings(torch.tensor([int(p)], dtype=torch.long)).squeeze(0)
        score1 = triple_score(s_emb, p_emb, o_emb)
        score2 = triple_score(o_emb, p_emb, s_emb)
        # triple_score_dict[(s,p,o)] = score
        g.add_edge(int(s),int(o),weight=score1)
        g.add_edge(int(o),int(s),weight=score2)
        pb.update(1)
    pb.close()

ent2id_dict = {}
with open(ent2id_path, 'r') as f:
    reader = csv.reader(f,delimiter='\t')
    next(reader)
    for row in reader:
        ent2id_dict[row[0]] = int(row[1])

movie_list = []
with open(movie_path, 'r', encoding="latin-1") as f:
    for line in f:
        row = line.split("::")
        movie_list.append("mr:Movie/"+row[0])

qrels_dict = {}
for i in range(1,6041,1):
    qrels_dict["mr:User/"+str(i)] = {}
with open(rating_path, 'r') as f:
    for line in f:
        row = line.split("::")
        qrels_dict["mr:User/"+row[0]]["mr:Movie/"+row[1]] = int(row[2])



# with open(kg_path, 'r') as f:
#     reader = csv.reader(f,delimiter='\t')
#     next(reader)
#     for row in reader:
#         g.add_edge(int(row[0]), int(row[1]))
paths = nx.johnson(g, weight='weight')
run_dict = {}
for i in tqdm(range(1,6041,1)):
    run_dict["mr:User/"+str(i)] = {}
    userid = ent2id_dict["mr:User/"+str(i)]
    for movie in tqdm(movie_list):
        if movie not in ent2id_dict:
            continue
        movieid = ent2id_dict[movie]
        # score = get_highest_path_with_score(g, userid, movieid, index, triple_score_dict)
        # length,path = nx.single_source_dijkstra(g, source=userid, target=movieid,cutoff=3, weight='weight')
        path = paths[userid][movieid]
        path_weight = sum(g[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))/(len(path)-1)
        run_dict["mr:User/"+str(i)][movie] = -path_weight
        
qrels = Qrels(qrels_dict)
run = Run(run_dict)
print(f"The results of {exp} are:")
print(evaluate(qrels, run, ["hits@10","precision@10","recall@10","ndcg@10","mrr@10"]))
