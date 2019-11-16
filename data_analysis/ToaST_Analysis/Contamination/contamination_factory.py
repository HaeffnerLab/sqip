from Contamination.contamination_import_data import *
from Contamination.ContaminationMeasurementMultiTrapComparison import *

data_root_location = '/Users/Maya/Dropbox/Data_and_Plotting_SQIP/Data/'


def multi_trap_comparison():
    #TODO: correct error given beta could be 2 or 4
    filename = data_root_location + 'Data_ToaST/multiple_untreated_traps.csv'
    measurements = import_multi_trap_comparison_data(filename)
    scaled_measurements = [scale_to_frequency(1.3, scale_to_distance(72, data, beta=2)) for data in measurements]

    scaled_measurements[0].label = 'Trap A'
    scaled_measurements[0].color = 'black'
    scaled_measurements[0].symbol = 'x'
    scaled_measurements[1].label = 'Trap B'
    scaled_measurements[1].color = 'blue'
    scaled_measurements[1].symbol = '.'
    scaled_measurements[2].label = 'Trap C'
    scaled_measurements[2].color = 'red'
    scaled_measurements[2].symbol = 'o'
    scaled_measurements[3].label = 'Trap C'
    scaled_measurements[3].color = 'red'
    scaled_measurements[3].symbol = 'o'

    return scaled_measurements