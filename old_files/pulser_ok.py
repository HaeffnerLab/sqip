#Created on Feb 22, 2012
#@author: Michael Ramm, Haeffner Lab
'''
### BEGIN NODE INFO
[info]
name = Pulser
version = 0.3
description = 
instancename = Pulser

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20
### END NODE INFO
'''
import ok
from labrad.server import LabradServer, setting, Signal
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue, DeferredLock, Deferred
from twisted.internet.threads import deferToThread
import numpy
import time
from hardwareConfiguration import hardwareConfiguration

okDeviceID = 'Pulser'
devicePollingPeriod = 10
channelTotal = 32
timeResolution = 40.0e-9 #seconds
timeResolvedResolution = timeResolution/4.0 #second
MIN_SEQUENCE = 0
MAX_SEQUENCE = 85 #seconds
MAX_SWITCHES = 1022 #maximum number of allowed switches in the sequence
collectionTimeRange = (0.010, 5.0)
class Pulser(LabradServer):
    name = 'Pulser'
    onSwitch = Signal(611051, 'signal: switch toggled', '(ss)')
    
    def initServer(self):
        self.channelDict =  hardwareConfiguration.channelDict
        self.collectionTime = hardwareConfiguration.collectionTime
        self.collectionMode = hardwareConfiguration.collectionMode
        self.sequenceType = hardwareConfiguration.sequenceType
        self.isProgrammed = hardwareConfiguration.isProgrammed
        self.inCommunication = DeferredLock()
        self.connectOKBoard()
        self.listeners = set()

    def connectOKBoard(self):
        self.xem = None
        fp = ok.FrontPanel()
        module_count = fp.GetDeviceCount()
        print "Found {} unused modules".format(module_count)
        for i in range(module_count):
            serial = fp.GetDeviceListSerial(i)
            tmp = ok.FrontPanel()
            tmp.OpenBySerial(serial)
            id = tmp.GetDeviceID()
            if id == okDeviceID:
                self.xem = tmp
                print 'Connected to {}'.format(id)
                self.programOKBoard()
                self.initializeSettings()
                return
        print 'Not found {}'.format(okDeviceID)
        print 'Will try again in {} seconds'.format(devicePollingPeriod)
        reactor.callLater(devicePollingPeriod, self.connectOKBoard)
    
    def programOKBoard(self):
        print 'Programming FPGA'
        prog = self.xem.ConfigureFPGA('photon.bit')
        if prog: raise("Not able to program FPGA")
        pll = ok.PLL22150()
        self.xem.GetEepromPLL22150Configuration(pll)
        pll.SetDiv1(pll.DivSrc_VCO,4)
        self.xem.SetPLL22150Configuration(pll)
    
    def initializeSettings(self):
        for channel in self.channelDict.itervalues():
            channelnumber = channel.channelnumber
            if channel.ismanual:
                state = self.cnot(channel.manualinv, channel.manualstate)
                self._setManual(channelnumber, state)
            else:
                self._setAuto(channelnumber, channel.autoinv)

    
    @setting(0, "New Sequence", returns = '')
    def newSequence(self, c):
        """
        Create New Pulse Sequence
        """
        c['sequence'] = Sequence()
    
    @setting(1, "Program Sequence", returns = '')
    def programSequence(self, c, sequence):
        """
        Programs Pulser with the current sequence.
        """
        if self.xem is None: raise Exception('Board not connected')
        sequence = c.get('sequence')
        if not sequence: raise Exception ("Please create new sequence first")
        parsedSequence = sequence.progRepresentation()
        yield self.inCommunication.acquire()
        yield deferToThread(self._programBoard, parsedSequence)    
        self.inCommunication.release()
        self.isProgrammed = True
    
    @setting(2, "Start Infinite", returns = '')
    def startInfinite(self,c):
        if not self.isProgrammed: raise Exception ("No Programmed Sequence")
        yield self.inCommunication.acquire()
        yield deferToThread(self._resetSeqCounter)
        yield deferToThread(self._startInfinite)
        self.sequenceType = 'Infinite'
        self.inCommunication.release()
    
    @setting(3, "Complete Infinite Iteration", returns = '')
    def completeInfinite(self,c):
        if self.sequenceType != 'Infinite': raise Exception( "Not Running Infinite Sequence")
        yield self.inCommunication.acquire()
        yield deferToThread(self._startSingle)
        self.inCommunication.release()
    
    @setting(4, "Start Single", returns = '')
    def start(self, c):
        if not self.isProgrammed: raise Exception ("No Programmed Sequence")
        yield self.inCommunication.acquire()
        yield deferToThread(self._resetSeqCounter)
        yield deferToThread(self._startSingle)
        self.sequenceType = 'One'
        self.inCommunication.release()
    
    @setting(5, 'Add TTL Pulse', channel = 's', start = 'v', duration = 'v')
    def addTTLPulse(self, c, channel, start, duration):
        """
        Add a TTL Pulse to the sequence, times are in seconds
        """
        hardwareAddr = self.channelDict.get(channel).channelnumber
        sequence = c.get('sequence')
        #simple error checking
        if hardwareAddr is None: raise Exception("Unknown Channel {}".format(channel))
        if not (MIN_SEQUENCE <= start,start + duration <= MAX_SEQUENCE): raise Exception ("Time boundaries are out of range")
        if not duration >= timeResolution: raise Exception ("Incorrect duration") 
        if not sequence: raise Exception ("Please create new sequence first")
        sequence.addTTLPulse(hardwareAddr, start, duration)
    
    @setting(6, 'Add TTL Pulses', pulses = '*(svv)')
    def addTTLPulses(self, c, pulses):
        """
        Add multiple TTL Pulses to the sequence, times are in seconds. The pulses are a list in the same format as 'add ttl pulse'.
        """
        for pulse in pulses:
            channel = pulse[0]
            start = pulse[1]
            duration = pulse[2]
            yield self.addTTLPulse(c, channel, start, duration)
    
    @setting(7, "Extend Sequence Length", timeLength = 'v')
    def extendSequenceLength(self, c, timeLength):
        """
        Allows to optionally extend the total length of the sequence beyond the last TTL pulse. 
        """
        sequence = c.get('sequence')
        if not (MIN_SEQUENCE <= timeLength <= MAX_SEQUENCE): raise Exception ("Time boundaries are out of range")
        if not sequence: raise Exception ("Please create new sequence first")
        sequence.extendSequenceLength(timeLength)
        
    
    @setting(8, "Stop Sequence")
    def stopSequence(self, c):
        """Stops any currently running  sequence"""
        yield self.inCommunication.acquire()
        yield deferToThread(self._resetRam)
        if self.sequenceType =='Infinite':
            yield deferToThread(self._stopInfinite)
        elif self.sequenceType =='One':
            yield deferToThread(self._stopSingle)
        self.inCommunication.release()
        self.sequenceType = None
    
    @setting(9, "Human Readable", returns = '*2s')
    def humanReadable(self, c):
        """
        Returns a readable form of the programmed sequence for debugging
        """
        sequence = c.get('sequence')
        if not sequence: raise Exception ("Please create new sequence first")
        ans = sequence.humanRepresentation()
        return ans.tolist()
    
    @setting(11, 'Get Channels', returns = '*s')
    def getChannels(self, c):
        """
        Returns all available channels
        """
        return self.channelDict.keys()
    
    @setting(12, 'Switch Manual', channelName = 's', state= 'b')
    def switchManual(self, c, channelName, state = None):  
        """
        Switches the given channel into the manual mode, by default will go into the last remembered state but can also
        pass the argument which state it should go into.
        """
        if channelName not in self.channelDict.keys(): raise Exception("Incorrect Channel")
        channel = self.channelDict[channelName]
        channelNumber = channel.channelnumber
        channel.ismanual = True
        if state is not None:
            channel.manualstate = state
        else:
            state = channel.manualstate
        yield self.inCommunication.acquire()
        yield deferToThread(self._setManual, channelNumber, self.cnot(channel.manualinv, state))
        self.inCommunication.release()
        if state:
            self.notifyOtherListeners(c,(channelName,'ManualOn'), self.onSwitch)
        else:
            self.notifyOtherListeners(c,(channelName,'ManualOff'), self.onSwitch)
    
    @setting(13, 'Switch Auto', channelName = 's', invert= 'b')
    def switchAuto(self, c, channelName, invert = None):  
        """
        Switches the given channel into the automatic mode, with an optional inversion.
        """
        if channelName not in self.channelDict.keys(): raise Exception("Incorrect Channel")
        channel = self.channelDict[channelName]
        channelNumber = channel.channelnumber
        channel.ismanual = False
        if invert is not None:
            channel.autoinv = invert
        else:
            invert = channel.autoinv
        yield self.inCommunication.acquire()
        yield deferToThread(self._setAuto, channelNumber, invert)
        self.inCommunication.release()
        self.notifyOtherListeners(c,(channelName,'Auto'), self.onSwitch)

    @setting(14, 'Get State', channelName = 's', returns = '(bbbb)')
    def getState(self, c, channelName):
        """
        Returns the current state of the switch: in the form (Manual/Auto, ManualOn/Off, ManualInversionOn/Off, AutoInversionOn/Off)
        """
        if channelName not in self.channelDict.keys(): raise Exception("Incorrect Channel")
        channel = self.channelDict[channelName]
        answer = (channel.ismanual,channel.manualstate,channel.manualinv,channel.autoinv)
        return answer
    
    @setting(15, 'Wait Sequence Done', timeout = 'v', returns = 'b')
    def waitSequenceDone(self, c, timeout = 10):
        """
        Returns true if the sequence has completed within a timeout period
        """
        requestCalls = int(timeout / 0.050 ) #number of request calls
        for i in range(requestCalls):
            yield self.inCommunication.acquire()
            done = yield deferToThread(self._isSeqDone)
            self.inCommunication.release()
            if done: returnValue(True)
            yield self.wait(0.050)
        returnValue(False)
    
    @setting(21, 'Set Mode', mode = 's', returns = '')
    def setMode(self, c, mode):
        """
        Set the counting mode, either 'Normal' or 'Differential'
        In the Normal Mode, the FPGA automatically sends the counts with a preset frequency
        In the differential mode, the FPGA uses triggers the pulse sequence
        frequency and to know when the repumping light is swtiched on or off.
        """
        if mode not in self.collectionTime.keys(): raise Exception("Incorrect mode")
        self.collectionMode = mode
        countRate = self.collectionTime[mode]
        yield self.inCommunication.acquire()
        if mode == 'Normal':
            #set the mode on the device and set update time for normal mode
            yield deferToThread(self._setModeNormal)
            yield deferToThread(self._setPMTCountRate, countRate)
        elif mode == 'Differential':
            yield deferToThread(self._setModeDifferential)
        yield deferToThread(self._resetFIFONormal)
        self.inCommunication.release()
    
    @setting(22, 'Set Collection Time', time = 'v', mode = 's', returns = '')
    def setCollectTime(self, c, time, mode):
        """
        Sets how long to collect photonslist in either 'Normal' or 'Differential' mode of operation
        """
        time = float(time)
        if not collectionTimeRange[0]<=time<=collectionTimeRange[1]: raise Exception('incorrect collection time')
        if mode not in self.collectionTime.keys(): raise("Incorrect mode")
        if mode == 'Normal':
            self.collectionTime[mode] = time
            yield self.inCommunication.acquire()
            yield deferToThread(self._resetFIFONormal)
            yield deferToThread(self._setPMTCountRate, time)
            self.inCommunication.release()
        elif mode == 'Differential':
            self.collectionTime[mode] = time
    
    @setting(23, 'Get Collection Time', returns = '(vv)')
    def getCollectTime(self, c):
        return collectionTimeRange
    
    @setting(24, 'Reset FIFO Normal', returns = '')
    def resetFIFONormal(self,c):
        """
        Resets the FIFO on board, deleting all queued counts
        """
        yield self.inCommunication.acquire()
        yield deferToThread(self._resetFIFONormal)
        self.inCommunication.release()
    
    @setting(25, 'Get PMT Counts', returns = '*(vsv)')
    def getALLCounts(self, c):
        """
        Returns the list of counts stored on the FPGA in the form (v,s1,s2) where v is the count rate in KC/SEC
        and s can be 'ON' in normal mode or in Differential mode with 866 on and 'OFF' for differential
        mode when 866 is off. s2 is the approximate time of acquisition.
        
        NOTE: For some reason, FGPA ReadFromBlockPipeOut never time outs, so can not implement requesting more packets than
        currently stored because it may hang the device.
        """
        yield self.inCommunication.acquire()
        countlist = yield deferToThread(self.doGetAllCounts)
        self.inCommunication.release()
        returnValue(countlist)
    
    def doGetAllCounts(self):
        inFIFO = self._getNormalTotal()
        reading = self._getNormalCounts(inFIFO)
        split = self.split_len(reading, 4)
        countlist = map(self.infoFromBuf, split)
        countlist = map(self.convertKCperSec, countlist)
        countlist = self.appendTimes(countlist, time.time())
        return countlist
    
    @staticmethod
    def infoFromBuf(buf):
        #converts the received buffer into useful information
        #the most significant digit of the buffer indicates wheter 866 is on or off
        count = 65536*(256*ord(buf[1])+ord(buf[0]))+(256*ord(buf[3])+ord(buf[2]))
        if count >= 2**31:
            status = 'OFF'
            count = count % 2**31
        else:
            status = 'ON'
        return [count, status]
    
    def convertKCperSec(self, input):
        [rawCount,type] = input
        countKCperSec = float(rawCount) / self.collectionTime[self.collectionMode] / 1000.
        return [countKCperSec, type]
        
    def appendTimes(self, list, timeLast):
        #in the case that we received multiple PMT counts, uses the current time
        #and the collectionTime to guess the arrival time of the previous readings
        #i.e ( [[1,2],[2,3]] , timeLAst = 1.0, normalupdatetime = 0.1) ->
        #    ( [(1,2,0.9),(2,3,1.0)])
        collectionTime = self.collectionTime[self.collectionMode]
        for i in range(len(list)):
            list[-i - 1].append(timeLast - i * collectionTime)
            list[-i - 1] = tuple(list[-i - 1])
        return list
    
    def split_len(self,seq, length):
        '''useful for splitting a string in length-long pieces'''
        return [seq[i:i+length] for i in range(0, len(seq), length)]
    
    @setting(26, 'Get Collection Mode', returns = 's')
    def getMode(self, c):
        return self.collectionMode
    
    @setting(31, "Reset Timetags")
    def resetTimetags(self, c):
        """Reset the time resolved FIFO to clear any residual timetags"""
        yield self.inCommunication.acquire()
        yield deferToThread(self._resetFIFOResolved)
        self.inCommunication.release()
    
    @setting(32, "Get Timetags", returns = '*v')
    def getTimetags(self, c):
        """Get the time resolved timetags"""
        yield self.inCommunication.acquire()
        counted = yield deferToThread(self._getResolvedTotal)
        raw = yield deferToThread(self._getResolvedCounts, counted)
        self.inCommunication.release()
        arr = numpy.fromstring(raw, dtype = numpy.uint16)
        del(raw)
        arr = arr.reshape(-1,2)
        timetags =( 65536  *  arr[:,0] + arr[:,1]) * timeResolvedResolution
        returnValue(timetags)
    
    @setting(33, "Get TimeTag Resolution", returns = 'v')
    def getTimeTagResolution(self, c):
        return timeResolvedResolution
    
    def wait(self, seconds, result=None):
        """Returns a deferred that will be fired later"""
        d = Deferred()
        reactor.callLater(seconds, d.callback, result)
        return d
    
    def _programBoard(self, sequence):
        self.xem.WriteToBlockPipeIn(0x80, 2, sequence)
  
    def _startInfinite(self):
        self.xem.SetWireInValue(0x00,0x06,0x06)
        self.xem.UpdateWireIns()
    
    def _stopInfinite(self):
        self.xem.SetWireInValue(0x00,0x02,0x06)
        self.xem.UpdateWireIns()
        
    def _startSingle(self):
        self.xem.SetWireInValue(0x00,0x04,0x06)
        self.xem.UpdateWireIns()
    
    def _stopSingle(self):
        self.xem.SetWireInValue(0x00,0x00,0x06)
        self.xem.UpdateWireIns()
    
    def _resetRam(self):
        self.xem.ActivateTriggerIn(0x40,1)
        
    def _resetSeqCounter(self):
        self.xem.ActivateTriggerIn(0x40,0)
    
    def _resetFIFONormal(self):
        self.xem.ActivateTriggerIn(0x40,2)
    
    def _resetFIFOResolved(self):
        self.xem.ActivateTriggerIn(0x40,3)
    
    def _setModeNormal(self):
        """user selects PMT counting rate"""
        self.xem.SetWireInValue(0x00,0x00,0x01)
        self.xem.UpdateWireIns()
    
    def _setModeDifferential(self):
        """pulse sequence controls the PMT counting rate"""
        self.xem.SetWireInValue(0x00,0x01,0x01)
        self.xem.UpdateWireIns()
    
    def _isSeqDone(self):
        self.xem.SetWireInValue(0x00,0x00,0xf0)
        self.xem.UpdateWireIns()
        self.xem.UpdateWireOuts()
        done = self.xem.GetWireOutValue(0x21)
        return done
    
    def _getResolvedTotal(self):
        self.xem.UpdateWireOuts()
        counted = self.xem.GetWireOutValue(0x22)
        return counted
    
    def _getResolvedCounts(self, number):
        buf = "\x00"*(number*2)
        self.xem.ReadFromBlockPipeOut(0xa0,2,buf)
        return buf
    
    def _getNormalTotal(self):
        self.xem.SetWireInValue(0x00,0x40,0xf0)
        self.xem.UpdateWireIns()
        self.xem.UpdateWireOuts()
        done = self.xem.GetWireOutValue(0x21)
        return done
    
    def _getNormalCounts(self, number):
        buf = "\x00"* ( number * 2 )
        self.xem.ReadFromBlockPipeOut(0xa1,2,buf)
        return buf
    
    def _howManySequencesDone(self):
        self.xem.SetWireInValue(0x00,0x20,0xf0)
        self.xem.UpdateWireIns()
        self.xem.UpdateWireOuts()
        completed = xem.GetWireOutValue(0x21)
        return completed
    
    def _setPMTCountRate(self, time):
        #takes time in seconds
        self.xem.SetWireInValue(0x01,int(1000 * time))
        self.xem.UpdateWireIns()
        
    def _setAuto(self, channel, inversion):
        self.xem.SetWireInValue(0x02,0x00, 2**channel)
        if not inversion:
            self.xem.SetWireInValue(0x03,0x00, 2**channel)
        else:
            self.xem.SetWireInValue(0x03,2**channel, 2**channel)
        self.xem.UpdateWireIns()
    
    def _setManual(self, channel, state):
        self.xem.SetWireInValue(0x02,2**channel, 2**channel )
        if state:
            self.xem.SetWireInValue(0x03,2**channel, 2**channel)
        else:
            self.xem.SetWireInValue(0x03,0x00, 2**channel)
        self.xem.UpdateWireIns()
    
    def cnot(self, control, input):
        if control:
            input = not input
        return input
    
    def notifyOtherListeners(self, context, message, f):
        """
        Notifies all listeners except the one in the given context, excuting function of
        """
        notified = self.listeners.copy()
        notified.remove(context.ID)
        f(message,notified)   
    
    def initContext(self, c):
        """Initialize a new context object."""
        self.listeners.add(c.ID)
    
    def expireContext(self, c):
        self.listeners.remove(c.ID)

            
class Sequence():
    """Sequence for programming pulses"""
    def __init__(self):
        #dictionary in the form time:which channels to switch
        #time is expressed as timestep with the given resolution
        #which channels to switch is a channelTotal-long array with 1 to switch ON, -1 to switch OFF, 0 to do nothing
        self.switchingTimes = {0:numpy.zeros(channelTotal, dtype = numpy.int8)} 
        self.switches = 1 #keeps track of how many switches are to be performed (same as the number of keys in the switching Times dictionary"
    
    def addTTLPulse(self, channel, start, duration):
        """adding TTL pulse, times are in seconds"""
        self._addNewSwitch(start, channel, 1)
        self._addNewSwitch(start + duration, channel, -1)
    
    def extendSequenceLength(self, timeLength):
        """Allows to extend the total length of the sequence"""
        self._addNewSwitch(timeLength,0,0)

    def secToStep(self, sec):
        '''converts seconds to time steps'''
        return int( sec / timeResolution) 
    
    def numToHex(self, number):
        '''converts the number to the hex representation for a total of 32 bits
        i.e: 3 -> 00000000...000100 ->  \x00\x00\x03\x00, note that the order of 8bit pieces is switched'''
        a,b = number // 65536, number % 65536
        return str(numpy.uint16([a,b]).data)

    def _addNewSwitch(self, t, chan, value):
        timeStep = self.secToStep(t)
        if self.switchingTimes.has_key(timeStep):
            if self.switchingTimes[timeStep][chan]: raise Exception ('Double switch at time {} for channel {}'.format(t, chan))
            self.switchingTimes[timeStep][chan] = value
        else:
            if self.switches == MAX_SWITCHES: raise Exception("Exceeded maximum number of switches {}".format(self.switches))
            self.switchingTimes[timeStep] = numpy.zeros(channelTotal, dtype = numpy.int8)
            self.switches += 1
            self.switchingTimes[timeStep][chan] = value
           
    def progRepresentation(self):
        """Returns the representation of the sequence for programming the FPGA"""
        rep = ''
        lastChannels = numpy.zeros(channelTotal)
        powerArray = 2**numpy.arange(channelTotal, dtype = numpy.uint64)
        for key,newChannels in sorted(self.switchingTimes.iteritems()):
            channels = lastChannels + newChannels #computes the action of switching on the state
            if (channels < 0).any(): raise Exception ('Trying to switch off channel that is not already on')
            channelInt = numpy.dot(channels,powerArray)
            rep = rep + self.numToHex(key) + self.numToHex(channelInt) #converts the new state to hex and adds it to the sequence
            lastChannels = channels
        rep = rep + 2*self.numToHex(0) #adding termination
        return rep
    
    def humanRepresentation(self):
        """Returns the human readable version of the sequence for FPGA for debugging"""
        rep = self.progRepresentation()
        arr = numpy.fromstring(rep, dtype = numpy.uint16) #does the decoding from the string
        arr = numpy.array(arr, dtype = numpy.uint32) #once decoded, need to be able to manipulate large numbers
        arr = arr.reshape(-1,4)
        times =( 65536  *  arr[:,0] + arr[:,1]) * timeResolution
        channels = ( 65536  *  arr[:,2] + arr[:,3])
        
        def expandChannel(ch):
            '''function for getting the binary representation, i.e 2**32 is 1000...0'''
            return bin(ch)[2:].zfill(32)
        
        channels = map(expandChannel,channels)
        return numpy.vstack((times,channels)).transpose()
     
if __name__ == "__main__":
    from labrad import util
    util.runServer( Pulser() )