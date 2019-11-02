import os

class Movie:
    def __init__(self, movie_path):
        self.path = movie_path

        self.poster = movie_path
        self.backdrop = None
        self.title = os.path.basename(self.path).split(".")[0]
        self.description = f'{os.path.basename(self.path)} details...'
        self.rating = 7.5
        self.release_date = '1998 08 15'
        self.trailer = None
        self.favorite = False
        self.watched = False

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title