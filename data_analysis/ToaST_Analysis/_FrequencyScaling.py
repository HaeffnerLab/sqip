import numpy as np
from _Measurement import Measurement

class FrequencyScaling:

    def __init__(self, measurements, temperature, dataset):

        self.measurements = measurements
        self.dataset = dataset
        self.temperature = temperature

        self.heatingrates = [measurement.heatingrate for measurement in measurements]
        self.heatingrate_errors = [measurement.heatingrate_error for measurement in measurements]
        self.frequencies = [measurement.frequency for measurement in measurements]

        self.alpha = self.calculate_alpha()

    def get_frequency_subset(self, freq_min, freq_max):
        #TODO: write this
        return

    def calculate_alpha(self):
        return