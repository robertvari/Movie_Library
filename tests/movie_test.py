from unittest import TestCase
import os

from objects.movie import Movie


class TestMovie(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.title = "The Matrix"

    @classmethod
    def tearDownClass(cls):
        """
        Remove database files
        """
        print("Clean up database...")
        database_files = [os.path.join(Movie.database_folder, i) for i in os.listdir(Movie.database_folder)]
        for file_item in database_files:
            os.remove(file_item)

    def test_create_movie(self):
        movie = Movie(self.title)

        self.assertIsNotNone(movie.title)

        database_file = os.path.join(Movie.database_folder, movie.title + ".json")
        self.assertTrue(os.path.exists(database_file))

    def test_movie_list(self):
        movie_list = [
            "The Matrix",
            "Star Wars",
            "Bourne Legacy",
             "Jaws"
        ]

        for i in movie_list:
            movie_object = Movie(i)
            self.assertIsNotNone(movie_object.release_date)


if __name__ == '__main__':
    TestCase()