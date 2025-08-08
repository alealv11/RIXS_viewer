import matplotlib.pyplot as plt

class Plotter:
    """Makes the plots of the rixs based on a list of lists input"""
    def __init__(self, comp_spectra):
        """Initialize class arguments"""
        self.comp_spectra = comp_spectra


    def show_plots(self):
        """Displays the plots in a readable and well oriented way."""

        # Transposes the list of lists by dark magic. 
        # https://stackoverflow.com/questions/6473679/transpose-list-of-lists
        disp_spectra = list(map(list, zip(*self.comp_spectra)))
        fig, ax = plt.subplots()
        im = ax.imshow(disp_spectra, cmap='viridis')
        ax.set_aspect('auto')
        plt.show(block=True)

    def export_igor(self):
        