# LBSF
LGAD Bias Scan Framework

Instructions for running scan:

1) Make sure HV is supplied to LGAD from TOP keithley
2) Start Sidet_Labview.gvi with only the DMM enabled (no sourcemeter)
3) Make sure motors are in appropriate position
4) Make sure photodiode and all testing channels are returned to VME
5) Specify scan parameters in AllModules.py
6) start listener: python LVScanListener.py (dedicated tab)
7) ./RunAutopilot.sh
