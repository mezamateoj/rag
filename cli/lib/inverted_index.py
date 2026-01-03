import os
import pickle
import string
from typing import Dict, List, Set

from .schema import Movie
from .search_utils import load_movies

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CACHE_PATH = os.path.join(PROJECT_ROOT, "cache")


class InvertedIndex:
    def __init__(self):
        self.index: Dict[str, Set[int]] = {}
        self.docmap: Dict[int, Movie] = {}
        self.index_path = os.path.join(CACHE_PATH, "index.pkl")
        self.docmap_path = os.path.join(CACHE_PATH, "docmap.pkl")

    def tokenize_text(self, movie_data: str) -> List[str]:
        text = str.maketrans("", "", string.punctuation)
        text = movie_data.translate(text).lower().strip()
        return text.split()

    def __add_document(self, doc_id: int, text: str):
        tokenize = self.tokenize_text(text)
        for token in set(tokenize):
            self.index.setdefault(token, set()).add(doc_id)

    def get_documents(self, term: str) -> List[int]:
        text = str.maketrans("", "", string.punctuation)
        text = term.translate(text).lower().strip()
        _set_doc_ids = self.index.get(term, set())
        return sorted(list(_set_doc_ids))

    def build(self):
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


def build_command(text: str) -> None:
    idx = InvertedIndex()
    idx.build()
    idx.save()
    docs = idx.get_documents(text)
    print(f"First document for token '{text}' = {docs[0]}")
