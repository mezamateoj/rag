from .search_utils import (
    DEFAULT_SEARCH_LIMIT,
    has_substring,
    load_file,
    load_movies,
)


def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    stop_words = load_file("data", "stopwords.txt")
    results = []
    for movie in movies:
        if has_substring(query, movie["title"], stop_words):
            results.append(movie)
            if len(results) >= limit:
                break
    return results
