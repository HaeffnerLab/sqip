from TemperatureScaling import *
from Measurement import *

class Dataset:

    def __init__(self, measurements, color='black', marker='o', line = '-', label='', last_treatment='', added_dose=0, cumulative_dose=0, smooth=True):
        # data is a list of heating rate objects that all correspond to the same temperature treatment dataset
        # test
        self.measurements = measurements
        # self.smoothing_function = univariate_spline
        self.smoothing_function = second_order_polynomial
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
        single_frequency_data = []
        for measurement in self.measurements:
            if frequency - bin_size/2 <= measurement.trap_frequency <= frequency + bin_size/2:
                scaled_data = measurement.scale_to_frequency(frequency)
                single_frequency_data.append(scaled_data)
        return TemperatureScaling(single_frequency_data, frequency, self)

    def get_relative_times_day(self):
        measurement_end_times_hrs = [times[-1] for times in self.times_in_hours]
        # measurement_end_times_hrs = self.times_in_hours
        # if not self.start_time:
        #     start_time = min(measurement_end_times_hrs)
        # starting_hour = start_time + self.offset_hours
        relative_times_day = [(time - self.start_time + self.offset_hours) / 24 for time in measurement_end_times_hrs]
        return relative_times_day

    def bin_each_day(self):
        #TODO make sure added properties aren't deleted deepcopy
        data_averaged = [] # list of heating rate objects
        measurement_days = []
        for day in self.dates:
            if day not in measurement_days: measurement_days.append(day)

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

def plot_heat_treatment(datasets):
    pyplot.figure()
    ax = pyplot.axes(xscale='linear', yscale='linear')
    pyplot.xlabel('Time(days)')
    pyplot.ylabel('Temperature(K)')
    pyplot.title('Heat Treatment Post Mill 7')

    for dataset in datasets:
        ax.plot(dataset.get_relative_times_day(), dataset.temperatures, color=dataset.color, label = dataset.label, linewidth=.5)


