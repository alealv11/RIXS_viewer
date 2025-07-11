from pathlib import Path
import matplotlib.pyplot as plt
import h5py
import numpy as np

from file_caller import FileCaller
from plotter import Plotter
from drift_rectifier import DriftRectifier

path = '../../DATOSRIXS/20250522_DLD1 (1).h5'

spec_0 = FileCaller(path,359,389)

comp_spectra = spec_0.list_maker()


linea = DriftRectifier(comp_spectra)

linea.negative_rectifier(0,5)
linea.linear_rectifier()
spectra = linea.spectra_rectifier(plot_switch=True)
# linea.maxima_rectifier(4000)
# spectra = linea.spectra_rectifier()
# linea.spectra_rectifier(plot_switch=False,column_number=2,
#     difference_val=5)
# linea.spectra_rectifier(plot_switch=False,column_number=4,
#     difference_val=5)
# linea.spectra_rectifier(plot_switch=True,column_number=5,
#     difference_val=5)

