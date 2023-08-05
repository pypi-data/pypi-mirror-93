from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QToolBar, QToolButton, \
    QMenu, QAction
from PyQt5.QtGui import QImage, QPixmap

from borec_tool.gui.band_slider import Slider
from .spectrum_window import SpectrumWindow
from .viewer import Viewer
from numpy import ndarray
import numpy as np
from pkg_resources import resource_filename


class ImgWindow(QWidget):

    mode_preview = True
    preview = None
    data = None
    band = 0

    slider_hide = pyqtSignal(bool)
    bands_sig = pyqtSignal(list)
    cube_sig = pyqtSignal(ndarray)

    def menu_action_triggered(self, item):
        self.img_selector.setDefaultAction(item)
        self.mode_preview = item.sender().text() == 'Preview'
        self.slider_hide.emit(self.mode_preview)
        if self.mode_preview:
            self.view.display_image(self.preview)
        else:
            self.display_raw(self.band)

    def single_point_triggered(self, status):
        self.view.add_points_button(status)
        self.spectrum.set_clear(not status)

    def __init__(self, parent=None):
        QWidget.__init__(self)
        toolbar = QToolBar('Markers')
        images = QMenu()
        preview = QAction('Preview', images)
        preview.triggered.connect(lambda chck, item=preview: self.menu_action_triggered(item))
        cube = QAction('Spectral', images)
        cube.triggered.connect(lambda chck, item=cube: self.menu_action_triggered(item))
        images.addAction(preview)
        images.addAction(cube)
        img_selector = QToolButton(self)
        img_selector.setMenu(images)
        img_selector.setDefaultAction(preview)
        img_selector.setPopupMode(QToolButton.InstantPopup)
        self.img_selector = img_selector

        self.spectrum = SpectrumWindow()
        view = Viewer(self)
        self.bands_sig.connect(self.spectrum.set_bands)
        self.cube_sig.connect(self.spectrum.set_cube)
        view.pos.connect(self.spectrum.draw_spectrum_at_pos)


        toolbar.addWidget(img_selector)
        single_mark = QAction(QIcon(resource_filename('borec_tool.resources.gui', 'cursor-cross.png')), 'Mark', self)
        single_mark.triggered.connect(lambda state, status=False: self.single_point_triggered(status))
        toolbar.addAction(single_mark)
        multi_mark = QAction(QIcon(resource_filename('borec_tool.resources.gui', 'multi-cross.png')), 'Multiple marks', self)
        multi_mark.triggered.connect(lambda state, status=True: self.single_point_triggered(status))
        toolbar.addAction(multi_mark)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        view.setMinimumHeight(512)
        self.spectrum.setMinimumWidth(512)
        self.view = view
        # view_size_policy = self.view.sizePolicy()
        # view_size_policy.setRetainSizeWhenHidden(True)
        # self.view.setSizePolicy(view_size_policy)
        images = QWidget()
        graph_layout = QHBoxLayout()
        graph_layout.addWidget(view)
        graph_layout.addWidget(self.spectrum)
        images.setLayout(graph_layout)
        self.images = images

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(images)
        slider = Slider(set_hidden=True)
        slider.band_idx.connect(self.display_raw)
        layout.addWidget(slider)
        self.slider = slider
        self.slider_hide.connect(slider.setHidden)
        self.setLayout(layout)

    def display_image(self):
        self.view.display_image()

    def set_data(self, data):
        self.data = data
        self.preview = data.preview
        cube = data.reflectance.data
        self.cube_max = np.max(cube)
        self.cube = cube
        self.bands = data.reflectance.header.bands.centers
        self.bands_sig.emit(self.bands)
        self.cube_sig.emit(self.cube)
        self.view.set_image(self.preview)
        self.slider.values = self.bands
        if self.mode_preview:
            self.view.display_image()
        else:
            self.display_raw()

    def set_bands(self, bands):
        self.bands_sig.emit(bands)

    def get_pixmap(self, band):
        image = self.cube[:,:,band]
        image = np.uint8(image/np.float(self.cube_max)*255)
        return QPixmap(QImage(image.tobytes(), *image.shape[0:2], image[0, :].nbytes, QImage.Format_Grayscale8))


    def display_raw(self, band=None):
        if band is not None:
            self.band = band
        if self.data is not None:
            self.view.display_image(self.get_pixmap(self.band))

    def save(self):
        return

