import labrad
import time

cxn = labrad.connect()

relay = cxn.sqip_expcontrol_ia_3133
dmm = cxn.keithley_2100_dmm

dmm.select_device('sqip_expcontrol GPIB Bus - USB0::0x05E6::0x2100::1243106')

relayList = [2,3,5,6,7,8,9,10,11,14,15,16,17,18,19,20,21,22,23,24,25] 

while True:    
    for channel in relayList:
        print "Channel", channel, " :"
        channel = channel - 1
        relay.activate_relay(channel) # - 1)
        time.sleep(2)
        val = dmm.get_dc_volts()
        print val, "Volt"

print 'Done'