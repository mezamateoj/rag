#!/usr/bin/env python3
import argparse
import json

from lib.inverted_index import InvertedIndex, build_command

# from lib.keyword_search import search_command
from lib.search_utils import (
    tokenize_text,
)


def load_data(filepath):
    return json.load(filepath)


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    subparsers.add_parser("build", help="Build Index")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            idx = InvertedIndex()
            cache_idx, doc_map = idx.load()
            movies = tokenize_text(args.query)

            for movie in movies:
                movies_from_index = cache_idx.get(movie, set())
                sorted_list = sorted(list(movies_from_index))
                for s in sorted_list[0:5]:
                    print(
                        f"Movies found: {doc_map[s].get('id')} - {doc_map[s].get('title')}"
                    )

        case "build":
            print("Building index")
            build_command()
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
