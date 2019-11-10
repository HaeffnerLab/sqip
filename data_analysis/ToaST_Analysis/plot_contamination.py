from matplotlib import pyplot
import numpy as np
from contamination_master import *
from dataset_factory import *

#TODO: rewrite everything with objects, check for errors

### plot room temperature rates from multiple traps as a function of time in atmosphere
plot_multi_trap_comparison(multi_trap_comparison())


## Plot data before and after auger
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

### Plot data before, immediately after, and day after milling
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



### Plot data with camera on and off
#########

datasets_mill = [('108 F on camera',
    [
        [(20191101, 1.300, ufloat(1.26, 0.050), "camera_off", 1),
         (20191101, 0.880, ufloat(2.98, 0.180), "camera_off", 1)],
        [(20191101, 0.880, ufloat(2.98, 0.190), "camera_on", 2),
         (20191101,	1.300, ufloat(1.44, 0.070), "camera_on", 2)],
        [(20191104,	1.300, ufloat(1.39, 0.060), "camera_on", 3),
         (20191104, 0.880, ufloat(2.88, 0.160), "camera_on", 3)],
        [(20191104,	0.880, ufloat(3.02, 0.160), "camera_off", 4),
         (20191104, 1.300, ufloat(1.24, 0.060), "camera_off", 4)],
        [(20191104,	1.300, ufloat(1.21, 0.060), "camera_on", 5),
         (20191104, 0.880, ufloat(2.52, 0.170), "camera_on",5)]
    ]
                  ),
        ('RT',
    [
        [(20191101,	1.300, ufloat(1.30, 0.050), "before heat", 1),
         (20191101,	0.880, ufloat(2.54, 0.110), "before heat", 1)],
        [(20191101,	0.880, ufloat(2.69, 0.170), "before heat", 1),
         (20191101,	1.300, ufloat(1.38, 0.060), "before heat", 1)],
        [(20191104,	0.880, ufloat(2.70, 0.160), "after heat", 2),
         (20191104,	1.300, ufloat(1.14, 0.070), "after heat", 2)],
        [(20191104, 1.300, ufloat(1.24, 0.070), "after heat", 2),
         (20191104,	0.880, ufloat(2.70, 0.170), "after heat", 2)]
    ]
                  )
                 ]


alldata_1p3 = []
alldata_p88 = []
alldata_alphas = []
plot_colors = ['gold', 'green']
plot_labels = ['mill 8c', 'mill 8d']


for set in datasets_mill:
    alphas = []
    data1p3 = []
    datap88 = []

    for measurement in set[1]:
        for heatingrate in measurement:
            if heatingrate[1] == 0.88:
                heatingrate_p88 = heatingrate[2]
            elif heatingrate[1] == 1.3:
                heatingrate_1p3 = heatingrate[2]

        rates = [heatingrate_p88.nominal_value, heatingrate_1p3.nominal_value]
        rateerrs = [heatingrate_p88.std_dev, heatingrate_1p3.std_dev]
        freqs = [0.88000, 1.3000]
        alpha, amp = calc_single_alpha(rates,rateerrs,freqs) # alpha is type ufloat

        print "alpha"
        print alpha-1

#         datap88.append(heatingrate_p88)
#         data1p3.append(heatingrate_1p3)
#         alphas.append(alpha)
#     alldata_p88.append(datap88)
#     alldata_1p3.append(data1p3)
#     alldata_alphas.append(alphas)
#
# # plot 0.88
# pyplot.figure()
# ax = pyplot.axes(xscale='linear',yscale='linear')
# pyplot.title('0.88 MHz')
# pyplot.ylabel('nbar/ms')
# # pyplot.xticks((0,1,2,4,5),('Before mill', '4 hr after mill', 'day after mill'))
# pyplot.xlim(-.2,5.2)
#
# for i in range(0,1):
#     rates = [rate.nominal_value for rate in alldata_p88[i]]
#     rateerr = [rate.std_dev for rate in alldata_p88[i]]
#     ax.errorbar(plot_x, rates, yerr=rateerr, fmt='-o', capsize=3, color = plot_colors[i], label=plot_labels[i])
#
# # plot 1.3
# pyplot.figure()
# ax = pyplot.axes(xscale='linear',yscale='linear')
# pyplot.title('1.3 MHz')
# pyplot.ylabel('nbar/ms')
# # pyplot.xticks((0,1,2),('Before mill', '4 hr after mill', 'day after mill'))
# pyplot.xlim(-.2,5.2)
#
# for i in range(0,1):
#     rates = [rate.nominal_value for rate in alldata_1p3[i]]
#     rateerr = [rate.std_dev for rate in alldata_1p3[i]]
#     ax.errorbar(plot_x, rates, yerr=rateerr, fmt='-o', capsize=3, color = plot_colors[i], label=plot_labels[i])
#
# # plot alpha
# pyplot.figure()
# ax = pyplot.axes(xscale='linear',yscale='linear')
# pyplot.title('Alpha')
# pyplot.ylabel('nbar/ms')
# # pyplot.xticks((0,1,2),('Before mill', '4 hr after mill', 'day after mill'))
# pyplot.xlim(-.2,5.2)
#
# for i in range(0,1):
#     alphas = [alpha.nominal_value-1 for alpha in alldata_alphas[i]]
#     alphaerr = [alpha.std_dev for alpha in alldata_alphas[i]]
#     ax.errorbar(plot_x, alphas, yerr=alphaerr, fmt='-o', capsize=3, color = plot_colors[i], label=plot_labels[i])


######### Plot 108 F data when camera is on vs off
x_camera_off = [0,3]
x_camera_on = [1,2,4]
alpha = [1.21, 0.86, 0.87, 1.28, 0.88]
alpha_err = [0.19, 0.21, 0.18, 0.18, 0.21]
heatingrate_1p3 = [1.26, 1.44, 1.39, 1.24, 1.21]
heatingrate_1p3_err = [0.05, 0.07, 0.06, 0.06, 0.06]
heatingrate_p88 = [2.98, 2.98, 2.88, 3.02, 2.52]
heatingrate_p88_err = [0.18, 0.19, 0.16, 0.16, 0.17]


# plot 1.3 MHz
pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('1.3 MHz, 108F')
pyplot.ylabel('nbar/ms')

for i in x_camera_off:
    ax.errorbar(i, heatingrate_1p3[i], yerr=heatingrate_1p3_err[i], fmt='o', color = 'red', label='camera off')
for i in x_camera_on:
    ax.errorbar(i, heatingrate_1p3[i], yerr=heatingrate_1p3_err[i], fmt='o', color = 'green', label='camera on')
pyplot.legend()

# plot 0.88 MHz
pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('0.88 MHz, 108F')
pyplot.ylabel('nbar/ms')
pyplot.xticks((-1,1),('Before heat', 'After heat'))

for i in x_camera_off:
    ax.errorbar(i, heatingrate_p88[i], yerr=heatingrate_p88_err[i], fmt='o', color = 'red', label='camera off')
for i in x_camera_on:
    ax.errorbar(i, heatingrate_p88[i], yerr=heatingrate_p88_err[i], fmt='o', color = 'green', label='camera on')
pyplot.legend()


# plot alpha
pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('Alpha, 108F')
pyplot.ylabel('alpha')
pyplot.xticks((-1,1),('Before heat', 'After heat'))

for i in x_camera_off:
    ax.errorbar(i, alpha[i], yerr=alpha_err[i], fmt='o', color = 'red', label='camera off')
for i in x_camera_on:
    ax.errorbar(i, alpha[i], yerr=alpha_err[i], fmt='o', color = 'green', label='camera on')
pyplot.legend()


######### Plot room temperature data before and after low-temperature heating
x = [-1,-1.05,1,1.05]
alpha = [0.72, 0.71, 1.21, 0.99]
alpha_err = [0.15, 0.20, 0.22, 0.22]
heatingrate_1p3 = [1.30, 1.38, 1.14, 1.24]
heatingrate_1p3_err = [0.05, 0.06, 0.07, 0.07]
heatingrate_p88 = [2.54, 2.69, 2.70, 2.70]
heatingrate_p88_err = [0.11, 0.17, 0.16, 0.17]

# plot 1.3 MHz
pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('1.3 MHz, room temperature')
pyplot.ylabel('nbar/ms')
pyplot.xticks((-1,1),('Before heat', 'After heat'))
# pyplot.xlim(-1.2,1.2)

for i in range(len(x)):
    ax.errorbar(x[i], heatingrate_1p3[i], yerr=heatingrate_1p3_err[i], fmt='o', color = 'black')

# plot 0.88 MHz
pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('0.88 MHz, room temperature')
pyplot.ylabel('nbar/ms')
pyplot.xticks((-1,1),('Before heat', 'After heat'))
# pyplot.xlim(-1.2,1.2)

for i in range(len(x)):
    ax.errorbar(x[i], heatingrate_p88[i], yerr=heatingrate_p88_err[i], fmt='o', color = 'black')


# plot alpha
pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('Alpha, room temperature')
pyplot.ylabel('alpha')
pyplot.xticks((-1,1),('Before heat', 'After heat'))
# pyplot.xlim(-1.2,1.2)

for i in range(len(x)):
    ax.errorbar(x[i], alpha[i], yerr=alpha_err[i], fmt='o', color = 'black')

pyplot.show()