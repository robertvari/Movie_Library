from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, \
    QAction, QFileDialog
import sys

from modules import movie_browser, movie_details
from utilities.file_utils import get_files
from objects.movie import Movie


class MovieLibrary(QMainWindow):
    def __init__(self):
        super(MovieLibrary, self).__init__()
        self.setWindowTitle("Movie Library")
        self.resize(1000, 800)
        # self.showMaximized()

        central_Widget = QWidget()
        self.setCentralWidget(central_Widget)

        main_layout = QVBoxLayout(central_Widget)
        main_layout.setContentsMargins(0,0,0,0)

        # main menu
        menu = self.menuBar()

        settings_menu = menu.addMenu("&Content")

        add_folder_action = QAction("Add Folder", settings_menu)
        add_folder_action.triggered.connect(self.add_folder_action)
        settings_menu.addAction(add_folder_action)

        add_movie_action = QAction("Add Movie", settings_menu)
        add_movie_action.triggered.connect(self.add_movie_acion)
        settings_menu.addAction(add_movie_action)

        manage_folder_action = QAction("Manage Movies", settings_menu)
        manage_folder_action.triggered.connect(self.manage_movies_action)
        settings_menu.addAction(manage_folder_action)

        # load modules
        self.movie_browser = movie_browser.MovieBrowser()
        main_layout.addWidget(self.movie_browser)

        self.movie_details = movie_details.MovieDetails()
        main_layout.addWidget(self.movie_details)

        self.movie_browser.movie_list.show_detail.connect(self.show_details)
        self.movie_details.close_details.connect(self.hide_details)

    def show_details(self, movie):
        self.movie_browser.setVisible(False)


        self.movie_details.setVisible(True)
        self.movie_details.set_movie(movie)

    def hide_details(self):
        self.movie_browser.setVisible(True)
        self.movie_details.setVisible(False)

    def add_folder_action(self):
        folder = QFileDialog.getExistingDirectory(self, "Select folder:", "c:")

        if folder:
            self.movie_browser.movie_list.create_movies( get_files(folder) )

    def add_movie_acion(self):
        files = QFileDialog.getOpenFileNames(self, "Select movie files:", "c:", "Movie File (*.mkv)")

        if files[0]:
            self.movie_browser.movie_list.create_movies(files[0])

    def manage_movies_action(self):
        print("manage movies")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MovieLibrary()
    win.show()
    app.exec_()