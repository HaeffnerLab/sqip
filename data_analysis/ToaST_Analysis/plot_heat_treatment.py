import pint
ureg = pint.UnitRegistry()
from uncertainties import umath
from scipy import optimize as op
from dataset_factory import heat_treatment_mill7
from _Dataset import Dataset
from functions_import_data import *
from matplotlib import pyplot

data_root_location = '/Users/Maya/Dropbox/Data_and_Plotting_SQIP/Data/'

def plot_heat_treatment(datasets):
    pyplot.figure()
    ax = pyplot.axes(xscale='linear', yscale='linear')
    pyplot.xlabel('Time(days)')
    pyplot.ylabel('Temperature(K)')
    pyplot.title('Heat Treatment Post Mill 7')

    for dataset in datasets:
        ax.plot(dataset.get_relative_times_day(), dataset.temperatures, color=dataset.color, label = dataset.label, linewidth=.5)


##### plot temperature as a function of time
heat_treatment = heat_treatment_mill7(color = 'purple')
plot_heat_treatment([heat_treatment])

#### plot temperature as a function of time

filename, temperature_calibration  = data_root_location + 'Data_scraped_for_ToaST/Week_of_09_23_2019_-_temp_scaling_post_mill_10.csv', 'android_new_lens'
allmeasurements = import_scraped_temperature_scaling_data(filename, temperature_calibration)
measurements = [measurement for measurement in allmeasurements if measurement.times_in_hours and measurement.temperature > 500]
# measurements = measurements[0:12]

dataset = Dataset(measurements)
rates_to_fit = [measurement for measurement in measurements if 522 < measurement.temperature < 538]
dataset_to_fit = Dataset(rates_to_fit)

fig, ax1 = pyplot.subplots()
pyplot.xlabel('Time(days)')
pyplot.ylabel('Temperature(K)')
pyplot.title('Heat Treatment Post Mill 10')
ax2 = ax1.twinx()
ax2.set_ylabel('nbar/ms', color = 'red')

ax1.plot(dataset.get_relative_times_day(), dataset.temperatures, marker = 'o', color='gray', linewidth=.5)
ax2.errorbar(dataset.get_relative_times_day(), dataset.heatingrates, yerr = dataset.heatingrate_errors, marker = 'o', color='red', linewidth=.5)
ax2.errorbar(dataset_to_fit.get_relative_times_day(), dataset_to_fit.heatingrates, yerr = dataset_to_fit.heatingrate_errors, marker = 'o', color='blue', linewidth=.5)


##### calculate reaction rates
R = 8.3145 * ureg.J / (ureg.mol * ureg.K)

def noisegrowth_fitfunction(time,heatingrate0,multiplier,k):
    heatingrate = heatingrate0 + multiplier*(1-np.exp(-k*time))
    return heatingrate

def fit_noisegrowth(days,rates,rateerrors):
    ## guess starting parameters
    heatingrate0, multiplier, k = 3, 3, 2
    popt,pcov = op.curve_fit(noisegrowth_fitfunction,days,rates,p0=[heatingrate0,multiplier,k],sigma=rateerrors,absolute_sigma=True)
    perr = np.sqrt(np.diag(pcov))
    heatingrate0 = ufloat(popt[0],perr[0])
    multiplier = ufloat(popt[1],perr[1])
    k = ufloat(popt[2],perr[2])
    return heatingrate0,multiplier,k

data_556 =[ ('20190925', 3, 0.88, ['1622_39'], ufloat(3.00, 0.14), 1.58, -1.490, 363),
        ('20190925', 3, 0.88, ['1910_01'], ufloat(3.01, 0.17), 1.58, -1.490, 363),
        ('20190926', 3, 0.88, ['1154_33'], ufloat(3.49, 0.13), 1.60, -1.500, 360),
        ('20190926', 3, 0.88, ['1731_57'], ufloat(3.45, 0.12), 1.60, -1.500, 363),
        ('20190927', 3, 0.88, ['1539_12'], ufloat(3.78, 0.14), 1.60, -1.500, 360),
        ('20190927', 3, 0.88, ['1724_30'], ufloat(3.61, 0.14), 1.60, -1.500, 360),
        ('20190930', 3, 0.88, ['1044_07'], ufloat(3.82, 0.12), 1.60, -1.500, 360),
        # # ('20190930', 3, 0.88, ['1222_36'], ufloat(5.03, 0.31), 1.66, -1.70, 390),
        # # ('20190930', 3, 0.88, ['1336_16'], ufloat(4.74, 0.26), 1.66, -1.70, 390),
        # # ('20190930', 3, 0.88, ['1347_53'], ufloat(4.89, 0.24), 1.66, -1.70, 390),
        ('20190930', 3, 0.88, ['1758_48'], ufloat(4.07, 0.16), 1.62, -1.49, 361),
        ('20191001', 3, 0.88, ['1357_35'], ufloat(4.34, 0.18), 1.62, -1.52, 358),
        # # ('20191001', 3, 0.88, ['1923_32'], ufloat(5.66, 0.25), 1.76, -1.89, 397),
        # # ('20191002', 3, 0.88, ['1143_05'], ufloat(4.97, 0.25), 1.76, -1.89, 390),
        # # ('20191002', 3, 0.88, ['1559_18'], ufloat(5.10, 0.22), 1.76, -1.88, 391),
        # # ('20191003', 3, 0.88, ['1315_37'], ufloat(4.87, 0.19), 1.76, -1.88, 395),
        # # ('20191003', 3,	0.88, ['1711_27'], ufloat(4.83, 0.16), 1.76, -1.88,	395),
        # # ('20191004', 3,	0.88, ['1507_17'], ufloat(5.08, 0.18), 1.76, -1.86,	396),
        # # ('20191004', 3,	0.88, ['1845_50'], ufloat(5.19, 0.40), 1.62, -1.49,	360),
        # ('20191007', 3,	0.88, ['1227_10'], ufloat(4.11, 0.15), 1.62, -1.46,	354),
        ('20191108', 3, 0.88, ['1357_35'], ufloat(5.0, 0.2), 1.62, -1.52, 360), #fake date
        ]


temperature_calibration = 'android_new_lens'
measurements_556 = [Measurement(date, electrode_number, trap_frequency, times_of_day, heatingrate, heater_current, fourwire_voltage, unscaled_temperature,temperature_calibration)
                       for date, electrode_number, trap_frequency, times_of_day, heatingrate, heater_current, fourwire_voltage, unscaled_temperature in data_556]
dataset_556 = Dataset(measurements_556)
dataset_556.offset_hours = -1
relative_days_556 = dataset_556.get_relative_times_day()

data_556_early = [ ('20190925', 3, 0.88, ['1622_39'], ufloat(3.00, 0.14), 1.58, -1.490, 363),
        ('20190925', 3, 0.88, ['1910_01'], ufloat(3.01, 0.17), 1.58, -1.490, 363),
        ('20190926', 3, 0.88, ['1154_33'], ufloat(3.49, 0.13), 1.60, -1.500, 360),
        ('20190926', 3, 0.88, ['1731_57'], ufloat(3.45, 0.12), 1.60, -1.500, 363),
        ('20190927', 3, 0.88, ['1539_12'], ufloat(3.78, 0.14), 1.60, -1.500, 360),
        ('20190927', 3, 0.88, ['1724_30'], ufloat(3.61, 0.14), 1.60, -1.500, 360),
        ('20190930', 3, 0.88, ['1044_07'], ufloat(3.82, 0.12), 1.60, -1.500, 360),
        ('20190930', 3, 0.88, ['1758_48'], ufloat(4.07, 0.16), 1.62, -1.49, 361),
        ('20191001', 3, 0.88, ['1357_35'], ufloat(4.34, 0.18), 1.62, -1.52, 358),
]
data_556_late = [
        ('20191108', 3, 0.88, ['1357_35'], ufloat(5.0, 0.2), 1.62, -1.52, 360), #fake date
]

measurements_556_early = [Measurement(date, electrode_number, trap_frequency, times_of_day, heatingrate, heater_current, fourwire_voltage, unscaled_temperature,temperature_calibration)
                       for date, electrode_number, trap_frequency, times_of_day, heatingrate, heater_current, fourwire_voltage, unscaled_temperature in data_556_early]
dataset_556_early = Dataset(measurements_556_early)
dataset_556_early.offset_hours = -1
relative_days_556_early = dataset_556_early.get_relative_times_day()

measurements_556_late = [Measurement(date, electrode_number, trap_frequency, times_of_day, heatingrate, heater_current, fourwire_voltage, unscaled_temperature,temperature_calibration)
                       for date, electrode_number, trap_frequency, times_of_day, heatingrate, heater_current, fourwire_voltage, unscaled_temperature in data_556_late]
dataset_556_late = Dataset(measurements_556_late)
dataset_556_late.offset_hours = -1
relative_days_556_late = [45]


####################################
pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('September 25, 556 K')
# ax.errorbar(relative_days_556,
#         dataset_556.heatingrates,
#         yerr = dataset_556.heatingrate_errors,
#         fmt = '-o',)
ax.errorbar(relative_days_556_early,
        dataset_556_early.heatingrates,
        yerr = dataset_556_early.heatingrate_errors,
        fmt = '-o',)


heatingrate0_556, multiplier_556, k_556 = fit_noisegrowth(relative_days_556, dataset_556.heatingrates, dataset_556.heatingrate_errors)

print "heatingrate0_556: "+ str(heatingrate0_556)
print "multiplier_556: "+ str(multiplier_556)
print "k_556 (1/day):"+ str(k_556)

times = np.linspace(-1,50,1000)
heatingrates = [noisegrowth_fitfunction(time, heatingrate0_556.nominal_value, multiplier_556.nominal_value, k_556.nominal_value) for time in times]
ax.plot(times,heatingrates)

ax.errorbar(relative_days_556_late,
        dataset_556_late.heatingrates,
        yerr = dataset_556_late.heatingrate_errors,
        fmt = '-o',)


pyplot.xlabel('Days at 556 K')
pyplot.ylabel('Heating Rate(nbar/ms)')
#################################

dataset_556_avg = Dataset(measurements_556).bin_each_day()
dataset_556_avg.offset_hours = -3
relative_days_556_avg = dataset_556_avg.get_relative_times_day()
temperature_average = sum(dataset_556_avg.temperatures)/len(dataset_556_avg.temperatures)

pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('Heat treatment post Mill 10')
ax.errorbar(relative_days_556_avg,
        dataset_556_avg.heatingrates,
        yerr = dataset_556_avg.heatingrate_errors,
        fmt = '-o',)

heatingrate0_577, multiplier_577, k_577 = fit_noisegrowth(relative_days_556_avg, dataset_556_avg.heatingrates, dataset_556_avg.heatingrate_errors)

print "heatingrate0_556 averaged: "+ str(heatingrate0_556)
print "multiplier_556 averaged: "+ str(multiplier_556)
print "k_556 averaged: "+ str(k_556)
print "average temperature:"+ str(temperature_average)

times = np.linspace(-1,50,1000)
heatingrates = [noisegrowth_fitfunction(time, heatingrate0_556.nominal_value, multiplier_556.nominal_value, k_556.nominal_value) for time in times]
ax.plot(times,heatingrates)
pyplot.xlabel('Days at 556 K')
pyplot.ylabel('Heating Rate(nbar/ms)')


####################################

########################

data_577 =[ ['20190606', 3,	0.88, ['1534_23'], ufloat(6.02, 0.25), 1.69, -1.75, 415],
        ['20190606', 3,	0.88, ['1628_10'], ufloat(6.11, 0.49), 1.69, -1.75, 415],
        ['20190606', 3,	0.88, ['1740_20'], ufloat(6.78, 0.40), 1.69, -1.75, 415],
        ['20190606', 3,	0.88, ['1818_00'], ufloat(5.89, 0.71), 1.69, -1.75, 415],
        ['20190606', 3,	0.88, ['1838_55'], ufloat(6.19, 0.27), 1.69, -1.75, 415],
        ['20190606', 3,	0.88, ['1904_58'], ufloat(5.28, 0.28), 1.69, -1.75, 415],
        ['20190607', 3,	0.88, ['1041_16'], ufloat(6.43, 0.26), 1.69, -1.79, 417],
        # ['20190607', 3,	0.88, ['1428_12'], ufloat(6.93, 0.30), 1.55, -1.37, 363],
        ['20190607', 3,	0.88, ['1624_45'], ufloat(6.74, 0.31), 1.74, -1.87, 410],
        ['20190607', 3,	0.88, ['1659_04'], ufloat(7.49, 0.48), 1.79, -2.01, 421],
        # ['20190607', 3,	0.88, ['1746_57'], ufloat(7.40, 0.38), 1.82, -2.09, 428],
        # ['20190607', 3,	0.88, ['1835_42'], ufloat(7.40, 0.36), 1.85, -2.18, 437],
        ['20190607', 3,	0.88, ['1947_20'], ufloat(7.02, 0.32), 1.72, -1.87, 417],
        ['20190610', 3,	0.88, ['1205_39'], ufloat(7.88, 0.31), 1.72, -1.85, 412],
        # ['20190610', 3,	0.88, ['1638_59'], ufloat(7.86, 0.35), 1.55, -1.36, 354],
        # ['20190610', 3,	0.88, ['1916_48'], ufloat(14.78, 0.75), 1.9, -2.34, 446],
        ['20190610', 3,	0.88, ['2054_30'], ufloat(7.60, 0.37), 1.72, -1.80, 417],
        # ['20190611', 3,	0.88, ['1306_36'], ufloat(9.16, 0.41), 1.72, -1.82, 410], #questionable data
        # ['20190613', 3,	0.88, ['1404_33'], ufloat(10.10, 0.79), 1.72,	-1.81,410], #questionable data
        ['20190613', 3,	0.88, ['1500_56'], ufloat(7.82, 0.40), 1.72, -1.82, 410],
        ['20190613', 3,	0.88, ['1615_29'], ufloat(8.11, 0.46), 1.72, -1.75, 410]
        ]

temperature_calibration = 'android_new_lens'
measurements_577 = [Measurement(date, electrode_number, trap_frequency, times_of_day, heatingrate, heater_current, fourwire_voltage, unscaled_temperature,temperature_calibration)
                       for date, electrode_number, trap_frequency, times_of_day, heatingrate, heater_current, fourwire_voltage, unscaled_temperature in data_577]
dataset_577 = Dataset(measurements_577)
dataset_577.offset_hours = -1
relative_days_577 = dataset_577.get_relative_times_day()

pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('June 6, 577 K')
ax.errorbar(relative_days_577,
        dataset_577.heatingrates,
        yerr = dataset_577.heatingrate_errors,
        fmt = '-o',)

heatingrate0_577, multiplier_577, k_577 = fit_noisegrowth(relative_days_577, dataset_577.heatingrates, dataset_577.heatingrate_errors)

print "heatingrate0_577: "+ str(heatingrate0_577)
print "multiplier_577: "+ str(multiplier_577)
print "k_577: "+ str(k_577)

times = np.linspace(0,15,1000)
heatingrates = [noisegrowth_fitfunction(time, heatingrate0_577.nominal_value, multiplier_577.nominal_value, k_577.nominal_value) for time in times]
ax.plot(times,heatingrates)
pyplot.xlabel('Days at 577 K')
pyplot.ylabel('Heating Rate(nbar/ms)')

######################
dataset_577_avg = Dataset(measurements_577).bin_each_day()
dataset_577_avg.offset_hours = -3
relative_days_577_avg = dataset_577_avg.get_relative_times_day()
temperature_average = sum(dataset_577_avg.temperatures)/len(dataset_577_avg.temperatures)

pyplot.figure()
ax = pyplot.axes(xscale='linear',yscale='linear')
pyplot.title('Heat treatment post Mill 7')
ax.errorbar(relative_days_577_avg,
        dataset_577_avg.heatingrates,
        yerr = dataset_577_avg.heatingrate_errors,
        fmt = '-o',)

heatingrate0_577, multiplier_577, k_577 = fit_noisegrowth(relative_days_577_avg, dataset_577_avg.heatingrates, dataset_577_avg.heatingrate_errors)

print "heatingrate0_577 averaged: "+ str(heatingrate0_577)
print "multiplier_577 averaged: "+ str(multiplier_577)
print "k_577 averaged: "+ str(k_577)
print "average temperature:"+ str(temperature_average)

times = np.linspace(0,15,1000)
heatingrates = [noisegrowth_fitfunction(time, heatingrate0_577.nominal_value, multiplier_577.nominal_value, k_577.nominal_value) for time in times]
ax.plot(times,heatingrates)
pyplot.xlabel('Days at 577 K')
pyplot.ylabel('Heating Rate(nbar/ms)')



##### Based on actual fits:
R = 8.3145 * ureg.J / (ureg.mol * ureg.K)
k1=.50 * 1/ ureg.day
T1 = 556.0 * ureg.K

k2=.56 * 1/ureg.day
T2 = 577.0 * ureg.K

E = np.log((k1/k2)) * R / (-1/T1 + 1/T2)


print 'from fit, reaction energy E = ' + str(E.to('kJ/mol'))
print '44 kJ/mol ~ 0.5 eV'

R = 8.3145 * ureg.J / (ureg.mol * ureg.K)
k1=ufloat(.141,.032) #* 1/ ureg.day
T1 = ufloat(556.0,2.0) #* ureg.K
half_life_1 = np.log(2)/k1

k2=ufloat(.56,.22) #* 1/ureg.day
T2 = ufloat(577.0,2.0) #* ureg.K
half_life_2 = np.log(2)/k2

print "half life 556 K: " + str(half_life_1)
print "half life 577 K: " + str(half_life_2)

E = umath.log((k1/k2)) * 8.3145 / (-1/T1 + 1/T2) /1000

print 'from fit, reaction energy E (kJ/mol)= ' + str(E)



pyplot.show()





######## Calculating reaction rates from heating experiments ##########

# k = A*exp(-E/RT)
# k = reaction rate, units 1/time
# E = reaction energy, units eV or kJ/mol
# T = temperature in Kelvin
# A = 'collision rate' or, on a surface, the rate at which the reactants interact with the catalyst.
# A is proportional to the available catalysts * reactants, or in the case of reactions that don't need a catalyst, just the smallest available reactant.
# The saturated noise magnitude should also be proportional to the available catalysts and reactants
# Therefore, A is proportional to the saturated noise magnitude (the absolute increase, not the % increase)
# sidenote - the metal must be part of the final product. Otherwise, as soon as the catalyst metal became available, the noise should have just have slowly gone up and up, not saturated.
# The product must cover the metal. But then shouldn't the signal go down? - not if the contaminants were already there, just differently bound.

#
# R = 8.3145 * ureg.J / (ureg.mol * ureg.K)
# # kb = 8.6173 * 10**(-5) * ureg.eV / ureg.K
#
# # these are approximations. With some plotting, may be possible to calculate better
#
# # This is based on June 4 0.88 MHz data
# T1 = 579 * ureg.K
# t1 = 3.5 * ureg.day
# noiseAdded1 = 4.5
#
# # This is roughly based on May 10 data, .88 MHz
# T2 = 546 * ureg.K
# t2 = 4 * ureg.day #+- 1 day
#
# noiseAdded2 = 8.5
#
# k1 = np.log2(2)/t1
# k2 = np.log2(2)/t2
#
# #A1/A2 = noiseAdded1/noiseAdded2
#
# E = np.log((k1/k2)*(noiseAdded2/noiseAdded1)) * R / (-1/T1 + 1/T2)
#
# # print 'reaction energy E = ' + str(E.to('eV'))
# print 'reaction energy E = ' + str(E.to('kJ/mol'))
#
#
# A1 = k1 / np.exp(-E/(R*T1))
# A2 = k2 / np.exp(-E/(R*T2))
#
# print 'attempt rate A1 = ' + str(A1.to('Hz'))
# print 'attempt rate A2 = ' + str(A2.to('Hz'))
#
# def reactionrate(temp,A):
#     return A*np.exp(-E/(R*temp*ureg.K))
#
# print 'May 10 time per reaction, room temperature = ' + str(1/reactionrate(295,A2).to('1/year'))
# print 'May 10 time per reaction, 575 K = ' + str(1/reactionrate(575,A2))
# print 'May 10 time per reaection, 615 K = ' + str(1/reactionrate(615,A2).to('1/hour'))
#
# print 'June 4 time per reaction, room temperature = ' + str(1/reactionrate(295,A1).to('1/year'))
# print 'June 4 time per reaction, 575 K = ' + str(1/reactionrate(575,A1))
# print 'June 4 time per reaection, 615 K = ' + str(1/reactionrate(615,A1).to('1/hour'))
#
# def relativetempeffect(T1,T2,E):
#     return np.exp(-E/(R*T1)) / np.exp(-E/(R*T2))
#
#
# print relativetempeffect(595*ureg('K'),546*ureg('K'),6*ureg('kJ/mol'))
# print relativetempeffect(595*ureg('K'),546*ureg('K'),38*ureg('kJ/mol'))
# print relativetempeffect(595*ureg('K'),546*ureg('K'),61*ureg('kJ/mol'))
#
#
# ### if t2 = 2 days, Energy = 6 kJ/mole =  0.06 eV, exp(-E/k600K)/exp(-E/k500K) = 1.3
# ### if t2 = 3 days, Energy = 38 kJ/mole = 0.38 eV, exp(-E/k579K)/exp(-E/k563K) = 4.5 *** This one is most likely
# ### if t2 = 4 days, Energy = 61 kJ/mole =  0.61 eV, exp(-E/k579K)/exp(-E/k563K) = 11.5
# ### So I could be off by a factor of 3 or so. Not too bad
#

#
# def heat_at_temp(t, initial_value, A, C, Ea, T):
#     return initial_value + C * (1 - np.exp(-A * np.exp(-Ea / (R * T)) * t))
#
# def piecewise_fit_function(times, initial_value, A, C, Ea):
#     list_of_times = dataset_to_fit.get_relative_times(offset_hours = -1)
#     t6 = list_of_times[6]
#     t7 = list_of_times[7]
#     t8 = list_of_times[8]
#
#     noise_interval_1 = heat_at_temp(t6, initial_value, C, A, Ea, T=534)
#     noise_interval_2 = heat_at_temp(t7-t6, initial_value, C, A, Ea, T=561)
#     noise_interval_3 = heat_at_temp(t8-t7, initial_value, C, A, Ea, T=534)
#
#     result =  [np.piecewise(t,
#                  [t<=t6, t6<t<=t7, t7<t<=t8, t>t8],
#                  [lambda t: heat_at_temp(t, initial_value, C, A, Ea, T=534),
#                   lambda t: noise_interval_1 + heat_at_temp(t-t6, initial_value, C, A, Ea, T=561),
#                   lambda t: noise_interval_1 + noise_interval_2 + heat_at_temp(t-t7, initial_value, C, A, Ea, T=534),
#                   lambda t: noise_interval_1 + noise_interval_2 + noise_interval_3 + heat_at_temp(t-t8, initial_value, C, A, Ea, T=561)
#                  ])
#           for t in times]
#     print [array[0] for array in result]
#     return [array[0] for array in result]
#
# def fit_heat_treatment(times,heatingrates,heatingrate_errors):
#     # p0 = [initial_value, A, C, Ea]
#     p0=[3, 3, 100, 50]
#     bounds = ([0, 0, 0, 0], [5, np.inf, np.inf, np.inf])
#
#     optimal_parameters, parameter_covariance = op.curve_fit(piecewise_fit_function, times, heatingrates, p0=p0, sigma=heatingrate_errors, absolute_sigma=True)
#     # optimal_parameters, parameter_covariance = op.curve_fit(test_function, times, heatingrates, p0=p0, sigma=heatingrate_errors, absolute_sigma=True)
#     # optimal_parameters, parameter_covariance = op.curve_fit(fit_function_vec, times, heatingrates, p0=p0, bounds = bounds, sigma=heatingrate_errors, absolute_sigma=True)
#
#     initial_value, A, C, Ea = optimal_parameters
#     parameter_error = np.sqrt(np.diag(parameter_covariance))
#
#     # r = heatingrates - piecewise_fit_function(initial_value, A, C, Ea, times, times)
#     # chisq = sum((r/rerr)**2)
#  #   print 'reduced chisq',chisq/(len(T)-len(popt))
#
#     plot_times = np.arange(min(times),max(times),(max(times)-min(times))/100)
#
#     result = piecewise_fit_function(plot_times, initial_value, A, C, Ea)
#     # result = [test_function(initial_value, A, C, Ea, t) for t in plot_times]
#     print result
#
# #    return tmps,result,p
#     print "initial_value, A, C, Ea:"
#     print initial_value, A, C, Ea
#     return plot_times, result
#
#
# fit_times = dataset_to_fit.get_relative_times(offset_hours = -1)
# fit_heatingrates = dataset_to_fit.heatingrates
# fit_heatingrate_errors = dataset_to_fit.heatingrate_errors
#
# plot_times, result = fit_heat_treatment(fit_times, fit_heatingrates, fit_heatingrate_errors)
#
# pyplot.figure()
# ax = pyplot.axes(xscale='linear',yscale='linear')
# ax.plot(plot_times, result)

#
#
# R = 8.3145 * ureg.J / (ureg.mol * ureg.K)
#
#
#
# # data = ['Data/Data_ToaST/E3_tempscaling_hysteresis_10May2019.txt',2]
# # data =['Data/Data_ToaST/E3_tempscaling_hysteresis_04Jun2019.txt',3]
# # data = ['Data/Data_ToaST/E3_tempscaling_16Jul2019_postmill8dandE3Auger.txt',3]
# # data = ['Data/Data_ToaST/E3_tempscaling_03Sep2019_postelectronmill8e.txt',0]
# data = ['Data/Data_ToaST/E3_tempscaling_24Sep2019_postmill10.txt',3]
# tempcalibration = data[1]
# filename = data[0]
# mydata = np.loadtxt(filename,skiprows=1)
# mydata = np.array(scale_temp(mydata,tempcalibration))
# mytrapfreq = mydata[:,1]
# mytemperature = mydata[:,6]
# myrates = mydata[:,2]
# myrateerror = mydata[:,3]
#
#
# # datas = [['Data/Data_ToaST/E3_TempAndFreqScaling_07mar2019_up.txt',1],
# #     ['Data/Data_ToaST/E3_TempAndFreqScaling_14mar2019_down.txt',1],
# #     ['Data/Data_ToaST/E3_tempscaling_08Apr2019.txt',2]]
#
#
# # # combine all data
# # mytrapfreq=[]
# # mytemperature=[]
# # myrates=[]
# # myrateerror=[]
# # for i in range(len(datas)):
# #     tempcalibration = datas[i][1]
# #     filename = datas[i][0]
# #     loaddata = np.loadtxt(filename,skiprows=1)
# #     scaleddata = np.array(scale_temp(loaddata,tempcalibration))
# #     mytrapfreq.extend(scaleddata[:,1])
# #     mytemperature.extend(scaleddata[:,6])
# #     myrates.extend(scaleddata[:,2])
# #     myrateerror.extend(scaleddata[:,3])
#
#
# freqs=[.88,1.3]
#
# # color = [['black','grey'],['red','orange']]
#
# for i in range(len(freqs)):
#
#     pyplot.figure()
#     ax = pyplot.axes(xscale='linear',yscale='linear')
#     pyplot.xlabel('Temperature(K)')
#     pyplot.ylabel('nbar/ms')
#     pyplot.title('Temperature Scaling')
#     # pyplot.ylim(0,17)
#
#     plotrates=[]
#     plotrateerr=[]
#     plottemp=[]
#
#     for j in range(len(mytrapfreq)):
#       if round(mytrapfreq[j],2)==freqs[i]:
#         plotrates.append(myrates[j])
#         plotrateerr.append(myrateerror[j])
#         plottemp.append(mytemperature[j])
#
#     rainbow_colors = cm.jet(np.linspace(1, 0, len(plotrates)))
#     if len(plotrates) != 0:
#       # ax.errorbar(plottemp,plotrates,yerr=plotrateerr,fmt='-o',capsize=3,color=color[i][0],label="0.88 MHz")
#       line = ax.errorbar(plottemp,plotrates,yerr=plotrateerr,fmt='-',capsize=3,color='gray', linewidth=.5, elinewidth=1)
#       ax.scatter(plottemp,plotrates,color=rainbow_colors,label=str(freqs[i])+" MHz", zorder=100)
#
#     pyplot.legend()
#
# # pyplot.show()


