from common.abstractdevices.script_scanner.scan_methods import experiment
from excitation_729_kicked import excitation_729_kicked
from sqip.scripts.scriptLibrary.common_methods_729 import common_methods_729 as cm
from sqip.scripts.scriptLibrary import dvParameters
import time
import labrad
from labrad.units import WithUnit
from numpy import linspace

class displaced_ramsey_scan_pulse(experiment):
    
    name = 'DisplacedRamseyScanPulse'
    trap_frequencies = [
                        ('TrapFrequencies','axial_frequency'),
                        ('TrapFrequencies','radial_frequency_1'),
                        ('TrapFrequencies','radial_frequency_2'),
                        ('TrapFrequencies','rf_drive_frequency'),                       
                        ]

    required_parameters = [
                           ('RabiFlopping','rabi_amplitude_729'),
                           ('RabiFlopping','manual_scan'),
                           ('RabiFlopping','manual_frequency_729'),
                           ('RabiFlopping','line_selection'),
                           ('RabiFlopping','rabi_amplitude_729'),
                           ('RabiFlopping','frequency_selection'),
                           ('RabiFlopping','sideband_selection'),

                           ('Heating', 'resonant_heating_duration'),
                           ('Heating', 'resonant_heating_repump_additional'),
                           ('Heating', 'resonant_heating_amplitude_397'),
                           ('Heating', 'resonant_heating_frequency_397'),
                           ('Heating', 'resonant_heating_frequency_866'),
                           ('Heating', 'resonant_heating_amplitude_866'),
                           ('Heating', 'coherent_evolution_time'),
                           ('Heating', 'resonant_kicking_frequency'),
                           ('Heating', 'enable_kicking'),
                           ('RabiFlopping_Sit', 'sit_on_excitation'),
                           
                           ('PulsedHeat','pulse_length_scan'),
                           ]
    required_parameters.extend(trap_frequencies)
    optional_parmeters = [
                          ('DisplacedRamseyPulse', 'window_name')
                          ]
    required_parameters.extend(excitation_729_kicked.required_parameters)
    #removing parameters we'll be overwriting, and they do not need to be loaded
    required_parameters.remove(('Excitation_729','rabi_excitation_amplitude'))
    required_parameters.remove(('Excitation_729','rabi_excitation_duration'))
    required_parameters.remove(('Excitation_729','rabi_excitation_frequency'))
    required_parameters.remove(('Heating','coherent_evolution_time'))
    
    def initialize(self, cxn, context, ident):
        self.ident = ident
        self.excite = self.make_experiment(excitation_729_kicked)
        self.excite.initialize(cxn, context, ident)
        self.scan = []
        self.amplitude = None
        self.duration = None
        self.cxnlab = labrad.connect('192.168.169.49') #connection to labwide network
        self.drift_tracker = cxn.sd_tracker
        self.square_pulse_generator = cxn.rigol_dg4062_server
        self.square_pulse_generator.select_device('sqip_expcontrol GPIB Bus - USB0::0x1AB1::0x0641::DG4D152500738')
        self.init_pulsing_freq = self.square_pulse_generator.frequency()
        self.init_pulsing_state = self.square_pulse_generator.output()
        self.square_pulse_generator.frequency(self.parameters.Heating.resonant_kicking_frequency)
#        self.square_pulse_generator.burst_mode('gated')
#        self.square_pulse_generator.burst_state(True)
        if self.parameters.Heating.enable_kicking:
            pass
            #self.square_pulse_generator.output(True)
        self.dv = cxn.data_vault
        self.data_save_context = cxn.context()
    
    def setup_sequence_parameters(self):
        self.load_frequency()
        flop = self.parameters.RabiFlopping
        self.parameters['Excitation_729.rabi_excitation_amplitude'] = flop.rabi_amplitude_729
        self.parameters['Excitation_729.rabi_excitation_duration'] = self.parameters.RabiFlopping_Sit.sit_on_excitation
        minim,maxim,steps = self.parameters.PulsedHeat.pulse_length_scan
        minim = minim['us']; maxim = maxim['us']
        self.scan = linspace(minim,maxim, steps)
        self.scan = [WithUnit(pt, 'us') for pt in self.scan]
        
    def setup_data_vault(self):
        localtime = time.localtime()
        datasetNameAppend = time.strftime("%Y%b%d_%H%M_%S",localtime)
        dirappend = [ time.strftime("%Y%b%d",localtime) ,time.strftime("%H%M_%S", localtime)]
        directory = ['','Experiments']
        directory.extend([self.name])
        directory.extend(dirappend)
        self.dv.cd(directory ,True, context = self.data_save_context)
        output_size = self.excite.output_size
        dependants = [('Excitation','Ion {}'.format(ion),'Probability') for ion in range(output_size)]
        self.dv.new('Displaced Ramsey {}'.format(datasetNameAppend),[('Excitation', 'us')], dependants , context = self.data_save_context)
        window_name = self.parameters.get('DisplacedRamseyScanPulse.window_name', ['Displaced Ramsey Scan Pulse'])
        self.dv.add_parameter('Window', window_name, context = self.data_save_context)
        self.dv.add_parameter('plotLive', True, context = self.data_save_context)
    
    def load_frequency(self):
        #reloads trap frequencyies and gets the latest information from the drift tracker
        self.reload_some_parameters(self.trap_frequencies) 
        flop = self.parameters.RabiFlopping
        frequency = cm.frequency_from_line_selection(flop.frequency_selection, flop.manual_frequency_729, flop.line_selection, self.drift_tracker)
        trap = self.parameters.TrapFrequencies
        if flop.frequency_selection == 'auto':
            frequency = cm.add_sidebands(frequency, flop.sideband_selection, trap)
        self.parameters['Excitation_729.rabi_excitation_frequency'] = frequency
        
    def run(self, cxn, context):
        self.setup_data_vault()
        self.setup_sequence_parameters()
        for i,duration in enumerate(self.scan):
            should_stop = self.pause_or_stop()
            if should_stop: break
            self.load_frequency()
            self.parameters['Heating.resonant_heating_duration'] = duration
            self.excite.set_parameters(self.parameters)
            excitation = self.excite.run(cxn, context)
            submission = [duration['us']]
            submission.extend(excitation)
            self.dv.add(submission, context = self.data_save_context)
            self.update_progress(i)
     
    def finalize(self, cxn, context):
        self.save_parameters(self.dv, cxn, self.cxnlab, self.data_save_context)
        self.square_pulse_generator.frequency(self.init_pulsing_freq)
        #self.square_pulse_generator.output(self.init_pulsing_state)
        self.excite.finalize(cxn, context)

    def update_progress(self, iteration):
        progress = self.min_progress + (self.max_progress - self.min_progress) * float(iteration + 1.0) / len(self.scan)
        self.sc.script_set_progress(self.ident,  progress)

    def save_parameters(self, dv, cxn, cxnlab, context):
        measuredDict = dvParameters.measureParameters(cxn, cxnlab)
        dvParameters.saveParameters(dv, measuredDict, context)
        dvParameters.saveParameters(dv, dict(self.parameters), context)   

if __name__ == '__main__':
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = displaced_ramsey_scan_pulse(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)