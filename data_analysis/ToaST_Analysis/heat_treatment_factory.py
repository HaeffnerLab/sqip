from Dataset import *
from import_data import *

data_root_location = '/Users/Maya/Dropbox/Data_and_Plotting_SQIP/Data/'


def heat_treatment_mill7(color = 'black', label = 'mill7'):
    filename = data_root_location + 'Data_scraped_for_ToaST/Week_of_06_04_2019_-_temperature_scaling_after_mill_7_2.csv'
    temperature_calibration = 'android_new_lens'
    dataset = Dataset(import_scraped_temperature_scaling_data(filename, temperature_calibration), color = color, label = label)
    return dataset

