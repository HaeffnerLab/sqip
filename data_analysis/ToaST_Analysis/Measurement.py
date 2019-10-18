from datetime import timedelta
from datetime import datetime
from time import mktime
from copy import deepcopy
import numpy as np
from uncertainties import ufloat

class Measurement:

    def __init__(self,
                 date = 0,
                 electrode_number = 0,
                 trap_frequency = 0,
                 times_of_day = 0,
                 heatingrate = ufloat(0,0),
                 heater_current = 0,
                 fourwire_voltage = 0,
                 unscaled_temperature = 298,
                 temperature_calibration=None):

        self.temperature_calibration = temperature_calibration
        self.electrode_number = electrode_number
        self.trap_frequency = trap_frequency
        self.heatingrate = heatingrate.nominal_value
        self.heatingrate_error = heatingrate.std_dev
        self.current = heater_current
        self.fourwire_voltage = fourwire_voltage
        self.temperature = scale_temperature(self.temperature_calibration, unscaled_temperature, self.current, self.fourwire_voltage)

        if date:
            self.date = datetime.strptime(date, '%Y%m%d')
        else:
            self.date = None
        if times_of_day:
            self.times_of_day = extract_time_string(times_of_day)
            computed_time = [self.date + time for time in self.times_of_day]
            self.times_in_hours = [get_time_in_seconds_from_datetime(time)/3600 for time in computed_time]
        else:
            self.times_of_day = None
            self.times_in_hours = None

    def scale_to_frequency(self, new_frequency, alpha = 1):
        scaled_data = deepcopy(self)
        scaled_data.heatingrate = self.heatingrate * (self.trap_frequency / new_frequency)**(alpha + 1)
        scaled_data.heatingrate_error = self.heatingrate_error * (self.trap_frequency / new_frequency)**(alpha + 1)
        scaled_data.trap_frequency = new_frequency
        return scaled_data


# splits string in format 1440_54 into 14, 40, 54 (h, m, s) and creates a time delta
def extract_time_string(time_strings):
    times = []
    for string in time_strings:
        hours = int(string[0:2])
        minutes = int(string[2:4])
        seconds = int(string[5:7])
        times.append(timedelta(hours=hours) + timedelta(minutes=minutes) + timedelta(seconds=seconds))
    return times

def get_time_in_seconds_from_datetime(computed_time):
    return mktime(computed_time.timetuple())

def farenheit_to_celcius(temp_F):
    temp_C = (temp_F - 32) * 5/9
    return temp_C

def scale_temperature(temperature_calibration, unscaled_temperature, current=0, fourwire_voltage=0):

    if temperature_calibration == 'iphone': # tempcalibration = 1, temp in Celcius
        cameraTemperatureC = unscaled_temperature
        yoffset = 0.435 #corrects telescope,window and glass
        x_offset = 21
        divisor = 18.24
        realTemperatureK = cameraTemperatureC_to_realTemperatureK(cameraTemperatureC, yoffset, x_offset, divisor)

    elif temperature_calibration == 'android': # temperaturecalibration = 2, temp in Farenheit
        cameraTemperatureC = farenheit_to_celcius(unscaled_temperature)
        y_offset = 0.492 #corrects telescope,window and glass
        x_offset = 22
        divisor = 19.96
        realTemperatureK = cameraTemperatureC_to_realTemperatureK(cameraTemperatureC, y_offset, x_offset, divisor)

    elif temperature_calibration == 'android_new_lens':# temperaturecalibration = 3, temp in Farenheit
        cameraTemperatureC = farenheit_to_celcius(unscaled_temperature)
        y_offset = 0.697 #corrects telescope,window and glass
        x_offset = 21.4
        divisor = 11.56
        realTemperatureK = cameraTemperatureC_to_realTemperatureK(cameraTemperatureC, y_offset, x_offset, divisor)

    elif temperature_calibration in ('power1','power5'):
        power = current * fourwire_voltage
        realTemperatureK = power_to_realTemperatureK(power,temperature_calibration)

    else:
        realTemperatureK = unscaled_temperature

    return realTemperatureK

def cameraTemperatureC_to_realTemperatureK(cameraTemperatureC_measured, y_offset, x_offset, divisor):
    realTemperatureC = np.arange(0, 400, 0.1)
    cameraTemperatureC_calculated = realTemperatureC * ((1 - y_offset) * np.exp( -(realTemperatureC-x_offset) / divisor) + y_offset)
    realtempK = realTemperatureC[np.argmin(np.abs(cameraTemperatureC_calculated - cameraTemperatureC_measured))] + 273
    return realtempK

def power_to_realTemperatureK(power, temperature_calibration):
    x_offset = 21
    divisor = 18.24

    if power ==0:
        return 297
    elif temperature_calibration == 'power5':
        cameraTemperatureC = 89.2 * (1 - np.exp(-1.387 * power)) * power**0.5 + 20.68 #calibration from 0509 (2018)
        y_offset = 0.678 #corrects window and glass only
    elif temperature_calibration == 'power1':
        cameraTemperatureC = 65.2 * (1 - np.exp(-1.6 * power)) * power**0.5 + 21 #appropriate for 13Jun2018 data
        y_offset = 0.435 #corrects telescope,window and glass

    realTemperatureK = cameraTemperatureC_to_realTemperatureK(cameraTemperatureC, y_offset, x_offset, divisor)

    return realTemperatureK
