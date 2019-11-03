from pymongo import MongoClient
from bson import ObjectId

class Client():
    def __init__(self, database_name="MovieLibrary"):
        self.database_name = database_name

        self._client = MongoClient("localhost", 27017)
        self._db = self._client[self.database_name]
        self.collection = self._db["movies"]

    def insert(self, data):
        return self.collection.insert_one(data).inserted_id

    def update(self, data):
        self.collection.update_one({"_id":data.get("_id")}, {"$set":data})

    def find_all_movies(self):
        return self.collection.find()

    def find_by_title(self, title):
        return self.collection.find_one({"title":title})

    def find_by_id(self, _id):
        return self.collection.find_one({"_id": _id})

    def find_by_path(self, path):
        return self.collection.find_one({"path": path})

    def delete(self, _id):
        self.collection.delete_one({"_id":_id})

    def drop_table(self):
        self._client.drop_database(self.database_name)


if __name__ == '__main__':
    client = Client()
    movie_data = client.find_by_title("Star wars")
    movie_data["title"] = "Jaws"
    client.update(movie_data)