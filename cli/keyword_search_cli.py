#!/usr/bin/env python3

import argparse
import json
import string
from nltk.stem import PorterStemmer
from inverted_index import InvertedIndex
from utils import *




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
            inverted_index = InvertedIndex()           
            try:
                inverted_index.load()
            except:
                print("Error loading index")
                exit(1)
            
            tokens = clean_text(args.query)
            results = []
            for token in tokens:
                    docs = inverted_index.get_documents(token)
                    if len(docs)>0:
                        for doc in docs:
                            if len(results)<5:
                                results.append(doc)
                                print(f"\nID: {doc}\nTitle: {inverted_index.docmap[doc]['title']}")
                
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
