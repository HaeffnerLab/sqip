from matplotlib import pyplot
import numpy as np
from scipy import optimize as op
from uncertainties import *
from uncertainties.umath import *

# from plot_freqscaling_master import *


def get_rates_to_plot(data,days):
    rates_to_plot = []

    for day in days:
        date_to_look_for = day[0]
        day_to_plot = day[1]
        mydata = []

        data_date_subset = filter(lambda x: x[0] == date_to_look_for, data)
        for line in data_date_subset:
            freq = line[1]
            rate = line[2]
            rateerr = line[3]
            mydata.append([rate,rateerr,freq,day_to_plot])

        rates_to_plot.append(mydata)

    return rates_to_plot

def process_rates_contamination(data,days):

    ratestoplot = get_rates_to_plot(data,days)

    alphas = []
    data1p3 = []
    datap88 = []
    days_to_plot = []

    for dataset in ratestoplot: # process each day
        dataset = np.array(dataset)

        #bin same freq


        rates = dataset[:,0]
        rateerrs = dataset[:,1]
        freqs = dataset[:,2]
        day_to_plot = dataset[0][3]

        if len(freqs)==2:
            alpha,amp = calc_single_alpha(rates,rateerrs,freqs) # alpha is type ufloat
        if len(freqs)>2:
            alpha_nominal,alphaerror,Amp, amperror = fit_freq_scaling(freqs, rates, rateerrs,p=0)
            alpha = ufloat(alpha_nominal,alphaerror)

        alphas.append(alpha-1)
        days_to_plot.append(day_to_plot)

        for line in dataset:
            freq = line[2]
            rate = line[0]
            rateerr = line[1]
            if freq == 1.3:
                data1p3.append(ufloat(rate,rateerr))
            if freq == 0.88:
                datap88.append(ufloat(rate,rateerr))
            #temporary hack
            if freq == 1.362 or freq == 1.34 or freq == 1.334 or freq == 1.301:
                data1p3.append(ufloat(rate,rateerr)*(freq/1.3)**alpha)
            if freq == 0.503 or freq == 0.7 or freq == 0.673 or freq == 0.879:
                datap88.append(ufloat(rate,rateerr)*(freq/.88)**alpha)

    return alphas, data1p3, datap88,days_to_plot


def getcolor(value_1, value_2):
    if value_2 > value_1:
        return 'green'
    if value_2 < value_1:
        return 'red'
    else:
        return 'black'

def fit_freq_scaling(freq, rate, rerr,label='',p=1): #removed ax input

        def f(x,Amp,alpha):
                return Amp/x**alpha
        popt,pcov = op.curve_fit(f,freq,rate,p0=[1,2],sigma=rerr,absolute_sigma=True)
        perr = np.sqrt(np.diag(pcov))
        Amp = popt[0]
        alpha = popt[1]

        if p==1:
            print label + ':'
            print "Amplitude: "+"{0:.2f}".format(Amp) + ' +- ' + "{0:.2f}".format(perr[0])
#           print "exponent: "+"{0:.2f}".format(alpha) + ' +- ' + "{0:.2f}".format(perr[1])
            print "exponent: "+"{0:.2f}".format(alpha) + ' +- ' + "{0:.2f}".format(perr[1])

            freq = np.sort(freq)
            ratefit = [f(x,Amp,alpha) for x in freq]

        return alpha,perr[1],Amp, perr[0]

def calc_single_alpha(rates,errors,freqs):
        #takes lists with two rates, two errors, two freqs
        #outputs alpha as a ufloat
        rate0 = ufloat(rates[0],errors[0])
        rate1 = ufloat(rates[1],errors[1])
        freq0 = ufloat(freqs[0],0)
        freq1 = ufloat(freqs[1],0)
        alpha = abs(log(rate0/rate1)/log(freq0/freq1))

        amp = rate0*freq0**(alpha)
        return alpha,amp
