from dataset_factory import *
from functions_plotting import plot_temperature_scaling

## electron bombardment: marker = "d", line = ':'
## heat: marker = 'x', line = '-'
## electron bombardment: marker = "o", line = '--'


#
# post  bake, electron  bombardment 1 baseline data - scaled to 1 MHz
pyplot.figure()
[('preauger_13June2018','black','x',)]
plot_temperature_scaling(data_to_temperature_scaling('preauger_13June2018',
                                                     get_frequency=1.0, temperature_bin=30,
                                                     color = 'black', marker='x', plot_label='No treatment'), plot_smooth = True)
plot_temperature_scaling(data_to_temperature_scaling('postauger_pre_saturation',
                                                     scale_to_frequency=1.0, temperature_bin=30,
                                                     color = 'maroon', marker='d', plot_label='Electron 1, up'), plot_smooth = True)
plot_temperature_scaling(data_to_temperature_scaling('baseline_all',
                                                     scale_to_frequency=1.0, temperature_bin=30, temp_max=575,
                                                     color = 'red', marker='x', plot_label='Electron 1, post-saturation'), plot_smooth = True)
ax = plot_temperature_scaling(data_to_temperature_scaling('baseline_all',
                                                     scale_to_frequency=1.0, temperature_bin=5, temp_min = 575, temp_max=598,
                                                     color = 'red', marker='--x', plot_label='do_not_label'), plot_smooth = False)
ax.set_ylim(ymin=0)
pyplot.legend()

# Mill (0, 1, 2, 3, 4) all heat up and down - scaled to 1 MHz
pyplot.figure()
plot_temperature_scaling(data_to_temperature_scaling('baseline_all',
                                                     scale_to_frequency=1.0, temperature_bin=30, temp_max=575,
                                                     color = 'red', marker='x', plot_label='Electron 1, post-saturation'), plot_smooth = True)
plot_temperature_scaling(data_to_temperature_scaling('baseline_all',
                                                     scale_to_frequency=1.0, temperature_bin=5, temp_min = 575, temp_max=598,
                                                     color = 'red', marker='--x', plot_label='do_not_label'), plot_smooth = False)
plot_temperature_scaling(data_to_temperature_scaling('postmill1_up',
                                                     scale_to_frequency=1.0, temperature_bin=30, temp_max=590,
                                                     color = 'orange', marker='o', plot_label='Mill 1, up'), plot_smooth = True)
# #This shootoff data was taken at 2 MHz only, not sure if it can be legitimately scaled to 1 MHz, since alpha is unclear here
# plot_temperature_scaling(data_to_temperature_scaling('postmill1_up',
#                                                      scale_to_frequency=1.0, temperature_bin=5, temp_min = 590,
#                                                      color = 'orange', marker='-x', plot_label='Mill 1, post-saturation'), plot_smooth = False)
plot_temperature_scaling(data_to_temperature_scaling('postmill1_down',
                                                     scale_to_frequency=1.0, temperature_bin=30,
                                                     color = 'orange', marker='x', plot_label='Mill 1, down'), plot_smooth = True)
plot_temperature_scaling(data_to_temperature_scaling('postmill2_up',
                                                     scale_to_frequency=1.0, temperature_bin=30, temp_max = 573,
                                                     color = 'gold', marker='o', plot_label='Mill 2, up'), plot_smooth = True)
plot_temperature_scaling(data_to_temperature_scaling('postmill2_up',
                                                     get_frequency = 1.3, scale_to_frequency=1.0, temperature_bin=5, temp_min = 565,
                                                     color = 'gold', marker='--o', plot_label='do_not_label'), plot_smooth = False)
plot_temperature_scaling(data_to_temperature_scaling('postmill2_down',
                                                     scale_to_frequency=1.0, temperature_bin=30,
                                                     color = 'gold', marker='x', plot_label='Mill 2, down'), plot_smooth = True)
plot_temperature_scaling(data_to_temperature_scaling('postmill3_up',
                                                     scale_to_frequency=1.0, temperature_bin=30, temp_max = 576,
                                                     color = 'green', marker='o', plot_label='Mill 3, up'), plot_smooth = True)
plot_temperature_scaling(data_to_temperature_scaling('postmill3_up',
                                                     scale_to_frequency=1.0, temperature_bin=5, temp_min = 576,
                                                     color = 'green', marker='--o', plot_label='do_not_label'), plot_smooth = False)
ax = plot_temperature_scaling(data_to_temperature_scaling('postmill3_down',
                                                     scale_to_frequency=1.0, temperature_bin=30,
                                                     color = 'green', marker='x', plot_label='Mill 3, down'), plot_smooth = True)
# ax = plot_temperature_scaling(data_to_temperature_scaling('postmill5_up',
#                                                      scale_to_frequency=1.0, temperature_bin=30, temp_max = 575,
#                                                      color = 'blue', marker='o', plot_label='Mill 5, up'), plot_smooth = True)
ax.set_ylim(ymin=0)
pyplot.legend()


# Mill 5, 6, 7repeat. heat up and down.
pyplot.figure()
plot_temperature_scaling(data_to_temperature_scaling('postmill5_up',
                                                     scale_to_frequency=1.0, temperature_bin=1, temp_max = 560,
                                                     color = 'blue', marker='o', plot_label='Mill 5, up'), plot_smooth = True)
ax = plot_temperature_scaling(data_to_temperature_scaling('postmill5_down_repeat',
                                                     scale_to_frequency=1.0, temperature_bin=30, temp_max = 560,
                                                     color = 'blue', marker='x', plot_label='Mill 5, post-saturation'), plot_smooth = True)
ax.set_ylim(ymin=0, ymax=12)
pyplot.legend()
pyplot.figure()
plot_temperature_scaling(data_to_temperature_scaling('postmill6_up',
                                                     scale_to_frequency=1.0, temperature_bin=28, temp_max = 580,
                                                     color = 'purple', marker='o', plot_label='Mill 6, up'), plot_smooth = True)
ax=plot_temperature_scaling(data_to_temperature_scaling('postmill6_down',
                                                     scale_to_frequency=1.0, temperature_bin=30, #temp_max = 560,
                                                     color = 'purple', marker='x', plot_label='Mill 6, post-saturation'), plot_smooth = True)
ax.set_ylim(ymin=0, ymax=12)
pyplot.legend()
pyplot.figure()
plot_temperature_scaling(data_to_temperature_scaling('postmill7_up',
                                                     scale_to_frequency=1.0, temperature_bin=30, temp_max = 560,
                                                     color = 'magenta', marker='o', plot_label='Mill 7, up'), plot_smooth = True)
ax = plot_temperature_scaling(data_to_temperature_scaling('postmill7_up_repeat',
                                                     scale_to_frequency=1.0, temperature_bin=30, temp_max = 560,
                                                     color = 'magenta', marker='x', plot_label='Mill 7, post-saturation'), plot_smooth = True)
ax.set_ylim(ymin=0, ymax=12)
pyplot.legend()

# Mill 7down, 8c, 8d,
# Electron  bombardment  2 + heat,
# Mill 8 e + heat maybe
# Electron bom-bardment  3 + heat maybe

pyplot.figure()
plot_temperature_scaling(data_to_temperature_scaling('postmill7_up_repeat',
                                                     scale_to_frequency=1.0, temperature_bin=30, #temp_max = 560,
                                                     color = 'magenta', marker='x', plot_label='Mill 7, post-saturation'), plot_smooth = True)
plot_temperature_scaling(data_to_temperature_scaling('postmill8C_up',
                                                     scale_to_frequency=1.0, temperature_bin=30, #temp_max = 560,
                                                     color = 'orange', marker='o', plot_label='Mill 8c'), plot_smooth = True)
plot_temperature_scaling(data_to_temperature_scaling('postmill8D_up',
                                                     scale_to_frequency=1.0, temperature_bin=30, #temp_max = 560,
                                                     color = 'green', marker='o', plot_label='Mill 8d'), plot_smooth = True)
plot_temperature_scaling(data_to_temperature_scaling('postmill8D_electron',
                                                     scale_to_frequency=1.0, temperature_bin=30, temp_max = 560,
                                                     color = 'teal', marker='d', plot_label='Mill 8d + Electron 2 up'), plot_smooth = True)
ax = plot_temperature_scaling(data_to_temperature_scaling('postmill8D_electron',
                                                     scale_to_frequency=1.0, temperature_bin=30, temp_min = 560,
                                                     color = 'teal', marker='--d', plot_label='do_not_label', smooth=False))
ax.set_ylim(ymin=0)
pyplot.legend()

pyplot.figure()
plot_temperature_scaling(data_to_temperature_scaling('postmill8D_up',
                                                     get_frequency = 1.3, temperature_bin=30, temp_max = 490,
                                                     color = 'magenta', marker='o', plot_label='before auger contamination'), plot_smooth = True)
ax = plot_temperature_scaling(data_to_temperature_scaling('postmill8D_postE8auger',
                                                     get_frequency = 1.3, temperature_bin=30, temp_max = 450,
                                                     color = 'purple', marker='.', plot_label='after auger contamination'), plot_smooth = True)
# measurement from July 15, 2019
ax.errorbar(295, 1.54, yerr=0.07, color = 'orange', marker = 'x')

pyplot.legend()

# pyplot.show()

pyplot.figure()
plot_temperature_scaling(data_to_temperature_scaling('postmill8D_electron',
                                                     scale_to_frequency=1.0, temperature_bin=30, temp_max = 560,
                                                     color = 'teal', marker='d', plot_label='Mill 8d + Electron 2 up'), plot_smooth = True)
ax = plot_temperature_scaling(data_to_temperature_scaling('postmill8D_electron_heat',
                                                     scale_to_frequency=1.0, temperature_bin=30, #temp_max = 560,
                                                     color = 'teal', marker='x', plot_label='Electron 2, post-saturation'), plot_smooth = True)
ax.set_ylim(ymin=0, ymax=12)
pyplot.legend()

## electron 2 heated, mill 8e + heat, electron 3
pyplot.figure()
plot_temperature_scaling(data_to_temperature_scaling('postmill8D_electron_heat',
                                                     scale_to_frequency=1.0, temperature_bin=30, #temp_max = 560,
                                                     color = 'teal', marker='x', plot_label='Electron 2, post-saturation'), plot_smooth = True)
plot_temperature_scaling(data_to_temperature_scaling('postmill8e',
                                                     scale_to_frequency=1.0, temperature_bin=30, #temp_max = 560,
                                                     color = 'blue', marker='o', plot_label='Mill 8e up'), plot_smooth = True)
ax = plot_temperature_scaling(data_to_temperature_scaling('postelectron8e',
                                                     scale_to_frequency=1.0, temperature_bin=30, #temp_max = 560,
                                                     color = 'black', marker='d', plot_label='Mill 8e + Electron 3'), plot_smooth = True)
ax.set_ylim(ymin=0)
pyplot.legend()

## mill 8e + heat
pyplot.figure()
plot_temperature_scaling(data_to_temperature_scaling('postmill8e',
                                                     scale_to_frequency=1.0, temperature_bin=30, #temp_max = 560,
                                                     color = 'blue', marker='o', plot_label='Mill 8e up'), plot_smooth = True)
ax = plot_temperature_scaling(data_to_temperature_scaling('postheat8e',
                                                     scale_to_frequency=1.0, temperature_bin=30, #temp_max = 560,
                                                     color = 'navy', marker='x', plot_label='Mill 8e, down'), plot_smooth = True)
ax.set_ylim(ymin=0, ymax=12)
pyplot.legend()




pyplot.show()