import os
import pickle
import string
from typing import Dict, List, Set

from .schema import Movie
from .search_utils import load_movies, tokenize_text

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CACHE_PATH = os.path.join(PROJECT_ROOT, "cache")


class InvertedIndex:
    def __init__(self):
        self.index: Dict[str, Set[int]] = {}
        self.docmap: Dict[int, Movie] = {}
        self.index_path = os.path.join(CACHE_PATH, "index.pkl")
        self.docmap_path = os.path.join(CACHE_PATH, "docmap.pkl")

    def __add_document(self, doc_id: int, text: str):
        tokenize = tokenize_text(text)
        for token in set(tokenize):
            self.index.setdefault(token, set()).add(doc_id)

    def get_documents(self, term: str, index: Dict[str, Set[int]]) -> List[int]:
        text = str.maketrans("", "", string.punctuation)
        text = term.translate(text).lower().strip()

        _set_doc_ids = index.get(term, set())

        return sorted(list(_set_doc_ids))

    def build(self):
        print("building")
        movies = load_movies()
        for movie in movies:
            doc_description = f"{movie.title} {movie.description}"
            self.__add_document(movie.id, doc_description)
            self.docmap[movie.id] = movie.model_dump()

    def save(self):
        os.makedirs(CACHE_PATH, exist_ok=True)
        filenames = [self.index_path, self.docmap_path]

        for file_path in filenames:
            with open(file_path, "wb") as file:
                if file_path == self.index_path:
                    pickle.dump(self.index, file)

                elif file_path == self.docmap_path:
                    pickle.dump(self.docmap, file)

    def load(self):
        filenames = [self.index_path, self.docmap_path]

        for file_path in filenames:
            with open(file_path, "rb") as file:
                if file_path == self.index_path:
                    index = pickle.load(file)

                elif file_path == self.docmap_path:
                    docmap = pickle.load(file)

        return index, docmap


def build_command() -> None:
    idx = InvertedIndex()
    idx.build()
    idx.save()
