from matplotlib import pyplot
#TODO: rewrite for clarity and consistency with rest of code base
from functions_plotting import plot_freq_scaling

pyplot.figure()
ax = pyplot.axes(xscale='log',yscale='log')
pyplot.title('Frequency scaling room temperature')
pyplot.xlabel('frequency (MHz)')
pyplot.ylabel('heating rate (nbar/ms)')

plot_freq_scaling(ax,'/Users/Maya/Dropbox/Data_and_Plotting_SQIP/Data/Data_ToaST/E3_freqscaling_RT_Nov052019.txt',1,'RT','black')


pyplot.figure()
ax = pyplot.axes(xscale='log',yscale='log')
pyplot.title('Frequency scaling shoot-off')
pyplot.xlabel('frequency (MHz)')
pyplot.ylabel('heating rate (nbar/ms)')

plot_freq_scaling(ax,'/Users/Maya/Dropbox/Data_and_Plotting_SQIP/Data/Data_ToaST/E3_freqscaling_shootoff_Nov082019.txt',1,'shootoff','black')




pyplot.show()