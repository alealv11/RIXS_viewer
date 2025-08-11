from pathlib import Path
import matplotlib.pyplot as plt
import h5py
#import numpy as np

from file_caller import FileCaller
from plotter import Plotter
from drift_rectifier import DriftRectifier

path = 'C:/Users/ciber/Documents/Nickelates/RawData/20250522_DLD1 (1).h5'


spectra = DriftRectifier(path,359,389)
myplot.ylim = 5