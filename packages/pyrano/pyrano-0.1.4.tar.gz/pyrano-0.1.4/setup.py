from distutils.core import setup
import os

long_description = '''
Pyrano is a Python package for simulating solar irradiance
on external built surfaces using Digital Surface Model (DSM)
point clouds as shading geometry. Pyrano aims to bridge the gap
between building energy, solar irradiance and PV power simulations.
It is compatible with EnergyPlus, Radiance and PVMismatch. \n
See more at https://gitlab.tue.nl/bp-tue/pyrano
'''

setup(
  name = 'pyrano',
  packages = ['pyrano'],
  version = '0.1.4',
  license = 'MIT',
  description = 'Solar irradiance simulations for PV and BPS applications',
  long_description_content_type = 'text/markdown',
  long_description = long_description,
  author = 'Adam Bognar',
  author_email = 'a.bognar@tue.nl',
  url = 'https://gitlab.tue.nl/bp-tue/pyrano',
  download_url = 'https://gitlab.tue.nl/bp-tue/pyrano/-/archive/v0.1.4/pyrano-v0.1.4.tar.gz',
  keywords = ['solar', 'irradiance', 'pv', 'radiance', 'energyplus', 'pvmismatch', 'lidar', 'pointclouds'],
  install_requires=['pandas==0.25.3',
                    'numpy==1.11.0',
                    'matplotlib==3.1.3',
                    'eppy==0.5.54',
                    'geomeppy==0.11.8',
                    'scikit-learn==0.24.1',
                    'Pillow==8.1.0',
                    'Rtree==0.9.7'],
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Development Status :: 4 - Beta',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python :: 3',
    'Topic :: Scientific/Engineering',
  ],
)
