#!/usr/bin/env python3

import argparse
import json
import string
from nltk.stem import PorterStemmer
from inverted_index import InvertedIndex


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

def tokenize_movie_title(movie_title)->str:
    return list(set([x for x in movie_title.split(' ') if len(x)>0]))

def stem_tokens(tokens):
    stemmer = PorterStemmer()
    stemmed_tokens = []
    for token in tokens:
        stemmed_tokens.append(stemmer.stem(token))
        
    return stemmed_tokens
        
    

def clean_movie_title(movie_title):
    # Cleaning Query
    movie_title = lower_and_remove_punctuation_from_movie_title(movie_title)
    # Tokenizing
    tokens = tokenize_movie_title(movie_title)
    # Removing Stopwords
    tokens = remove_stopwords_from_tokens(tokens)
    # Stemming tokens
    tokens = stem_tokens(tokens)
    
    return tokens 

def get_titles_from_query(movies_dict,args)->list:
    
    query_tokens = clean_movie_title(args.query)
    results = []
    if 'movies' in movies_dict:
        movies_list = movies_dict['movies']
        
        for movie in movies_list:
            movie_tokens = clean_movie_title(movie['title'])
            for token in query_tokens:
                for movie_token in movie_tokens:
                    if token in movie_token:
                        if movie not in results:
                            results.append(movie)
                            pass
                
    results = sorted(results, key=lambda x: x['id'])
                    
    return results[:5]
    


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="Build Inverted Index table")
    args = parser.parse_args()
    
    #Loading movies
    path = r'./data/movies.json'
    movies_dict = get_movies_dict(path)

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            results = get_titles_from_query(movies_dict,args)
            for movie in results:
                print(f"{movie['id']}. {movie['title']}")
                
        case "build":
            inverted_index = InvertedIndex()
            inverted_index.build(movies_dict['movies'])
            inverted_index.save()
            docs = inverted_index.get_documents('merida')
            print(f"First document for token 'merida' = {docs[0]}")
            
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
