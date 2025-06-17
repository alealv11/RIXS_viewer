from pathlib import Path
import matplotlib.pyplot as plt
import h5py
import numpy as np

from file_caller import FileCaller
from plotter import Plotter
from drift_rectifier import DriftRectifier

path = '../../DATOSRIXS/20250520_DLD1 (1).h5'

spec_0 = FileCaller(path,77,127)

comp_spectra = spec_0.list_maker()


linea = DriftRectifier(comp_spectra)

difference = linea.linear_rectifier()


spectra = linea.spectra_rectifier()

data = Plotter(spectra)

data.show_plots()



plt.show()

