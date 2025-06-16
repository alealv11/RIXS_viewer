from pathlib import Path
import matplotlib.pyplot as plt
import h5py

from file_caller import FileCaller

path = '../../DATOSRIXS/20250521_DLD1 (1).h5'

spec_0 = FileCaller(path,130,135)

calib_x_spectrum = spec_0.hdf5_loader(130)

comp_spectra = spec_0.list_maker()

print(sum(comp_spectra[0]))

x_comp = list(range(0,len(calib_x_spectrum)))
plt.scatter(x_comp,calib_x_spectrum,s=1)
plt.show()

