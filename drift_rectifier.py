from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

from file_caller import FileCaller

class DriftRectifier:
    """Rectifies the thermal drift of the RIXS map."""

    def __init__(self, path, first_spectra, last_spectra, auto=False):
        raw_spectra = FileCaller(path, first_spectra, last_spectra)
        self.comp_spectra = raw_spectra.list_maker()

        # Automatic correction of negative values at the start.
        i = 0
        while i < len(self.comp_spectra):
            self.comp_spectra[i] = [abs(x) for x in self.comp_spectra[i]]
            i += 1

        # Automatic linear rectification and display at the start.
        if auto == True:
            self.maxima_rectifier()
        else:
            self.plotter()


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

        self.plotter()

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

    def cut_and_paste(self, cut_col, paste_col, show_plots=True):
        """Cuts from the col number provided to the paste col provided"""
        for column in range(cut_col, paste_col+1):
            self.comp_spectra.pop(cut_col)
        if show_plots==True:
            self.plotter()


    def linear_rectifier(self, show_plots=False):
        """
        Substract a linear function to the spectra using the elastic peak start 
        and end as reference.
        """
        differences = []
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
            differences.append(abs_difference)
            spectra_index += 1
        self.diff_set(differences)

        if show_plots==True:
            self.plotter()

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

    def plotter(self, show_plots=True):
        """Deals with plotting and scaling"""

        disp_spectra = list(map(list, zip(*self.comp_spectra)))
        fig, ax = plt.subplots()
        im = ax.imshow(disp_spectra, cmap='viridis')
        ax.set_aspect('auto')
        if show_plots == True:
            plt.show(block=True)

    def export_igor(self, path):
        """Export to a igor readable format (.csv)"""
        save_spectra = list(map(list, zip(*self.comp_spectra)))
        np.savetxt(path + '_igor.csv',
                     save_spectra, delimiter=",")
