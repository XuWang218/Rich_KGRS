import rdflib
import tqdm

def query_movie_info_via_imdbid_over_wikidata_endpoint(item_uri,imdbid):
    if not imdbid.startswith('tt0'):
        imdbid = 'tt0'+imdbid
    g = rdflib.Graph()
    imdbid = imdbid.strip()
    construct_query = """
    Prefix wdt: <http://www.wikidata.org/prop/direct/>
    Prefix wd: <http://www.wikidata.org/entity/>
    Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    CONStruct {
        """+item_uri+""" ?predicate ?object.
        ?object rdfs:label ?object_label.
        }
    WHERE
    {
      SERVICE <https://query.wikidata.org/sparql>{
      ?item wdt:P345 '"""+imdbid+"""'.
      ?item ?predicate ?object.
      OPTIONAL {
      ?object rdfs:label ?object_label.
      FILTER(lang(?object_label) = 'en')
      }
      FILTER(STRSTARTS(STR(?predicate), STR(wdt:)))
    #   FILTER(STRSTARTS(STR(?object), STR(wd:)))
      }
    }
    """
    qres = g.query(construct_query)
    return qres

#read merged data
import pandas as pd

df_merged = pd.read_csv('merged.csv')
for i in tqdm.tqdm(range(len(df_merged))):
    item_uri = "<http://anonymous.nl/movie-rating-ontology/"+str(df_merged.loc[i]['movieId'])+">"
    imdbid = str(df_merged.loc[i]['imdbId'])
    # print(imdbid)
    qres = query_movie_info_via_imdbid_over_wikidata_endpoint(item_uri,imdbid)
    #convert qres to triples and store triples in a file
    with open('../knowledge_graph/KG_wikidata_literal_object.ttl', 'a+') as f:
        for row in qres:
            # print(row[0], row[1], row[2])
            # convert row to rdflib tiple and store in the ttl file
            f.write(row[0].n3()+' '+row[1].n3()+' '+row[2].n3()+' .\n')
            
