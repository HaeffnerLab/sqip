import numpy as np
from matplotlib import pyplot

from functions_fitting import fit_freq_scaling, exponential_fit


def plot_freq_scaling(ax,filename,skiprows,label,mycolor,fmt='o',dotsize=3):
    #TODO rewrite this
        mydata = np.loadtxt(filename,skiprows=skiprows)
        date = np.array(mydata[:,0])
        freq = np.array(mydata[:,1])
        rate = np.array(mydata[:,2])
        error = np.array(mydata[:,3])

        inds = np.argsort(freq)
        freq = freq[inds]
        rate = rate[inds]
        error = error[inds]

        amp, amp_err, alpha, alpha_err = fit_freq_scaling(freq, rate, error, label=label)
        ax.errorbar(freq,rate,yerr=error,color=mycolor,fmt=fmt,label=label,capsize=3)

        x = np.linspace(.47, 2, num=300)
        rate_fit = exponential_fit(x, amp, alpha)
        ax.plot(x,rate_fit,color = 'black')

        # ax.tick_params(labelsize=14,which='both')
        return


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


def plot_cumulative_dose(temperature_scalings, plot_500K = False, plot_295K = False, label = [0]):
    heatingrates_295K = []
    heatingrates_500K = []
    total_dose = []
    added_dose = []
    markers = []
    lines = []

    for data in temperature_scalings:
        heatingrates_295K.append(data.get_rate_at_nearest_temperature(295))
        heatingrates_500K.append(data.get_rate_at_nearest_temperature(500))
        total_dose.append(data.dataset.cumulative_dose)
        added_dose.append(data.dataset.added_dose)
        markers.append(data.marker)
        lines.append(data.line)

    pyplot.figure()
    ax = pyplot.axes(xscale='linear', yscale='log')
    pyplot.xlabel('Total deposited energy (J / surface atom)')
    pyplot.ylabel('Heating rate (nbar / ms)')

    # plot lines between points
    for i in range(1,len(lines)):
        if plot_295K:
            ax.plot([total_dose[i-1], total_dose[i]], [heatingrates_295K[i-1], heatingrates_295K[i]], linestyle = lines[i], color = 'blue')
        if plot_500K:
            ax.plot([total_dose[i-1], total_dose[i]], [heatingrates_500K[i-1], heatingrates_500K[i]], linestyle = lines[i], color = 'red')

    # plot data points
    i=0
    for data in temperature_scalings:
        rate_RT = data.get_rate_at_nearest_temperature(295)
        rate_HOT = data.get_rate_at_nearest_temperature(500)
        dose = data.dataset.cumulative_dose
        marker = data.marker
        last_treatment = data.dataset.last_treatment

        if i in label:
            labelRT = labelHOT = last_treatment
            if plot_295K and plot_500K:
                labelRT = labelRT + ' 295 K'
                labelHOT = labelHOT + ' 500 K'

        else:
            labelRT = None
            labelHOT = None
        i+=1

        if plot_295K:
            ax.plot(dose, rate_RT, marker = marker, color = 'blue', label = labelHOT)
        if plot_500K:
            ax.plot(dose, rate_HOT, marker = marker, color = 'red', label = labelRT)
    pyplot.legend()


def plot_added_dose(temperature_scalings):
    heatingrates_295K = []
    heatingrates_500K = []
    total_dose = [data.dataset.cumulative_dose for data in temperature_scalings]
    added_dose = [data.dataset.added_dose for data in temperature_scalings]
    markers = [data.marker for data in temperature_scalings]
    lines = [data.line for data in temperature_scalings]
    treatments = [data.dataset.last_treatment for data in temperature_scalings]
    labelsmaybe = [data.dataset.label for data in temperature_scalings]


    for data in temperature_scalings:
        heatingrates_295K.append(data.get_rate_at_nearest_temperature(295))
        heatingrates_500K.append(data.get_rate_at_nearest_temperature(500))

    pyplot.figure()
    ax = pyplot.axes(xscale='linear', yscale='log')
    pyplot.xlabel('Added energy (J / surface atom)')
    pyplot.ylabel('Heating rate (nbar / ms)')

    #print % and absolute changes in heating rates

    for i in range(1,len(lines)):
        print treatments[i] + ' :' + labelsmaybe[i]+ ' :'
        print str((heatingrates_295K[i]-heatingrates_295K[i-1])/(heatingrates_295K[i])*100) + '%'


    # plot lines between points
    for i in range(1,len(lines)):
        ax.plot([added_dose[i-1], added_dose[i]], [heatingrates_500K[i-1], heatingrates_500K[i]], linestyle = lines[i], color = 'red')

    # plot data points
    label = True
    for data in temperature_scalings:
        rate_HOT = data.get_rate_at_nearest_temperature(500)
        dose = data.dataset.added_dose
        marker = data.marker

        if label:
            labelHOT = '500 K'
            label = False
        else:
            labelHOT = None

        ax.plot(dose, rate_HOT, marker = marker, color = 'red', label = labelHOT)
    pyplot.legend()

    pyplot.figure()
    ax = pyplot.axes(xscale='linear', yscale='log')
    pyplot.xlabel('Added energy (J / surface atom)')
    pyplot.ylabel('Heating rate (nbar / ms)')
    # plot lines between points
    for i in range(1,len(lines)):
        ax.plot([added_dose[i-1], added_dose[i]], [heatingrates_295K[i-1], heatingrates_295K[i]], linestyle = lines[i], color = 'blue')

    # plot data points
    label = True
    for data in temperature_scalings:
        rate_RT = data.get_rate_at_nearest_temperature(295)
        dose = data.dataset.added_dose
        marker = data.marker

        if label:
            labelRT = '295 K'
            label = False
        else:
            labelRT = None

        ax.plot(dose, rate_RT, marker = marker, color = 'blue', label = labelRT)
    pyplot.legend()