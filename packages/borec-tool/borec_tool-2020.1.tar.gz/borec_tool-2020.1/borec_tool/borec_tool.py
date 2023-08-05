from __future__ import absolute_import
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QApplication, QAction, QSplitter, QGridLayout, QWidget,
                             QMenuBar, QVBoxLayout, QListWidget, QMessageBox)
from PyQt5.QtCore import pyqtSignal

from tkinter import Tk
from tkinter.filedialog import askdirectory
from .data_utilities import loader as loader
from .clustering import Clustering, SpinBoxParams
from .wavelet import Wavelet
from .data_utilities.cube import Hyperspectral, DataHdr
from pathlib import Path
from .img_sigma import Sigma
from .processing import KMeans, MiniBatchKMeans, PCA_KMeans, PCA_HDBSCAN
from .img_quantiles import Quantiles
from .tab_widget import SpectralTabs
from numpy import ndarray
from .img_pca import EvalPCA

import sys


class ListSlider(QtWidgets.QSlider):
    elementChanged = QtCore.pyqtSignal(int, float)

    def __init__(self, values=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimum(0)
        self._values = []
        self.valueChanged.connect(self._on_value_changed)
        self.values = values or []

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        self._values = values
        maximum = max(0, len(self._values) - 1)
        self.setMaximum(maximum)
        self.setValue(0)

    @QtCore.pyqtSlot(int)
    def _on_value_changed(self, index):
        value = self.values[index]
        self.elementChanged.emit(index, value)

class Window(QWidget):
    MaxRecentFiles = 5
    bands_sig = pyqtSignal(list)
    reflect_sig = pyqtSignal(DataHdr)
    sig_data = pyqtSignal(ndarray)
    sig_dir = pyqtSignal(Path)
    # full_data_sig = pyqtSignal(dict)
    data_hyperspectral_sig = pyqtSignal(Hyperspectral)

    def __init__(self):
        QWidget.__init__(self)
        self.recentFileActs = []

        # Navbar
        navbarLayout = QGridLayout()
        # Buttons
        openfolder_button = QAction("Open folder", self)
        close_button = QAction("Close", self)
        # Actions of buttons
        openfolder_button.triggered.connect(self.menu_open_folder)
        close_button.triggered.connect(self.close)
        # Create menu
        menubar = QMenuBar()
        navbarLayout.addWidget(menubar, 0, 0)
        fileMenu = menubar.addMenu("File")
        fileMenu.addAction(openfolder_button)
        # recent files
        recent_file = fileMenu.addMenu("Open recent")
        self.createRecentFileActions()
        for i in range(Window.MaxRecentFiles):
            recent_file.addAction(self.recentFileActs[i])
        self.updateRecentFileActions()
        save_file = QAction("&Save", self)
        save_file.setShortcut("Ctrl+S")
        save_file.setStatusTip('Save File')
        save_as = QAction("Save as", self)
        fileMenu.addAction(save_file)
        fileMenu.addAction(save_as)
        fileMenu.addSeparator()
        fileMenu.addAction(close_button)
        fcn_menu = menubar.addMenu("Functions")
        self.fcn_menu = fcn_menu
        menu_sigma = QAction("Data mean", self)
        menu_sigma.setEnabled(False)
        menu_sigma.triggered.connect(lambda status, cls=Sigma, text="Data mean": self.menu_tabs.tab_window(cls, text))
        fcn_menu.addAction(menu_sigma)
        self.menu_sigma = menu_sigma

        menu_quartiles = QAction("Quantiles", self)
        menu_quartiles.setEnabled(False)
        menu_quartiles.triggered.connect(lambda status, cls=Quantiles, text="Quantiles": self.menu_tabs.tab_window(cls, text))
        fcn_menu.addAction(menu_quartiles)
        self.menu_sigma = menu_sigma


        menu_clustering = QAction("KMeans", self)
        menu_clustering.setEnabled(False)
        params = {'n_clusters': SpinBoxParams(max=99, value=5, label="N clusters: "),
                  'max_iter': SpinBoxParams(max=999, value=100, step=100, label="N iterations: ")}
        menu_clustering.triggered.connect(lambda status: self.menu_tabs.tab_window(Clustering, "KMeans",
                                                                         clusterer=KMeans, parameters=params))
        fcn_menu.addAction(menu_clustering)

        menu_minibatch = QAction("Mini-Batch KMeans", self)
        menu_minibatch.setEnabled(False)
        menu_minibatch.triggered.connect(lambda status: self.menu_tabs.tab_window(Clustering, "Mini-Batch KMeans",
                                                                        clusterer=MiniBatchKMeans, parameters=params))
        fcn_menu.addAction(menu_minibatch)

        menu_pca_kmeans = QAction("PCA-KMeans", self)
        menu_pca_kmeans.setEnabled(False)
        params_pca_km = {'n_components': SpinBoxParams(max=10, value=2, label="N components"),
                  'n_clusters': SpinBoxParams(max=99, value=5, label="N clusters: "),
                  'max_iter': SpinBoxParams(max=999, value=100, step=100, label="N iterations: ")}
        menu_pca_kmeans.triggered.connect(lambda status: self.menu_tabs.tab_window(Clustering, "PCA-KMeans",
                                                                        clusterer=PCA_KMeans, parameters=params_pca_km))
        fcn_menu.addAction(menu_pca_kmeans)

        params_pca_dbscan = {'n_components': SpinBoxParams(max=100, value=5, label="N components"),
                             'min_cluster_size': SpinBoxParams(max=30000, value=1000, step=100, label="Min cluster size")}
        menu_dbscan = QAction("PCA HDBSCAN", self)
        menu_dbscan.setEnabled(False)
        menu_dbscan.triggered.connect(lambda status: self.menu_tabs.tab_window(Clustering, "PCA HDBSCAN",
                                                                                      clusterer=PCA_HDBSCAN,
                                                                                      parameters=params_pca_dbscan))
        fcn_menu.addAction(menu_dbscan)


        menu_pca = QAction("PCA", self)
        menu_pca.setEnabled(False)
        menu_pca.triggered.connect(lambda status: self.menu_tabs.tab_window(EvalPCA, "PCA"))
        fcn_menu.addAction(menu_pca)

        menu_wavelet = QAction("Wavelet denoising", self)
        menu_wavelet.setEnabled(False)
        menu_wavelet.triggered.connect(lambda status: self.menu_tabs.tab_window(Wavelet, "Wavelet", wavelet='db1'))
        fcn_menu.addAction(menu_wavelet)

        help_menu = menubar.addMenu("Help")
        about = QAction("About", self)
        about.triggered.connect(self.about_box)
        help_menu.addAction(about)

        self.menu_tabs = SpectralTabs(parent=self)
        self.sig_dir.connect(self.menu_tabs.set_directory)
        self.reflect_sig.connect(self.menu_tabs.reflect_sig)
        self.data_hyperspectral_sig.connect(self.menu_tabs.update_display)
        save_file.triggered.connect(lambda: self.menu_tabs.save_slot())
        save_as.triggered.connect(lambda: self.menu_tabs.save_as_slot())

        self.menu_tabs.led.sig_radiance.connect(self.menu_tabs.radiance.set_illumination)

        list_splitter = QSplitter()

        self.opened_listwidget = QListWidget(parent=self)
        self.opened_listwidget.itemClicked.connect(self.switch_image)
        list_splitter.addWidget(self.opened_listwidget)

        main_splitter = QSplitter()
        main_splitter.addWidget(list_splitter)

        imageLayout = QVBoxLayout()
        # imageLayout.addWidget(self.toolbar)
        imageLayout.addWidget(self.menu_tabs)
        image = QWidget()
        image.setLayout(imageLayout)
        # File browser
        main_splitter.addWidget(image)

        # Layouts
        self.mainLayout = QVBoxLayout()

        self.mainLayout.addLayout(navbarLayout)
        self.mainLayout.addWidget(main_splitter)
        # self.mainLayout.addLayout(self._lay)
        self.setLayout(self.mainLayout)
        self.setGeometry(50, 50, 1400, 540)
        self.setWindowTitle('BOREC tool')
        self.show()

    def createRecentFileActions(self):
        self.files = loader.load_history()
        for i in range(Window.MaxRecentFiles):
            self.recentFileActs.append(
                QAction(self, visible=False,
                        triggered=self.openRecentFile))

    def updateRecentFileActions(self):
        numRecentFiles = min(len(self.files), Window.MaxRecentFiles) if self.files else 0

        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, Path(self.files[i]).name)
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(self.files[i])
            self.recentFileActs[i].setVisible(True)

        for j in range(numRecentFiles, Window.MaxRecentFiles):
            self.recentFileActs[j].setVisible(False)

    def strippedName(self, fullFileName):
        return QtCore.QFileInfo(fullFileName).fileName()

    def openRecentFile(self):
        action = self.sender()
        if action:
            self.menu_open_folder(directory=Path(action.data()))

    def get_dir(self):
        root = Tk()
        root.withdraw()
        dir_string = askdirectory()
        dir = Path(dir_string) if dir_string else None
        return dir

    def update_recent(self):
        try:
            self.files.remove(str(self.directory))
        except (ValueError):
            pass

        self.files.insert(0, str(self.directory))
        del self.files[Window.MaxRecentFiles:]

        loader.save_history(self.files)
        self.updateRecentFileActions()

    def file_not_found(text=None):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        return msg.exec()

    def about_box(self):
        msg = QMessageBox()
        text = 'The development of this software has been supopported\n' \
                ' by the Technology Agency of the Czech Republic grant No. TH03010330\n' \
                '\n' \
                'The tool is licensed under the BSD-3 license\n\n' \
                'For the source code, please contact\nJan Schier\n' \
                'Instute of Information Theory and Automation\n' \
                'Department of Image Processing\n' \
                'schier@uta.cas.cz'
        msg.setText(text)
        msg.setWindowTitle('Info')
        msg.setStandardButtons(QMessageBox.Ok)
        return msg.exec()

    def open_folder(self, directory=None):
        if directory is False:
            self.directory = self.get_dir()
        else:
            self.directory = directory
        if self.directory is None: return None
        self.sig_dir.emit(self.directory)
        try:
            self.full_data = loader.read_cube(self.directory)
            full_data = Hyperspectral(**self.full_data)
            self.reflect_sig.emit(full_data.reflectance)
#            self.data = full_data.raw.data
#            self.bands = full_data.reflectance.header.bands.centers
            return full_data
        except FileNotFoundError:
            text = 'Valid file not found!'
            if self.directory:
                text = 'Directory: ' + str(self.directory) + "\nNo valid hyperspectral data."
            self.file_not_found(text=text)
        except TypeError:
            self.file_not_found(text="Error - no file selected?")
        return None

    def menu_open_folder(self, directory=None, add_to_open=True):
        full_data = self.open_folder(directory=directory)
        if full_data:
            self.menu_tabs.full_data_obj = full_data
            self.data_hyperspectral_sig.emit(full_data)
            self.update_recent()
            # self.menu_tabs.update_display(full_data)
            if add_to_open:
                self.opened_listwidget.addItem(str(self.directory))
            for action in self.fcn_menu.actions():
                action.setEnabled(True)

    def get_data(self, spectra_all):
        if hasattr(self, 'full_data'):
            self.sig_data.emit(spectra_all)
            self.menu_tabs.addTab(self.menu_tabs.tab_radiance, "Radiance")

    def switch_image(self, item):
        self.menu_open_folder(Path(item.text()), add_to_open=False)


def main():
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()