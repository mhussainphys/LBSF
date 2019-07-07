from LVScanFunc import * 
from FileComm import *
from AllModules import *

Resource = InitiateResource()

Voltage = InitialVoltage

IncludeLowVoltageScan(True) #Tells Autopilot to include low voltage scan

if LowVoltageBoolean():
    ScanNumber = GetNextNumber(ScanFilename)
    print "\n*********************** Starting scan %d ****************************" % ScanNumber

while abs(Voltage) <= abs(FinalVoltage):
    print '\n*************************'
    print 'Waiting for the green signal from the autopilot\n'
    RunNumber = ReceiveLVGreenSignal()

    if RunNumber != 0:

        print 'Changing the Voltage to %f V' % Voltage
        MeasVoltage, MeasCurrent = SetVoltage(Resource, Voltage, VoltageSettleTime, False)
        
        EnvTimestamp = (datetime.now() - datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).total_seconds() - 3600 #For daylight savings time
        Temp20 = ConvertEnv(EnvTimestamp)

        ##### Write scan data for this run
        WriteVoltageScanDataFile(ScanNumber, RunNumber, Voltage, MeasVoltage, MeasCurrent, Temp20)
        
        if InitialVoltage != FinalVoltage:
            Voltage = Voltage + VoltageStep

        if abs(Voltage) > abs(FinalVoltage):
            
            StopAutopilot = raw_input("This is the last allowed voltage value. Do you want to stop the autopilot after this iteration (y/n) ? ")
            if StopAutopilot == "y" or StopAutopilot == "Y" : 
                os.system("source %s" % StopAutopilotFileName)
            else:
                print 'Now the autopilot will keep on taking data even after the scan completes, at Voltage %f V' % (Voltage - VoltageStep)
                IncludeLowVoltageScan(False) # Tells Autopilot to keep on running without including the LV scan program

        print 'The current run number is ', RunNumber
        print '*************************\n'
        SendAutopilotGreenSignal()

print "\n*********************** Scan %d complete ****************************" % ScanNumber

time.sleep(10)
DisableOutput = raw_input("Ramp down (y), disable Low Voltage Output (n)?")
if  DisableOutput == "y" or DisableOutput == "Y" :
    RampDown(Resource, Voltage, VoltageSettleTime, False)
if  DisableOutput == "n" or DisableOutput == "N" :
    DisableLVOutput(Resource)
