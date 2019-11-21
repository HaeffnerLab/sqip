import numpy as np
from _Measurement import Measurement
from functions_fitting import *


class Dataset:

    def __init__(self, measurements, color='black', marker='o', line = '-', label='', last_treatment='', added_dose=0, cumulative_dose=0, smooth=True):
        # data is a list of heating rate objects that all correspond to the same temperature treatment dataset
        # test
        self.measurements = measurements
        # self.smoothing_function = univariate_spline
        self.smoothing_function = fit_second_order_polynomial
        # self.smoothing_function = third_order_polynomial
        self.color = color
        self.label = label
        self.last_treatment = last_treatment
        self.added_dose = added_dose
        self.cumulative_dose = cumulative_dose
        self.marker = marker
        self.line = line
        self.smooth = smooth

        self.trap_frequencies = [measurement.trap_frequency for measurement in measurements]
        self.dates = [measurement.date for measurement in measurements]
        self.temperatures = [measurement.temperature for measurement in measurements]
        self.heatingrates = [measurement.heatingrate for measurement in measurements]
        self.heatingrate_errors = [measurement.heatingrate_error for measurement in measurements]
        self.times_in_hours = [measurement.times_in_hours for measurement in measurements]

        self.offset_hours = 0

        if self.times_in_hours[0]:
            self.start_time = min([times[0] for times in self.times_in_hours])

    def get_single_frequency(self, frequency, bin_size=.1):
        single_frequency_measurements = []
        for measurement in self.measurements:
            if frequency - bin_size/2 <= measurement.trap_frequency <= frequency + bin_size/2:
                scaled_measurement = measurement.scale_to_frequency(frequency)
                single_frequency_measurements.append(scaled_measurement)
        return single_frequency_measurements


    def get_single_temperature(self, temperature_bin):
        single_temperature_data = []
        for measurement in self.measurements:
            if in_bin(measurement.temperature, temperature_bin):
                single_temperature_data.append(measurement)
        return single_temperature_data


    def get_relative_times_day(self):
        measurement_end_times_hrs = [times[-1] for times in self.times_in_hours]
        # measurement_end_times_hrs = self.times_in_hours
        # if not self.start_time:
        #     start_time = min(measurement_end_times_hrs)
        # starting_hour = start_time + self.offset_hours
        relative_times_day = [(time - self.start_time + self.offset_hours) / 24 for time in measurement_end_times_hrs]
        return relative_times_day

    def bin_by_day(self):
        data_averaged = [] # list of heating rate objects
        measurement_days = sorted(set(self.dates))

        for day in measurement_days:
            data_to_average = []
            for measurement in self.measurements:
                if measurement.date == day:
                    data_to_average.append(measurement)
            if data_to_average:
                # add new heating rate object to new data list
                averaged_measurement = average_data(data_to_average)
                data_averaged.append(averaged_measurement)

        binned_dataset = Dataset(data_averaged, color=self.color, label=self.label, last_treatment=self.last_treatment, added_dose=self.added_dose, cumulative_dose=self.cumulative_dose)

        return binned_dataset


def get_measured_frequencies(measurements):
    measured_frequencies = set([measurement.trap_frequency for measurement in measurements])
    return measured_frequencies


def get_measured_temperatures(measurements):
    measured_frequencies = set([measurement.temperature for measurement in measurements])
    return measured_frequencies


def get_linetype(last_treatment):
    linetype = {
	"electron_bombardment" : ':',
    "heating" : '-',
    "argon_milling" : '--'
	}
    return linetype.get(last_treatment)


def average_data(measurements):
    heatingrates = [measurement.heatingrate for measurement in measurements]
    heatingrate_errors = [measurement.heatingrate_error for measurement in measurements]
    temperatures = [measurement.temperature for measurement in measurements]
    frequencies = [measurement.trap_frequency for measurement in measurements]

    heatingrate_average = weighted_average(heatingrates, heatingrate_errors).nominal_value
    heatingrate_error_average = weighted_average(heatingrates, heatingrate_errors).std_dev
    temperature_average = weighted_average(temperatures, heatingrate_errors).nominal_value
    frequency_average = weighted_average(frequencies, heatingrate_errors).nominal_value

    data_averaged = Measurement()
    data_averaged.heatingrate = heatingrate_average
    data_averaged.heatingrate_error = heatingrate_error_average
    data_averaged.temperature = temperature_average
    data_averaged.trap_frequency = frequency_average

    if measurements[0].times_in_hours:
        times = [measurement.times_in_hours[-1] for measurement in measurements]
        time_average = weighted_average(times, heatingrate_errors).nominal_value
        data_averaged.times_in_hours = [time_average]

    return data_averaged


def make_bins(list, bin_size, temperature_scaling=False):
    #TODO: make bins in a more sophisticated way. If a bin is empty, start the next bin at the next datapoint?
    if temperature_scaling:
        bins = [(290, 304)] # first bin is always room temperature
        bottom_of_bin = max(min(list), 304)
    else:
        bins = []
        bottom_of_bin = min(list)

    while bottom_of_bin < max(list):
        top_of_bin = bottom_of_bin + bin_size
        bins.append((bottom_of_bin, top_of_bin))
        bottom_of_bin = top_of_bin
    return bins

def in_bin(value, bin):
    if min(bin) <= value < max(bin):
        return True
    else:
        return False