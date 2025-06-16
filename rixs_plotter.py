from pathlib import Path
import matplotlib.pyplot as plt
import h5py

from file_caller import FileCaller

path = '../../DATOSRIXS/20250521_DLD1 (1).h5'

spec_0 = FileCaller(path,130,180)

calib_x_spectrum = spec_0.hdf5_loader(130)

comp_spectra = spec_0.list_maker()

print(len(comp_spectra[0]))
print(len(comp_spectra))

fig, ax = plt.subplots()
im = ax.imshow(comp_spectra, cmap='plasma')
ax.set_aspect('auto')

plt.show()

