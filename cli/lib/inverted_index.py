import os
from typing import Dict, Set

from .schema import Movie
from .search_utils import load_movies

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "cache")


class InvertedIndex:
    index: Dict[int, Set[str]] = {}
    docmap: Dict[int, Movie] = {}

    def __add_document(self, doc_id, text):
        pass

    def get_documents(self, term):
        pass

    def build(self):
        movies = load_movies()
        for movie in movies[0:1]:
            tokenize = movie.description.split()
            if movie.id not in self.index.keys():
                self.index[movie.id] = set(tokenize)
                self.docmap[movie.id] = movie.model_dump()

        print(self.index.get(1))
        print()
        print(self.docmap)

    def save(self):
        pass
