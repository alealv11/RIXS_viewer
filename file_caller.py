import h5py
import matplotlib.pyplot as plt
import numpy as np


class FileCaller:
    """
    This deals with the VERITAS beamline hdf5 data structure and returns the
    necessary data in a workable format. Also deals with exporting the
    modified data to IGOR.

    """
    def __init__(self, path, first_acq, last_acq):
        """Initialize the class arguments"""
        self.path = path
        self.first_acq = first_acq
        self.last_acq = last_acq
        self.comp_spectra = []

    def hdf5_loader(self, acq_number):
        """
        Loads the hdf5 file and returns the calibrated spectrum list for 
        one acquisition.
        """
        f = h5py.File(self.path, 'r')
        # Returns a list of the calibrated spectrum of a given acquisition.
        calib_x_spectrum = f["/acq"+str(acq_number)]["data"]["calib_x_spectrum"]
        return calib_x_spectrum

    def list_maker(self):
        """Makes the lists of all the acquisition spectra for one measurement"""

        # Define the loop start number as the first acquisition.
        acq_number = self.first_acq

        # Run over all the acquisitions, transforming them from dataset into
        # floats and then apending them to a compilation of lists.
        while self.first_acq <= acq_number <= self.last_acq:
            #Convert numpy object to list.
            current_spectra = self.hdf5_loader(acq_number)[:].tolist()
            self.comp_spectra.append(current_spectra)
            acq_number += 1
        return self.comp_spectra

    #def export_igor(self):
