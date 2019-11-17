from PySide2.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QLabel, \
    QHBoxLayout, QSizePolicy, QSpacerItem
from PySide2.QtCore import Signal, Qt

from .customWidgets import BackdropImageWidget, Button

class MovieDetails(BackdropImageWidget):
    close_details = Signal()

    def __init__(self):
        super().__init__()
        self.setVisible(False)

        main_layout = QHBoxLayout(self)

        self.poster = QLabel()
        self.poster.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        self.poster.setMaximumWidth(320)
        main_layout.addWidget(self.poster)


        details_layout = QVBoxLayout()
        details_layout.setAlignment(Qt.AlignTop)
        main_layout.addLayout(details_layout)

        title_layout = QHBoxLayout()
        details_layout.addLayout(title_layout)
        self.title = QLabel()
        self.title.setObjectName("movie_title")

        self.release_date = QLabel()
        self.release_date.setObjectName("small_text")

        self.rating = QLabel()
        self.rating.setObjectName("small_text")

        overview_lbl = QLabel("Overview")
        overview_lbl.setObjectName("subtitle")

        self.description = QLabel()
        self.description.setWordWrap(True)

        title_layout.addWidget(self.title)
        title_layout.addWidget(self.release_date)

        title_layout.addItem(QSpacerItem(10,10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        close_btn = Button("Close")
        title_layout.addWidget(close_btn)

        details_layout.addWidget(self.rating)

        details_layout.addWidget(overview_lbl)
        details_layout.addWidget(self.description)


        close_btn.clicked.connect(self.close_action)

    def set_movie(self, movie):
        self.movie = movie

        self.poster.setPixmap(movie.poster)
        self.title.setText(movie.title)
        self.rating.setText( f"Raing: {movie.rating}")
        self.release_date.setText(f" ({movie.release_date})"  )
        self.description.setText(movie.description)

        self.set_backdrop_image(movie.backdrop)

        self.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close_action()

    def close_action(self):
        self.close_details.emit()