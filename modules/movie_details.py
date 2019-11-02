from PySide2.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton
from PySide2.QtCore import Signal

class MovieDetails(QWidget):
    close_details = Signal()

    def __init__(self):
        super().__init__()
        self.setVisible(False)

        main_layout = QVBoxLayout(self)

        close_btn = QPushButton("Close")
        main_layout.addWidget(close_btn)
        close_btn.clicked.connect(self.close_action)

    def close_action(self):
        self.close_details.emit()