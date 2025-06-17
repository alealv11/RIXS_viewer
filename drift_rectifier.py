import numpy as np

class DriftRectifier:
    """Rectifies the thermal drift of the RIXS map."""
    def __init__(self, comp_spectra):
        self.comp_spectra = comp_spectra
        self.difference = difference = []

    def linear_rectifier(self):
        """
        Substract a linear function to the spectra using the elastic peak start 
        and end as reference.
        """
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
        

    def spectra_rectifier(self):
        """General way to recttify the spectra given a difference array"""
        # Define an output spectra as not to modify the original.
        aux_comp_spectra = []
        spectra_index = 0

        for spectra in self.comp_spectra:
            # Change to python lists to use pop and append method.
            aux_spectra = spectra[:].tolist()
            difference_val = self.difference[spectra_index]
            while difference_val != 0:
                # Generalisation for "wiggly" data that goes positive or negative.
                if difference_val > 0:
                    # Pop and append the data where it corresponds.
                    popped_value = aux_spectra.pop(-1)
                    aux_spectra.insert(popped_value, 0)
                    difference_val += -1
                elif difference_val < 0:
                    popped_value = aux_spectra.pop(0)
                    aux_spectra.append(popped_value)
                    difference_val += 1
            # Append the each corrected spectrum to the aux variable.
            aux_comp_spectra.append(aux_spectra)
            spectra_index += 1
        return aux_comp_spectra



        