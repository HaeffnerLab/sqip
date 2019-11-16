import numericalunits
import numpy as np
import pint
ureg = pint.UnitRegistry()

#ENERGY DEPENDENCE OF THE ION-INDUCED SPUTTERING YIELDS OF MONATOMIC SOLIDS
# M1=4 #incident ion = He, mass in AMU
# M2=63.55 #target ion = Cu, mass in AMU
# Z1=2
# Z2=29
# Energy = 1000 # eV

M1_Ar= 39.95#incident ion = Argon
Z1_Ar= 18#
M2_C= 12.01#target = Carbon
Z2_C= 6
M2_Al= 26.98#target = Aluminum
Z2_Al= 13
Energy = 500 # eV

def get_ion_crosssection(M1,Z1,M2,Z2,Energy):
    reduced_energy = 0.03255 / ( Z1*Z2* (Z1**(2.0/3.0)+Z2**(2.0/3.0))**.5) * M2/(M1+M2) * Energy
    s_n = 3.441 * reduced_energy**0.5* np.log(reduced_energy+2.718)/(1+6.355*reduced_energy**0.5+reduced_energy*(-1.708+6.882*reduced_energy**0.5))#Lindhard's elastic reduced stopping cross section
    k = 0.079*(M1+M2)**1.5/(M1**1.5 * M2**.5) * Z1**(2.0/3.0) * Z2**0.5 / (Z1**(2.0/3.0) + Z2 **(2.0/3.0))**0.75
    s_e = k*reduced_energy**.5
    K = 8.478 * Z1*Z2 / (Z1**(2.0/3.0)+Z2**(2.0/3.0))**0.5 * M1 / (M1+M2)#conversion factor
    S_n = K * s_n /10**15 # converts to stopping cross section in units of cm^2
    return S_n


S_n_Carbon = get_ion_crosssection(M1_Ar,Z1_Ar,M2_C,Z2_C,Energy)
print("400 eV Argon ion, Carbon stopping cross section = " + str(S_n_Carbon) + " cm^2")
S_n_Aluminum = get_ion_crosssection(M1_Ar,Z1_Ar,M2_Al,Z2_Al,Energy)
print("400 eV Argon ion, Aluminum stopping cross section = " + str(S_n_Aluminum) + " cm^2")


######################
## Get electron stopping powers from NIST database - convert to stopping cross section
## Numbers are for 2 keV electrons

energy_electron = .002 # MeV

stoppingpower_Al = 50.18 # MeV cm^2 /g
stoppingpower_C_amorphous = 66.17 # MeV cm^2 /g

density_C_amorphous = 2 # g/cm^3
density_Al = 2.7 # g/cm^3

mass_C = 1.99*10**(-23) # g / atom
mass_Al = 4.48*10**(-23) # g / atom

def crosssection(energy, stoppingpower,atomicmass):
    crosssection = stoppingpower * atomicmass / energy
    return crosssection

crosssection_C = crosssection(energy_electron,stoppingpower_C_amorphous,mass_C)
print("2 keV electron, Carbon stopping cross section = " + str(crosssection_C) + " cm^2")
crosssection_Al = crosssection(energy_electron,stoppingpower_C_amorphous,mass_C)
print("2 keV electron, Aluminum stopping cross section = " + str(crosssection_Al) + " cm^2")

