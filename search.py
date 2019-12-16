from nltk.stem import PorterStemmer
import json
import operator
from collections import defaultdict
import time
ps = PorterStemmer()
'''
def load_yaml(file_name):
    with open(file_name, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded
'''
def load_json(file_name):
    with open(file_name, 'r') as stream:
        dictionary=json.load(stream)
    return dictionary

def sumsquare(ls):
    return sum([x*x for x in ls])**0.5

def cosinesimilarity(query,document):
    return 0.5*sum(document)+0.5*sum([x*y for x,y in zip(query,document)])/(sumsquare(query)*sumsquare(document))


def stem_query(query, idf_dict):
    new_query = defaultdict(float)
    for word in query.split(' '):
        word = ps.stem(word)
        if word in idf_dict:
            new_query[word]+=1
    for words in new_query:
        new_query[words]*=idf_dict[words]
    return new_query

def remove_duplicates(query):
    return list(set(stem_query(query).split(' ')))

def get_results(database, query):
    num_results = 20
    query_total_scores = defaultdict(int)
    cossim={}
    queryvals=[]
    for idx,word in enumerate(query):
        print (word)
        results=database[word]
        queryvals.append(query[word])
        for result in results:
            # key of document to tfidf score
            if result not in cossim:
                cossim[result]=[0]*len(query)
            cossim[result][idx]=results[result]
    for keys in cossim:
        cossim[keys]=cosinesimilarity(queryvals,cossim[keys])
    # sorted_x=sorted(cossim.items(),key=lambda x:cosinesimilarity(query.values(),cossim[x]),reverse=True)
    sorted_x=sorted(cossim.keys(),key=lambda x:cossim[x],reverse=True)
    for x in sorted_x[:num_results]:
        print(x+ '  ' + str(cossim[x]))
    
    '''
    for word in query:
        if word not in database:
            continue
        results = database[word]
        sorted_x = sorted(results.items(), key=lambda kv: kv[1])[::-1]
        for x,y in sorted_x:
            query_total_scores[x] += y
    sorted_x = sorted(query_total_scores.items(), key=lambda kv: kv[1])[::-1]
    '''
    return sorted_x[:num_results]
    #return sorted_x[:num_results]

if __name__=='__main__':
    #tfidf_dict = load_yaml('minitfidf.yml')
    tfidf_dict=load_json('dictionary_data/tfidf.json')
    idf_dict=load_json('dictionary_data/idf.json')
    query = input("Enter your search query: ") 
    start_time=time.time()
    #processed_query = remove_duplicates(stem_query(query))
    processed_query=stem_query(query,idf_dict)
    results = get_results(tfidf_dict, processed_query)
    print(time.time()-start_time)
    #for url, score in results:
    #    print (url)
    for url in results:
        print(url)
