from file_caller import FileCaller
from drift_rectifier import DriftRectifier

path = 'C:/Path/to/your/folder/20250524_DLD1 (1).h5'


#Make the measurement object from the path and the starting and ending spectra.
spectra = DriftRectifier(path,749,775)

#Function to cut bad data.
spectra.cut_and_paste(5,54)

#Function that rectifies the thermal drift. The optional argument is to 
#put the minimum value of y axis from where to look, as the function doest
#distinguish between maximums and sometimes can correct to other maxima that
#is not the elastic.
spectra.maxima_rectifier(4300)

#Function that rectifies the thermal drift by substracting a linear function.
#Has the same problem of detecting bad maxima sometimes.
spectra.linear_rectifier()

#Function that exports to a CSV the data.
spectra.export_igor(path)