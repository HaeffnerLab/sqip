from _Dataset import average_data, make_bins
from functions_fitting import fit_exponential, exponential
import numpy as np

class FrequencyScaling:

    def __init__(self, measurements, dataset):

        self.measurements = measurements
        self.dataset = dataset
        self.temperature = self.get_average_temperature()

        self.heatingrates = [measurement.heatingrate for measurement in measurements]
        self.heatingrate_errors = [measurement.heatingrate_error for measurement in measurements]
        self.frequencies = [measurement.trap_frequency for measurement in measurements]

        self.color = dataset.color
        self.marker = dataset.marker
        self.line = dataset.line

        if dataset.label:
            self.label = dataset.label + ' (' + str(self.temperature) + ' (K)'
            self.label = dataset.label
        else:
            self.label = None


    def get_frequency_subset(self, freq_min, freq_max):
        measurement_subset = [measurement for measurement in self.measurements
                                if freq_min <= measurement.trap_frequency <= freq_max]
        frequency_scaling_subset = FrequencyScaling(measurement_subset, self.dataset)
        return frequency_scaling_subset


    def get_average_temperature(self):
        return average_data(self.measurements).temperature


    def bin_similar_frequencies(self, frequency_bin_size = 0.05):
        if not self.measurements:
            return self
        data_averaged = [] # list of measurement objects
        for bin_min, bin_max in make_bins([.1, 10], frequency_bin_size):
            data_to_average = []

            for measurement in self.measurements:
                if bin_min <= measurement.trap_frequency <= bin_max:
                    data_to_average.append(measurement)

            if data_to_average:
                # add averaged measurement object to new data list
                data_averaged.append(average_data(data_to_average))

        binned_frequency_scaling = FrequencyScaling(data_averaged, self.dataset)

        return binned_frequency_scaling

    def get_alpha(self):
        frequency_scaling_binned = self.bin_similar_frequencies()
        frequencies_binned = frequency_scaling_binned.frequencies
        heatingrates_binned = frequency_scaling_binned.heatingrates
        heatingrate_errors_binned = frequency_scaling_binned.heatingrate_errors

        amplitude, exponent = fit_exponential(frequencies_binned, heatingrates_binned, heatingrate_errors_binned)

        return exponent - 1

    def get_amplitude(self):
        frequency_scaling_binned = self.bin_similar_frequencies()
        frequencies_binned = frequency_scaling_binned.frequencies
        heatingrates_binned = frequency_scaling_binned.heatingrates
        heatingrate_errors_binned = frequency_scaling_binned.heatingrate_errors

        amplitude, exponent = fit_exponential(frequencies_binned, heatingrates_binned, heatingrate_errors_binned)

        return amplitude

    def get_frequencies_fit(self):
        return np.linspace(min(self.frequencies), max(self.frequencies), num=300)

    def get_heatingrates_fit(self):
        heatingrates_fit = [exponential(freq, self.get_amplitude().nominal_value, self.get_alpha().nominal_value+1)
                                 for freq in self.get_frequencies_fit()]
        return heatingrates_fit