from sqip.scripts.experiments.Experiments729.rabi_flopping import rabi_flopping
from common.abstractdevices.script_scanner.scan_methods import experiment
from sqip.scripts.experiments.Experiments729.excitations import excitation_729
from sqip.scripts.scriptLibrary.common_methods_729 import common_methods_729 as cm
from common.abstractdevices.script_scanner.scan_methods import experiment
from sqip.scripts.experiments.CalibrationScans.calibrate_temperature import calibrate_temperature
from sqip.scripts.scriptLibrary import scan_methods
from sqip.scripts.scriptLibrary import dvParameters
from fitters import peak_fitter
from labrad.units import WithUnit
from treedict import TreeDict
import time
import numpy as np
import labrad
from fitters import rate_from_flops_fitter

class rabi_calib_heating_rate(experiment):

    name = 'RabiCalibHeatingRates'

    trap_frequencies = [
                        ('TrapFrequencies','axial_frequency'),
                        ('TrapFrequencies','radial_frequency_1'),
                        ('TrapFrequencies','radial_frequency_2'),
                        ('TrapFrequencies','rf_drive_frequency'),                       
                        ]
    rabi_required_parameters = [
                           ('RabiFlopping','rabi_amplitude_729'),
                           ('RabiFlopping','manual_scan'),
                           ('RabiFlopping','manual_frequency_729'),
                           ('RabiFlopping','line_selection'),
                           ('RabiFlopping','rabi_amplitude_729'),
                           ('RabiFlopping','frequency_selection'),
                           ('RabiFlopping','sideband_selection'),
                           
                           ('Crystallization', 'auto_crystallization'),
                           ('Crystallization', 'camera_record_exposure'),
                           ('Crystallization', 'camera_threshold'),
                           ('Crystallization', 'max_attempts'),
                           ('Crystallization', 'max_duration'),
                           ('Crystallization', 'min_duration'),
                           ('Crystallization', 'pmt_record_duration'),
                           ('Crystallization', 'pmt_threshold'),
                           ('Crystallization', 'use_camera'),

                           ('CalibrationScans', 'heating_rate_scan_interval'),
                           ]

    @classmethod
    def all_required_parameters(cls):
        parameters = set(cls.rabi_required_parameters)
        parameters = parameters.union(set(cls.trap_frequencies))
        parameters = parameters.union(set(excitation_729.all_required_parameters()))
        parameters = list(parameters)
        #removing parameters we'll be overwriting, and they do not need to be loaded
        parameters.remove(('Excitation_729','rabi_excitation_amplitude'))
        parameters.remove(('Excitation_729','rabi_excitation_duration'))
        parameters.remove(('Excitation_729','rabi_excitation_frequency'))
        return parameters
    
    def initialize(self, cxn, context, ident):

        self.ident = ident
        #self.drift_tracker = cxn.sd_tracker
        #self.calibrate_temp = self.make_experiment(calibrate_temperature)
        #self.calibrate_temp.initialize(cxn, context, ident)

        self.rabi_flopping = self.make_experiment(rabi_flopping)
        self.rabi_flopping.initialize(cxn, context, ident)
        self.fitter = rate_from_flops_fitter()

        self.save_context = cxn.context()
        self.dv = cxn.data_vault
        self.pv = cxn.parametervault
        #self.dds_cw = cxn.dds_cw
        self.cxnlab = labrad.connect('192.168.169.49', password='lab', tls_mode='off') #connection to labwide network
        
    def run(self, cxn, context):

        dv_args = {'output_size': 1,
                    'experiment_name' : self.name,
                    'window_name': 'heatingrate',
                    'dataset_name' : 'Heating_Rate'
                    }

        scan_methods.setup_data_vault(cxn, self.save_context, dv_args)

        scan_param = self.parameters.CalibrationScans.heating_rate_scan_interval

        self.scan = scan_methods.simple_scan(scan_param, 'us')

        for i,heat_time in enumerate(self.scan):
            #should_stop = self.pause_or_stop()
            #if should_stop: break
       
            replace = TreeDict.fromdict({
                                    'Heating.background_heating_time':heat_time,
                                    'Documentation.sequence':'calibrate_heating_rates',
                                       })
            self.rabi_flopping.set_parameters(replace)
            #self.calibrate_temp.set_parameters(replace)
            #self.calibrate_temp.set_progress_limits(0, 33.0)
   
            #(rsb_ex, bsb_ex) = self.calibrate_temp.run(cxn, context)
            
            #This only works for 1st order sideband
            #fac = rsb_ex/bsb_ex
	    
	    #correction for higher order sidebands
	    #k=abs(self.parameters.Spectrum.sideband_selection[2])
            #print "sideband order:",k
	    #fac= (rsb_ex/bsb_ex)**(1./k)
            
	    #nbar = fac/(1.0-fac)

            t,ex = self.rabi_flopping.run(cxn, context)
            t = np.array(t)
            ex = np.array(ex)
            ex = ex.flatten()
            if heat_time == 0:
                time_2pi = self.fitter.calc_2pitime(t,ex)
            
            trap_freq = self.parameters.TrapFrequencies.axial_frequency['Hz']
            nbar,time_2pi = self.fitter.fit_single_flop(heat_time,t,ex,trap_freq,time_2pi)
            
            
            submission = [heat_time['us']]
            submission.extend([nbar])
            print nbar
            if nbar > 0:
                self.dv.add(submission, context = self.save_context)
                print 'added submission'
            self.rabi_flopping.finalize(cxn, context)
            
    def finalize(self, cxn, context):
        self.rabi_flopping.save_parameters(self.dv, cxn, self.cxnlab, self.save_context)

if __name__ == '__main__':
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = rabi_calib_heating_rate(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)
