import requests
import ast
from datetime import datetime
import time
import numpy as np
import getpass
import os
import subprocess as sp
import socket
import sys
import glob
import subprocess
from subprocess import Popen, PIPE
import pipes
from pipes import quote
import argparse
import visa
import time
from GetEnv import *
from bisect import bisect_left
import getpass

#### OTSDAQ parameters ####
ip_address = "192.168.133.50"
use_socket = 8000
RunFilename = "/home/daq/otsdaq/srcs/otsdaq_cmstiming/Data_2018_09_September/ServiceData/RunNumber/OtherRuns0NextRunNumber.txt"

### Voltage Scan Parameters ###
InitialVoltage = 0 
FinalVoltage = -340
VoltageStep = -10
VoltageSettleTime = 10 
Compliance = 100e-06
LBSFBaseDir = '/home/daq/BiasScan/LBSF/'
ScanFilename = '%sNextScanNumber.txt' % LBSFBaseDir
LowVoltageControlFileName = '%sLVControl.txt' % LBSFBaseDir
VoltageScanDataFileName = '%sVoltageScanDataRegistry/' % LBSFBaseDir
IncludeLowVoltageFileName = '%sIncludeLowVoltageFile.txt' % LBSFBaseDir
StopAutopilotFileName = '%sStopAutopilot.sh' % LBSFBaseDir
