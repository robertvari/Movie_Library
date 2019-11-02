import os

from utilities.movieDB import get_movie_data

class Movie:
    def __init__(self, movie_path):
        self.path = movie_path

        self.poster = None
        self.backdrop = None
        self.title = None
        self.description = None
        self.rating = 0
        self.release_date = None
        self.trailer = None
        self.favorite = False
        self.watched = False
        self.original_language = None

        self.refresh_movie_data()

    def refresh_movie_data(self):

        movie_name = os.path.basename(self.path).split(".")[0]
        movie_data_list = get_movie_data(movie_name)

        if len(movie_data_list):
            # todo get some ui for select a movie
            movie_data = movie_data_list[0]

            self.title = movie_data["original_title"]
            self.description = movie_data["overview"]
            self.release_date = movie_data["release_date"]
            self.original_language = movie_data["original_language"]
            self.rating = movie_data["vote_average"]

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


if __name__ == '__main__':
    movie = Movie("The Matrix")
    print(movie.title)
    print(movie.release_date)
    print(movie.original_language)
    print(movie.rating)
    print(movie.description)