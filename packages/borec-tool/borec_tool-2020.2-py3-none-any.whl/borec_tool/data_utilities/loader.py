from PyQt5.QtGui import QPixmap, QImage
import numpy as np
import imageio
from bs4 import BeautifulSoup
import spectral.io.envi as envi
import yaml
from pathlib import Path
from pkg_resources import resource_filename
import os

def load_history():
    try:
        cwd = os.getcwd()
        config_file = open(Path(cwd)/"configuration.yaml", "r")
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        config_file.close()
        return config
    except FileNotFoundError:
        return []

def save_history(files):
    # for backward compatibility, save file list as dictionary
    # config_dict = {}
    # for file in files:
    #     config_dict[Path(file).name] = str(file)
    cwd = os.getcwd()
    config_file = open(Path(cwd)/"configuration.yaml", "w")
    yaml.dump(files, config_file)
    config_file.close()


def get_name(dir):
    return dir.name


class Manifest():

    def __init__(self, directory):
        file = directory / 'manifest.xml'
        f_manifest = open(file, "r")
        self.manifest_data = BeautifulSoup(f_manifest, "lxml")

    def keys(self):
        return set([elem['type'] for elem in self.manifest_data.find_all('file')])

    def hdr_file(self, type):
        return [elem.string for elem in self.manifest_data.find_all('file') if
         (elem['type'] == type and elem['extension'] == 'hdr')][0]

    def data_file(self, type):
        return [elem.string for elem in self.manifest_data.find_all('file') if
         (elem['type'] == type and elem['extension'] in ['raw', 'dat'])][0]

    def preview_file(self):
        return [elem.string for elem in self.manifest_data.find_all('file') if
                (elem['type'] == 'preview')][0]


def get_manifest(directory, format):
    capt = directory / 'manifest.xml'
    f_manifest = open(capt, "r")
    manifest_data = BeautifulSoup(f_manifest, "lxml")
    b_files = manifest_data.find_all('file', {'type': format})
    f_manifest.close()
    return b_files # list of 2 elements, first is directory of header, second is directory of data


def get_hdr(directory):
    lib = envi.open(directory)
    # lib = open_image(directory)
    return lib

def get_preview(path):
    # file = list(Path(directory).glob('*.png'))
    image = imageio.imread(path, pilmode='RGB')
    return QPixmap(QImage(image, *image.shape[0:2], image[0, :].nbytes, QImage.Format_RGB888))

def read_cube(directory):
    manifest = Manifest(directory)
    f_types = manifest.keys()
    # keys = ['raw', 'darkref', 'whiteref', 'whitedarkref']
    data = {}
    # raw, darkref, whiteref, whitedarkref
    for type in f_types:
        if type in ['raw', 'darkref', 'whiteref', 'whitedarkref']:
            data[type] = open_file(directory, manifest, type)
    data['preview'] = get_preview(Path(directory)/manifest.preview_file())
    return data


def open_file(directory, manifest, format):
    # b_files = get_manifest(directory, format)
    # if format == 'reflectance':
    #     hdr_text = b_files[1].text
    #     dat_text = b_files[0].text
    # else:
    #     hdr_text = b_files[0].text
    #     dat_text = b_files[1].text
    lib = get_hdr(directory / manifest.hdr_file(format))
    rawfile = directory / manifest.data_file(format)
    img = envi.open(directory / manifest.hdr_file(format), rawfile)
    im = np.fliplr(img.load().swapaxes(1, 0))
    # f_raw = open(rawfile, "r")
    # im = np.fromfile(f_raw, dtype=np.uint16)
    # im = np.reshape(im, [lib.shape[1], lib.shape[2], lib.shape[0]])
    # im = np.transpose(im, (2, 0, 1))[:, ::-1, :]
    return {'data': im, 'header': lib}


def load_graphs():
    try:
        graph_file = open(resource_filename('borec_tool.resources', 'graph.yaml'), "r")
        graphs = yaml.load(graph_file, Loader=yaml.FullLoader)
        graph_file.close()
        return graphs
    except FileNotFoundError:
        return None


def save_graphs(graph):
    try:
        graph_file = open(resource_filename('borec_tool.resources', 'graph.yaml'), "r")
        graph_dict = yaml.load(graph_file, Loader=yaml.FullLoader)
        graph_file.close()
    except FileNotFoundError:
        graph_dict = {}
    new_graph_dict = {**graph_dict, **graph}
    graph_file = open(resource_filename('borec_tool.resources','graph.yaml'), "w")
    yaml.dump(new_graph_dict, graph_file)
    graph_file.close()
