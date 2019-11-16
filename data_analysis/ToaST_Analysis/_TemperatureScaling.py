from _Dataset import *
from _Measurement import *

class TemperatureScaling:

    def __init__(self, measurements, trap_frequency, dataset):

        self.measurements = measurements
        self.dataset = dataset
        self.trap_frequency = trap_frequency
        self.color = dataset.color
        self.marker = dataset.marker
        self.line = dataset.line

        if dataset.label:
            # self.label = dataset.label + ' (' + str(self.trap_frequency) + ' MHz)'
            self.label = dataset.label
        else:
            self.label = None

        self.heatingrates = [measurement.heatingrate for measurement in measurements]
        self.heatingrate_errors = [measurement.heatingrate_error for measurement in measurements]
        self.temperatures = [measurement.temperature for measurement in measurements]

        # Temperature and smoothed heating rate
        if self.temperatures and self.dataset.smooth == True:
            self.temperatures_smooth, self.heatingrates_smooth = dataset.smoothing_function(self.temperatures, self.heatingrates, self.heatingrate_errors)


    def get_rate_at_nearest_temperature(self, temperature):
        index = np.argmin(np.abs(self.temperatures_smooth - temperature))
        return self.heatingrates_smooth[index]


    def bin_similar_temperatures(self, temperature_bin_size):
        if not self.measurements:
            return self
        data_averaged = [] # list of heating rate objects
        for bin_min, bin_max in make_bins(self.temperatures, temperature_bin_size):
            data_to_average = []

            for measurement in self.measurements:
                if bin_min <= measurement.temperature <= bin_max:
                    data_to_average.append(measurement)

            if data_to_average:
                new_data = average_data(data_to_average)
                # make sure room temp measurements are all the same temp
                if bin_min == 290:
                    new_data.temperature = 295
                # add new heating rate object to new data list
                data_averaged.append(new_data)

        binned_temperature_scaling = TemperatureScaling(data_averaged, self.trap_frequency, self.dataset)

        return binned_temperature_scaling


    def get_temperature_subset(self, temp_min, temp_max):
        #TODO make sure added properties aren't deleted using deepcopy(object)
        measurement_subset = [measurement for measurement in self.measurements
                       if temp_min <= measurement.temperature <= temp_max]
        temperature_scaling_subset = TemperatureScaling(measurement_subset, self.trap_frequency, self.dataset)
        return temperature_scaling_subset


def make_bins(list, bin_size):
    bins = [(290, 304)] # first bin is always room temperature
    bottom_of_bin = max(min(list), 306)
    while bottom_of_bin < max(list):
        top_of_bin = bottom_of_bin + bin_size
        bins.append((bottom_of_bin, top_of_bin))
        bottom_of_bin = top_of_bin
    return bins


def extract_all_temperature_scalings(Dataset):
    #TODO: fill in
    return