from PySide2.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLineEdit, \
    QPushButton, QListWidget, QListWidgetItem, QItemDelegate, QStyle

from PySide2.QtGui import QPen, QBrush, QColor, QPixmap

from PySide2.QtCore import Qt, QSize

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


# The movie list

class MovieList(QListWidget):
    def __init__(self):
        super(MovieList, self).__init__()
        self.setItemDelegate(MovieListDelegate())
        self.setSpacing(5)

        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setMovement(QListWidget.Static)

        # todo remove this later
        self.create_test_content()

        self.setStyleSheet("background-color:#222")


    def create_test_content(self):
        for i in range(10):
            MovieItem(self)

from utilities.static_utils import get_static

class MovieListDelegate(QItemDelegate):
    def __init__(self):
        super(MovieListDelegate, self).__init__()

        self.outline_pen = QPen(QColor("#444444"))
        self.background_brush = QBrush(QColor("black"))
        self.selected_brush = QBrush(QColor(76, 228, 239, 80))
        self.mouse_over_brush = QBrush(QColor("yellow"))
        self.temp_poster = QPixmap(get_static("placeholder_poster.jpg"))

    def paint(self, painter, option, index):
        rect = option.rect

        painter.setPen(self.outline_pen)
        painter.setBrush(self.background_brush)
        painter.drawRect(rect)

        # posters
        painter.drawPixmap(rect, self.temp_poster)

        if option.state & QStyle.State_Selected:
            painter.setBrush(self.selected_brush)
            painter.drawRect(rect)


class MovieItem(QListWidgetItem):
    def __init__(self, parentWidget):
        super(MovieItem, self).__init__(parentWidget)
        self.setSizeHint(QSize(200,300))
