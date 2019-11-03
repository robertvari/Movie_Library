import os, json, time
from utilities.movieDB import get_movie_data

from utilities.file_utils import download_image
from objects.database import Client

class Movie:
    home_folder = os.path.join(os.path.expanduser("~"), "Movie_Library")
    client = None

    def __init__(self, movie_path, client=None):
        self.path = movie_path
        Movie.client = client

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
        self.database_file = None

        self.refresh_movie_data()

    def refresh_movie_data(self):

        movie_name = os.path.basename(self.path).split(".")[0]

        movie_db_data = self.client.find_by_path(self.path)
        if not movie_db_data:
            # get datafrom MovieDB
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
        else:
            for k,v in movie_db_data.items():
                setattr(self, k,v)

    def download_poster(self, movie_data):
        if not os.path.exists(self.home_folder):
            os.makedirs(self.home_folder)

        posterPathString = "https://image.tmdb.org/t/p/w300/" + movie_data["poster_path"]
        backdropPathString = "https://image.tmdb.org/t/p/w500/" + movie_data["backdrop_path"]
        poster_url = posterPathString
        backdrop_url = backdropPathString

        timestamp = int(time.time())
        poster_path = os.path.join(self.home_folder, str(timestamp) + ".jpg")
        backdrop_path = os.path.join(self.home_folder, str(timestamp) + "_backdrop.jpg")

        if not os.path.exists(poster_path):
            self.poster = download_image(poster_url, poster_path)
            self.backdrop = download_image(backdrop_url, backdrop_path)
        else:
            self.poster = poster_path
            self.backdrop = backdrop_path

    def save(self):
        if self.client:
            self._id = self.client.insert(self.__dict__)
        else:
            database_file = os.path.join(os.path.dirname(self.poster), self.title + ".json")

            with open(database_file, "w") as f:
                json.dump(self.__dict__, f)

    def delete(self):
        # remove posters
        if self.poster:
            os.remove(self.poster)

        if self.backdrop:
            os.remove(self.backdrop)

        # delete database files
        if self.database_file:
            os.remove(self.database_file)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

if __name__ == '__main__':
    client = Client("MovieLibrary")
    movie = Movie(r"E:\_PythonSuli\Desktop_App_1019\movies\Terminator.mkv", client)