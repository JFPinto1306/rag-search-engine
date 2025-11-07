#!/usr/bin/env python3

import argparse
import json
import string


def get_movies_dict(path)->dict:
    with open(path, 'r') as f:
        movies = json.load(f)
        
    return movies    
    
def get_titles_from_query(movies_dict,query)->list:
    results = []
    if 'movies' in movies_dict:
        movies_list = movies_dict['movies']
        
        for movie in movies_list:
            if query in movie['title'].lower():
                results.append(movie)
                
    results = sorted(results, key=lambda x: x['id'])
                    
    return results[:5]
    
def clean_query(query)->str:
    query = args.query.lower()
    query = query.translate(str.maketrans('', '', string.punctuation))
    

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()
    
    #Loading movies
    path = r'./data/movies.json'
    movies_dict = get_movies_dict(path)

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            query = args.query
            
            # Handling query

            results = get_titles_from_query(movies_dict,query)
            for movie in results:
                print(f"{movie['id']}. {movie['title']}")
            
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
