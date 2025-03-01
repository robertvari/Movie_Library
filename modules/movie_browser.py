from PySide2.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLineEdit, \
    QPushButton, QListWidget, QListWidgetItem, QItemDelegate, QStyle, QProgressBar, QTreeWidget, \
    QTreeWidgetItem, QHeaderView
from PySide2.QtGui import QPen, QBrush, QColor, QPixmap
from PySide2.QtCore import Qt, QSize, QRect, Signal, QThread

from objects.movie import Movie
import os, time, random

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

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        self.movie_list = MovieList()
        main_layout.addWidget(self.movie_list)

        self.movie_tree_list = MovieTreeList()
        self.movie_tree_list.setVisible(False)
        self.movie_tree_list.refresh(self.movie_list.movie_db_list)
        main_layout.addWidget(self.movie_tree_list)

        self.movie_list.movie_downloader.download_started.connect(self.start_progress)
        self.movie_list.movie_downloader.download_progress.connect(self.download_progress)
        self.movie_list.movie_downloader.download_progress_finished.connect(self.progress_bar.setVisible)

        self.search_bar.search_field.textChanged.connect(self.movie_list.do_search)
        self.search_bar.search_field.textChanged.connect(self.movie_tree_list.do_search)

        self.search_bar.az_button.clicked.connect(self.movie_list.sort_by_title)

        self.search_bar.toggle_view_btn.clicked.connect(self.toggle_views_action)

    def toggle_views_action(self, value):
        self.movie_list.setVisible(not value)
        self.movie_tree_list.setVisible(value)

    def start_progress(self, movie_list_length):
        self.progress_bar.setMaximum(movie_list_length)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

    def download_progress(self, download_data):
        self.progress_bar.setValue(download_data["progress_value"])
        self.progress_bar.setFormat(download_data["movie_file"])


class SearchBar(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5,5,5,0)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search by Title, Release date or Rating...")
        main_layout.addWidget(self.search_field)

        self.az_button = IconButton(get_static("sort_AZ.png"), size=30, checkbox=True)
        main_layout.addWidget(self.az_button)

        self.time_button = IconButton(get_static("sort_time.png"), size=30, checkbox=True)
        main_layout.addWidget(self.time_button)

        self.toggle_view_btn = IconButton(get_static("tree_view.png"), size=30, checkbox=True)
        main_layout.addWidget(self.toggle_view_btn)

    def sort_by_title(self):
        pass


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

    def do_search(self, filter_string):
        for index in range(self.count()):
            movie_item = self.item(index)

            if movie_item.has_name(filter_string):
                movie_item.setHidden(False)
            else:
                movie_item.setHidden(True)

    def sort_by_title(self, value):
        if value:
            self.movie_db_list = sorted(self.movie_db_list, key= lambda m: m.title.lower(), reverse=True)
        else:
            self.movie_db_list = sorted(self.movie_db_list, key= lambda m: m.title.lower())

        self.refresh()

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


class MovieTreeList(QTreeWidget):
    show_details = Signal(object)

    def __init__(self):
        super(MovieTreeList, self).__init__()
        self.setHeaderLabels(["Title", "Release Date", "Rating", "Original Language"])
        self.setSortingEnabled(True)

        header = self.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.itemDoubleClicked.connect(self.show_details_action)

    def show_details_action(self, item):
        self.show_details.emit(item.movie_object)

    def do_search(self, filter_string):
        root = self.invisibleRootItem()

        for index in range(root.childCount()):
            movie_item = root.child(index)

            if movie_item.has_name(filter_string):
                movie_item.setHidden(False)
            else:
                movie_item.setHidden(True)



    def refresh(self, movie_list):
        self.clear()

        for movie in movie_list:
            movie_item = MovieTreeItem(movie, self)

class DownloaderWorker(QThread):
    download_finished = Signal(object)

    download_started = Signal(int)
    download_progress = Signal(dict)
    download_progress_finished = Signal(bool)

    def __init__(self):
        super(DownloaderWorker, self).__init__()

        self.file_list = []

    def set_file_list(self, file_list):
        self.file_list = file_list

    def run(self):
        self.download_started.emit(len(self.file_list))

        for index, file in enumerate(self.file_list):
            self.download_progress.emit({"progress_value": index, "movie_file":f"Downloading data for: {os.path.basename(file)}..."})

            movie_object = Movie(movie_path=file, client=MovieList.client)
            self.download_finished.emit(movie_object)

        self.download_progress_finished.emit(False)


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

    def has_name(self, filter_string):
        item_filter_string = self.movie.title.lower()
        item_filter_string += f" {self.movie.release_date}"
        item_filter_string += f" {self.movie.rating}"

        if filter_string.lower() in item_filter_string:
            return True

        return False

class MovieTreeItem(QTreeWidgetItem):
    def __init__(self, movie_object, parent):
        super(MovieTreeItem, self).__init__(parent)

        self.movie = movie_object

        self.setText(0, movie_object.title)
        self.setText(1, movie_object.release_date)
        self.setText(2, str(movie_object.rating))
        self.setText(3, str(movie_object.original_language))

    def has_name(self, filter_string):
        item_filter_string = self.movie.title.lower()
        item_filter_string += f" {self.movie.release_date}"
        item_filter_string += f" {self.movie.rating}"

        if filter_string.lower() in item_filter_string:
            return True

        return False

class ChildItem(QTreeWidgetItem):
    def __init__(self, parent):
        super(ChildItem, self).__init__(parent)
        self.setText(0, "Child Item")