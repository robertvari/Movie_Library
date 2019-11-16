from PySide2.QtWidgets import QWidget, QApplication
from PySide2.QtGui import QPainter, QColor, QBrush, QPen, QPixmap, QFont, QFontMetrics
from PySide2.QtCore import Qt, Signal, QRect


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

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = Button("Test Button")
    win.show()
    app.exec_()