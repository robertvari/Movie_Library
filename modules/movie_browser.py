from PySide2.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLineEdit, \
    QPushButton, QListWidget, QListWidgetItem, QItemDelegate, QStyle
from PySide2.QtGui import QPen, QBrush, QColor, QPixmap
from PySide2.QtCore import Qt, QSize, QRect, Signal

from objects.movie import Movie
import os

from utilities.static_utils import get_static
from utilities.file_utils import get_files

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
    show_detail = Signal(object)

    def __init__(self):
        super(MovieList, self).__init__()

        self.setItemDelegate(MovieListDelegate())
        self.setSpacing(5)

        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setSelectionMode(QListWidget.ExtendedSelection)

        self.refresh()

        self.setStyleSheet("background-color:#222")

        self.itemDoubleClicked.connect(self.show_details_action)

    def check_drop_data(self, urls):

        self.mkv_files = []
        for item in urls:
            file_path = item.toLocalFile()

            if os.path.isfile(file_path):
                if file_path.endswith(".mkv"):
                    self.mkv_files.append(file_path)
            else:
                self.mkv_files += get_files(file_path)

        if self.mkv_files:
            return True

        return False

    def dragEnterEvent(self, event):
        # check drag data
        if event.mimeData().hasUrls():
            if self.check_drop_data(event.mimeData().urls()):
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        self.create_movies(self.mkv_files)
        event.accept()

    def create_movies(self, files):
        for item in files:
            movie_object = Movie(item)

    def show_details_action(self, item):
        self.show_detail.emit(item.movie)

    def refresh(self):
        self.clear()

        # todo replace this with database query
        # for movie_file in get_files():
        #     MovieItem(self, Movie(movie_file))


class MovieListDelegate(QItemDelegate):
    def __init__(self):
        super(MovieListDelegate, self).__init__()

        self.outline_pen = QPen(QColor("#444444"))
        self.background_brush = QBrush(QColor("black"))
        self.selected_brush = QBrush(QColor(76, 228, 239, 80))
        self.mouse_over_brush = QBrush(QColor("yellow"))
        self.poster_pixmap = QPixmap()
        # self.temp_poster = pixmap.scaled(MovieItem.poster_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def paint(self, painter, option, index):
        rect = option.rect

        poster_file = index.data(Qt.UserRole)
        self.poster_pixmap.load(poster_file)
        poster_file_rescaled = self.poster_pixmap.scaled(MovieItem.poster_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        painter.setPen(self.outline_pen)
        painter.setBrush(self.background_brush)
        painter.drawRect(rect)

        # posters
        poster_rect = QRect(rect.x(), rect.y(), poster_file_rescaled.width(), poster_file_rescaled.height())
        poster_rect.moveCenter(rect.center())
        painter.drawPixmap(poster_rect, poster_file_rescaled)

        if option.state & QStyle.State_Selected:
            painter.setBrush(self.selected_brush)
            painter.drawRect(rect)

class MovieItem(QListWidgetItem):
    poster_size = QSize(200, 300)

    def __init__(self, parentWidget, movie_object):
        super(MovieItem, self).__init__(parentWidget)
        self.setSizeHint(self.poster_size)
        self.movie = movie_object

        self.setData(Qt.UserRole, movie_object.poster)
