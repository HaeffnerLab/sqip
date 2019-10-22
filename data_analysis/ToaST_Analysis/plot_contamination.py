from matplotlib import pyplot
import numpy as np
from plot_contamination_master import *

#TODO: rewrite everything with objects, check for errors


# Add all the data to the "many dates" file
# Import 'before' and 'after' heating rates for each auger
# Calculate alpha, plot as function of 'days auger on'. Always start with 0.
# Scale to 1.3 and 0.88 MHz, plot each separately as function of 'days auger on'

# look through notes and notebook, find out how many days auger on each time, and get all the rest of the dates
# Plot recent evolution of alpha
# Plot temp scaling/ taf distribution before and after auger when possible (maybe only possible twice)
# In another file, do a whole "before and after treatment" integrated taf number

data_root_location = '/Users/Maya/Dropbox/Data_and_Plotting_SQIP/Data/'


filename = data_root_location + 'Data_ToaST/E3_roomtemp_heatingrates_manydates.txt'
alldata = np.loadtxt(filename,skiprows=1)
### bin data if it has same frequency AND same day
### rescale to 0.88 MHz and 1.3 MHz

#days=0: pre auger
#days=0.5: turned on auger, trap facing away
#days=1: post auger
#days=2: post heat

datasets_auger = [
    # ['label','color',[['date','days'],['date','days']]], # note about whether current measured on E3. For auger data, days = # of days auger was on.
    ['20170810 - Auger pre test heat','red',[[20170726,0],[20170829,1]]],
    ['20170926 - Auger post test heat','red',[[20170829,0],[20170927,1]]],#,[20171026,2]]],
    ['20180130 - Auger pre TAF paper','red',[[20180126,0],[20180131,1]]],
    # ['20180622 - Auger pre baseline','red',[[20180611,0],[20180724,1]]],#,[20180906,2]]],#turned on once, electrons on e3
    # ['20180622 - Auger pre baseline post heat','red',[[20180724,1],[20180906,1]]], #no auger, just heated
    # ['20190207 - Auger post heat 3','teal',['no 'after' taken']],
    # ['20190416 - Auger post heat 5','orange',[[20190410,0],[20190415,0.5],[20190418,1]]], #auger on once for first rate, twice for second rate
    ['20190416 - Auger post heat 5','red',[[20190410,0],[20190418,1]]], #auger on once for first rate, twice for second rate
    ['20190506 - Auger post mill 6','blue',[[20190430,0],[20190509,1]]], #auger on three times
    ['20190524 - Auger post heat 6','red',[[20190522,0],[20190528,1]]],#auger on three times
    ['20190603 - Auger post mill 7','red',[[20190530,0],[20190604,1]]],#auger on two times
    ['20190625 - Auger post heat 7','red', [[20190618,0],[20190626,1]]],#auger on two times
    ['20190711 - Auger post mill 8d','red', [[20190711,0],[20190712,1]]],#auger on two times
]

# datasets = [
#     ['recent rates','black', [[20190702,32],[20190701.2,31.5],[20190701.1,31],[20190627,27],[20190626,26],[20190618,18],[20190604,4],[20190530,-1]]]
# ]

pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('0.88 MHz')
pyplot.ylabel('nbar/ms')
pyplot.xticks((0,1),('Before contamination','After contamination'))
pyplot.xlim(-.2,1.2)

for set in datasets_auger:
    label = set[0]
    days = set[2]
    alphas, data1p3, datap88, days_to_plot = process_rates_contamination(alldata,days)
    rates = map(lambda x: x.nominal_value, datap88)
    rateerr = map(lambda x: x.std_dev, datap88)
    if rates:
        color = getcolor(rates[0],rates[1])
        ax.errorbar(days_to_plot,rates,yerr=rateerr,fmt='-o',capsize=3,label=label,color=color)

pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('1.3 MHz')
pyplot.ylabel('nbar/ms')
pyplot.xticks((0,1),('Before contamination','After contamination'))
pyplot.xlim(-.2,1.2)

for set in datasets_auger:
    label = set[0]
    days = set[2]
    alphas, data1p3, datap88, days_to_plot = process_rates_contamination(alldata,days)
    rates = map(lambda x: x.nominal_value, data1p3)
    rateerr = map(lambda x: x.std_dev, data1p3)
    if rates:
        color = getcolor(rates[0],rates[1])
        ax.errorbar(days_to_plot,rates,yerr=rateerr,fmt='-o',capsize=3,label=label,color=color)

pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('Alpha')
pyplot.ylabel('alpha')
pyplot.xticks((0,1),('Before contamination','After contamination'))
pyplot.xlim(-.2,1.2)

for set in datasets_auger:
    label = set[0]
    days = set[2]
    alphas, data1p3, datap88, days_to_plot = process_rates_contamination(alldata,days)
    alpha = map(lambda x: x.nominal_value, alphas)
    alpha_err = map(lambda x: x.std_dev, alphas)
    if alpha:
        color = getcolor(alpha[0],alpha[1])
        ax.errorbar(days_to_plot,alpha,yerr=alpha_err,fmt='-o',capsize=3,label=label,color=color)


#########

datasets_mill = [('mill 8c',
    [[(20190701, 0.88, ufloat(4.61, 0.22), "RT, pre-mill 8c"), (20190701, 1.3, ufloat(1.96, 0.09), "RT, pre-mill 8c")],
    [(20190701, 0.88, ufloat(3.93, 0.19), "RT, post-mill same day"), (20190701, 1.3, ufloat(2.03, 0.06), "RT, post-mill same day")],
    [(20190702, 0.88, ufloat(4.17, 0.11), "RT, day after mill 8c"), (20190702, 1.3, ufloat(1.95, 0.04), "RT, day after mill 8c")],
    ]),
    ('mill 8d',
    [[(20190708, 0.88, ufloat(4.89, 0.13), "RT, pre-mill 8d"), (20190708, 1.3, ufloat(2.13, 0.05), "RT, pre-mill 8d")],
    [(20190708, 0.88, ufloat(3.11, 0.17), "RT, post-mill same day"), (20190708, 1.3, ufloat(1.58, 0.06), "RT, post-mill same day")],
    [(20190709, 0.88, ufloat(3.31, 0.14), "RT, day after mill 8d"), (20190709, 1.3, ufloat(1.58, 0.05), "RT, day after mill 8d")],
    ])
]

alldata_1p3 = []
alldata_p88 = []
alldata_alphas = []
plot_x = [0,1,2]
plot_colors = ['gold', 'green']
plot_labels = ['mill 8c', 'mill 8d']


for set in datasets_mill:
    alphas = []
    data1p3 = []
    datap88 = []

    for measurement in set[1]:
        measurement_p88 = measurement[1][2]
        measurement_1p3 = measurement[0][2]

        rates = [measurement_p88.nominal_value, measurement_1p3.nominal_value]
        rateerrs = [measurement_p88.std_dev, measurement_p88.std_dev]
        freqs = [0.88, 1.3]
        alpha, amp = calc_single_alpha(rates,rateerrs,freqs) # alpha is type ufloat

        datap88.append(measurement_p88)
        data1p3.append(measurement_1p3)
        alphas.append(alpha)
    alldata_p88.append(datap88)
    alldata_1p3.append(data1p3)
    alldata_alphas.append(alphas)

# plot 0.88
pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('0.88 MHz')
pyplot.ylabel('nbar/ms')
pyplot.xticks((0,1,2),('Before mill', '4 hr after mill', 'day after mill'))
pyplot.xlim(-.2,2.2)

for i in range(0,2):
    rates = [rate.nominal_value for rate in alldata_p88[i]]
    rateerr = [rate.std_dev for rate in alldata_p88[i]]
    ax.errorbar(plot_x, rates, yerr=rateerr, fmt='-o', capsize=3, color = plot_colors[i], label=plot_labels[i])

# plot 1.3
pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('1.3 MHz')
pyplot.ylabel('nbar/ms')
pyplot.xticks((0,1,2),('Before mill', '4 hr after mill', 'day after mill'))
pyplot.xlim(-.2,2.2)

for i in range(0,2):
    rates = [rate.nominal_value for rate in alldata_1p3[i]]
    rateerr = [rate.std_dev for rate in alldata_1p3[i]]
    ax.errorbar(plot_x, rates, yerr=rateerr, fmt='-o', capsize=3, color = plot_colors[i], label=plot_labels[i])

# plot alpha
pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('Alpha')
pyplot.ylabel('nbar/ms')
pyplot.xticks((0,1,2),('Before mill', '4 hr after mill', 'day after mill'))
pyplot.xlim(-.2,2.2)

for i in range(0,2):
    alphas = [alpha.nominal_value-1 for alpha in alldata_alphas[i]]
    alphaerr = [alpha.std_dev for alpha in alldata_alphas[i]]
    ax.errorbar(plot_x, alphas, yerr=alphaerr, fmt='-o', capsize=3, color = plot_colors[i], label=plot_labels[i])







pyplot.show()