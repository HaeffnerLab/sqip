from _Dataset import Dataset
from functions_import_data import *
from _TemperatureScaling import TemperatureScaling
from _FrequencyScaling import FrequencyScaling

## This dictionary contains immutable properties of the dataset:
##      file name, import function, and temperature calibration
## The functions take as arguments the properties that we want to be able to change easily:
##      max & min temperature, temperature binning window, trap frequency, plot label, plot color
from functions_import_data import import_scraped_temperature_scaling_data

data_root_location = '/Users/Maya/Dropbox/Data_and_Plotting_SQIP/Data/'

dataset_factory_dictionary = {
    # 'name_of_data': (list_of measurements,
    #                  'last_treatment', 'added dose per surface atom', 'cumulative dose per surface atom'),
    'preauger_13June2018' : (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_13Jun2018.txt', 'power5'),
    				'heat', 0, 0),
    'postauger_pre_saturation' : (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_27Jul2018.txt', 'power5')
                                # + import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempScaling_22Aug2018_up.txt', 'iphone')[-5:]
    				,'electron', 0.14, 0.14),
    'baseline_1' : (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempScaling_22Aug2018_up.txt', 'iphone'),
                    'heat', 0, 0.14),
    'baseline_all' : (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempScaling_22Aug2018_up.txt', 'iphone') +
    				  import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempScaling_24Aug2018_down.txt', 'iphone') +
    				  import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempAndFreqScaling_30Aug2018_condensed.txt', 'iphone') +
    				  import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempAndFreqScaling_06sept2018.txt', 'iphone') +
    				  import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempScaling_20sept2018_up.txt', 'iphone') +
    				  import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempScaling_20sept2018_down.txt', 'iphone') +
    				  import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempScaling_24sept2018_down.txt', 'iphone') +
    				  import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempScaling_27sept2018_up.txt', 'iphone') +
    				  import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempAndFreqScaling_08Oct2018.txt', 'iphone'),
                    'heat', 0, 0.14),
    'postmill1_up': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempAndFreqScaling_13dec2018_up.txt', 'iphone'),
    				'mill', 0.48, 0.62),
    'postmill1_down': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_3freqtempscaling_down_Dec172018.txt', 'iphone'),
    				'heat', 0, 0.62),
    'postmill2_up': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_3freqtempscaling_up_Jan152018.txt', 'iphone'),
    				'mill', 0.48, 1.10),
    'postmill2_down': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_3freqtempscaling_down_Jan152018.txt', 'iphone'),
    				'heat', 0, 1.10),
    'postmill3_up': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempAndFreqScaling_18jan2019_up.txt', 'iphone'),
    				'mill', 2.22, 3.32),
    'postmill3_down': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempAndFreqScaling_25jan2019_down.txt', 'iphone'),
    				'heat', 0, 3.32),
    'postmill4_up': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_up_Feb142019.txt', 'iphone'),
    				'mill', 5.65, 8.97),
    'postmill5_up': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempAndFreqScaling_07mar2019_up.txt', 'iphone'),
    				'mill', 18.0, 26.97),
    'postmill5_down': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_TempAndFreqScaling_14mar2019_down.txt', 'iphone'),
    				'heat', 0, 26.97),
    'postmill5_down_repeat': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_08Apr2019.txt', 'android'),
    				'heat', 0, 26.97),
    'postmill6_up': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_hysteresis_10May2019.txt', 'android')[0:40],
    				'mill', 46.5, 73.47),
    'postmill6_down': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_hysteresis_10May2019.txt', 'android')[40:],
    				'heat', 0, 73.47),
    'postmill7_up': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_hysteresis_04Jun2019.txt', 'android_new_lens')[0:17],
    				'mill', 42.3, 115.77),
    'postmill7_down': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_hysteresis_04Jun2019.txt', 'android_new_lens')[27:],
    				'heat', 0, 115.77),
    'postmill7_up_repeat': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_mill7repeat_2019jun18.txt', 'android_new_lens'),
    				'heat', 0, 115.77),
    'postmill8C_up': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_02Jul2019_postmill8c.txt', 'android_new_lens'),
    				'mill', 0.97, 116.74),
    'postmill8D_up': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_09Jul2019_postmill8d.txt', 'android_new_lens'),
    				'mill', 2.65, 119.39),
    'postmill8D_postE8auger': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_11Jul2019_postmill8dandE8Auger.txt', 'android_new_lens'),
    				'contaminate', 0, 119.39),
    'postmill8D_electron': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_16Jul2019_postmill8dandE3Auger.txt', 'android_new_lens')[0:27],
    				'electron', 4.97, 124.36),
    ### add intermediate
    'postmill8D_electron_heat': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_16Jul2019_postmill8dandE3Auger.txt', 'android_new_lens')[53:],
    				'heat', 0, 124.36),
    'postmill8e': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_31Jul2019_postmill8e.txt', 'android_new_lens')[0:14],
    				'mill', 23.8, 148.16),
    'postheat8e': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_31Jul2019_postmill8e.txt', 'android_new_lens')[14:],
    				'heat', 0, 148.16),
    'postelectron8e': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_03Sep2019_postelectronmill8e.txt', None),
    				'electron', 11.50, 159.66),
    'postmill10': (import_handformatted_datafile(data_root_location + 'Data_ToaST/E3_tempscaling_24Sep2019_postmill10.txt', 'android_new_lens'),
    				'mill', 94.2, 253.86) #this really isn't a reasonable set of data
}

def data_to_dataset(dictionary_key,
                            plot_label = None,
                            color = 'black'):
    if not plot_label:
        plot_label = dictionary_key
    if plot_label == 'do_not_label':
        plot_label = None
    measurements, last_treatment, added_dose_per_surface_atom, cumulative_dose_per_surface_atom = dataset_factory_dictionary[dictionary_key]
    dataset = Dataset(measurements, color, plot_label, last_treatment, added_dose_per_surface_atom, cumulative_dose_per_surface_atom)
    return dataset

def data_to_temperature_scaling(dictionary_key,
                            get_frequency = None,
                            scale_to_frequency = None,
                            plot_label = None,
                            color = 'black',
                            marker = 'x',
                            line = '-',
                            temp_min = 0,
                            temp_max = 800,
                            temperature_bin = 1,
                            smooth = True):
    if not plot_label:
        plot_label = dictionary_key
    if plot_label == 'do_not_label':
        plot_label = None
    measurements, last_treatment, added_dose_per_surface_atom, cumulative_dose_per_surface_atom = dataset_factory_dictionary[dictionary_key]
    dataset = Dataset(measurements, color, marker, line, plot_label, last_treatment, added_dose_per_surface_atom, cumulative_dose_per_surface_atom, smooth=smooth)
    if get_frequency and not scale_to_frequency:
        temperature_scaling = TemperatureScaling(dataset.get_single_frequency(get_frequency), get_frequency, dataset)
    if get_frequency and scale_to_frequency:
        temperature_scaling = TemperatureScaling(dataset.get_single_frequency(get_frequency), get_frequency, dataset)
        temperature_scaling.measurements = [measurement.scale_to_frequency(scale_to_frequency) for measurement in temperature_scaling.measurements]
    if scale_to_frequency and not get_frequency:
        measurements = [measurement.scale_to_frequency(scale_to_frequency) for measurement in dataset.measurements]
        temperature_scaling = TemperatureScaling(measurements, scale_to_frequency, dataset)
    return temperature_scaling.get_temperature_subset(temp_min, temp_max).bin_similar_temperatures(temperature_bin)

# def data_to_frequency_scaling(dictionary_key,
#                             get_frequency = None,
#                             scale_to_frequency = None,
#                             plot_label = None,
#                             color = 'black',
#                             marker = 'x',
#                             line = '-',
#                             temp_min = 0,
#                             temp_max = 800,
#                             temperature_bin = 1,
#                             smooth = True):
#     if not plot_label:
#         plot_label = dictionary_key
#     if plot_label == 'do_not_label':
#         plot_label = None
#     measurements, last_treatment, added_dose_per_surface_atom, cumulative_dose_per_surface_atom = dataset_factory_dictionary[dictionary_key]
#     dataset = Dataset(measurements, color, marker, line, plot_label, last_treatment, added_dose_per_surface_atom, cumulative_dose_per_surface_atom, smooth=smooth)
#     if get_frequency and not scale_to_frequency:
#         temperature_scaling = TemperatureScaling(dataset.get_single_frequency(get_frequency), get_frequency, dataset)
#     if get_frequency and scale_to_frequency:
#         temperature_scaling = TemperatureScaling(dataset.get_single_frequency(get_frequency), get_frequency, dataset)
#         temperature_scaling.measurements = [measurement.scale_to_frequency(scale_to_frequency) for measurement in temperature_scaling.measurements]
#     if scale_to_frequency and not get_frequency:
#         dataset.measurements = [measurement.scale_to_frequency(scale_to_frequency) for measurement in dataset.measurements]
#         temperature_scaling = dataset.get_single_frequency(scale_to_frequency)
#     return temperature_scaling.get_temperature_subset(temp_min, temp_max).bin_similar_temperatures(temperature_bin)
#
#


def heat_treatment_mill7(color = 'black', label = 'mill7'):
    filename = data_root_location + 'Data_scraped_for_ToaST/Week_of_06_04_2019_-_temperature_scaling_after_mill_7_2.csv'
    temperature_calibration = 'android_new_lens'
    dataset = Dataset(import_scraped_temperature_scaling_data(filename, temperature_calibration), color = color, label = label)
    return dataset