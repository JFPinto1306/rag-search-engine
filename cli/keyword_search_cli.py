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

    build_parser = subparsers.add_parser("build", help="Build Inverted Index table")
    tf_parser = subparsers.add_parser("tf", help="Look for term frequency in document")
    tf_parser.add_argument("doc_id", type=str, help="Search query")
    tf_parser.add_argument("token", type=str, help="Search query")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()
    
    #Loading movies
    path = r'./data/movies.json'
    movies_dict = get_movies_dict(path)
    inverted_index = InvertedIndex()           

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
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

        case "tf":

            doc_id, token = int(args.doc_id), args.token
            term = clean_text(token)[0]
            try:
                inverted_index.load()
            except:
                print("Error loading index")
                exit(1)

            freq = inverted_index.get_tf(doc_id,term)
            print(f"Document {doc_id} contains the term {term} {freq} times")
            
            
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
