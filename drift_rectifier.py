from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

from file_caller import FileCaller
from plotter import Plotter

class DriftRectifier:
    """Rectifies the thermal drift of the RIXS map."""

    def __init__(self, path, first_spectra, last_spectra):
        raw_spectra = FileCaller(path, first_spectra, last_spectra)
        self.comp_spectra = raw_spectra.list_maker()
        self.myplot = []

        # Automatic correction of negative values at the start.
        i = 0
        while i < len(self.comp_spectra):
            self.comp_spectra[i] = [abs(x) for x in self.comp_spectra[i]]
            i += 1

        # Automatic linear rectification and display at the start.
        self.maxima_rectifier()


    def diff_set(self, differences, show_plots =True):
        """
        Takes the difference between the corrected position for each 
        correction method and the actual position and corrects it.
        """
        if len(differences) == len(self.comp_spectra):
            column = 0
            for difference in differences:
                while difference != 0:
                    # Sign generalisation for "wiggly" data.
                    if difference > 0:
                        # Pop and append the data where it corresponds.
                        popped_value = self.comp_spectra[column].pop(-1)
                        self.comp_spectra[column].insert(0, popped_value)
                        difference += -1
                    elif difference < 0:
                        popped_value = self.comp_spectra[column].pop(0)
                        self.comp_spectra[column].append(popped_value)
                        difference += 1
                column += 1
        else:
            print('Mismatch of array lenght.')

        myplot = Plotter(self.comp_spectra)
        if show_plots == True:
            myplot.show_plots()

    def maxima_rectifier(self, min_value=0):
        """Gives the maxima of each spectra in a difference list"""
        differences = []
        spectra_index = 0
        first_max = np.argmax(self.comp_spectra[0])
        for spectra in self.comp_spectra:
            # Corrections for non null min value.
            if min_value == 0:
                maximum = np.argmax(self.comp_spectra[spectra_index][min_value:])
            else:
                maximum = min_value + np.argmax(self.comp_spectra[spectra_index][min_value:])
            abs_differences = np.round(first_max - maximum)  
            differences.append(abs_differences)
            spectra_index += 1
        self.diff_set(differences)

    def negative_rectifier(self, neg_start_col, neg_end_col):
        """Manually rectifies negative values of the intensity."""
        for column in range(neg_start_col,neg_end_col+1):
            #print(self.comp_spectra[column])
            self.comp_spectra[column] = [-x for x in self.comp_spectra[column]]

    def cut_and_paste(self, cut_col, paste_col):
        """Cuts from the col number provided to the paste col provided"""
        for column in range(cut_col, paste_col+1):
            self.comp_spectra.pop(cut_col)


    #Not implemented need to redo
    def linear_rectifier(self):
        """
        Substract a linear function to the spectra using the elastic peak start 
        and end as reference.
        """
        self.difference = []
        first_spectra = 0
        # Minus one to correct for python starting index.
        last_spectra = len(self.comp_spectra) - 1

        # Find where the first and last elastic peaks are.
        first_max = np.argmax(self.comp_spectra[first_spectra])
        last_max = np.argmax(self.comp_spectra[last_spectra])

        def linear_function(first_spectra, last_spectra, first_max, last_max):
            """Arbitrary linear function to calculate slope and y-intercept."""
            # Calculate slope and y-intercept
            m = (last_max-first_max)/(last_spectra-first_spectra)
            b = first_max
            # Make the line
            line = [i*m + b for i in range(first_spectra, last_spectra+1)]
            return line

        line = linear_function(first_spectra, last_spectra, first_max, last_max)
        spectra_index = 0
        while spectra_index <= last_spectra:
            abs_difference = np.round(first_max - line[spectra_index])
            self.difference.append(abs_difference)
            spectra_index += 1

    # Not yet implemented
    def gaussian_rectifier(self):
        """Find the elastic peaks using a gaussian fit."""
        self.difference = []
        def gauss(x, H, A, B):
            return H + A * np.exp(-B * x**2)
        
        spectra_index = 0
        for spectra in self.comp_spectra:
            maximum = np.argmax(self.comp_spectra[spectra_index])
            x_fit = np.linspace(maximum-50, maximum+50, 100)
            popt, pcov= curve_fit(gauss, x_fit, 
                self.comp_spectra[spectra_index][maximum-50:maximum+50],
                p0 = [0,1,1])
            spectra_index += 1
            print(pcov)
