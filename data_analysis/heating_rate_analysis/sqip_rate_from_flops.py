#import matplotlib
#matplotlib.use('Qt4Agg')
# from simple_analysis.get_data import *
from sqip_rabi_flop_fitter import *
#from nbar_rabi import *
import scipy.optimize as op
import lmfit
from matplotlib import pyplot
import os
current_dir=os.getcwd()

# from U2freqcalc import freq_from_U2

#this is for cycling colors so you can plot in multiple colors and coordinate data points and fits
from itertools import cycle
cycol = cycle('bgrcmk').next 

hbar = 1.0546e-34
m = 39.96*1.66e-27

def import_data(filename):
	t,p = np.loadtxt(filename,unpack=True, delimiter=',')
	return t,p

def calc_eta(trap_freq,theta):
        theta = np.deg2rad(theta)
        return 2*np.pi/729.e-9*np.sqrt(hbar/(2*m*2*np.pi*trap_freq))*np.cos(theta)

def compute_approx_thermal(nbars,time_2pi,etas,t):
        omega = np.pi/time_2pi
        scaling = sum([etas[i]**2*nbars[i] for i in range(len(nbars))])
        Qfunc = [np.exp(2j*omega*x)/(1+1j*omega*x*scaling) for x in t]
        return [0.5*(1-np.real(x)) for x in Qfunc]

def plot_heating_rate(times,data,err,label='',mycolor='black'):
        #mycolor = cycol()
        pyplot.errorbar(times, data,yerr=err,fmt='o',color=mycolor,markersize=8,capsize=None)
        pyplot.ylabel(r'$\bar{n}$', fontsize=36)
        pyplot.xlabel('time (ms)',fontsize=18)
        pyplot.tick_params(labelsize=18)
        def f(x,rate,offset):
                return rate*x+offset
        popt,pcov = op.curve_fit(f,times,data,p0=[1,20],sigma=err,absolute_sigma=True)
        

        #variance = cov_matrix[0][0]
        perr = np.sqrt(np.diag(pcov))
        rate = popt[0]
        offset = popt[1]
        #print popt
        #print perr
        #stderr = np.sqrt(variance)
        stderr = perr[0]
        #print "{0:.2f}".format(rate) + ' +- ' + "{0:.2f}".format(stderr) + ' n/ms'
        #print str(rate*1000.)+' n/s'
        times = np.sort(times)
        pyplot.plot(times, rate*times+offset,label=label,color=mycolor)
        #pyplot.title('heating rate of ' + "{0:.2f}".format(rate) + ' +- ' + "{0:.2f}".format(stderr) + ' n/ms for trap freq ' + str(int(trap_freq/1000)) + ' kHz')
        return rate,stderr

def fit_rabi_flops(file_loc,file_ext,data_dict,trap_freq,plot_flops,excitation_scaling,time_2pi,nbar,etas,delta,sideband_order,runfree=False):
        nbarlist = []
        nbarerrs = []
        pitimes = []
        pitimeserr = []
        deltas = []
        deltaserr = []
        excitation_scaling_list = []
        excitation_scaling_errs = []
        # if plot_flops:
                # pyplot.figure()
        #this part does the rabi flop fitting for each data set
        times = np.sort(data_dict.keys())
        eta = etas[0]
        for key in times:
                #import data and calculate errors based on 100 experiments
                t,p = import_data(file_loc + str(data_dict[key][0]) + ".dir/" + file_ext + str(data_dict[key][0]) + ".csv")
                perr = [np.sqrt(x*(1-x)/100.) for x in p]
                for index in range(0,len(p)):
                    if perr[index] == 0:
                        perr[index] = np.sqrt(0.01*(1-0.01)/100.)
                # N = len(t)/3
                # t = t[0:N]
                # p = p[0:N]
                # perr = perr[0:N]

                #model for Rabi flops, use 0 for sidebands, +-1 etc for sidebands..
                te = rabi_flop_time_evolution(sideband_order,eta,nmax=10000) #if you get the error that the hilbert space is too small, then increase nmax
                params = lmfit.Parameters()
                params.add('delta',value = 0.0,vary=False)
                #params.add('delta',value = delta ,vary=True,min=0.01,max=0.04)
                params.add('nbar',value = nbar,min=0.01,max=200.0)

                if key == 0 or runfree:
                        params.add('time_2pi',value = time_2pi,vary=True)
                        # params.add('time_2pi',value = time_2pi,vary=False)
                        params.add('excitation_scaling',value = excitation_scaling,vary=True, min=0.95,max=1.0)
                else:
                        params.add('time_2pi',value = time_2pi,vary=False)
                        #params.add('excitation_scaling',value = excitation_scaling,vary=False)
                        params.add('excitation_scaling',value = excitation_scaling,vary=True, min=0.95,max=1.0)
                        
                        
##                params.add('nbar1',value = nbar,min=0.0,max=100.0,vary=True)
##                params.add('nbar2',value = nbar,min=0.0,max=100.0,vary=True)
##              
                guess_values = te.compute_evolution_thermal(params['nbar'].value, params['delta'].value, params['time_2pi'].value, t,params['excitation_scaling'].value)
                
                def rabi_fit_thermal(params,t,data,err):
                        model = te.compute_evolution_thermal(params['nbar'].value, params['delta'].value, params['time_2pi'].value, t,params['excitation_scaling'].value)
                        resid = model-data
                        weighted = [np.sqrt(resid[x]**2/err[x]**2) for x in range(len(err))]
                        # sum_weighted = sum(weighted)
                        # print "sum of residuals: " + str(sum_weighted)
                        return weighted

                def rabi_fit_approx(params,t,data,err):
                        #print params['nbar2'].value                      
                        model = compute_approx_thermal([params['nbar1'].value,params['nbar2'].value], params['time_2pi'].value,etas,t)
                        resid = model-data
                        weighted = [np.sqrt(resid[x]**2/err[x]**2) for x in range(len(err))]
                        return weighted

                if len(etas)<2:
                        result = lmfit.minimize(rabi_fit_thermal,params,method='leastsq',maxfev = 500, xtol = 1.e-7, ftol = 1.e-7, args = (t,p,perr))
                        # result = lmfit.minimize(rabi_fit_thermal,params, args = (t,p,perr))
                        # print "status" + str(result.status)
                        # print "number of evaluations: " + str(result.nfev)
                        # print "residuals: " + str(result.residual)
                        # print "fit success message: " + str(result.message)
                        # print "least squares message: " + str(result.lmdif_message)
                        print "reduced chi^2 " + str(result.redchi)
                        params = result.params
                        if key == 0:
                                time_2pi = params['time_2pi'].value
                                excitation_scaling = params['excitation_scaling'].value
                        fit_values = te.compute_evolution_thermal(params['nbar'].value, params['delta'].value, params['time_2pi'].value, t, params['excitation_scaling'].value)
                        nbarlist=np.append(nbarlist,params['nbar'].value)
                        nbarerrs=np.append(nbarerrs,params['nbar'].stderr)
                        print params['time_2pi'].stderr

                else:
                        print "approx_thermal"
                        result = lmfit.minimize(rabi_fit_approx,params,args = (t,p,perr))
                        params = result.params
                        if key == 0:
                                time_2pi = params['time_2pi'].value
                                excitation_scaling = params['excitation_scaling'].value
                        fit_values = compute_approx_thermal([params['nbar1'].value,params['nbar2'].value], params['time_2pi'].value,etas,t)
                        nbarlist=np.append(nbarlist,params['nbar1'].value)
                        nbarerrs=np.append(nbarerrs,params['nbar1'].stderr)
                        # print nbarerrs

                #print "nbar fit for " + str(key) + "   " + str(params['nbar'].value) + " +- " + str(params['nbar'].stderr)
                #print "reduced chisquared: " + str(result.redchi)
                print str(key) + "   " + str(params['time_2pi'].value) + " +- " + str(params['time_2pi'].stderr)         

                pitimes = np.append(pitimes,params['time_2pi'].value/2.0)
                pitimeserr = np.append(pitimeserr,params['time_2pi'].stderr/2.0)
                deltas = np.append(deltas,params['delta'].value)
                deltaserr = np.append(deltaserr,params['delta'].stderr)
                excitation_scaling_list=np.append(excitation_scaling_list,params['excitation_scaling'].value)
                excitation_scaling_errs=np.append(excitation_scaling_errs,params['excitation_scaling'].stderr)
                # print 'optical pumping estimate from fit:' + str(params['excitation_scaling'].value)
                
                
                if plot_flops:
                        pyplot.figure()
                        mycolor = cycol()
                        pyplot.plot(t,p,'-o',label = 'data ' + str(key),color=mycolor)
                        pyplot.plot(t,fit_values,'r',label = 'fitted '+ str(key),color=mycolor)
                        pyplot.title('flops for trap freq ' + str(int(trap_freq/1000)) + ' kHz')
                        #pyplot.plot(t,guess_values,'r',label = 'guess '+ str(key),color='black')

                        pyplot.legend()
        return (times,nbarlist,nbarerrs,excitation_scaling_list,excitation_scaling_errs)
 

def fit_freq_scaling(freq, rate, rerr,mycolor='b',label=''):
        

        def f(x,Amp,alpha):
                return Amp/x**alpha
        #def f(x,Amp,alpha,offset):
        #        return Amp/x**alpha+offset
        popt,pcov = op.curve_fit(f,freq,rate,p0=[1,2],sigma=rerr)
        #variance = cov_matrix[0][0]
        perr = np.sqrt(np.diag(pcov))
        Amp = popt[0]
        alpha = popt[1]
        #offset = popt[2]
        print popt
        print perr
        #stderr = np.sqrt(variance)
        stderr = perr[1]
        #print "{0:.2f}".format(rate) + ' +- ' + "{0:.2f}".format(stderr) + ' n/ms'
        #print str(rate*1000.)+' n/s'
        
        #pyplot.title('heating rate of ' + "{0:.2f}".format(rate) + ' +- ' + "{0:.2f}".format(stderr) + ' n/ms for trap freq ' + str(int(trap_freq/1000)) + ' kHz')
        freq = np.array(freq)
        rate = np.array(rate)
        rerr = np.array(rerr)
        myorder = np.argsort(freq)
        rate = np.array([rate[x] for x in myorder])
        rerr = np.array([rerr[x] for x in myorder])
        freq = np.array([freq[x] for x in myorder])
        todel = []
        for x in range(len(freq)):
                if freq[x]==freq[x-1]:
                        tmp = [rate[x],rate[x-1]]
                        tmp1 = [rerr[x],rerr[x-1]]
                        lgindx = np.argmax(tmp)
                        newy = (rate[x]+rate[x-1])/2
                        newerr = ((tmp[lgindx]+tmp1[lgindx])-(tmp[lgindx-1]-tmp1[lgindx-1]))/2
                        rate[x-1] = newy
                        rerr[x-1] = newerr
                        rate[x] = newy
                        rerr[x] = newerr
                        todel.append(x)
        for x in todel:
                np.delete(freq,x)
                np.delete(rate,x)
                np.delete(rerr,x)


        pyplot.fill_between(freq, rate-rerr, rate+rerr,facecolor=mycolor,alpha=0.5)
       # pyplot.fill_betweenx(rate,freq-xerr,x+xerr,facecolor='b',alpha=0.5)
        freq = np.sort(freq)
        ratefit = [f(x,Amp,alpha) for x in freq]
        pyplot.plot(freq, ratefit,label=label,color=mycolor)
        return alpha,stderr


def calculate_and_plot_nbar_from_rabiflop_data(dataset,timex,date1,date2,trap_freq,nbar,excitation_scaling,plot_flops,theta,time_2pi,sideband_order,runfree=False):

    etas = [calc_eta(trap_freq,theta)]
    print etas
    delta={}
    #data without ramping
    #file_loc = "//192.168.169.99/RabiFlopping/" + date2 + ".dir/"
    file_loc = current_dir + "/Data_rabiflops/" + date1 + " heating rates/"
    file_ext = "00001 - Rabi Flopping "+ date2 +"_"
    data_dict = {} #keys are the wait time in ms

    for i in range(len(dataset)):
        data_dict[timex[i]]=dataset[i]

    (times,nbarlist,nbarerrs,excitation_scaling_list,excitation_scaling_errs) = fit_rabi_flops(file_loc,file_ext,data_dict,trap_freq,plot_flops,excitation_scaling,time_2pi,nbar,etas,delta,sideband_order,runfree)

    j=0
    while j < len(times):
        if abs(nbarlist[j]-nbar) < .001:
            times = np.delete(times,j)
            nbarlist = np.delete(nbarlist,j)
            nbarerrs = np.delete(nbarerrs,j)
        else:
            j = j+1

    print (excitation_scaling_list,excitation_scaling_errs,times,nbarlist,nbarerrs)
    pyplot.figure()
    # print "times, nbarlist, nbarerrs:"
    # print times,nbarlist,nbarerrs
    return times,nbarlist,nbarerrs


def whichscriptscanner(date1):
    year = int(date1[0:4]) 
    month = int(date1[5:7])
    day = int(date1[8:10])
    if year > 2018 and month > 1:
        whichscriptscanner=2
    elif year==2019 and month==1 and day == 31:
        whichscriptscanner=2
    else:
        whichscriptscanner=1
    return whichscriptscanner

def calculate_and_plot_nbar_from_signatureflop(signatureflop,whichdata,waittimes,date1,date2,trap_freq,nbar,excitation_scaling,plot_flops,theta,time_2pi,sideband_order,runfree=False):
    etas = [calc_eta(trap_freq,theta)]
    print etas
    delta={}
    #data without ramping

    if whichscriptscanner(date1)==1:
        file_loc = current_dir + "/Data_rabiflops/" + date1 + " heating rates/"
        file_ext = "00001 - Rabi Flopping "+ date2 +"_"
    if whichscriptscanner(date1)==2:
        file_loc = "//192.168.169.99/Experiments/" + date1.replace("_","") + ".dir/flop.dir/"
        file_ext = "00001 - "


    data_dict = {} #keys are the wait time in ms

    datafiles = os.listdir(file_loc)
    for i in range(len(datafiles)):
        if datafiles[i]==signatureflop +'.dir':
            for x in whichdata:
                if whichscriptscanner(date1)==1:
                    data_dict[waittimes[x]]=[datafiles[i+x][0:7]]
                if whichscriptscanner(date1)==2:
                    data_dict[waittimes[x]]=[datafiles[i+x-1][0:7]]
    # print data_dict
    (times,nbarlist,nbarerrs,excitation_scaling_list,excitation_scaling_errs) = fit_rabi_flops(file_loc,file_ext,data_dict,trap_freq,plot_flops,excitation_scaling,time_2pi,nbar,etas,delta,sideband_order,runfree)

    j=0
    while j < len(times):
        if abs(nbarlist[j]-nbar) < .001:
            times = np.delete(times,j)
            nbarlist = np.delete(nbarlist,j)
            nbarerrs = np.delete(nbarerrs,j)
        else:
            j = j+1

    print (excitation_scaling_list,excitation_scaling_errs,times,nbarlist,nbarerrs)
    pyplot.figure()
    # print "times, nbarlist, nbarerrs:"
    # print times,nbarlist,nbarerrs
    return times,nbarlist,nbarerrs

# calculate and nbar from rabiflop data

def import_nbar_data(nbarfiles,date1,date2,sideband_order):
    current_dir=os.getcwd()


    if whichscriptscanner(date1)==1:
        file_loc = "//192.168.169.99/RabiCalibHeatingRates/" + date2 + ".dir/"
        #file_loc = current_dir + "/Data_nbars/" + date + ".dir/"
        file_ext = ".dir/00001 - Heating_Rate " + date2 + "_"

    if whichscriptscanner(date1)==2:
        if sideband_order == 0:
            file_loc = "//192.168.169.99/Experiments/" + date1.replace("_","") + ".dir/Heating_Rate_Rabi.dir/"
            file_ext = ".dir/00001 - "
        elif sideband_order == 1:
            file_loc = "//192.168.169.99/Experiments/" + date1.replace("_","") + ".dir/Heating_Rate_BlueRabi.dir/"
            file_ext = ".dir/00001 - "     



    #Add values by hand to arrays below, if necessary
    times=[]
    nbarlist=[]
    nbarerrs=[]
    for file in nbarfiles:
        filename = file_loc+file+file_ext+file+".csv"
        time,nbar,error = np.loadtxt(filename,unpack=True, delimiter=',')
        times = np.append(times,time)
        nbarlist = np.append(nbarlist,nbar)
        nbarerrs = np.append(nbarerrs,error)
    i=0

    while i < len(times):
        if abs(nbarlist[i]-20) < .001:
            times = np.delete(times,i)
            nbarlist = np.delete(nbarlist,i)
            nbarerrs = np.delete(nbarerrs,i)
        else:
            i = i+1
 #   print "times, nbarlist, nbarerrs:"
 #   print times,nbarlist,nbarerrs

    return times,nbarlist,nbarerrs

def import_waittimes(nbarfiles,date1,date2,sideband_order):
    current_dir=os.getcwd()


    if whichscriptscanner(date1)==1:
        file_loc = "//192.168.169.99/RabiCalibHeatingRates/" + date2 + ".dir/"
        file_ext = ".dir/00001 - Heating_Rate " + date2 + "_"

    if whichscriptscanner(date1)==2:
        if sideband_order == 0:
            file_loc = "//192.168.169.99/Experiments/" + date1.replace("_","") + ".dir/Heating_Rate_Rabi.dir/"
            file_ext = ".dir/00001 - "
        elif sideband_order == 1:
            file_loc = "//192.168.169.99/Experiments/" + date1.replace("_","") + ".dir/Heating_Rate_BlueRabi.dir/"
            file_ext = ".dir/00001 - "    


    #Add values by hand to arrays below, if necessary
    times=[]
    for i in range(len(nbarfiles)):
        filename = file_loc+nbarfiles[i]+file_ext+nbarfiles[i]+".csv"
        time,nbar,error = np.loadtxt(filename,unpack=True, delimiter=',')
        times.append(time)
        # print 'times: ' + str(times)
    return times


def nbar_0waittime(times,nbarlist,nbarerrs):
    nbar0=[]
    nbar0weight=[]
    for i in range(len(times)):
        if times[i]==0:
            nbar0.append(nbarlist[i])
            nbar0weight.append(nbarerrs[i]**-2)
    nbar0avg=np.sum(np.array(nbar0)*np.array(nbar0weight))/np.sum(nbar0weight)
    nbar0avgerror=np.sqrt(1/np.sum(nbar0weight))        
    print "nbar zero weight time average, error, standard deviation:"
    print nbar0avg,nbar0avgerror, np.std(nbar0)
    return nbar0avg, nbar0avgerror,np.std(nbar0)



def make_nbararray_from_rabiflopdata(datafiles,timex,date1,date2,trap_freq,nbar,excitation_scaling,plot_flops,theta,time_2pi,sideband_order,runfree=False):
    times=[]
    nbarlist=[]
    nbarerrs=[]

    for i in range(len(datafiles)):
        # print datafiles[i],timex[i]
        ##datatimes, datanbarlist,datanbarerrs=calculate_and_plot_nbar_from_rabiflop_data(dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5],timex) 
        datatimes, datanbarlist,datanbarerrs=calculate_and_plot_nbar_from_rabiflop_data(datafiles[i],timex[i],date1,date2,trap_freq,nbar,excitation_scaling,plot_flops,theta,time_2pi,sideband_order,runfree) 
        print 'success for set: ' + str(i)
        times=np.append(times,datatimes)
        nbarlist=np.append(nbarlist,datanbarlist)
        nbarerrs=np.append(nbarerrs,datanbarerrs)

    print "times, nbarlist, nbarerrs:"
    print times,nbarlist,nbarerrs
    return times,nbarlist,nbarerrs

def make_nbararray_from_rabiflopdata_signaturefile(signaturefiles,whichdata,timex,date1,date2,trap_freq,nbar,excitation_scaling,plot_flops,theta,time_2pi,sideband_order,runfree=False):
    times=[]
    nbarlist=[]
    nbarerrs=[]

    for i in range(len(signaturefiles)):
        datatimes, datanbarlist,datanbarerrs=calculate_and_plot_nbar_from_signatureflop(signaturefiles[i],whichdata[i],timex[i],date1,date2,trap_freq,nbar,excitation_scaling,plot_flops,theta,time_2pi,sideband_order,runfree)

        times=np.append(times,datatimes)
        nbarlist=np.append(nbarlist,datanbarlist)
        nbarerrs=np.append(nbarerrs,datanbarerrs)

    print "times, nbarlist, nbarerrs:"
    print times,nbarlist,nbarerrs
    return times,nbarlist,nbarerrs

def reformat_dict(data_dict):
# datafiles=[
# [['1859_21'],['1859_39'],['1859_57'],['1900_17'], ['1900_38'], ['1901_02']],
# [['1901_56'], ['1902_13'],['1902_31'], ['1902_51'], ['1903_13'],['1903_37']],
# [['1904_30'], ['1904_47'],['1905_06'], ['1905_26'], ['1905_47'],['1906_11']]

# ]

# timex=[
# [0.0,0.6,1.2,1.8,2.4,3.0],
# [0.0,0.6,1.2,1.8,2.4,3.0],
# [0.0,0.6,1.2,1.8,2.4,3.0],
# ]

    times = data_dict.keys()
    times = np.sort(times)
    data = [data_dict[key] for key in times]


    return data,times