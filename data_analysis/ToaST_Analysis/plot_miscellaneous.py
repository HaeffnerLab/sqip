from dataset_factory import *
from functions_plotting import *
from matplotlib import pyplot

pyplot.figure()

temperature_scalings = extract_all_temperature_scalings('postmill8D_electron_heat')
for temperature_scaling in temperature_scalings:
    temperature_scaling.color = get_random_color()
    plot_temperature_scaling(temperature_scaling, plot_smooth = True)

pyplot.legend()


pyplot.figure()

frequency_scalings = extract_all_frequency_scalings('postmill8D_electron_heat', bin_size=10)
plot_alpha_versus_temperature(frequency_scalings)

pyplot.show()