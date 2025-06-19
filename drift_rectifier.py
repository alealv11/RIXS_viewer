import numpy as np
from scipy.optimize import curve_fit

from plotter import Plotter

class DriftRectifier:
    """Rectifies the thermal drift of the RIXS map."""
    def __init__(self, comp_spectra):
        self.comp_spectra = comp_spectra
        self.aux_comp_spectra = []
        self.difference = []
        

    def spectra_rectifier(self, plot_switch=False, column_number='', 
        difference_val=0):
        """General and manual way to rectify the spectra given a difference array"""
        # Define an output spectra as not to modify the original.
        self.aux_comp_spectra = []
        spectra_index = 0
        # Manual way to move spectra around activated by giving a column number.
        if column_number:
            while difference_val != 0:
                    # Sign generalisation for "wiggly" data.
                    if difference_val > 0:
                        # Pop and append the data where it corresponds.
                        popped_value = self.comp_spectra[column_number].pop(-1)
                        self.comp_spectra[column_number].insert(0, popped_value)
                        difference_val += -1
                    elif difference_val < 0:
                        popped_value = self.comp_spectra[column_number].pop(0)
                        self.comp_spectra[column_number].append(popped_value)
                        difference_val += 1
        else:
            for spectra in self.comp_spectra:
                # Change to python lists to use pop and append method.
                if type(spectra) is not list:
                    aux_spectra = spectra[:].tolist()
                else:
                    aux_spectra = spectra[:]
                difference_val = self.difference[spectra_index]
                while difference_val != 0:
                    # Sign generalisation for "wiggly" data.
                    if difference_val > 0:
                        # Pop and append the data where it corresponds.
                        popped_value = aux_spectra.pop(-1)
                        aux_spectra.insert(0, popped_value)
                        difference_val += -1
                    elif difference_val < 0:
                        popped_value = aux_spectra.pop(0)
                        aux_spectra.append(popped_value)
                        difference_val += 1
                # Append the each corrected spectrum to the aux variable.
                self.aux_comp_spectra.append(aux_spectra)
                spectra_index += 1
                self.comp_spectra = self.aux_comp_spectra[:][:]

        if plot_switch == True:
            plot = Plotter(self.comp_spectra)
            plot.show_plots()
        return self.comp_spectra


    def maxima_rectifier(self, min_value=0):
        """Gives the maxima of each spectra in a difference list"""
        self.difference = []
        spectra_index = 0
        first_max = np.argmax(self.comp_spectra[0])
        for spectra in self.comp_spectra:
            # Corrections for non null min value.
            if min_value == 0:
                maximum = np.argmax(self.comp_spectra[spectra_index][min_value:])
            else:
                maximum = min_value + np.argmax(self.comp_spectra[spectra_index][min_value:])
            abs_difference = np.round(first_max - maximum)  
            self.difference.append(abs_difference)
            spectra_index += 1


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

    def negative_rectifier(self, neg_start_col, neg_end_col):
        """Recrtifies negative values of the intensity"""
        for column in range(neg_start_col,neg_end_col+1):
            self.comp_spectra[column] = -1*self.comp_spectra[column]