from PySide2.QtWidgets import QWidget, QVBoxLayout, QGroupBox

class MovieDetails(QWidget):
    def __init__(self):
        super().__init__()
        self.setVisible(False)

        main_layout = QVBoxLayout(self)

        group_box = QGroupBox("Movie Details")
        main_layout.addWidget(group_box)