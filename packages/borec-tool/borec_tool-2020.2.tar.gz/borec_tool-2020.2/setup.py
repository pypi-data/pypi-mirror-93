from __future__ import absolute_import
from setuptools import setup, find_packages
from os import path

_dir = path.abspath(path.dirname(__file__))

with open(path.join(_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='borec_tool',
      version='2020.2',
      author='Jan Schier',
      author_email='schier@utia.cas.cz',
      description='Tool for visualization and analysis of hyperspectral data',
      long_description=long_description,
	  long_description_content_type='text/x-rst',
      url='https://gita.utia.cas.cz/schier/borec-tool.git',
      license='BSD 3-Clause License',
      packages=find_packages(),
      package_data = {'': ['*.png', '*.yaml', '*.mat', '*.svg']},

      project_urls={
          'Repository': 'https://gita.utia.cas.cz/schier/borec-tool.git',
      },

      classifiers=[
        'Development Status :: 4 - Beta',  # 3 - Alpha, 4 - Beta, 5 - Production/Stable
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Image Processing',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent'
      ],

      install_requires=[
        'pyqt5',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'scikit-learn',
        'seaborn',
        'scikit-image',
        'hdbscan',
        'svgpathtools',
        'setuptools',
        'spectral',
        'beautifulsoup4',
        'imageio',
        'pyyaml'
       ]
      )
