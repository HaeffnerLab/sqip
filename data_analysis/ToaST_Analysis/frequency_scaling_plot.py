from matplotlib import pyplot
from frequency_scaling_functions import *
#TODO: rewrite for clarity and consistency with rest of code base

pyplot.figure()
ax = pyplot.axes(xscale='log',yscale='log')
pyplot.title('Frequency scaling room temperature')
pyplot.ylabel('frequency (MHz)')
pyplot.xlabel('heting rate (nbar/ms)')

plot_freq_scaling(ax,'/Users/Maya/Dropbox/Data_and_Plotting_SQIP/Data/Data_ToaST/E3_freqscaling_RT_Nov052019.txt',1,'label','black')

pyplot.show()