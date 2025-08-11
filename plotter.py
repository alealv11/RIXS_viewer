import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    """Makes the plots of the rixs based on a list of lists input"""
    def __init__(self, comp_spectra):
        """Initialize class arguments"""
        self.comp_spectra = comp_spectra
        # Transposes the list of lists by dark magic. 
        # https://stackoverflow.com/questions/6473679/transpose-list-of-lists
        self.disp_spectra = list(map(list, zip(*self.comp_spectra)))
        self.fig, self.ax = plt.subplots()
        self.xlim = []
        self.ylim = []




    def show_plots(self):
        """Displays the plots in a readable and well oriented way."""
        im = self.ax.imshow(self.disp_spectra, cmap='viridis')
        self.ax.set_aspect('auto')
        if self.xlim:
            plt.xlim(xlim)
        if self.ylim:
            plt.xlim(ylim)
        plt.show(block=True)


    def reescale_loss(self, step, elastic_position):
        """
        Reescales the energy loss using the step and the approximate position
        of the elastic peak.
        """
        elastic = np.argmax(self.disp_spectra)
        print(elastic)


