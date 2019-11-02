from PySide2.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QLabel
from PySide2.QtCore import Signal

class MovieDetails(QWidget):
    close_details = Signal()

    def __init__(self):
        super().__init__()
        self.setVisible(False)

        main_layout = QVBoxLayout(self)

        self.poster = QLabel()
        self.description = QLabel()
        self.rating = QLabel()
        self.title = QLabel()
        self.release_date = QLabel()

        main_layout.addWidget(self.poster)
        main_layout.addWidget(self.description)
        main_layout.addWidget(self.rating)
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.release_date)

        close_btn = QPushButton("Close")
        main_layout.addWidget(close_btn)
        close_btn.clicked.connect(self.close_action)

    def set_movie(self, movie):
        self.movie = movie

        self.poster.setPixmap(movie.poster)
        self.title.setText(movie.title)
        self.rating.setText(str(movie.rating))
        self.release_date.setText(movie.release_date)

    def close_action(self):
        self.close_details.emit()