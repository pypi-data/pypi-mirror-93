import sys
import os
import numpy as np
from matplotlib import pyplot as plt
import skimage.restoration
from skimage import measure
from bs4 import BeautifulSoup
import spectral.io.envi as envi
import pandas as pd  # knihovna pro save_as_csv_c
import csv  # knihovna pro save_as_csv_r
import operator


def box_plot(data):
    fig, ax = plt.subplots()
    ax.set_title('Box plot')
    a = ax.boxplot(data)
    plt.show()
    b = {}
    for i in a.keys():
        b.update({i: []})
        for j in a[i]:
            b[i].append(j.get_xydata())
    return [a, b]

def quantile(label, data):
    return np.percentile(data, q=(25, 50, 75))

def quantiles(data):
    label_image = np.ones(data.shape[0:2], dtype=np.uint)
    df = pd.DataFrame()
    for idx in range(data.shape[2]):
        props = measure.regionprops_table(label_image, intensity_image=data[...,idx],
                                          properties = ['label'], extra_properties = (quantile,))
        df = df.append(pd.DataFrame(props), ignore_index=True)
    return df

def est_sigma(data):
    es = []
    for n in range(0, data.shape[2]):
        es.append(skimage.restoration.estimate_sigma(data[:, :, n]))
    return es


def save_as_csv(data, name):  # data musÃ­ bÃ½t formÃ¡tu DataFrame
    data.to_csv(name + '.csv', index=False, header=True)
