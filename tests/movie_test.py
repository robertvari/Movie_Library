from unittest import TestCase
import os

from objects.movie import Movie

class TestMovie(TestCase):

    def tearDown(self) -> None:
        if hasattr(self, "movies"):
            print(f"Cleaning up after {self.movies}")
            [i.delete() for i in self.movies]
        else:
            print(f'Cleaning up: {self.movie}')
            self.movie.delete()

    def test_create_movie(self):
        self.movie = Movie("Star Wars")

        self.assertIsNotNone(self.movie.title)
        self.assertTrue(os.path.exists(self.movie.database_file))

    def test_movie_list(self):
        movie_list = [
            "The Matrix",
            "Star Wars",
            "Bourne Legacy",
             "Jaws"
        ]

        self.movies = []
        for i in movie_list:
            movie_object = Movie(i)
            self.movies.append(movie_object)
            self.assertIsNotNone(movie_object.release_date)


if __name__ == '__main__':
    TestCase()