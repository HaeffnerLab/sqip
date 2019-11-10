from temperature_scaling_factory import *

## electron bombardment: marker = "d", line = ':'
## heat: marker = 'x', line = '-'
## electron bombardment: marker = "o", line = '--'

### Plot treatment summary:

all_temperature_scalings = [
    data_to_temperature_scaling('preauger_13June2018', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postauger_pre_saturation', scale_to_frequency=1.0, temperature_bin=30, marker='d', line=':'),
    data_to_temperature_scaling('baseline_all', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postmill1_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    data_to_temperature_scaling('postmill1_down', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postmill2_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    data_to_temperature_scaling('postmill2_down', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postmill3_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    data_to_temperature_scaling('postmill3_down', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postmill5_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    data_to_temperature_scaling('postmill5_down_repeat', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postmill6_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    data_to_temperature_scaling('postmill6_down', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postmill7_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    data_to_temperature_scaling('postmill7_up_repeat', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postmill8C_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    data_to_temperature_scaling('postmill8D_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    data_to_temperature_scaling('postmill8D_electron', scale_to_frequency=1.0, temperature_bin=30, marker='d', line=':'),
    data_to_temperature_scaling('postmill8D_electron_heat', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postmill8e', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    data_to_temperature_scaling('postheat8e', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postelectron8e', scale_to_frequency=1.0, temperature_bin=30, marker='d', line=':'),
    # data_to_temperature_scaling('postmill10', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='-.')
]
temperature_scalings_without_most_heatings = [
    data_to_temperature_scaling('preauger_13June2018', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    # data_to_temperature_scaling('postauger_pre_saturation', scale_to_frequency=1.0, temperature_bin=30, marker='d', line=':'),
    data_to_temperature_scaling('baseline_all', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postmill1_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    # data_to_temperature_scaling('postmill1_down', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postmill2_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    # data_to_temperature_scaling('postmill2_down', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postmill3_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    # data_to_temperature_scaling('postmill3_down', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postmill5_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    # data_to_temperature_scaling('postmill5_down_repeat', scale_to_frequency=1.0, temperature_bin=30, marker='x'),
    data_to_temperature_scaling('postmill6_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    # data_to_temperature_scaling('postmill6_down', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postmill7_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    # data_to_temperature_scaling('postmill7_up_repeat', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postmill8C_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    data_to_temperature_scaling('postmill8D_up', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    data_to_temperature_scaling('postmill8D_electron', scale_to_frequency=1.0, temperature_bin=30, marker='d', line=':'),
    # data_to_temperature_scaling('postmill8D_electron_heat', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postmill8e', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='--'),
    # data_to_temperature_scaling('postheat8e', scale_to_frequency=1.0, temperature_bin=30, marker='x', line='-'),
    data_to_temperature_scaling('postelectron8e', scale_to_frequency=1.0, temperature_bin=30, marker='d', line=':'),
    # data_to_temperature_scaling('postmill10', scale_to_frequency=1.0, temperature_bin=30, marker='o', line='-.')
]


# plot_cumulative_dose(temperature_scalings_without_most_heatings, plot_295K=True, label=[0,1,3])
# plot_cumulative_dose(temperature_scalings_without_most_heatings, plot_500K=True, label=[0,1,3])
# plot_cumulative_dose(temperature_scalings_without_most_heatings, plot_500K=True, plot_295K=True, label=[0,1,3])
# plot_added_dose(temperature_scalings_without_most_heatings)


plot_cumulative_dose(all_temperature_scalings, plot_295K=True, label=[0,1,3])
plot_cumulative_dose(all_temperature_scalings, plot_500K=True, label=[0,1,3])
plot_cumulative_dose(all_temperature_scalings, plot_500K=True, plot_295K=True, label=[0,1,3])
plot_added_dose(all_temperature_scalings)


pyplot.show()