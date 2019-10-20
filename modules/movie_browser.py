from PySide2.QtWidgets import QWidget, QVBoxLayout, QGroupBox

class MovieBrowser(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)

        group_box = QGroupBox("Movie Browser")
        box_layout = QVBoxLayout(group_box)
        main_layout.addWidget(group_box)

        self.search_bar = SearchBar()
        box_layout.addWidget(self.search_bar)


class SearchBar(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)

        group_box = QGroupBox("Search bar")
        main_layout.addWidget(group_box)