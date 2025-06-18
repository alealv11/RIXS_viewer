                  ---README---
---This code was made by Alejandro Álvarez-Chico---

<b>Description:</b>\
RIXS viewer is a code that reads and displays RIXS data from the VERITAS beamline in MAX IV.\
It also provides thermal drift correction of the data.\\

<b>Usage:</b>\
1. Clone the repository to your machine and open rixs_plotter.py.\\
2. Change the path to where your rixs data is stored.\\
3. In the FileCaller class line change the numbers for your first and last spectrum number.\\
4. To rectify the data there is currently three methods:\
a. Linear rectifier: Rectifies thermal drift substracting a line.\
b. Maxima rectifier: Tries to align the maxima of the elastic peak. You can also pass a number to\
"cut" from where it starts searching the maxima as to not get spureous secondary peaks.\
c. Manual rectifier: Self explanatory. To use this pass the spectra_rectifier method a column number\
and the number of data points you want to move.\\
5. To plot just call the spectra_rectifier method with plot_switch=True anytime.


