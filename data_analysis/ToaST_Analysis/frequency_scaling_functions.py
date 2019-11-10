from scipy import optimize as op
import numpy as np

def exponential_fit(x,amplitude,exponent):
    return amplitude/x**exponent

def fit_freq_scaling(freq, rate, rerr,label='',p=1): #removed ax input

        popt,pcov = op.curve_fit(exponential_fit,freq,rate,p0=[1,2],sigma=rerr,absolute_sigma=True)
        perr = np.sqrt(np.diag(pcov))
        amplitude = popt[0]
        exponent = popt[1]

        if p==1:
            print label + ':'
            print "Amplitude: "+"{0:.2f}".format(amplitude) + ' +- ' + "{0:.2f}".format(perr[0])
#           print "exponent: "+"{0:.2f}".format(alpha) + ' +- ' + "{0:.2f}".format(perr[1])
            print "Alpha: "+"{0:.2f}".format(exponent-1) + ' +- ' + "{0:.2f}".format(perr[1])

            freq = np.sort(freq)
            ratefit = [exponential_fit(x,amplitude,exponent) for x in freq]

        return amplitude,perr[1],exponent, perr[0]

def plot_freq_scaling(ax,filename,skiprows,label,mycolor,fmt='o',dotsize=3):
        mydata = np.loadtxt(filename,skiprows=skiprows)
        date = np.array(mydata[:,0])
        freq = np.array(mydata[:,1])
        rate = np.array(mydata[:,2])
        error = np.array(mydata[:,3])

        inds = np.argsort(freq)
        freq = freq[inds]
        rate = rate[inds]
        error = error[inds]

        alpha, alpha_err, amp, amp_err = fit_freq_scaling(freq,rate,error,label=label)
        ax.errorbar(freq,rate,yerr=error,color=mycolor,fmt=fmt,label=label,capsize=3)

        x = np.linspace(.47, 2, num=300)
        rate_fit = exponential_fit(x,amp,alpha)
        ax.plot(x,rate_fit,color = 'black')

        # ax.tick_params(labelsize=14,which='both')
        return

