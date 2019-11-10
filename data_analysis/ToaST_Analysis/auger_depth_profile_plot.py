import matplotlib.pyplot as plt
import numpy as np


def depth_profile_plot(doses, metal_profiles):
    total = np.array(0)
    metals_proportional = {}
    for metal in metal_profiles:
        total = total + np.array(metal.depths)
    for metal in metal_profiles:
        metals_proportional[(metal.color, metal.label)] = np.true_divide(metal.depths, total) * 100
    ind = [x for x, _ in enumerate(doses)]

    left = np.array(0)
    for ((color, label), proportion) in metals_proportional.iteritems():
        plt.barh(doses, proportion, height=10, label=label, color=color, left=left)
        left = left + proportion

    plt.ylabel("Doses")
    plt.xlabel("Percentages")
    plt.legend(loc="upper right")
    plt.title("Percentage of Element by Milling Dose")

    plt.show()


class MetalDepthProfile:
    def __init__(self, label, color, depths):
        self.label = label
        self.color = color
        self.depths = depths


if __name__ == '__main__':
    doses = [10,30,45,60,100]
    calcium = MetalDepthProfile('Calcium', 'red', [38, 17, 26, 19, 15])
    oxygen = MetalDepthProfile('Oxygen', 'blue', [37, 23, 18, 18, 10])
    aluminum = MetalDepthProfile('Aluminum', 'green', [46, 27, 26, 19, 17])
    cadmium = MetalDepthProfile('Cadmium', 'brown', [2, 23, 12, 95, 3])
    depth_profile_plot(doses, [calcium, oxygen, aluminum, cadmium])
