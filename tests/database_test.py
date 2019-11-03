from unittest import TestCase

from objects.database import Client

class DatabaseTest(TestCase):
    def setUp(self) -> None:
        self.client = Client("MovieLibrary_test")

        self.movie_data = {
            "path":r"E:\_PythonSuli\Desktop_App_1019\movies\Aliens.mkv",
            "title": "Aliens",
            "language": "eng"
        }

    def tearDown(self) -> None:
        print("Deleting database", self.client.database_name)
        self.client.drop_table()

    def test_insert(self):
        id = self.client.insert(self.movie_data)

        self.assertIsNotNone(id)

    def test_title(self):
        id = self.client.insert(self.movie_data)

        movie_data = self.client.find_by_id(id)

        self.assertIsNotNone(movie_data)
        self.assertEqual(movie_data["title"], self.movie_data["title"])

    def test_delete(self):
        id = self.client.insert(self.movie_data)
        self.client.delete(id)

        movie_data = self.client.find_by_id(id)
        self.assertIsNone(movie_data)
