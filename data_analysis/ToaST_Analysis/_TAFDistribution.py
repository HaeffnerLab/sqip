class TAFDistribution:

    def __init__(self, temperature_scalings, dataset):

        self.temperature_scalings = temperature_scalings
        self.dataset = dataset

        self.taf_measurements = None

        self.taf_smooth = None