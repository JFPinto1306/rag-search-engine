from inverted_index import InvertedIndex
from utils import *
import math

def run_search(query):
    print(f"Searching for: {query}")
    inverted_index = InvertedIndex()    
    try:
        inverted_index.load()
    except:
        print("Error loading index")
        exit(1)
    
    tokens = clean_text(query)
    results = []
    for token in tokens:
            docs = inverted_index.get_documents(token)
            if len(docs)>0:
                for doc in docs:
                    if len(results)<5:
                        results.append(doc)
                        print(f"\nID: {doc}\nTitle: {inverted_index.docmap[doc]['title']}")

    return results

def run_build():
    #Loading movies
    path = r'./data/movies.json'
    movies_dict = get_movies_dict(path)

    inverted_index = InvertedIndex()
    inverted_index.build(movies_dict['movies'])
    inverted_index.save()

def run_tf(doc_id,term):
    inverted_index = InvertedIndex()
    try:
        inverted_index.load()
    except:
        print("Error loading index")
        exit(1)

    token = clean_text(term)[0]

    freq = inverted_index.get_tf(doc_id,token)
    print(f"Document {doc_id} contains the term {term} {freq} time(s)")     
    return freq


def run_idf(term):
    inverted_index = InvertedIndex()
    try:
        inverted_index.load()
    except:
        print("Error loading index")
        exit(1)     

    term = clean_text(term)[0]
    term_doc_count = len(inverted_index.get_documents(term))
    doc_count = len(inverted_index.docmap)

    idf = math.log((doc_count + 1) / (term_doc_count + 1))
    print(f"Inverse document frequency of '{term}': {idf:.2f}")    

    return idf


def run_tfidf(doc_id,term):
    inverted_index = InvertedIndex()
    try:
        inverted_index.load()
    except:
        print("Error loading index")
        exit(1)     

    tf = run_tf(doc_id,term)
    idf = run_idf(term)
    tf_idf = tf*idf

    print(f"TF-IDF score of '{term}' in document '{doc_id}': {tf_idf:.2f}")

    return tf_idf