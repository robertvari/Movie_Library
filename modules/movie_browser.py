from PySide2.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLineEdit, \
    QPushButton, QListWidget
from PySide2.QtCore import Qt

class MovieBrowser(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setAlignment(Qt.AlignTop)

        self.search_bar = SearchBar()
        main_layout.addWidget(self.search_bar)

        self.movie_list = MovieList()
        main_layout.addWidget(self.movie_list)


class MovieList(QListWidget):
    def __init__(self):
        super(MovieList, self).__init__()


class SearchBar(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5,5,5,0)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search...")
        main_layout.addWidget(self.search_field)

        az_button = QPushButton('A-Z')
        main_layout.addWidget(az_button)

        time_button = QPushButton('T')
        main_layout.addWidget(time_button)