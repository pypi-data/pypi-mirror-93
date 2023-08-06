import matplotlib
matplotlib.use("Qt5Agg", force=True)

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSlot
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class SpectrumWindow(FigureCanvasQTAgg):
    clear = True
    position = None
    cube = None
    bands = None
    max = None

    def __init__(self, parent=None):
        fig = Figure(figsize=(10, 5))
        FigureCanvasQTAgg.__init__(self,fig)
        self._fig = fig
        self._ax = fig.canvas.figure.subplots()
        fig.set_visible(False)

    def set_bands(self, bands):
        self.bands = np.array(bands)

    def set_cube(self, cube):
        self.cube = cube
        self.max = np.ceil(np.max(cube)*10)/10
        if self.position:
            self._ax.clear()
            self.draw_spectrum_at_pos(self.position)

    def draw_data(self):
        if self.position:
            self._ax.clear()
            self.draw_spectrum_at_pos(self.position)

    @pyqtSlot(bool)
    def set_clear(self, clear):
        self.clear = clear
        if clear:
            self._ax.clear()
            self._ax.figure.canvas.draw()

    def draw_spectrum_at_pos(self, position):
        if self.cube is not None:
            x = self.bands
            self._fig.set_visible(True)
            if not isinstance(position, list):
                position = [position]
            if self.clear:
                self.position = position
            else:
                self.position.extend(position)
                # convert positioin to list
            pos_x = self.position[-1].x()
            pos_y = self.position[-1].y()
    #        self.setWindowTitle('Spectrum for coordinates: x = {}, y = {}'.format(pos_x, pos_y))
            if self.clear:
                self._ax.clear()
            self._ax.title.set_text('Spectrum for coordinates: x = {}, y = {}'.format(pos_x, pos_y))
            self._ax.set_xlabel('wavelength [nm]')
            for pos in self.position:
                pos_x = pos.x()
                pos_y = pos.y()
                y = self.cube[pos_x][pos_y]
                self._ax.plot(x, y)
                self._ax.set_xlabel('wavelength [nm]')
                self._ax.set_ylim([0, self.max])
            self._ax.figure.canvas.draw()
            self.show()

    def draw_vectors(self, vectors):
        x = self.bands
        self._fig.set_visible(True)
        self._ax.clear()
        self._ax.plot(x, vectors.transpose())
        self._ax.figure.canvas.draw()
        self.show()
