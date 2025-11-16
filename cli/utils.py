
import argparse
import json
import string
from nltk.stem import PorterStemmer


def get_movies_dict(path)->dict:
    with open(path, 'r') as f:
        movies = json.load(f)
        
    return movies    

def get_stopwords(stopwords_path)->list:
    with open(stopwords_path, 'r') as f:
        data = f.read()
        
    return data

def remove_stopwords_from_tokens(tokens)->list:
    stopwords = get_stopwords(stopwords_path=r'./data/stopwords.txt')
    return [token for token in tokens if token not in stopwords]

def lower_and_remove_punctuation_from_movie_title(movie_title)->str:
    
    return movie_title.lower().translate(str.maketrans('', '', string.punctuation))

def tokenize_text(text)->str:
    return list(set([x for x in text.split(' ') if len(x)>0]))

def stem_tokens(tokens):
    stemmer = PorterStemmer()
    stemmed_tokens = []
    for token in tokens:
        stemmed_tokens.append(stemmer.stem(token))
        
    return stemmed_tokens
        
    

def clean_text(text):
    # Cleaning Query
    movie_title = lower_and_remove_punctuation_from_movie_title(text)
    # Tokenizing
    tokens = tokenize_text(movie_title)
    # Removing Stopwords
    tokens = remove_stopwords_from_tokens(tokens)
    # Stemming tokens
    tokens = stem_tokens(tokens)
    
    return tokens 

def get_titles_from_query(movies_dict,args)->list:
    
    query_tokens = clean_text(args.query)
    results = []
    if 'movies' in movies_dict:
        movies_list = movies_dict['movies']
        
        for movie in movies_list:
            movie_tokens = clean_text(movie['title'])
            for token in query_tokens:
                for movie_token in movie_tokens:
                    if token in movie_token:
                        if movie not in results:
                            results.append(movie)
                            pass
                
    results = sorted(results, key=lambda x: x['id'])
                    
    return results[:5]
    