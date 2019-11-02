import os, json
from utilities.movieDB import get_movie_data

class Movie:
    database_folder = r"E:\_PythonSuli\Desktop_App_1019\Movie_Library\database"
    home_folder = os.path.join(os.path.expanduser("~"), "Movie_Library")

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

            self.download_poster(movie_data)

            self.save()

    def download_poster(self, movie_data):
        posterPathString = "https://image.tmdb.org/t/p/w300/" + movie_data["poster_path"]
        backdropPathString = "https://image.tmdb.org/t/p/w500/" + movie_data["backdrop_path"]

        poster_url = posterPathString
        backdrop_url = backdropPathString

        print(poster_url)

        if not os.path.exists(self.home_folder):
            os.makedirs(self.home_folder)

        self.poster = os.path.join(self.home_folder, self.title + ".jpg")
        self.backdrop = os.path.join(self.home_folder, self.title + "_backdrop.jpg")



    def save(self):
        data_file = os.path.join(self.database_folder, self.title + ".json")
        with open(data_file, "w") as f:
            json.dump(self.__dict__, f)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

if __name__ == '__main__':
    movie = Movie("The Matrix")