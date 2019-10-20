from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QAction
import sys

class MovieLibrary(QMainWindow):
    def __init__(self):
        super(MovieLibrary, self).__init__()
        self.setWindowTitle("Movie Library")
        self.resize(1000, 800)
        # self.showMaximized()

        central_Widget = QWidget()
        self.setCentralWidget(central_Widget)

        main_layout = QVBoxLayout(central_Widget)

        # main menu
        menu = self.menuBar()

        settings_menu = menu.addMenu("&Settings")

        add_folder_action = QAction("Add Folder", settings_menu)
        add_folder_action.triggered.connect(self.add_folder_action)
        settings_menu.addAction(add_folder_action)

        manage_folder_action = QAction("Manage Folders", settings_menu)
        manage_folder_action.triggered.connect(self.manage_folders_action)
        settings_menu.addAction(manage_folder_action)

    def add_folder_action(self):
        print("Add folder action")

    def manage_folders_action(self):
        print("manage folder")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MovieLibrary()
    win.show()
    app.exec_()