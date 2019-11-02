import tmdbsimple as tmdb

tmdb.API_KEY = '83cbec0139273280b9a3f8ebc9e35ca9'
search = tmdb.Search()


def get_movie(title):
    search.movie(query=title)

    print(type(search), search)
    # for item in search.results:
    #     movie = tmdb.Movies(item["id"])
    #     # print(item)
    #     print(movie.info())


if __name__ == '__main__':
    get_movie("The Matrix")