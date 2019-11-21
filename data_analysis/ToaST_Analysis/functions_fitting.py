import numpy as np
from scipy import optimize as op
from scipy.interpolate import UnivariateSpline
from uncertainties import ufloat, umath

def univariate_spline(x_input, y_input, y_errors):
    weights = [1 / err for err in y_errors]
    bbox = [min(x_input), max(y_input)]
    # bbox = [0,800]
    smoothingpolynomial = 2
    numberofknots = 100
    uspline = UnivariateSpline(x_input, y_input, weights, k=smoothingpolynomial, s=numberofknots, ext=1, bbox=bbox)
    x_output = np.arange(min(x_input), max(x_input), 1)
    return x_output, uspline(x_output)


def fit_second_order_polynomial(x_input, y_input, y_errors):
    weights = [1 / err ** 2 for err in y_errors]
    # returns polynomial coefficients ordered from low to high:
    po, p1, p2 = np.polynomial.polynomial.polyfit(x_input, y_input, deg=2, rcond=None, full=False, w=weights)
    x_output = np.arange(min(x_input), max(x_input), 1)
    y_output = [po + p1*x + p2*x**2 for x in x_output]
    return x_output, y_output


def fit_third_order_polynomial(x_input, y_input, y_errors):
    weights = [1 / err ** 2 for err in y_errors]
    # returns polynomial coefficients ordered from low to high:
    po, p1, p2, p3 = np.polynomial.polynomial.polyfit(x_input, y_input, deg=3, rcond=None, full=False, w=weights)
    x_output = np.arange(min(x_input), max(x_input), 1)
    y_output = [po + p1*x + p2*x**2 + p3*x**3 for x in x_output]
    return x_output, y_output


def gaussian(a,b,c):
    return


def exponential(x,amplitude,exponent):
    return amplitude/x**exponent


def weighted_average(values, absolute_errors):
    weights = [error**-2 for error in absolute_errors]
    average_value = np.sum( np.multiply(values, weights) ) / np.sum(weights)
    new_absolute_error = np.sqrt(1/np.sum(weights))
    return ufloat(average_value, new_absolute_error)


def fit_exponential(frequencies, heatingrates, heatingrate_errors):

    if len(set(frequencies)) <= 1:
        amplitude, exponent = None, None

    if len(set(frequencies)) >= 3:
        popt, pcov = op.curve_fit(exponential, frequencies, heatingrates, p0=[2, 2], sigma=heatingrate_errors, absolute_sigma=True)
        perr = np.sqrt(np.diag(pcov))
        amplitude = ufloat(popt[0], perr[0])
        exponent = ufloat(popt[1], perr[1])

    if len(frequencies) == 2:
        heatingrate_0 = ufloat(heatingrates[0], heatingrate_errors[0])
        heatingrate_1 = ufloat(heatingrates[1], heatingrate_errors[1])

        exponent = abs(umath.log(heatingrate_0/heatingrate_1)/umath.log(frequencies[0]/frequencies[1]))
        amplitude = heatingrate_0*frequencies[0] ** exponent

    return amplitude, exponent

