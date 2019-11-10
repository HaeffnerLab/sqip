import numpy as np
from Measurement import *
from scipy.interpolate import UnivariateSpline
from matplotlib import pyplot

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
        self.linetype = get_linetype(dataset.last_treatment)

        self.heatingrates = [measurement.heatingrate for measurement in measurements]
        self.heatingrate_errors = [measurement.heatingrate_error for measurement in measurements]
        self.temperatures = [measurement.temperature for measurement in measurements]

        # Temperature and smoothed heating rate
        if self.temperatures and self.dataset.smooth == True:
            self.temperatures_smooth, self.heatingrates_smooth = dataset.smoothing_function(self.temperatures, self.heatingrates, self.heatingrate_errors)

        # TODO
        # #collect data from tempscaling files, convert to temperature, calculate TAF dist, smooth, calc alpha prediction
        # self.Vb,self.d_ebar = calc_dist(self.temperature,self.rate,self.rateerror,self.trapfreq)
        # self.Vb_smooth, self.d_ebar_smooth = calc_dist(self.T_smooth,self.rates_smooth,self.rates_smooth*0,self.trapfreq)
        #
        # # myfiterr = 0
        # self.smoothT_predict,self.smoothalpha_predict = direct_alpha(self.T_smooth,self.rates_smooth,self.trapfreq) # This is the alpha prediction from the smoothed slope
        # self.roughT_predict,self.roughalpha_predict = direct_alpha(self.temperature,self.rate,self.trapfreq)  # This is the alpha prediction from the raw slope
        #

    def get_rate_at_nearest_temperature(self, temperature):
        index = np.argmin(np.abs(self.temperatures_smooth - temperature))
        return self.heatingrates_smooth[index]

    def scale_temperature_scaling_to_frequency(self, new_frequency):
        #TODO make sure added characteristics aren't deleted
        scaled_data = []
        for measurement in self.measurements:
            scaled_data.append(measurement.scale_to_frequency(new_frequency, alpha = 1))

        scaled_temperature_scaling = TemperatureScaling(scaled_data, self.trap_frequency, self.dataset)
        return scaled_temperature_scaling

    def bin_similar_temperatures(self, temperature_bin_size):
        #TODO make sure added properties aren't deleted deepcopy
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

def average_data(measurements):
    heatingrates = [measurement.heatingrate for measurement in measurements]
    heatingrate_errors = [measurement.heatingrate_error for measurement in measurements]
    temperatures = [measurement.temperature for measurement in measurements]

    weights = [error**-2 for error in heatingrate_errors]

    heatingrate_average = np.sum(np.multiply(heatingrates,weights))/np.sum(weights)
    heatingrate_error_average = np.sqrt(1/np.sum(weights)) 
    temperature_average = np.sum(np.multiply(temperatures,weights))/np.sum(weights)

    data_averaged = Measurement()
    data_averaged.heatingrate = heatingrate_average
    data_averaged.heatingrate_error = heatingrate_error_average
    data_averaged.temperature = temperature_average
    data_averaged.trap_frequency = measurements[0].trap_frequency

    if measurements[0].times_in_hours:
        times = [measurement.times_in_hours[-1] for measurement in measurements]
        time_average = np.sum(np.multiply(times,weights))/np.sum(weights)
        data_averaged.times_in_hours = [time_average]

    return data_averaged


def get_linetype(last_treatment):
    linetype = {
	"electron_bombardment" : ':',
    "heating" : '-',
    "argon_milling" : '--'
	}
    return linetype.get(last_treatment)

def univariate_spline(x_input, y_input, y_errors):
    weights = [1 / err for err in y_errors]
    bbox = [min(x_input), max(y_input)]
    # bbox = [0,800]
    smoothingpolynomial = 2
    numberofknots = 100
    uspline = UnivariateSpline(x_input, y_input, weights, k=smoothingpolynomial, s=numberofknots, ext=1, bbox=bbox)
    x_output = np.arange(min(x_input), max(x_input), 1)
    return x_output, uspline(x_output)

def second_order_polynomial(x_input, y_input, y_errors):
    weights = [1 / err ** 2 for err in y_errors]
    # returns polynomial coefficients ordered from low to high:
    po, p1, p2 = np.polynomial.polynomial.polyfit(x_input, y_input, deg=2, rcond=None, full=False, w=weights)
    x_output = np.arange(min(x_input), max(x_input), 1)
    y_output = [po + p1*x + p2*x**2 for x in x_output]
    return x_output, y_output

def third_order_polynomial(x_input, y_input, y_errors):
    weights = [1 / err ** 2 for err in y_errors]
    # returns polynomial coefficients ordered from low to high:
    po, p1, p2, p3 = np.polynomial.polynomial.polyfit(x_input, y_input, deg=3, rcond=None, full=False, w=weights)
    x_output = np.arange(min(x_input), max(x_input), 1)
    y_output = [po + p1*x + p2*x**2 + p3*x**3 for x in x_output]
    return x_output, y_output

def plot_temperature_scaling(temperature_scaling, plot_data = True, plot_smooth = False):
    ax = pyplot.axes(xscale='linear', yscale='linear')

    pyplot.xlabel('Temperature (K)')
    pyplot.ylabel('nbar/ms')
    # pyplot.title('Heating rates as a function of temperature')

    if plot_data:
        ax.errorbar(temperature_scaling.temperatures, temperature_scaling.heatingrates, yerr=temperature_scaling.heatingrate_errors, fmt=temperature_scaling.marker, label=temperature_scaling.label, color=temperature_scaling.color)
        # ax.errorbar(temperature_scaling.temperatures, temperature_scaling.heatingrates, yerr=temperature_scaling.heatingrate_errors, fmt='o', label=temperature_scaling.label, color=temperature_scaling.color)

    if plot_smooth:
        ax.plot(temperature_scaling.temperatures_smooth,  temperature_scaling.heatingrates_smooth, linestyle = temperature_scaling.line, color=temperature_scaling.color)
    return ax
