import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import auger_master as ft

### Plot various elements as a function of milling dose, and plot % increase in heating rates as a function of milling dose ###

'''
Z2= 79. #Atomic number of element of substrate
Z1= 18. #Atomic number of element of beam
M2= 196.967 #Atomic mass number of element of substrate
M1= 39.948 #Atomic mass number of element of beam
E= 2e3 #Ion beam energy in eV
US= 3.81 #Sublimation energy of substrate in eV from table 1 of "Enery dependence of the ion induced sputtering yields of monatomic solids" N. Matsunami et al
Q= 1.04 #Fit parameter of substrate from table 1 of "Enery dependence of the ion induced sputtering yields of monatomic solids" N. Matsunami et al
'''

#####Method 1 from "Evidence for multiple mechanisms underlying surface electric-field noise in ion traps" J. A. Sedlacek et al#########

#Sensitivity factor Email with OCVIM company who made our auger
carbon_sensitivity=.2426 #Carbon
#titanium_sensitivity=.3297 #Titanium
titanium_sensitivity=.2685 #Titanium387
oxygen_sensitivity=.3023  #Oxygen
copper_sensitivity=.0639 #Copper
aluminum_sensitivity=.0076 #Aluminum
nitrogen_sensitivity=.0921  #Nitrogen

#Intenistiy peak to peak in June 2018 pre mill
intensity_peak2peak_JC=21.9e-3 #Carbon
#intensity_peak2peak_JTi=1.35e-3#Titanium
intensity_peak2peak_JN=2.776e-3#Nitrogen Ti387 peak
intensity_peak2peak_JTi=2.776e-3#Ti387
intensity_peak2peak_JO=12.7e-3 #Oxygen
intensity_peak2peak_JCu=232.e-6#Copper
intensity_peak2peak_JAl=289.e-6#Aluminum

#Intenistiy peak to peak in May 2019 post mill 6
intensity_peak2peak_MC=17.6e-3 #Carbon
#intensity_peak2peak_MTi=1.02e-3#Titanium
intensity_peak2peak_MN=1.45e-3#Nitrogen Ti387 peak
intensity_peak2peak_MTi=1.45e-3#Ti387
intensity_peak2peak_MO=5.e-3   #Oxygen
intensity_peak2peak_MCu=1.04e-3#Copper
intensity_peak2peak_MAl=.94e-3 #Aluminum

#Intensity peak to peak in May 2019 after heating post heat mill 6
intensity_peak2peak_MC_after_heat=12.661e-3#Carbon
#intensity_peak2peak_MTi_after_heat=.53e-3#Titanium
intensity_peak2peak_MN_after_heat=1.31e-3#Nitrogen Ti387 peak
intensity_peak2peak_MTi_after_heat=1.31e-3#Ti387
intensity_peak2peak_MO_after_heat=5.43e-3 #Oxygen
intensity_peak2peak_MCu_after_heat=.66e-3#Copper
intensity_peak2peak_MAl_after_heat=.831e-3#Aluminum

#Intensity peak to peak in June 2019 post mill 7
intensity_peak2peak_J2C=6.3e-3  #Carbon
#intensity_peak2peak_J2Ti=1.29e-3#Titanium
intensity_peak2peak_J2N=4.71e-3#Nitrogen Ti387 peak
intensity_peak2peak_J2Ti=4.71e-3#Ti387
intensity_peak2peak_J2O=3.5e-3  #Oxygen
intensity_peak2peak_J2Cu=.92e-3 #Copper
intensity_peak2peak_J2Al=.94e-3 #Aluminum
intensity_peak2peak_JC2=6.3e-3  #Carbon
#intensity_peak2peak_JTi2=1.29e-3#Titanium
intensity_peak2peak_JN2=4.71e-3#Nitrogen Ti387 peak
intensity_peak2peak_JTi2=4.71e-3#Ti387
intensity_peak2peak_JO2=3.5e-3  #Oxygen
intensity_peak2peak_JCu2=.92e-3 #Copper
intensity_peak2peak_JAl2=.94e-3 #Aluminum

#Intensity peak to peak in June 2019 after heating post mill 7
intensity_peak2peak_J2C_after_heat=7.3e-3  #Carbon
#intensity_peak2peak_J2Ti_after_heat=.69e-3#Titanium
intensity_peak2peak_J2N_after_heat=3.288e-3#Nitrogen Ti387 peak
intensity_peak2peak_J2Ti_after_heat=3.288e-3#Ti387
intensity_peak2peak_J2O_after_heat=3.9e-3  #Oxygen
intensity_peak2peak_J2Cu_after_heat=.59e-3 #Copper
intensity_peak2peak_J2Al_after_heat=.78e-3 #Aluminum

#Intensity peak to peak in July 2019 after mill8D
intensity_peak2peak_J3C=4.42  #Carbon
#intensity_peak2peak_J3Ti=.609#Titanium
intensity_peak2peak_J3N=9.6#Nitrogen Ti387 peak
intensity_peak2peak_J3Ti=9.6#Ti387
intensity_peak2peak_J3O=7.44  #Oxygen
intensity_peak2peak_J3Cu=.37 #Copper
intensity_peak2peak_J3Al=.62 #Aluminum

#Intenstiy peak to peak in August 2019 after mill 8e
intensity_peak2peak_AC=3.63#Carbon
#intensity_peak2peak_ATi=.518#Titanium
intensity_peak2peak_AN=8.8#Nitrogen Ti387 peak
intensity_peak2peak_ATi=8.8#Ti387
intensity_peak2peak_AO=6.14#Oxygen
intensity_peak2peak_ACu=.17#Copper
intensity_peak2peak_AAl=.44#Aluminum

#Atomic Diameter in nanometers
atomic_diameter_C=.14e-9   #Carbon
atomic_diameter_Ti=.294e-9 #Titanium
atomic_diameter_O=.120e-9  #Oxygen
atomic_diameter_Cu=.256e-9 #Copper
atomic_diameter_Al=.286e-9 #Aluminum
#
###################FOR MILLINGS 1-4######################

SRFJ=(intensity_peak2peak_JC/carbon_sensitivity)+(intensity_peak2peak_JTi/titanium_sensitivity)+(intensity_peak2peak_JO/oxygen_sensitivity)+(intensity_peak2peak_JCu/copper_sensitivity)+(intensity_peak2peak_JAl/aluminum_sensitivity)
SRFM=(intensity_peak2peak_MC/carbon_sensitivity)+(intensity_peak2peak_MTi/titanium_sensitivity)+(intensity_peak2peak_MO/oxygen_sensitivity)+(intensity_peak2peak_MCu/copper_sensitivity)+(intensity_peak2peak_MAl/aluminum_sensitivity)
SRFJ2=(intensity_peak2peak_J2C/carbon_sensitivity)+(intensity_peak2peak_J2Ti/titanium_sensitivity)+(intensity_peak2peak_J2O/oxygen_sensitivity)+(intensity_peak2peak_J2Cu/copper_sensitivity)+(intensity_peak2peak_J2Al/aluminum_sensitivity)



#Lattice Constants, height in meters
lattice_constant_carbon=.405e-9#.671e-9 #Carbon
lattice_constant_Ti=.405e-9#.469e-9#Titanium
lattice_constant_O=.405e-9#.509e-9 #Oxygen
lattice_constant_Cu=.405e-9#.361e-9#Copper
lattice_constant_Alattice_constant_=.405e-9#Aluminum


#Cumulative Dose in J/cm^2
HR=[7.59,5.55,5.3,5.01,3.79,3.01,2.5,1.75,2.46,1.11,2.95,1.08]
HRErr=[0.23,0.31,0.22,0.19,0.13,0.12,0.11,0.09,0.11,0.05,0.14,0.05]
CumulDose=[0,.12,.24,.78,2.14,5.14,13.89,23.89]
# plt.figure
#Atomic concentrations after milling
carbon_concentration=[]
titanium_concentration=[]
Al_concentration=[]
copper_concentration=[]
oxygen_concentration=[]
nitrogen_concentration=[]

#Sensitivity factor Email with OCVIM company who made our auger
carbon_sensitivity=.2426 #Carbon
#titanium_sensitivity=.3297 #Titanium
titanium_sensitivity=.2685 #Titanium387
oxygen_sensitivity=.3023  #Oxygen
copper_sensitivity=.0639 #Copper
aluminum_sensitivity=.0076 #Aluminum
nitrogen_sensitivity=.0921  #Nitrogen

#Atomic concentrations After Heating
carbon_concentration_after_heat=[]
titanium_concentration_after_heat=[]
Al_concentration_after_heat=[]
copper_concentration_after_heat=[]
oxygen_concentration_after_heat=[]
nitrogen_concentration_after_heat=[]


Mcarbon_concentration=[]
Mtitanium_concentration=[]
MAl_concentration=[]
Mcopper_concentration=[]
Moxygen_concentration=[]

Dayx=[1,2,3]

SRFJ=(intensity_peak2peak_JC/carbon_sensitivity)+(intensity_peak2peak_JTi/titanium_sensitivity)+(intensity_peak2peak_JO/oxygen_sensitivity)+(intensity_peak2peak_JCu/copper_sensitivity)+(intensity_peak2peak_JAl/aluminum_sensitivity)#+(intensity_peak2peak_JN/nitrogen_sensitivity)
carbon_concentration.append(((intensity_peak2peak_JC/carbon_sensitivity)/SRFJ))
titanium_concentration.append(((intensity_peak2peak_JTi/titanium_sensitivity)/SRFJ))
oxygen_concentration.append((intensity_peak2peak_JO/oxygen_sensitivity)/SRFJ)
copper_concentration.append((intensity_peak2peak_JCu/copper_sensitivity)/SRFJ)
Al_concentration.append((intensity_peak2peak_JAl/aluminum_sensitivity)/SRFJ)
#nitrogen_concentration.append((intensity_peak2peak_JN/nitrogen_sensitivity)/SRFJ)

SRFM=(intensity_peak2peak_MC/carbon_sensitivity)+(intensity_peak2peak_MTi/titanium_sensitivity)+(intensity_peak2peak_MO/oxygen_sensitivity)+(intensity_peak2peak_MCu/copper_sensitivity)+(intensity_peak2peak_MAl/aluminum_sensitivity)#+(intensity_peak2peak_MN/nitrogen_sensitivity) #sum of relative frequencies
carbon_concentration.append((intensity_peak2peak_MC/carbon_sensitivity)/SRFM)
titanium_concentration.append(((intensity_peak2peak_MTi/titanium_sensitivity)/SRFM))
oxygen_concentration.append((intensity_peak2peak_MO/oxygen_sensitivity)/SRFM)
copper_concentration.append((intensity_peak2peak_MCu/copper_sensitivity)/SRFM)
Al_concentration.append((intensity_peak2peak_MAl/aluminum_sensitivity)/SRFM)
#nitrogen_concentration.append((intensity_peak2peak_MN/nitrogen_sensitivity)/SRFM)

SRFM_after_heat=(intensity_peak2peak_MC_after_heat/carbon_sensitivity)+(intensity_peak2peak_MTi_after_heat/titanium_sensitivity)+(intensity_peak2peak_MO_after_heat/oxygen_sensitivity)+(intensity_peak2peak_MCu_after_heat/copper_sensitivity)+(intensity_peak2peak_MAl_after_heat/aluminum_sensitivity)#+(intensity_peak2peak_MN_after_heat/nitrogen_sensitivity) #sum of relative frequencies
carbon_concentration_after_heat.append((intensity_peak2peak_MC_after_heat/carbon_sensitivity)/SRFM_after_heat)
titanium_concentration_after_heat.append(((intensity_peak2peak_MTi_after_heat/titanium_sensitivity)/SRFM_after_heat))
oxygen_concentration_after_heat.append((intensity_peak2peak_MO_after_heat/oxygen_sensitivity)/SRFM_after_heat)
copper_concentration_after_heat.append((intensity_peak2peak_MCu_after_heat/copper_sensitivity)/SRFM_after_heat)
Al_concentration_after_heat.append((intensity_peak2peak_MAl_after_heat/aluminum_sensitivity)/SRFM_after_heat)
#nitrogen_concentration_after_heat.append((intensity_peak2peak_MN_after_heat/nitrogen_sensitivity)/SRFM_after_heat)

SRFJ2=(intensity_peak2peak_J2C/carbon_sensitivity)+(intensity_peak2peak_J2Ti/titanium_sensitivity)+(intensity_peak2peak_J2O/oxygen_sensitivity)+(intensity_peak2peak_J2Cu/copper_sensitivity)+(intensity_peak2peak_J2Al/aluminum_sensitivity)#+(intensity_peak2peak_J2N/nitrogen_sensitivity)
carbon_concentration.append(((intensity_peak2peak_J2C/carbon_sensitivity)/SRFJ2))
titanium_concentration.append(((intensity_peak2peak_J2Ti/titanium_sensitivity)/SRFJ2))
oxygen_concentration.append((intensity_peak2peak_J2O/oxygen_sensitivity)/SRFJ2)
copper_concentration.append((intensity_peak2peak_J2Cu/copper_sensitivity)/SRFJ2)
Al_concentration.append((intensity_peak2peak_J2Al/aluminum_sensitivity)/SRFJ2)
#nitrogen_concentration.append((intensity_peak2peak_J2N/nitrogen_sensitivity)/SRFJ2)

SRFJ2_after_heat=(intensity_peak2peak_J2C_after_heat/carbon_sensitivity)+(intensity_peak2peak_J2Ti_after_heat/titanium_sensitivity)+(intensity_peak2peak_J2O_after_heat/oxygen_sensitivity)+(intensity_peak2peak_J2Cu_after_heat/copper_sensitivity)+(intensity_peak2peak_J2Al_after_heat/aluminum_sensitivity)#+(intensity_peak2peak_J2N_after_heat/nitrogen_sensitivity)
carbon_concentration_after_heat.append(((intensity_peak2peak_J2C_after_heat/carbon_sensitivity)/SRFJ2_after_heat))
titanium_concentration_after_heat.append(((intensity_peak2peak_J2Ti_after_heat/titanium_sensitivity)/SRFJ2_after_heat))
oxygen_concentration_after_heat.append((intensity_peak2peak_J2O_after_heat/oxygen_sensitivity)/SRFJ2_after_heat)
copper_concentration_after_heat.append((intensity_peak2peak_J2Cu_after_heat/copper_sensitivity)/SRFJ2_after_heat)
Al_concentration_after_heat.append((intensity_peak2peak_J2Al_after_heat/aluminum_sensitivity)/SRFJ2_after_heat)
#nitrogen_concentration_after_heat.append(((intensity_peak2peak_J2N_after_heat/nitrogen_sensitivity)/SRFJ2_after_heat))


SRFJ3=(intensity_peak2peak_J3C/carbon_sensitivity)+(intensity_peak2peak_J3Ti/titanium_sensitivity)+(intensity_peak2peak_J3O/oxygen_sensitivity)+(intensity_peak2peak_J3Cu/copper_sensitivity)+(intensity_peak2peak_J3Al/aluminum_sensitivity)#+(intensity_peak2peak_J3N/nitrogen_sensitivity)
carbon_concentration.append(((intensity_peak2peak_J3C/carbon_sensitivity)/SRFJ3))
titanium_concentration.append(((intensity_peak2peak_J3Ti/titanium_sensitivity)/SRFJ3))
oxygen_concentration.append((intensity_peak2peak_J3O/oxygen_sensitivity)/SRFJ3)
copper_concentration.append((intensity_peak2peak_J3Cu/copper_sensitivity)/SRFJ3)
Al_concentration.append((intensity_peak2peak_J3Al/aluminum_sensitivity)/SRFJ3)
#nitrogen_concentration.append(((intensity_peak2peak_J3N/nitrogen_sensitivity)/SRFJ3))

SRFA=(intensity_peak2peak_AC/carbon_sensitivity)+(intensity_peak2peak_ATi/titanium_sensitivity)+(intensity_peak2peak_AO/oxygen_sensitivity)+(intensity_peak2peak_ACu/copper_sensitivity)+(intensity_peak2peak_AAl/aluminum_sensitivity)#+(intensity_peak2peak_AN/nitrogen_sensitivity)
carbon_concentration.append(((intensity_peak2peak_AC/carbon_sensitivity)/SRFA))
titanium_concentration.append(((intensity_peak2peak_ATi/titanium_sensitivity)/SRFA))
oxygen_concentration.append((intensity_peak2peak_AO/oxygen_sensitivity)/SRFA)
copper_concentration.append((intensity_peak2peak_ACu/copper_sensitivity)/SRFA)
Al_concentration.append((intensity_peak2peak_AAl/aluminum_sensitivity)/SRFA)
#nitrogen_concentration.append((intensity_peak2peak_AN/nitrogen_sensitivity)/SRFA)


mill_total_dose_1=0
mill_total_dose_2=11.95
mill_total_dose_3=20.56
mill_total_dose_4=21.31
mill_total_dose_5=26.24
mill_total_doses=[mill_total_dose_1,mill_total_dose_2,mill_total_dose_3,mill_total_dose_4,mill_total_dose_5]

# Create some mock data
t = mill_total_doses
Al_total_concentration = Al_concentration
Al_unoxidised_concentration=[0,Al_concentration[1],Al_concentration[2],Al_concentration[3]/2.,Al_concentration[4]/2.]
data2 =[7.59,1.11,1.08,1.58,.94]

fig, ax1 = plt.subplots()

color = 'g'
ax1.set_xlabel('Milling dose (J/cm^2)')
ax1.set_ylabel('Atomic Concentration', color=color)
ax1.plot(t, Al_unoxidised_concentration, color=color,label="Al")
ax1.plot(t,Al_total_concentration,color='g', linestyle=":",label='Al + Al2O3')
ax1.plot(t,carbon_concentration,color='g',linestyle='--',label='Carbon')
ax1.scatter(t,carbon_concentration,color='g',linestyle='--')
ax1.scatter(t, Al_unoxidised_concentration, color=color)
ax1.set_ylim(0,.8)
ax1.legend(loc='best')
ax1.tick_params(axis='y', labelcolor=color)



ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
HR=[7.59,5.55,5.3,3.79,2.5,1.75,1.11,1.08,2.03,2.02,1.95,1.58,.94]
HRErr=[0.23,0.31,0.22,0.19,0.13,0.12,0.11,0.09,0.11,0.05,0.14,0.05]
CumulDose=[0,.1,.21,.67,1.84,4.42,11.95,20.56,20.581,20.625,20.763,21.31,26.24]
color = 'r'
ax2.set_ylabel('% change heating rate post heating', color='r')  # we already handled the x-label with ax1
#ax2.plot(CumulDose, HR, color=color)
#ax2.scatter(CumulDose, HR, color=color)
CumulDose_after_heat=[0,.1,.21,.67,1.84,4.42,11.95,20.56,21.31,26.24]
HRAl_after_heat=[0,0,0,0,0,(2.46-1.75)/1.75,(2.95-1.11)/1.11,(2.01-1.08)/1.08 ,(1.06-.92)/.92,(.94-.9)/.94]
print(len(HRAl_after_heat),len(CumulDose))
ax2.scatter(CumulDose_after_heat,HRAl_after_heat,color='r')
ax2.set_ylim(0,2.2)
ax2.plot(CumulDose_after_heat,HRAl_after_heat,color='r')
ax2.tick_params(axis='y', labelcolor='r')

ax2.set_title("% change heating rate, Al concentration vs Milling dose")
fig.tight_layout()  # otherwise the right y-label is slightly clintensity_peak2peak_ed


### Plot full auger spectra ####



plt.figure()
Y=0
SGWL=17
SGP=2


dir='/Users/Maya/Dropbox/Data_and_Plotting_SQIP/Auger/AugerData/PrinceEdward_2017-2019/'

energy,readout,peaks0 = ft.import_data(dir+'2018Jun22_fullscan.aes',265,275,Y)
readout=[i+1 for i in readout]
y=readout
# y=scipy.signal.savgol_filter(y,SGWL,SGP)
plt.plot(energy,y,'r',label="Pre Mill")

energy,readout,peaks0 = ft.import_data(dir+'fullscan_2019May06.aes',265,275,Y)
readout=[i+.3 for i in readout]
y=readout
# y=scipy.signal.savgol_filter(y,SGWL,SGP)
plt.plot(energy,y,color='gold',label="Post Mill 6")



energy,readout,peaks0 = ft.import_data(dir+'fullscan_2019Jun03_1s_Normal_direction.aes',265,275,Y)
#readout=[i*-1 for i in readout]
readout=[i for i in readout]
y=readout
# y=scipy.signal.savgol_filter(y,SGWL,SGP)
plt.plot(energy,y,'green',label="Post Mill 7")


energy,readout,peaks0 = ft.import_data(dir+'2019Jul15_after_mill8D_1924_highres_Al.aes',265,275,Y)
#readout=[i*-1 for i in readout]
readout=[i-.6 for i in readout]
y=readout
# y=scipy.signal.savgol_filter(y,SGWL,SGP)
plt.plot(energy,y,color='b',label="Post Mill 8")

plt.legend(loc='lower left')
plt.title("Aluminum")


### plot depth profile ###



plt.show()





