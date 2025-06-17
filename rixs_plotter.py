from pathlib import Path
import matplotlib.pyplot as plt
import h5py

from file_caller import FileCaller
from plotter import Plotter

path = '../../DATOSRIXS/20250521_DLD1 (1).h5'

spec_0 = FileCaller(path,130,180)

comp_spectra = spec_0.list_maker()

data = Plotter(comp_spectra)

data.show_plots()



plt.show()

