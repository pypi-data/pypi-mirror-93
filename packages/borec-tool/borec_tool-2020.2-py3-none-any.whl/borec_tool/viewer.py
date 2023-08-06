from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtCore import pyqtSignal, QPoint, QPointF, Qt, QEvent
from PyQt5 import QtGui
from numpy import ndarray

class Viewer(QGraphicsView):
    pos = pyqtSignal(QPoint)
    clear = pyqtSignal(bool)
    pixmap = None

    def __init__(self, parent=None):
        QGraphicsView.__init__(self)
        self.setWindowTitle("scene")
        self.setStyleSheet("border: 0px")
        self.scene = QGraphicsScene(self)
        self.crosshair = QtGui.QPixmap('borec_tool/resources/gui/cursor-cross.png')
        self.cursor_center = self.crosshair.rect().center()
        self.cursorPos = None

        self.setScene(self.scene)
        self.setMinimumSize(512,512)
        self.setGeometry(0,0,512,512)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.add_points = False
        self.markers = []

        self.installEventFilter(self)


    def setCursorPos(self, cursorPos):
        if not self.add_points and self.markers:
            self._remove_markers()
        cursor = QGraphicsPixmapItem(self.crosshair)
        cursor.setPos(cursorPos-self.cursor_center)
        cursor.setZValue(1)
        self.markers.append(cursor)
        self.scene.addItem(cursor)

    # def mousePressEvent(self, event):
    #
    #     items = self.items(event.pos())
    #     for item in items:
    #         if item is self.pixmap_item:
    #             print(item.mapFromScene(self.mapToScene(event.pos())))
    #     super(Viewer, self).mousePressEvent(event)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress and self.pixmap is not None:
            # set the current position and schedule a repaint of the label
            cursorPos = self.mapToScene(event.pos()).toPoint()
            self.setCursorPos(cursorPos)
            self.pos.emit(cursorPos)
        return super().eventFilter(source, event)

    def set_image(self, image):
        if self.pixmap is not None:
            self.scene.removeItem(self.pixmap)
        pixmap = self.scene.addPixmap(image)
        pixmap.setZValue(0)
        self.pixmap = pixmap
        self.viewport().setCursor(Qt.CrossCursor)

    def display_image(self, image=None):
        if image is not None:
            self.set_image(image)
        self.show()


    def _remove_markers(self):
        for marker in self.markers:
            self.scene.removeItem(marker)
        self.markers = []

    def add_points_button(self, selected):
        self.add_points = selected
        self.clear.emit(not selected)
        if not selected: self._remove_markers()

