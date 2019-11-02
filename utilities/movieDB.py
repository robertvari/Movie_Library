import tmdbsimple as tmdb

tmdb.API_KEY = '83cbec0139273280b9a3f8ebc9e35ca9'
search = tmdb.Search()


def get_movie_data(title):
    search.movie(query=title)
    return search.results

    #     movie = tmdb.Movies(item["id"])
    #     # print(item)
    #     print(movie.info())


if __name__ == '__main__':
    get_movie_data("The Matrix")