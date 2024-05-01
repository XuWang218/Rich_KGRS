import rdflib

g_wiki = rdflib.Graph()
g_wiki.parse("knowledge_graph/KG_wikidata_literal_object.ttl", format="ttl")

mr = rdflib.Namespace("http://anonymous.nl/movie-rating-ontology/")
rdf = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")
owl = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
xsd = rdflib.Namespace("http://www.w3.org/2001/XMLSchema#")

alignment_file = "Mapping/Alignment.tsv"
alignment_dict = {}
with open(alignment_file, 'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('\t')
        alignment_dict["http://www.wikidata.org/prop/direct/"+line[1]] = line[0].replace('mr:','http://anonymous.nl/movie-rating-ontology/')
Occupation_dict = {}
with open('Mapping/occupation.csv', 'r') as f:
    for line in f:
        line = line.strip()
        line = line.split(',')
        Occupation_dict[line[0]] = line[1]
genre_dict = {}
with open('Mapping/genre.csv', 'r') as f:
    for line in f:
        line = line.strip()
        line = line.split(',')
        genre_dict[line[0]] = line[1].replace('mr:','http://ontology.tno.nl/movie-ontology/')
rating_dict = {}
with open('Mapping/rating.csv', 'r') as f:
    for line in f:
        line = line.strip()
        line = line.split(',')
        rating_dict[line[0]] = line[1].replace('mr:','http://ontology.tno.nl/movie-ontology/')

movielens_user_file = "ml-1m/users.dat"
movielens_movie_file = "ml-1m/movies.dat"
movielens_rating_file = "ml-1m/ratings.dat"

# kg0
g0 = rdflib.Graph()
g0.bind("mr", mr)
g0.bind("rdf", rdf)
g0.bind("rdfs", rdfs)
g0.bind("owl", owl)
g0.bind("xsd", xsd)
g0.parse("ontologies/full_ontologies/ontology0.ttl", format="ttl")

with open(movielens_rating_file,'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        user = rdflib.URIRef(mr+"User/"+line[0])
        movie = rdflib.URIRef(mr+"Movie/"+line[1])
        rating = rdflib.URIRef(mr+"Rating/"+line[0]+"_"+line[1])
        g0.add((user, rdf.type, mr.User))
        g0.add((movie, rdf.type, mr.Movie))
        g0.add((rating, rdf.type, mr.Rating))
        g0.add((user, mr.providesRating, rating))
        g0.add((movie, mr.hasRating, rating))
        g0.add((rating,mr.providedByUser,user))
        g0.add((rating,mr.isAboutMovie,movie))
g0.parse("ontologies/full_ontologies/ontology0.ttl", format="ttl")
g0.serialize("knowledge_graph/KG0.ttl", format="ttl")
g0.close()

# kg1
g1 = rdflib.Graph()
g1.bind("mr", mr)
g1.bind("rdf", rdf)
g1.bind("rdfs", rdfs)
g1.bind("owl", owl)
g1.bind("xsd", xsd)
g1.parse("ontologies/full_ontologies/ontology1.ttl", format="ttl")

for triple in g_wiki:
    if str(triple[1]) == "http://www.wikidata.org/prop/direct/P1476":
        movie = triple[0]
        g1.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))

with open(movielens_user_file,'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        user = rdflib.URIRef(mr+"User/"+line[0])
        zipcode = rdflib.Literal(line[4], datatype=xsd.string)
        gender = rdflib.Literal(line[1], datatype=xsd.string)
        age = rdflib.Literal(line[2], datatype=xsd.string)
        occupation = rdflib.URIRef(mr+"Occupation/"+line[3])
        g1.add((user, rdf.type, mr.User))
        g1.add((user, mr.hasZipcode, zipcode))
        g1.add((user, mr.hasGender, gender))
        g1.add((user, mr.hasAgeRange, age))
        g1.add((user, mr.hasOccupation, occupation))
with open(movielens_movie_file,'r',encoding='latin-1') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        movie = rdflib.URIRef(mr+"Movie/"+line[0])
        genre_list = line[2].split('|')
        g1.add((movie, rdf.type, mr.Movie))
        for genre in genre_list:
            g1.add((movie, mr.hasGenre, rdflib.Literal(genre, datatype=xsd.string)))
with open(movielens_rating_file,'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        user = rdflib.URIRef(mr+"User/"+line[0])
        movie = rdflib.URIRef(mr+"Movie/"+line[1])
        rating = rdflib.URIRef(mr+"Rating/"+line[0]+"_"+line[1])
        g1.add((rating, mr.hasRatingValue, rdflib.Literal(line[2], datatype=xsd.string)))
        g1.add((rating, mr.hasTimestamp, rdflib.Literal(line[3], datatype=xsd.string)))
        g1.add((rating, rdf.type, mr.Rating))
        g1.add((rating, mr.providedByUser, user))
        g1.add((rating, mr.isAboutMovie, movie))
        g1.add((user, mr.providesRating, rating))
        g1.add((movie, mr.hasRating, rating))
g1.serialize("knowledge_graph/KG1.ttl", format="ttl")
g1.close()

# kg1+

gender_dict = {
    "M": mr["Male"],
    "F": mr["Female"]
}

age_dict = {
    "1": mr["AgeRangeUnder18"],
    "18": mr["AgeRange18to24"],
    "25": mr["AgeRange25to34"],
    "35": mr["AgeRange35to44"],
    "45": mr["AgeRange45to49"],
    "50": mr["AgeRange50to55"],
    "56": mr["AgeRange56plus"]
}

occupation_dict = {
    "0": mr["OccupationOther"],
    "1": mr["OccupationAcademicEducator"],
    "2": mr["OccupationArtist"],
    "3": mr["OccupationClericalAdmin"],
    "4": mr["OccupationCollegeGradStudent"],
    "5": mr["OccupationCustomerService"],
    "6": mr["OccupationDoctorHealthCare"],
    "7": mr["OccupationExecutiveManagerial"],
    "8": mr["OccupationFarmer"],
    "9": mr["OccupationHomemaker"],
    "10": mr["OccupationK12Student"],
    "11": mr["OccupationLawyer"],
    "12": mr["OccupationProgrammer"],
    "13": mr["OccupationRetired"],
    "14": mr["OccupationSalesMarketing"],
    "15": mr["OccupationScientist"],
    "16": mr["OccupationSelfEmployed"],
    "17": mr["OccupationTechnicianEngineer"],
    "18": mr["OccupationTradesmanCraftsman"],
    "19": mr["OccupationUnemployed"],
    "20": mr["OccupationWriter"]
}

genre_dict = {
    "Action": mr["GenreAction"],
    "Adventure": mr["GenreAdventure"],
    "Animation": mr["GenreAnimation"],
    "Children's": mr["GenreChildrens"],
    "Comedy": mr["GenreComedy"],
    "Crime": mr["GenreCrime"],
    "Documentary": mr["GenreDocumentary"],
    "Drama": mr["GenreDrama"],
    "Fantasy": mr["GenreFantasy"],
    "Film-Noir": mr["GenreFilmNoir"],
    "Horror": mr["GenreHorror"],
    "Musical": mr["GenreMusical"],
    "Mystery": mr["GenreMystery"],
    "Romance": mr["GenreRomance"],
    "Sci-Fi": mr["GenreSciFi"],
    "Thriller": mr["GenreThriller"],
    "War": mr["GenreWar"],
    "Western": mr["GenreWestern"]
}

rating_dict = {
    "1": mr["OneStar"],
    "2": mr["TwoStar"],
    "3": mr["ThreeStar"],
    "4": mr["FourStar"],
    "5": mr["FiveStar"]
}

def add_score_data(g:rdflib.Graph, rating_dict):
    g.add((rating_dict["1"], mr["StarScore"], rdflib.Literal("1", datatype=rdflib.XSD.integer)))
    g.add((rating_dict["2"], mr["StarScore"], rdflib.Literal("2", datatype=rdflib.XSD.integer)))
    g.add((rating_dict["3"], mr["StarScore"], rdflib.Literal("3", datatype=rdflib.XSD.integer)))
    g.add((rating_dict["4"], mr["StarScore"], rdflib.Literal("4", datatype=rdflib.XSD.integer)))
    g.add((rating_dict["5"], mr["StarScore"], rdflib.Literal("5", datatype=rdflib.XSD.integer)))

def delete_score_data(g:rdflib.Graph, rating_dict):
    g.remove((rating_dict["1"], mr["StarScore"], rdflib.Literal("1", datatype=rdflib.XSD.integer)))
    g.remove((rating_dict["2"], mr["StarScore"], rdflib.Literal("2", datatype=rdflib.XSD.integer)))
    g.remove((rating_dict["3"], mr["StarScore"], rdflib.Literal("3", datatype=rdflib.XSD.integer)))
    g.remove((rating_dict["4"], mr["StarScore"], rdflib.Literal("4", datatype=rdflib.XSD.integer)))
    g.remove((rating_dict["5"], mr["StarScore"], rdflib.Literal("5", datatype=rdflib.XSD.integer)))

g1_plus = rdflib.Graph()
g1_plus.bind("mr", mr)
g1_plus.bind("rdf", rdf)
g1_plus.bind("rdfs", rdfs)
g1_plus.bind("owl", owl)
g1_plus.bind("xsd", xsd)
g1_plus.parse("ontologies/full_ontologies/ontology1+.ttl", format="ttl")

for triple in g_wiki:
    if str(triple[1]) == "http://www.wikidata.org/prop/direct/P1476":
        movie = triple[0]
        g1_plus.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))

with open(movielens_user_file,'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        user = rdflib.URIRef(mr+"User/"+line[0])
        zipcode = rdflib.Literal(line[4], datatype=xsd.string)
        gender = gender_dict[line[1]]
        age = age_dict[line[2]]
        occupation = occupation_dict[line[3]]
        g1_plus.add((user, rdf.type, mr.User))
        g1_plus.add((user, mr.hasZipcode, zipcode))
        g1_plus.add((user, mr.hasGender, gender))
        g1_plus.add((user, mr.hasAgeRange, age))
        g1_plus.add((user, mr.hasOccupation, occupation))

with open(movielens_movie_file,'r',encoding='latin-1') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        movie = rdflib.URIRef(mr+"Movie/"+line[0])
        title = rdflib.Literal(line[1], datatype=xsd.string)
        genre_list = line[2].split('|')
        g1_plus.add((movie, rdf.type, mr.Movie))
        g1_plus.add((movie, mr.hasTitle, title))
        for genre in genre_list:
            g1_plus.add((movie, mr.hasGenre, genre_dict[genre]))

with open(movielens_rating_file,'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        user = rdflib.URIRef(mr+"User/"+line[0])
        movie = rdflib.URIRef(mr+"Movie/"+line[1])
        rating = rdflib.URIRef(mr+"Rating/"+line[0]+"_"+line[1])
        # g1.add((rating, mr.hasRatingValue, rdflib.Literal(line[2], datatype=xsd.string)))
        g1_plus.add((rating, mr.hasStars, rating_dict[line[2]]))
        g1_plus.add((rating, mr.hasTimestamp, rdflib.Literal(line[3], datatype=xsd.string)))
        g1_plus.add((rating, rdf.type, mr.Rating))
        g1_plus.add((rating, mr.providedByUser, user))
        g1_plus.add((rating, mr.isAboutMovie, movie))
        g1_plus.add((user, mr.providesRating, rating))
        g1_plus.add((movie, mr.hasRating, rating))
g1_plus.serialize("knowledge_graph/KG1+.ttl", format="ttl")
g1_plus.close()

# kg2
g2 = rdflib.Graph()
g2.bind("mr", mr)
g2.bind("rdf", rdf)
g2.bind("rdfs", rdfs)
g2.bind("owl", owl)
g2.bind("xsd", xsd)
g2.parse("knowledge_graph/movie_description.ttl", format="ttl")
g2.parse("ontologies/full_ontologies/ontology2.ttl", format="ttl")

for triple in g_wiki:
    if str(triple[1]) == "http://www.wikidata.org/prop/direct/P1476":
        movie = triple[0]
        g2.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
    elif str(triple[1]) in alignment_dict.keys():
        if isinstance(triple[2], rdflib.URIRef):
            for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
                g2.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), obj))
        else:
            g2.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))

with open(movielens_user_file,'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        user = rdflib.URIRef(mr+"User/"+line[0])
        zipcode = rdflib.Literal(line[4], datatype=xsd.string)
        gender = gender_dict[line[1]]
        age = age_dict[line[2]]
        occupation = occupation_dict[line[3]]
        g2.add((user, rdf.type, mr.User))
        g2.add((user, mr.hasZipcode, zipcode))
        g2.add((user, mr.hasGender, gender))
        g2.add((user, mr.hasAgeRange, age))
        g2.add((user, mr.hasOccupation, occupation))

with open(movielens_movie_file,'r',encoding='latin-1') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        movie = rdflib.URIRef(mr+"Movie/"+line[0])
        title = rdflib.Literal(line[1], datatype=xsd.string)
        genre_list = line[2].split('|')
        g2.add((movie, rdf.type, mr.Movie))
        g2.add((movie, mr.hasTitle, title))
        for genre in genre_list:
            g2.add((movie, mr.hasGenre, genre_dict[genre]))

with open(movielens_rating_file,'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        user = rdflib.URIRef(mr+"User/"+line[0])
        movie = rdflib.URIRef(mr+"Movie/"+line[1])
        rating = rdflib.URIRef(mr+"Rating/"+line[0]+"_"+line[1])
        g2.add((rating, mr.hasStars, rating_dict[line[2]]))
        g2.add((rating, mr.hasTimestamp, rdflib.Literal(line[3], datatype=xsd.string)))
        g2.add((rating, rdf.type, mr.Rating))
        g2.add((rating, mr.providedByUser, user))
        g2.add((rating, mr.isAboutMovie, movie))
        g2.add((user, mr.providesRating, rating))
        g2.add((movie, mr.hasRating, rating))
g2.serialize("knowledge_graph/KG2.ttl", format="ttl")
g2.close()

# kg2+
g2_plus = rdflib.Graph()
g2_plus.bind("mr", mr)
g2_plus.bind("rdf", rdf)
g2_plus.bind("rdfs", rdfs)
g2_plus.bind("owl", owl)
g2_plus.bind("xsd", xsd)
g2_plus.parse("knowledge_graph/movie_description.ttl", format="ttl")
g2_plus.parse("ontologies/full_ontologies/ontology2+.ttl", format="ttl")

for triple in g_wiki:
    if str(triple[1]) == "http://www.wikidata.org/prop/direct/P1476":
        movie = triple[0]
        g2_plus.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
    elif str(triple[1]) == "http://www.wikidata.org/prop/direct/P161" or str(triple[1]) == "http://www.wikidata.org/prop/direct/P725":
        movie = triple[0]
        g2_plus.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
        g2_plus.add((triple[2], rdf.type, mr.Actor))
        for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
            g2_plus.add((triple[2], mr.hasName, obj))
    elif str(triple[1]) == "http://www.wikidata.org/prop/direct/P57":
        movie = triple[0]
        g2_plus.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
        g2_plus.add((triple[2], rdf.type, mr.Director))
        for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
            g2_plus.add((triple[2], mr.hasName, obj))
    elif str(triple[1]) == "http://www.wikidata.org/prop/direct/P58":
        movie = triple[0]
        g2_plus.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
        g2_plus.add((triple[2], rdf.type, mr.Writer))
        for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
            g2_plus.add((triple[2], mr.hasName, obj))
    elif str(triple[1]) == "http://www.wikidata.org/prop/direct/P272":
        movie = triple[0]
        g2_plus.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
        g2_plus.add((triple[2], rdf.type, mr.Producer))
        for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
            g2_plus.add((triple[2], mr.hasName, obj))
    elif str(triple[1]) in alignment_dict.keys():
        movie = triple[0]
        if isinstance(triple[2], rdflib.URIRef):
            for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
                g2_plus.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), obj))
        else:
            g2_plus.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))

with open(movielens_user_file,'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        user = rdflib.URIRef(mr+"User/"+line[0])
        zipcode = rdflib.Literal(line[4], datatype=xsd.string)
        gender = gender_dict[line[1]]
        age = age_dict[line[2]]
        occupation = occupation_dict[line[3]]
        g2_plus.add((user, rdf.type, mr.User))
        g2_plus.add((user, mr.hasZipcode, zipcode))
        g2_plus.add((user, mr.hasGender, gender))
        g2_plus.add((user, mr.hasAgeRange, age))
        g2_plus.add((user, mr.hasOccupation, occupation))

with open(movielens_movie_file,'r',encoding='latin-1') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        movie = rdflib.URIRef(mr+"Movie/"+line[0])
        title = rdflib.Literal(line[1], datatype=xsd.string)
        genre_list = line[2].split('|')
        g2_plus.add((movie, rdf.type, mr.Movie))
        g2_plus.add((movie, mr.hasTitle, title))
        for genre in genre_list:
            g2_plus.add((movie, mr.hasGenre, genre_dict[genre]))

with open(movielens_rating_file,'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        user = rdflib.URIRef(mr+"User/"+line[0])
        movie = rdflib.URIRef(mr+"Movie/"+line[1])
        rating = rdflib.URIRef(mr+"Rating/"+line[0]+"_"+line[1])
        g2_plus.add((rating, mr.hasStars, rating_dict[line[2]]))
        g2_plus.add((rating, mr.hasTimestamp, rdflib.Literal(line[3], datatype=xsd.string)))
        g2_plus.add((rating, rdf.type, mr.Rating))
        g2_plus.add((rating, mr.providedByUser, user))
        g2_plus.add((rating, mr.isAboutMovie, movie))
        g2_plus.add((user, mr.providesRating, rating))
        g2_plus.add((movie, mr.hasRating, rating))

worked_with_sparql = """
PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
SELECT Distinct ?person1 ?person2
WHERE {
    ?movie ?relation1 ?person1 .
    ?movie ?relation2 ?person2 .
    Filter(?person1 != ?person2)
    Values ?relation1 {wdt:P161 wdt:P725 wdt:P272 wdt:P58 wdt:P57}
    Values ?relation2 {wdt:P161 wdt:P725 wdt:P272 wdt:P58 wdt:P57}
}
"""
res = g_wiki.query(worked_with_sparql)
for row in res:
    g2_plus.add((row[0], mr.workedWith, row[1]))
    g2_plus.add((row[1], mr.workedWith, row[0]))
g2_plus.serialize("knowledge_graph/KG2+.ttl", format="ttl")
g2_plus.close()

#kg3
g3 = rdflib.Graph()
g3.bind("mr", mr)
g3.bind("rdf", rdf)
g3.bind("rdfs", rdfs)
g3.bind("owl", owl)
g3.bind("xsd", xsd)
g3.parse("knowledge_graph/movie_description.ttl", format="ttl")
g3.parse("ontologies/full_ontologies/ontology3.ttl", format="ttl")

for triple in g_wiki:
    if str(triple[1]) == "http://www.wikidata.org/prop/direct/P1476":
        movie = triple[0]
        g3.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
    elif str(triple[1]) == "http://www.wikidata.org/prop/direct/P161" or str(triple[1]) == "http://www.wikidata.org/prop/direct/P725":
        movie = triple[0]
        g3.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
        g3.add((triple[2], rdf.type, mr.Actor))
        for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
            g3.add((triple[2], mr.hasName, obj))
    elif str(triple[1]) == "http://www.wikidata.org/prop/direct/P57":
        movie = triple[0]
        g3.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
        g3.add((triple[2], rdf.type, mr.Director))
        for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
            g3.add((triple[2], mr.hasName, obj))
    elif str(triple[1]) == "http://www.wikidata.org/prop/direct/P58":
        movie = triple[0]
        g3.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
        g3.add((triple[2], rdf.type, mr.Writer))
        for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
            g3.add((triple[2], mr.hasName, obj))
    elif str(triple[1]) == "http://www.wikidata.org/prop/direct/P272":
        movie = triple[0]
        g3.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
        g3.add((triple[2], rdf.type, mr.Producer))
        for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
            g3.add((triple[2], mr.hasName, obj))
    elif str(triple[1]) in alignment_dict.keys():
        movie = triple[0]
        if isinstance(triple[2], rdflib.URIRef):
            for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
                g3.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), obj))
        else:
            g3.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))

with open(movielens_user_file,'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        user = rdflib.URIRef(mr+"User/"+line[0])
        zipcode = rdflib.Literal(line[4], datatype=xsd.string)
        gender = gender_dict[line[1]]
        age = age_dict[line[2]]
        occupation = occupation_dict[line[3]]
        g3.add((user, rdf.type, mr.User))
        g3.add((user, mr.hasZipcode, zipcode))
        g3.add((user, mr.hasGender, gender))
        g3.add((user, mr.hasAgeRange, age))
        g3.add((user, mr.hasOccupation, occupation))

with open(movielens_movie_file,'r',encoding='latin-1') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        movie = rdflib.URIRef(mr+"Movie/"+line[0])
        title = rdflib.Literal(line[1], datatype=xsd.string)
        genre_list = line[2].split('|')
        g3.add((movie, rdf.type, mr.Movie))
        g3.add((movie, mr.hasTitle, title))
        for genre in genre_list:
            g3.add((movie, mr.hasGenre, genre_dict[genre]))

with open(movielens_rating_file,'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        user = rdflib.URIRef(mr+"User/"+line[0])
        movie = rdflib.URIRef(mr+"Movie/"+line[1])
        rating = rdflib.URIRef(mr+"Rating/"+line[0]+"_"+line[1])
        g3.add((rating, mr.hasStars, rating_dict[line[2]]))
        g3.add((rating, mr.hasTimestamp, rdflib.Literal(line[3], datatype=xsd.string)))
        g3.add((rating, rdf.type, mr.Rating))
        g3.add((rating, mr.providedByUser, user))
        g3.add((rating, mr.isAboutMovie, movie))
        g3.add((user, mr.providesRating, rating))
        g3.add((movie, mr.hasRating, rating))

like_movie_sparql = """
PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT Distinct ?user ?title
WHERE {
    ?user rdf:type mr:User .
    ?user mr:providesRating ?rating .
    ?rating mr:isAboutMovie ?movie .
    ?movie mr:hasTitle ?title .
    ?rating mr:hasStars ?stars .
    Filter(?stars != mr:OneStar)
    Filter(?stars != mr:TwoStar)
}
"""
res = g3.query(like_movie_sparql)
for row in res:
    g3.add((row[0], mr.likesMovie, row[1]))
    
worked_with_sparql = """
PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT ?person1 ?person2
WHERE {
    ?movie ?relation1 ?person1 .
    ?movie ?relation2 ?person2 .
    FILTER(?person1 != ?person2)
    VALUES ?relation1 {mr:starsActor mr:directedBy mr:writtenBy mr:producedBy}
    VALUES ?relation2 {mr:starsActor mr:directedBy mr:writtenBy mr:producedBy}
}
"""
res = g3.query(worked_with_sparql)
for row in res:
    g3.add((row[0], mr.workedWith, row[1]))
    g3.add((row[1], mr.workedWith, row[0]))
# g3.update(like_movie_sparql)
#
add_score_data(g3, rating_dict)

for num in range(1,6041,1):
    user = "User/"+str(num)
    user = mr[user]

    like_genre_sparql = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
    SELECT ?genre_label (AVG(?score) as ?avg_rating) WHERE {
    ?movie mr:hasGenre ?genre .
    ?genre rdfs:label ?genre_label .
    ?rating mr:isAboutMovie ?movie .
    <"""+str(user)+"""> mr:providesRating ?rating.
    ?rating mr:hasStars ?s.
    ?s mr:StarScore ?score.
    } Group by ?genre_label
    HAVING(AVG(?score) > 2.5)
    ORDER by desc(?avg_rating)
    """
    res  = g3.query(like_genre_sparql)
    for row in res:
        g3.add((user, mr.likesGenre, row[0]))
    
    like_actor_sparql = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
    SELECT ?actor_label (AVG(?score) as ?avg_rating) WHERE {
    ?movie mr:starsActor ?actor .
    ?actor rdfs:label ?actor_label .
    ?rating mr:isAboutMovie ?movie .
    <"""+str(user)+"""> mr:providesRating ?rating.
    ?rating mr:hasStars ?s.
    ?s mr:StarScore ?score.
    } Group by ?actor_label
    HAVING(AVG(?score) > 2.5)
    ORDER by desc(?avg_rating)
    """
    res  = g3.query(like_actor_sparql)
    for row in res:
        g3.add((user, mr.likesGenre, row[0]))
    
    like_director_sparql = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
    SELECT ?director_label (AVG(?score) as ?avg_rating) WHERE {
    ?movie mr:directedBy ?director .
    ?director rdfs:label ?director_label .
    ?rating mr:isAboutMovie ?movie .
    <"""+str(user)+"""> mr:providesRating ?rating.
    ?rating mr:hasStars ?s.
    ?s mr:StarScore ?score.
    } Group by ?director_label
    HAVING(AVG(?score) > 2.5)
    ORDER by desc(?avg_rating)
    """
    res  = g3.query(like_actor_sparql)
    for row in res:
        g3.add((user, mr.likesGenre, row[0]))
    
    like_writer_sparql = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
    SELECT ?writer_label (AVG(?score) as ?avg_rating) WHERE {
    ?movie mr:writtenBy ?writer .
    ?writer rdfs:label ?writer_label .
    ?rating mr:isAboutMovie ?movie .
    <"""+str(user)+"""> mr:providesRating ?rating.
    ?rating mr:hasStars ?s.
    ?s mr:StarScore ?score.
    } Group by ?writer_label
    HAVING(AVG(?score) > 2.5)
    ORDER by desc(?avg_rating)
    """
    res  = g3.query(like_actor_sparql)
    for row in res:
        g3.add((user, mr.likesGenre, row[0]))
    
    like_producer_sparql = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
    SELECT ?producer_label (AVG(?score) as ?avg_rating) WHERE {
    ?movie mr:producedBy ?producer .
    ?producer rdfs:label ?producer_label .
    ?rating mr:isAboutMovie ?movie .
    <"""+str(user)+"""> mr:providesRating ?rating.
    ?rating mr:hasStars ?s.
    ?s mr:StarScore ?score.
    } Group by ?producer_label
    HAVING(AVG(?score) > 2.5)
    ORDER by desc(?avg_rating)
    """
    res  = g3.query(like_actor_sparql)
    for row in res:
        g3.add((user, mr.likesGenre, row[0]))

delete_score_data(g3, rating_dict)

g3.serialize("knowledge_graph/KG3.ttl", format="ttl")
g3.close()

# kg3+

g3_plus = rdflib.Graph()

g3_plus.bind("mr", mr)
g3_plus.bind("rdf", rdf)
g3_plus.bind("rdfs", rdfs)
g3_plus.bind("owl", owl)
g3_plus.bind("xsd", xsd)

g3_plus.parse("knowledge_graph/movie_description.ttl", format="ttl")
g3_plus.parse("ontologies/full_ontologies/ontology3+.ttl", format="ttl")

for triple in g_wiki:
    if str(triple[1]) == "http://www.wikidata.org/prop/direct/P1476":
        movie = triple[0]
        g3_plus.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
    elif str(triple[1]) == "http://www.wikidata.org/prop/direct/P161" or str(triple[1]) == "http://www.wikidata.org/prop/direct/P725":
        movie = triple[0]
        g3_plus.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
        g3_plus.add((triple[2], rdf.type, mr.Actor))
        for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
            g3_plus.add((triple[2], mr.hasName, obj))
    elif str(triple[1]) == "http://www.wikidata.org/prop/direct/P57":
        movie = triple[0]
        g3_plus.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
        g3_plus.add((triple[2], rdf.type, mr.Director))
        for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
            g3_plus.add((triple[2], mr.hasName, obj))
    elif str(triple[1]) == "http://www.wikidata.org/prop/direct/P58":
        movie = triple[0]
        g3_plus.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
        g3_plus.add((triple[2], rdf.type, mr.Writer))
        for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
            g3_plus.add((triple[2], mr.hasName, obj))
    elif str(triple[1]) == "http://www.wikidata.org/prop/direct/P272":
        movie = triple[0]
        g3_plus.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))
        g3_plus.add((triple[2], rdf.type, mr.Producer))
        for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
            g3_plus.add((triple[2], mr.hasName, obj))
    elif str(triple[1]) in alignment_dict.keys():
        movie = triple[0]
        if isinstance(triple[2], rdflib.URIRef):
            for subj, pred, obj in g_wiki.triples((triple[2], rdflib.RDFS.label, None)):
                g3_plus.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), obj))
        else:
            g3_plus.add((movie, rdflib.URIRef(alignment_dict[str(triple[1])]), triple[2]))

with open(movielens_user_file,'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        user = rdflib.URIRef(mr+"User/"+line[0])
        zipcode = rdflib.Literal(line[4], datatype=xsd.string)
        gender = gender_dict[line[1]]
        age = age_dict[line[2]]
        occupation = occupation_dict[line[3]]
        g3_plus.add((user, rdf.type, mr.User))
        g3_plus.add((user, mr.hasZipcode, zipcode))
        g3_plus.add((user, mr.hasGender, gender))
        g3_plus.add((user, mr.hasAgeRange, age))
        g3_plus.add((user, mr.hasOccupation, occupation))
        
with open(movielens_movie_file,'r',encoding='latin-1') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        movie = rdflib.URIRef(mr+"Movie/"+line[0])
        title = rdflib.Literal(line[1], datatype=xsd.string)
        genre_list = line[2].split('|')
        g3_plus.add((movie, rdf.type, mr.Movie))
        g3_plus.add((movie, mr.hasTitle, title))
        for genre in genre_list:
            g3_plus.add((movie, mr.hasGenre, genre_dict[genre]))

with open(movielens_rating_file,'r') as f:
    for line in f:
        line = line.strip()
        line = line.split('::')
        user = rdflib.URIRef(mr+"User/"+line[0])
        movie = rdflib.URIRef(mr+"Movie/"+line[1])
        rating = rdflib.URIRef(mr+"Rating/"+line[0]+"_"+line[1])
        g3_plus.add((rating, mr.hasStars, rating_dict[line[2]]))
        g3_plus.add((rating, mr.hasTimestamp, rdflib.Literal(line[3], datatype=xsd.string)))
        g3_plus.add((rating, rdf.type, mr.Rating))
        g3_plus.add((rating, mr.providedByUser, user))
        g3_plus.add((rating, mr.isAboutMovie, movie))
        g3_plus.add((user, mr.providesRating, rating))
        g3_plus.add((movie, mr.hasRating, rating))
        
like_movie_sparql = """
PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT Distinct ?user ?movie
WHERE {
    ?user rdf:type mr:User .
    ?user mr:providesRating ?rating .
    ?rating mr:isAboutMovie ?movie .
    ?movie mr:hasTitle ?title .
    ?rating mr:hasStars ?stars .
    Filter(?stars != mr:OneStar)
    Filter(?stars != mr:TwoStar)
}
"""
res = g3_plus.query(like_movie_sparql)
for row in res:
    g3_plus.add((row[0], mr.likesMovie, row[1]))
    
worked_pairs = []
worked_with_sparql = """
PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT ?person1 ?person2
WHERE {
    ?movie ?relation1 ?person1 .
    ?movie ?relation2 ?person2 .
    FILTER(?person1 != ?person2)
    VALUES ?relation1 {mr:starsActor mr:directedBy mr:writtenBy mr:producedBy}
    VALUES ?relation2 {mr:starsActor mr:directedBy mr:writtenBy mr:producedBy}
}
"""
res = g3_plus.query(worked_with_sparql)
for row in res:
    g3_plus.add((row[0], mr.workedWith, row[1]))
    g3_plus.add((row[1], mr.workedWith, row[0]))
    worked_pairs.append((row[0], row[1]))

from collections import Counter

def sort_and_count_pairs(pair_list):
    # Sort each pair alphabetically
    sorted_pairs = [tuple(sorted(pair)) for pair in pair_list]
    
    # Count occurrences of each sorted pair
    pair_counts = Counter(sorted_pairs)
    
    # Calculate the total number of pairs
    total_pairs = sum(pair_counts.values())
    
    # Calculate the average number of occurrences
    average_occurrences = total_pairs / len(pair_counts)
    
    return average_occurrences, pair_counts

average, pair_counts = sort_and_count_pairs(worked_pairs)
for pair, count in pair_counts.items():
    if count >= average:
        g3_plus.add((pair[0], mr.worksOftenWith, pair[1]))
        g3_plus.add((pair[1], mr.worksOftenWith, pair[0]))
    
add_score_data(g3_plus, rating_dict)

for num in range(1,6041,1):
    user = "User/"+str(num)
    user = mr[user]

    like_genre_sparql = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
    SELECT ?genre (AVG(?score) as ?avg_rating) WHERE {
    ?movie mr:hasGenre ?genre .
    ?genre rdfs:label ?genre .
    ?rating mr:isAboutMovie ?movie .
    <"""+str(user)+"""> mr:providesRating ?rating.
    ?rating mr:hasStars ?s.
    ?s mr:StarScore ?score.
    } Group by ?genre
    HAVING(AVG(?score) > 2.5)
    ORDER by desc(?avg_rating)
    """
    res  = g3_plus.query(like_genre_sparql)
    for row in res:
        g3_plus.add((user, mr.likesGenre, row[0]))
    
    like_actor_sparql = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
    SELECT ?actor (AVG(?score) as ?avg_rating) WHERE {
    ?movie mr:starsActor ?actor .
    ?rating mr:isAboutMovie ?movie .
    <"""+str(user)+"""> mr:providesRating ?rating.
    ?rating mr:hasStars ?s.
    ?s mr:StarScore ?score.
    } Group by ?actor
    HAVING(AVG(?score) > 2.5)
    ORDER by desc(?avg_rating)
    """
    res  = g3_plus.query(like_actor_sparql)
    for row in res:
        g3_plus.add((user, mr.likesGenre, row[0]))
    
    like_director_sparql = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
    SELECT ?director (AVG(?score) as ?avg_rating) WHERE {
    ?movie mr:directedBy ?director .
    ?rating mr:isAboutMovie ?movie .
    <"""+str(user)+"""> mr:providesRating ?rating.
    ?rating mr:hasStars ?s.
    ?s mr:StarScore ?score.
    } Group by ?director
    HAVING(AVG(?score) > 2.5)
    ORDER by desc(?avg_rating)
    """
    res  = g3_plus.query(like_actor_sparql)
    for row in res:
        g3_plus.add((user, mr.likesGenre, row[0]))
    
    like_writer_sparql = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
    SELECT ?writer (AVG(?score) as ?avg_rating) WHERE {
    ?movie mr:writtenBy ?writer .
    ?rating mr:isAboutMovie ?movie .
    <"""+str(user)+"""> mr:providesRating ?rating.
    ?rating mr:hasStars ?s.
    ?s mr:StarScore ?score.
    } Group by ?writer
    HAVING(AVG(?score) > 2.5)
    ORDER by desc(?avg_rating)
    """
    res  = g3_plus.query(like_actor_sparql)
    for row in res:
        g3_plus.add((user, mr.likesGenre, row[0]))
    
    like_producer_sparql = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
    SELECT ?producer (AVG(?score) as ?avg_rating) WHERE {
    ?movie mr:producedBy ?producer .
    ?rating mr:isAboutMovie ?movie .
    <"""+str(user)+"""> mr:providesRating ?rating.
    ?rating mr:hasStars ?s.
    ?s mr:StarScore ?score.
    } Group by ?producer
    HAVING(AVG(?score) > 2.5)
    ORDER by desc(?avg_rating)
    """
    res  = g3_plus.query(like_actor_sparql)
    for row in res:
        g3_plus.add((user, mr.likesGenre, row[0]))
    
    favorite_movie_sparql = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
    SELECT ?movie ?score
    WHERE {
    ?rating mr:isAboutMovie ?movie .
    <"""+str(user)+"""> mr:providesRating ?rating .
    ?rating mr:hasStars ?s .
    ?s mr:StarScore ?score .
    {
        SELECT ?maxmovie ?maxscore
        WHERE {
        ?rating mr:isAboutMovie ?maxmovie .
        <"""+str(user)+"""> mr:providesRating ?rating .
        ?rating mr:hasStars ?s .
        ?s mr:StarScore ?maxscore .
        }
        ORDER by desc(?maxscore)
        LIMIT 1
    }
    FILTER(?score = ?maxscore)
    }
    """
    res = g3_plus.query(favorite_movie_sparql)
    for row in res:
        g3_plus.add((row[0], mr.isFavoriteMovie, user))
        
    top10_movie_sparql = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>

    SELECT ?movie ?score
    WHERE {
    ?rating mr:isAboutMovie ?movie .
    <"""+str(user)+"""> mr:providesRating ?rating .
    ?rating mr:hasStars ?s .
    ?s mr:StarScore ?score .
    }
    ORDER BY DESC(?score)
    LIMIT 10
    """
    res = g3_plus.query(top10_movie_sparql)
    for row in res:
        g3_plus.add((row[0], mr.isPartOfTopFavoriteMovies, user))
    
    favorite_genre_sparql = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
    SELECT ?genre (AVG(?score) as ?avg_rating) WHERE {
    ?movie mr:hasGenre ?genre .
    ?genre rdfs:label ?genre .
    ?rating mr:isAboutMovie ?movie .
    <"""+str(user)+"""> mr:providesRating ?rating.
    ?rating mr:hasStars ?s.
    ?s mr:StarScore ?score.
    } Group by ?genre
    HAVING(AVG(?score) > 2.5)
    ORDER by desc(?avg_rating)
    LIMIT 1
    """
    res = g3_plus.query(favorite_genre_sparql)
    for row in res:
        g3_plus.add((row[0], mr.isFavoriteGenre, user))
    
    top5_genre_sparql = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mr: <http://anonymous.nl/movie-rating-ontology/>
    SELECT ?genre (AVG(?score) as ?avg_rating) WHERE {
    ?movie mr:hasGenre ?genre .
    ?genre rdfs:label ?genre .
    ?rating mr:isAboutMovie ?movie .
    <"""+str(user)+"""> mr:providesRating ?rating.
    ?rating mr:hasStars ?s.
    ?s mr:StarScore ?score.
    } Group by ?genre
    HAVING(AVG(?score) > 2.5)
    ORDER by desc(?avg_rating)
    LIMIT 5
    """
    res = g3_plus.query(top5_genre_sparql)
    for row in res:
        g3_plus.add((row[0], mr.isPartofTopFavoriteGenres, user))

delete_score_data(g3_plus, rating_dict)

g3_plus.serialize("knowledge_graph/KG3+.ttl", format="ttl")
g3_plus.close()