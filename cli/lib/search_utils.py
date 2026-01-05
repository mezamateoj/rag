import json
import os
import string
from typing import List

from nltk.stem import PorterStemmer

from .schema import Movie, MovieListValidator

DEFAULT_SEARCH_LIMIT = 5

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "movies.json")


def load_movies() -> List[Movie]:
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return MovieListValidator.validate_python(data["movies"])


def load_file(dir, filename) -> list[str]:
    file_path = os.path.join(PROJECT_ROOT, dir, filename)
    with open(file_path, "r") as f:
        return f.read().splitlines()


def preprocess_text(s: str, stopwords: list[str]) -> list[str]:
    text = str.maketrans("", "", string.punctuation)
    text = s.translate(text).lower().strip()
    words_list = text.split()

    for word in words_list:
        if word in stopwords:
            words_list.remove(word)
    return words_list


def has_substring(list_a, list_b, stop_words=""):
    if not stop_words:
        stop_words = load_file("data", "stopwords.txt")

    stemmer = PorterStemmer()
    for a in preprocess_text(list_a, stop_words):
        for b in preprocess_text(list_b, stop_words):
            if stemmer.stem(a) in stemmer.stem(b):
                return True
    return False


def tokenize_text(text: str) -> list[str]:
    stop_words = load_file("data", "stopwords.txt")

    stemmer = PorterStemmer()  # <-- Creates stemmer
    stemmed_words = []
    for word in preprocess_text(text, stop_words):
        stemmed_words.append(stemmer.stem(word))  # <-- Stems each word
    return stemmed_words  # <-- Returns stemmed words
