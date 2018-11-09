# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 15:20:17 2018

@author: jwalters

Get Isc and Voc then put array for equal time index


"""


# set pathway for access to local functions
import sys
sys.path.insert(0, 'C:\8157_PythonClone\8157UCF\P_Functions') #destination directory


# import library and functions from world
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from numpy import array

from scipy.interpolate import interp1d
from scipy import linalg
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from scipy.interpolate import UnivariateSpline

#from datetime import date
#from datetime import time

from datetime import timedelta
from datetime import datetime

# import functions and values from local library or functions

from Pithon_functions import * 
from Pithon_functions import connect_to_Server
from Pithon_functions import get_tag_snapshot
from Pithon_functions import get_tag_value
from Pithon_functions import get_tag_values
from Pithon_functions import get_tag_attribute_values

#from RUNFILE import String
#from RUNFILE import Module
#from RUNFILE import Day_Start
#from RUNFILE import Day_End
#from RUNFILE import Day_Noon


# cononect to PI server
piServer ='net1552.net.ucf.edu'
connect_to_Server(piServer)  

# Get IV pair for single tracer

# Assign the IV tracer name for which you want the data
String ='S2'
Module=792

# Generate the full Tag name(s) from the IV tracer ID for the different variables of interest

P_tag=[String,'.A',Module,'.IV_P']
P_Tag=''.join(map(str,P_tag)) #concantenate for full string name

Isc_tag=[String,'.A',Module,'.Isc']
Isc_Tag=''.join(map(str,Isc_tag))  #concantenate for full string name

Voc_tag=[String,'.A',Module,'.Voc']
Voc_Tag=''.join(map(str,Voc_tag))  #concantenate for full string name


# Specify date anf time
Day_Start = '2/01/2018 4:00:00.000'
Day_End = '2/083/2018 21:00:00.000'
print(' Isc Tag ' ,Isc_Tag)

