import csv
from collections import deque
from itertools import islice
from Measurement_Multi_Trap_Comparison import *
from Measurement import Measurement
from uncertainties import ufloat


## Measurement object takes "raw_data" is a list of the form:
##      ('date',
##       electrode_number,
##       trap_frequency_MHz,
##       ['time', 'time'],
##       ufloat(heatingrate, heatingrate error),
##       heater_current_A,
##       fourwire_voltage_V,
##       unscaled camera temperature)

def import_handformatted_datafile(filename, temperature_calibration):
    """
    :param filename, temperature_calibration
    :return: [Measurement, Measurement]
    """
    measurements = []

    data_unformatted = extract_data_from_handformatted_file(filename)
    for line in data_unformatted:
        date, electrode_number, trap_frequency, times_of_day, heatingrate, heater_current, fourwire_voltage, unscaled_temperature = format_handformatted_datafile(line)

        measurements.append(Measurement(date, electrode_number, trap_frequency, times_of_day, heatingrate, heater_current, fourwire_voltage, unscaled_temperature,temperature_calibration))
    return measurements

def extract_data_from_handformatted_file(filename):
    loaded_data = np.loadtxt(filename,skiprows=1)
    return loaded_data

def format_handformatted_datafile(line):
    date = str(int(line[0]))
    electrode_number = 0
    trap_frequency = line[1]
    times_of_day = []
    heatingrate = ufloat(line[2],line[3])
    heater_current = line[4]
    fourwire_voltage = line[5]
    unscaled_temperature = line[6]
    return date, electrode_number, trap_frequency, times_of_day, heatingrate, heater_current, fourwire_voltage, unscaled_temperature

def import_scraped_temperature_scaling_data(filename, temperature_calibration):
    """
    :param filename, temperature_calibration
    :return: [Measurement, Measurement]
    """
    measurements = []
    data_unformatted = extract_data_from_scraped_file(filename)
    for line in data_unformatted:
        date, electrode_number, trap_frequency, times_of_day, heatingrate, heater_current, fourwire_voltage, unscaled_temperature = format_scraped_data(line)
        measurements.append(Measurement(date, electrode_number, trap_frequency, times_of_day, heatingrate, heater_current, fourwire_voltage, unscaled_temperature,temperature_calibration))
    return measurements # a single list of heating rate objects

def format_scraped_data(line):
    date = line[0]
    electrode_number = float(line[1])
    trap_frequency = float(line[2])
    times_of_day = extract_times(line[4])
    heatingrate = ufloat(line[5].split('+')[0], line[5].split('-')[1])
    heater_current = float(line[6])
    fourwire_voltage = float(line[7])
    unscaled_temperature = float(line[8])

    return date, electrode_number, trap_frequency, times_of_day, heatingrate, heater_current, fourwire_voltage, unscaled_temperature


# skip last n lines of an iterator
# https://stackoverflow.com/questions/16846460/
def skip_last_n(iterator, n=1):
    it = iter(iterator)
    prev = deque(islice(it, n), n)
    for item in it:
        yield prev.popleft()
        prev.append(item)


def extract_data_from_scraped_file(filename):
    reader = csv.reader(open(filename))
    # skip header line
    next(reader)

    loaded_data = []
    for line in skip_last_n(reader, 6):
        # data isn't really clean, so if the heating rate is empty or short we'll just assume the whole thing is junk
        if len(line[5]) > 2:
            loaded_data.append(line)
    return loaded_data


def extract_times(string):
    #format of string = "'1332_45', '1332_46', '1332_47'"
    timelist=[]
    times = string.split(',')
    for time in times:
        if len(time)>8: timelist.append(time[-8:-1])
    return timelist


def format_multi_trap_comparison(line):
    ## Measurement_Multi_Trap_Comparison object takes "raw_data" is a list of the form:
    ##      ['trap name',
    ##       trapping_height_um,
    ##       trap_frequency_MHz,
    ##       days_in_atmosphere,
    ##       weeks_baked
    ##       ufloat(heatingrate,error),
    ##       times_broke_vacuum,
    ##       'evaporation_date']

    trap_name = line[0]
    trapping_height_um = float(line[1])
    trap_frequency_MHz = float(line[2])
    days_in_atmosphere = float(line[3])
    weeks_baked = float(line[4])
    heatingrate = ufloat(line[5].split('+')[0], line[5].split('-')[1])
    times_broke_vacuum = float(line[6])
    evaporation_date = line[7]

    return trap_name, trapping_height_um, trap_frequency_MHz, days_in_atmosphere, weeks_baked, heatingrate, times_broke_vacuum, evaporation_date

def import_multi_trap_comparison_data(filename):
    reader = csv.reader(open(filename))
    # skip header line
    next(reader)

    heatingrate_list = []
    for line in reader:
        trap_name, trapping_height_um, trap_frequency_MHz, days_in_atmosphere, weeks_baked, heatingrate, times_broke_vacuum, evaporation_date = format_multi_trap_comparison(line)
        heatingrate_list.append(Measurement_Multi_Trap_Comparison(trap_name, trapping_height_um, trap_frequency_MHz, days_in_atmosphere, weeks_baked, heatingrate, times_broke_vacuum, evaporation_date))

    return heatingrate_list


