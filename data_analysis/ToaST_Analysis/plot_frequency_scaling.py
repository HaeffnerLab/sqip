from matplotlib import pyplot
from functions_plotting import plot_frequency_scaling
from dataset_factory import data_to_frequency_scaling


pyplot.figure()
frequency_scaling = data_to_frequency_scaling('mill10_hot_freqscaling')
plot_frequency_scaling(frequency_scaling, plot_fit = True)
print("alpha = " + str(frequency_scaling.get_alpha()))


pyplot.figure()
frequency_scaling = data_to_frequency_scaling('mill10_RT_freqscaling')
plot_frequency_scaling(frequency_scaling, plot_fit = True)
print("alpha = " + str(frequency_scaling.get_alpha()))


pyplot.show()