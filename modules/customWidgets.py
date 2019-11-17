from PySide2.QtWidgets import QWidget, QApplication
from PySide2.QtGui import QPainter, QColor, QBrush, QPen, QPixmap, QFont, QFontMetrics
from PySide2.QtCore import Qt, Signal, QRect, QSize

import os


class Button(QWidget):
    clicked = Signal()

    def __init__(self, text):
        super(Button, self).__init__()
        self.text = text

        self.roundness = 10

        self.painter = QPainter()

        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setBold(True)

        metrics = QFontMetrics(self.font)
        self.setMinimumSize(metrics.width(text) + 40, 50)

        self.pen = QPen(QColor("#01d277"))
        self.pen.setWidth(5)

        self.hover_brush = QBrush(QColor(1, 210, 119, 100))

        self.hover = False

    def enterEvent(self, event):
        QApplication.setOverrideCursor(Qt.PointingHandCursor)
        self.hover = True
        self.repaint()
        super(Button, self).enterEvent(event)

    def leaveEvent(self, event):
        QApplication.restoreOverrideCursor()
        self.hover = False
        self.repaint()
        super(Button, self).leaveEvent(event)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super(Button, self).mousePressEvent(event)

    def paintEvent(self, event):
        self.painter.begin(self)
        self.draw()
        self.painter.end()

    def draw(self):
        rect = self.rect()
        self.painter.setRenderHint(self.painter.Antialiasing)

        self.painter.setPen(self.pen)
        border_rect = QRect(rect.x() + 5, rect.y() + 5, rect.width()-10, rect.height() -10 )
        self.painter.drawRoundedRect(border_rect, self.roundness, self.roundness)

        self.painter.setFont(self.font)
        self.painter.drawText(border_rect, Qt.AlignVCenter|Qt.AlignHCenter, self.text)

        if self.hover:
            self.painter.setBrush(self.hover_brush)
            self.painter.setPen(Qt.NoPen)
            self.painter.drawRoundedRect(border_rect, self.roundness, self.roundness)


class IconButton(QWidget):
    clicked = Signal()

    def __init__(self, image_path, size=40):
        super(IconButton, self).__init__()
        self.setMinimumSize(size, size)
        self.setMaximumSize(size, size)

        self.hover = False

        pixmap_image = ""
        if os.path.exists(image_path):
            pixmap_image = image_path

        pixmap = QPixmap(pixmap_image)
        self.pixmap = pixmap.scaled(QSize(size, size), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.painter = QPainter()

    def enterEvent(self, event):
        QApplication.setOverrideCursor(Qt.PointingHandCursor)
        self.hover = True
        self.repaint()
        super(IconButton, self).enterEvent(event)

    def leaveEvent(self, event):
        QApplication.restoreOverrideCursor()
        self.hover = False
        self.repaint()
        super(IconButton, self).leaveEvent(event)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super(IconButton, self).mousePressEvent(event)

    def paintEvent(self, event):
        self.painter.begin(self)
        self.draw()
        self.painter.end()

    def draw(self):
        rect = self.rect()

        self.painter.setOpacity(0.5)

        if self.hover:
            self.painter.setOpacity(1)

        self.painter.drawPixmap(rect, self.pixmap)


class BackdropImageWidget(QWidget):
    def __init__(self):
        super(BackdropImageWidget, self).__init__()
        self.backdrop_image = ""
        self.painter = QPainter()

        self.pixmap = QPixmap(self.backdrop_image)
        self.fill_brush = QBrush(QColor(0, 0, 0, 210))

    def set_backdrop_image(self, image_path):
        self.backdrop_image = image_path
        self.pixmap.load(image_path)

    def paintEvent(self, event):
        self.painter.begin(self)
        self.draw()
        self.painter.end()

    def draw(self):
        rect = self.rect()

        scaled_image = self.pixmap.scaledToWidth(rect.width(), Qt.SmoothTransformation)

        if scaled_image.height() < rect.height():
            scaled_image = self.pixmap.scaledToHeight(rect.height(), Qt.SmoothTransformation)

        image_rect = QRect(rect.x(), rect.y(), scaled_image.width(), scaled_image.height())
        image_rect.moveCenter(rect.center())
        self.painter.drawPixmap(image_rect, scaled_image)

        self.painter.setBrush(self.fill_brush)
        self.painter.setPen(Qt.NoPen)
        self.painter.drawRect(rect)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = BackdropImageWidget()
    win.set_backdrop_image(r"C:\Users\Robert\Movie_Library\1573910895_backdrop.jpg")
    win.show()
    app.exec_()