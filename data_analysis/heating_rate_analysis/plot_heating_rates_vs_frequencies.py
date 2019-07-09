
from matplotlib import pyplot as plt
from sqip_rate_from_flops import fit_freq_scaling


##Before Auger on Trap

##Electrode 3
## Date data was taken (yymmdd)
Dates= [170726,170726,170727,170727,170727,170727,170727,170728,170728,170804,170804,170807,170807,170807,170808,170808]
##trap frequency
E3_freq = [1.347,1.347,1.349,1.527,1.0137,0.7955,0.491,1.247,0.6133,1.354,1.018,1.018,0.63,0.63,1.026,0.631]
##heating rate
E3_hRate = [3.2,2.87,2.92,2.41,5.11,9.41,23.35,3.88,17.67,2.63,5.14,4.59,25.45,17.22,5.21,16.62]
## error on heating rate
E3_error= [0.15,0.08,0.09,0.12,0.19,0.54,2.33,0.17,0.88,0.24,0.31,0.30,3.0,1.59,0.30,1.18]

E3_error.pop(-4)
E3_freq.pop(-4)
E3_hRate.pop(-4)

##Electrode 8
Dates= [170719,170719,170720,170720,170721,170721,170712,170712,170712,170712,170713,170713,170713,170713,170713,170713,170713,170713,170713]
E8_freq = [0.857,0.857,0.844,0.846,1.4098,0.358,1.4348,1.3322,1.2159,1.1151,1.1151,1.02,0.9041,0.8052,0.6546,0.5344,0.4639,0.4639,0.355]
E8_hRate = [6.24,6.34,7.65,7.16,2.59,32.1,2.33,2.88,2.93,3.89,3.46,4.19,6.33,6.05,10.15,19.62,23.25,25.19,52.42]
E8_error= [0.31,0.30,0.34,0.16,0.26,1.11,0.05,0.11,0.22,0.19,0.39,0.34,0.37,0.61,1.66,0.81,0.41,0.89,3.57]


##After Auger on Trap
Dates= [170815,170815,170815,170815,170816,170816,170816]
af_E8_freq = [0.99,0.99,1.225,0.67,0.4996,0.4996,0.4996]
af_E8_hRate = [5.63,7.14,3.83,20.28,20.14,29.78,40.17]
af_E8_error= [0.41,0.9,0.22,1.39,4.53,1.63,1.62]




##Heater On
Dates=[170817,170817,170817]
Heater_E8_freq = [0.9432,0.9432,0.9432]
Heater_E8_hRate = [51.12,26.22,11.66]
Heater_E8_error= [3.11,6.84,2.11]
Power_E8=[0.0382,0.0382,0.033] 

Heater_E8_freq = [0.9432]
Heater_E8_hRate = [11.66]
Heater_E8_error= [2.11]
Power_E8=[0.033] 


##Heater connection tests
Dates=[170822,170822,170822,170822,170822,170822]
HTest_E8_freq = [.8117,.8117,.8117,.8117,.8117,.8117]
HTest_E8_hRate = [9.2, 10.91, 11.9, 9.52, 10.1, 9.29]
HTest_E8_error= [.97,1.95,2.26,0.64,1.39,1.13]

##August 24 and later; post Auger and heater maybe a little bit
Dates=[170824,170824,170825,170825,170825]
af24_E8_freq = [.8968,.8110,.4279,.6009,1.4106]
af24_E8_hRate = [8.78,9.7,41.68,21.09,3.72]
af24_E8_error= [.52,1.02,4.0,2.08,0.13]

af24_E8_freq.extend(af_E8_freq)
af24_E8_hRate.extend(af_E8_hRate)
af24_E8_error.extend(af_E8_error)

##E3 after auger week of 8/28
af_E3_freq = [1.133, 0.7016, 0.7016, 0.7014, 0.6014, 0.5440, 0.6539, 0.7033, 0.7904, 0.9054, 1.009, 1.009, 1.131, 1.2425, 1.3447]
af_E3_hrate = [5.16, 16.00, 12.92, 18.27, 21.27, 30.34, 17.41, 15.03, 10.64, 9.47, 7.53, 7.46, 4.62, 3.86, 3.45]
af_E3_error = [0.97, 1.15, 1.36, 2.71, 2.82, 0.82, 1.71, 2.27, 0.96, 0.83, .49, 0.56, 0.42, 0.36, 0.30]

plt.figure()
plt.ylabel('Heating Rate (quanta/ms)')
plt.xlabel('Frequency (MHz)')
plt.xscale('log')
plt.xlim( 0.3, 2 )
plt.yscale('log', nonposy='clip')

#plt.errorbar(E8_freq,E8_hRate,yerr=E8_error, fmt= '.',color= 'black',label='Electrode 8')

plt.errorbar(E3_freq,E3_hRate,yerr=E3_error, fmt= '.',color= 'r',label='Electrode 3')



#plt.errorbar(af_E8_freq,af_E8_hRate,yerr=af_E8_error, fmt= '.',color= 'b',label='Electrode 8 After Auger')
#plt.errorbar(Heater_E8_freq,Heater_E8_hRate,yerr=Heater_E8_error, fmt= '.',color= 'g',label='Heater On')
#plt.errorbar(HTest_E8_freq,HTest_E8_hRate,yerr=HTest_E8_error, fmt= '.',color= 'r',label='Test')
plt.errorbar(af24_E8_freq,af24_E8_hRate,yerr=af24_E8_error, fmt= '.',color= 'b',label='E8 after Auger')

plt.errorbar(af_E3_freq,af_E3_hrate,yerr=af_E3_error, fmt= '.',color= 'purple',label='E3 after Auger')
##this section is for shading
#print fit_freq_scaling(E8_freq,E8_hRate,E8_error,mycolor= 'black')#,label='Electrode 8 fit')
print fit_freq_scaling(E3_freq,E3_hRate,E3_error,mycolor= 'r')#,label='Electrode 3 fit ')
#print fit_freq_scaling(af24_E8_freq,af24_E8_hRate,af24_E8_error,mycolor= 'b')#,label='E8 after Auger')

print fit_freq_scaling(af24_E8_freq,af24_E8_hRate,af24_E8_error,mycolor= 'b',label='Electrode 8 after Auger fit ')

plt.legend(loc = 'lower left')
plt.title('Heating Rates Before and after Auger')
plt.show()