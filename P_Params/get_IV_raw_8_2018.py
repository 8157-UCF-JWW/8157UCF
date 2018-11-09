# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 16:25:58 2018

@author: Hubert Seigneur
modified by Joe Walters to create smaller 'get IV function' August 2018

"""

#from IPython import get_ipython
#get_ipython().magic('reset -sf') # Erase all variables

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


# ******** TO DO: write a script that automatically get tag names


# Assign the IV tracer name for which you want the data
String ='S2'
Module=792

# Generate the full Tag name(s) from the IV tracer ID for the different variables of interest

I_tag=[String,'.A',Module,'.IV_I']
I_Tag=''.join(map(str,I_tag))  #concantenate for full string name

V_tag=[String,'.A',Module,'.IV_V']
V_Tag=''.join(map(str,V_tag))  #concantenate for full string name

P_tag=[String,'.A',Module,'.IV_P']
P_Tag=''.join(map(str,P_tag)) #concantenate for full string name

Isc_tag=[String,'.A',Module,'.Isc']
Isc_Tag=''.join(map(str,Isc_tag))  #concantenate for full string name

Voc_tag=[String,'.A',Module,'.Voc']
Voc_Tag=''.join(map(str,Voc_tag))  #concantenate for full string name

Flag_tag=[String,'.A',Module,'.IV_Flag']
Flag_Tag=''.join(map(str,Flag_tag))  #concantenate for full string name


# Specify date anf time
Day_Start = '2/08/2018 4:00:00.000'
Day_End = '2/08/2018 21:00:00.000'
print(' Isc Tag ' ,Isc_Tag)

#new code to get maximum
Time_Max = get_time_at_MaxIsc(Isc_Tag, Day_Start, Day_End)
print(Time_Max)

# print('index = ',Isc_Max_index[0],' Isc Maximum = ', Isc_Max_val)
# print('  at time stamp :',Isc_Values[Isc_Max_index[0],1]) # NOTE important syntax to get value, need ot inculde[] postions

""" Get the temperature value at the time the maximum value of tag was obtained """

TemperatureTag='Module_Temperatures.Median_Mod_Temp.fef629b9-de32-49c8-b171-a672c4f21fc3'
Module_temp = get_tag_value(TemperatureTag,Time_Max[0])
print('module temp = ',Module_temp, '  C')
  
""" Get irradiance at maximum tag value point,  Two irradiance sensors at field """

# IMT Solar Si-420TC
IrradianceTag1 = 'Ground_Pyra2_mV_Avg' # Plane of Array sensor at the array
Irradiance_max1 = get_tag_value(IrradianceTag1,Time_Max[0])
print('Irradiance = ',Irradiance_max1, ' mV')

# c-Si reference cell, tempearture compensated
IrradianceTag2 = 'Ground_RefCell1_Wm2_Avg' # Plane of Array Reference cell at the array
Irradiance_max2 = get_tag_value(IrradianceTag2,Time_Max[0])
print('Irradiance = ',Irradiance_max2, ' W/m2')

# get the IV data set for IV tag at time

timestart = Time_Max
I_Values, V_Values = get_IV_at_Time(I_Tag, V_Tag,timestart)

## Get the IV data set for that time stamp
#print(' Max Time @ ',Time_Max[0])
## Need the start time and end time of the IV curve trace
##   need to convert time as objects to time as datetime so you can add 1 minute
#
#IV_start=pd.to_datetime(Time_Max[0], dayfirst =True, format='%m/%d/%Y %H:%M:%S.%f')
## add 1 minute to that time
#IV_end = IV_start + timedelta(seconds=60)
#
#
#print('start IV @',IV_start, ' end IV @ ',IV_end)
#
## Need to convert time back to type and format the function will accept
#T_format_pd = '%Y-%m-%d %H:%M:%S'
#T_format_PI = '%m/%d/%Y %H:%M:%S.%f'
##  make strings
#IV_start_date_pd = datetime.strftime(IV_start, T_format_pd )
#IV_end_date_pd = datetime.strftime(IV_end, T_format_pd )
#print('srt pd ', IV_start_date_pd,'   end pd ', IV_end_date_pd)
##  make datetimes
#new_IV_start = datetime.strptime(IV_start_date_pd, T_format_pd)
#new_IV_end = datetime.strptime(IV_end_date_pd, T_format_pd)
#
#print(' new IV ', new_IV_end)
## make string
#IV_start = new_IV_start.strftime(T_format_PI)
#IV_end = new_IV_end.strftime(T_format_PI)
#
#
#print('start IV @', IV_start,'  end IV @ ',IV_end)
##
#
#
#I_Values =get_tag_values(I_Tag,IV_start, IV_end)
#V_Values =get_tag_values(V_Tag,IV_start, IV_end)


#Isc_Max_val = np.max(Isc_Values)
#
## Calculate standard mean, median and standard deviation for each object
## These values may indicate the smoothness of the dataset
#I_mean = np.mean(I_Values)
##Isc_mean = np.mean(Isc_Values)
#
#I_median =np.median(I_Values)
##Isc_median = np.median(Isc_Values)
#
#I_std = np.std(I_Values)
##Isc_std = np.std(Isc_Values)
#
## print the output from above
#print('I max = ',I_Max_val,'I mean = ',I_mean,'   I median = ', I_median,'  I stdev = ',I_std)
##print('Isc max = ',Isc_Max_val,'Isc mean = ',Isc_mean,'   Isc median = ', Isc_median,'  Isc stdev = ',Isc_std)
#

## create dataframe for each object
#df_I=pd.DataFrame(I_Values)
##df_Isc=pd.DataFrame(Isc_Values)
## create an array of rolling averages and rolling standard deviations
#I_mean_rolling_val = df_I.rolling(window=2).mean()
#I_std_rolling_val = df_I.rolling(window=3).std()
#
##Isc_mean_rolling_val = df_Isc.rolling(window=2).mean()
##Isc_std_rolling_val = df_Isc.rolling(window=3).std()
#
###print('')
###print a specific index
##print(I_Values[20],I_Values[28])
##print('shape I_Values = ', I_Values.shape)
##
#
#print(I_mean_rolling_val, I_std_rolling_val)
#
##
#I_roll_max = np.max(I_mean_rolling_val)
#print('max of I rolling ',I_roll_max)
#
## find the index of where the array has its maximum
#I_max_index = np.where(I_mean_rolling_val == I_mean_rolling_val.max())
#print('Index of max I rolling ', I_max_index)
#
#




