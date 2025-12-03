#!/usr/bin/env python3

import argparse
import json
import string
from nltk.stem import PorterStemmer
from inverted_index import InvertedIndex
from utils import *
import math
from keyword_utils import *

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    build_parser = subparsers.add_parser("build", help="Build Inverted Index table")
    tf_parser = subparsers.add_parser("tf", help="Look for term frequency in document")
    tf_parser.add_argument("doc_id", type=str, help="Search query")
    tf_parser.add_argument("term", type=str, help="Search query")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    idf_parser = subparsers.add_parser("idf", help="Look for inverted term frequency in document")
    idf_parser.add_argument("term", type=str, help="Search query")


    tfidf_parser = subparsers.add_parser("tfidf", help="Look for TF-IDF in document")
    tfidf_parser.add_argument("doc_id", type=str, help="Search query")
    tfidf_parser.add_argument("term", type=str, help="Search query")

    args = parser.parse_args()
    
       

    match args.command:
        case "search":
            run_search(args.query)
                
        case "build":
            run_build()

        case "tf":
            run_tf(int(args.doc_id), args.term)
            
        case "idf":
            run_idf(args.term)

        case "tfidf":
            run_tfidf(int(args.doc_id), args.term)

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
