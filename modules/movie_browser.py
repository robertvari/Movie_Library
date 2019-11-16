from PySide2.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLineEdit, \
    QPushButton, QListWidget, QListWidgetItem, QItemDelegate, QStyle
from PySide2.QtGui import QPen, QBrush, QColor, QPixmap
from PySide2.QtCore import Qt, QSize, QRect, Signal, QThread

from objects.movie import Movie
import os

from utilities.static_utils import get_static
from utilities.file_utils import get_files
from objects.database import Client
from .customWidgets import Button, IconButton

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

        az_button = IconButton(get_static("sort_AZ.png"), size=30)
        main_layout.addWidget(az_button)

        time_button = IconButton(get_static("sort_time.png"), size=30)
        main_layout.addWidget(time_button)


# The movie list

class MovieList(QListWidget):
    show_detail = Signal(object)
    client = Client()

    def __init__(self):
        super(MovieList, self).__init__()

        self.movie_downloader = DownloaderWorker()

        self.setItemDelegate(MovieListDelegate())
        self.setSpacing(5)

        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setSelectionMode(QListWidget.ExtendedSelection)

        self.itemDoubleClicked.connect(self.show_details_action)

        self.movie_db_list = Movie.get_all_movies_from_db()
        self.refresh()

        self.movie_downloader.download_finished.connect(self.update_movie_list)

    def update_movie_list(self, movie_object):
        self.movie_db_list.append(movie_object)
        self.refresh()

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            current_selection = self.selectedItems()
            if current_selection:
                for item in current_selection:
                    movie_object = item.movie
                    movie_object.delete()
                    self.movie_db_list.remove(movie_object)

                self.refresh()

    def create_movies(self, files):
        self.movie_db_list = []

        self.movie_downloader.set_file_list(files)
        self.movie_downloader.start()

    def show_details_action(self, item):
        self.show_detail.emit(item.movie)

    def refresh(self):
        self.clear()

        for movie_object in self.movie_db_list:
            MovieItem(self, movie_object)


class DownloaderWorker(QThread):
    download_finished = Signal(object)

    def __init__(self):
        super(DownloaderWorker, self).__init__()

        self.file_list = []

    def set_file_list(self, file_list):
        self.file_list = file_list

    def run(self):
        # create Movie objects based on file_path

        for file in self.file_list:
            print("Downloading", file)

            movie_object = Movie(movie_path=file, client=MovieList.client)
            self.download_finished.emit(movie_object)


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
