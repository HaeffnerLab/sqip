from datetime import timedelta
from datetime import datetime
from time import mktime
import numpy as np
from _Measurement import *
from matplotlib import pyplot


class ContaminationMeasurementMultiTrapComparison():

    def __init__(self,trap_name, trapping_height_um, trap_frequency_MHz, days_in_atmosphere, weeks_baked, heatingrate, times_broke_vacuum, evaporation_date):
        ##      'trap_name',
        ##       trappingheight,
        ##       trapfrequency,
        ##       days_in_atmosphere,
        ##       weeks_baked,
        ##       ufloat(heatingrate, error),
        ##       times_broke_vacuum,
        ##       'evaporation_date'

        self.trap_name = trap_name
        self.trapping_height = trapping_height_um #microns
        self.trap_frequency = trap_frequency_MHz #MHz
        self.days_in_atmosphere = days_in_atmosphere
        self.weeks_baked = weeks_baked
        self.heatingrate = heatingrate.nominal_value
        self.heatingrate_error = heatingrate.std_dev
        self.times_broke_vacuum = times_broke_vacuum

        if evaporation_date:
            self.evaporation_date = datetime.strptime(evaporation_date, '%Y%m%d')

        self.color = 'black'
        self.label = self.trap_name
        self.symbol = 'o'


def scale_to_distance(new_distance_um, measurement_multi_trap_comparison, beta=2.6):
    #TODO: get error assuming beta is between 4 and 2.6
    scaled_data = deepcopy(measurement_multi_trap_comparison)
    scaled_data.trapping_height = new_distance_um
    scaled_data.heatingrate = measurement_multi_trap_comparison.heatingrate * (measurement_multi_trap_comparison.trapping_height**beta) / (new_distance_um**beta)
    scaled_data.heatingrate_error = measurement_multi_trap_comparison.heatingrate_error * (measurement_multi_trap_comparison.trapping_height**beta) / (new_distance_um**beta)
    return scaled_data

def scale_to_frequency(new_frequency_MHz, measurement_multi_trap_comparison):
    scaled_data = deepcopy(measurement_multi_trap_comparison)
    scaled_data.trap_frequency = new_frequency_MHz
    scaled_data.heatingrate = measurement_multi_trap_comparison.heatingrate * (measurement_multi_trap_comparison.trap_frequency**2) / (new_frequency_MHz**2)
    scaled_data.heatingrate_error = measurement_multi_trap_comparison.heatingrate_error * (measurement_multi_trap_comparison.trap_frequency**2) / (new_frequency_MHz**2)
    return scaled_data


def plot_multi_trap_comparison(list_of_measurements):
    pyplot.figure()
    ax = pyplot.axes(xscale='linear', yscale='linear')
    pyplot.xlabel('Time in atmosphere (days)')
    pyplot.ylabel('Heating Rate(nbar/ms)')
    pyplot.title('Room temperature heating rates')

    for data in list_of_measurements:
        ax.errorbar(data.days_in_atmosphere, data.heatingrate, fmt=data.symbol, yerr=data.heatingrate_error, color=data.color, label=data.label)

    ax.legend()
    return
