#!/usr/bin/env python3

import argparse
import json

from lib.inverted_index import InvertedIndex
from lib.keyword_search import search_command


def load_data(filepath):
    return json.load(filepath)


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    sub_parser = subparsers.add_parser("build", help="Create a Pub/Sub subscription")
    sub_parser.add_argument(
        "build", type=str, help="Name of the subscription to create"
    )

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            movies = search_command(args.query)
            for index, title in enumerate(movies, 1):
                print(f"{index}. Movie Title {title['title']}")
        case "build":
            print("Building")
            test = InvertedIndex()
            test.build()

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
