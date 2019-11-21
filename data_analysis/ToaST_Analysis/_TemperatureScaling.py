from _Dataset import average_data, make_bins
import numpy as np

class TemperatureScaling:

    def __init__(self, measurements, dataset):

        self.measurements = measurements
        self.dataset = dataset
        self.trap_frequency = self.get_average_frequency()
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


    def get_average_frequency(self):
        return average_data(self.measurements).trap_frequency


    def bin_similar_temperatures(self, temperature_bin_size):
        if not self.measurements:
            return self
        data_averaged = [] # list of heating rate objects
        for bin_min, bin_max in make_bins(self.temperatures, temperature_bin_size, temperature_scaling = True):
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

        binned_temperature_scaling = TemperatureScaling(data_averaged, self.dataset)

        return binned_temperature_scaling


    def get_temperature_subset(self, temp_min, temp_max):
        measurement_subset = [measurement for measurement in self.measurements
            if temp_min <= measurement.temperature <= temp_max]
        temperature_scaling_subset = TemperatureScaling(measurement_subset, self.dataset)
        return temperature_scaling_subset

