from sqip_rate_from_flops import *
import os

current_dir=os.getcwd()
#parameters inserted into calculation
trap_freq =0.88*1e6 #in Hz
nbar = 20 #guess for nbar
excitation_scaling=.99 #guess how well OP works
plot_flops=True #set to true to plot the flops
theta=11.5 #the0 angle of the laser with the trap axis
time_2pi=20 #guess for 2pi time in microseconds
sideband_order = 0

times1, nbarlist1, nbarerrs1,times2, nbarlist2,nbarerrs2=[],[],[],[],[],[]
datafiles,timex = [],[]

# date1="2019_07_03"
# date2="2019Jul03"
# runfree=False

# ## Refit all flops ###

# heatingratefiles=[
# '1639_10'
# ] 

# signature_flops=heatingratefiles #Sometimes the heating rate filename is one second off from the zerowaittime flop and will need to be typed in separately. in scriptscanner2, heatingratefile = second flop
# signature_flops=[
# '1639_10'
# ] 

# whichdata=[
# [0,1,2,3,4,5],
# [0,1,2,3,4,5],
# [0,1,2,3,4,5]
# ] #use this to choose which flops to use. Typically will be [0,1,2,3,4,5]. For example, to skip the third flop, set to [0,1,3,4,5]. If dataset has 8 flops, set to [0,1,2,3,4,5,6,7]
# waittimes=import_waittimes(heatingratefiles,date1,date2,sideband_order) #[[0,1.8,3.6,5.4,7.2,9],[0,1.8,3.6,5.4,7.2,9]] #Type in wait times by hand if heating rate file does not exist
# times1, nbarlist1, nbarerrs1=make_nbararray_from_rabiflopdata_signaturefile(signature_flops,whichdata,waittimes,date1,date2,trap_freq,nbar,excitation_scaling,plot_flops,theta,time_2pi,sideband_order,runfree)

#Import nbar values and fit heating rate ### 
date2='2019Jul03'
date1='2019_07_03'

nbarfiles=[
'1918_31',
'1927_09',
'1932_46',
]

times2, nbarlist2,nbarerrs2=import_nbar_data(nbarfiles,date1,date2,sideband_order)  

times,nbarlist,nbarerrs = np.append(times1,times2),np.append(nbarlist1,nbarlist2),np.append(nbarerrs1,nbarerrs2)
nbar_0waittime(times,nbarlist,nbarerrs)
### Linear fit and heating rate plot ###
rate,stderr = plot_heating_rate(times,nbarlist,nbarerrs,'{} MHz'.format(trap_freq/1000000)) #linear fit of nbar
print "{0:.2f}".format(rate) + ' +- ' + "{0:.2f}".format(stderr) + ' n/ms for {} MHz'.format(trap_freq/1000000) #prints out heating rate
pyplot.title("{0:.2f}".format(rate) + ' +- ' + "{0:.2f}".format(stderr)+"quanta/ms",fontsize=18)
pyplot.legend()

pyplot.show()



## Fit rabi flops to find nbar lists for multiple data sets, return all nbars ###
#datafiles=[
#[['1548_45'],['1549_05'],['1549_31'],['1550_02'],['1550_39'],['1551_21']],
#[['1552_10'],['1552_29'],['1552_55'],['1553_25'],['1554_02'],['1554_44']],
#]
#timex=[
#[0,1.8,3.6,5.4,7.2,9],
#[0,1.8,3.6,5.4,7.2,9],
#]
#times1, nbarlist1, nbarerrs1=make_nbararray_from_rabiflopdata(datafiles,timex,date1,date2,trap_freq,nbar,excitation_scaling,plot_flops,theta,time_2pi)

