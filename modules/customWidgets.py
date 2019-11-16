from PySide2.QtWidgets import QWidget, QApplication
from PySide2.QtGui import QPainter, QColor, QBrush, QPen, QPixmap
from PySide2.QtCore import Qt, Signal


class Button(QWidget):
    clicked = Signal()

    def __init__(self, text):
        super(Button, self).__init__()
        self.text = text

        self.setMinimumSize(100, 100)
        self.setMaximumSize(100, 100)

    def enterEvent(self, event):
        QApplication.setOverrideCursor(Qt.PointingHandCursor)
        super(Button, self).enterEvent(event)

    def leaveEvent(self, event):
        QApplication.restoreOverrideCursor()
        super(Button, self).leaveEvent(event)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super(Button, self).mousePressEvent(event)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = Button("Test Button")
    win.show()
    app.exec_()