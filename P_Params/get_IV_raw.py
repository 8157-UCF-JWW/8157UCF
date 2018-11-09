# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 16:25:58 2018
@author: Siyu Guo
Modified by July 27, 2018 by Joe Walters
    Create function to get the raw I-V trace from PI server


"""# -*- coding: utf-8 -*-
"""

"""
# import functions needed for this module
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy import linalg
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from scipy.interpolate import UnivariateSpline
# Allow this program to see programs in different directories
import sys  
sys.path.append('C:\Program Files (x86)\PIPC\AF\PublicAssemblies\4.0\\')  
import clr  
#clr.AddReference('OSIsoft.AFSDK')  
from OSIsoft.AF.PI import *  
from OSIsoft.AF.Search import *  
from OSIsoft.AF.Asset import *  
from OSIsoft.AF.Data import *  
from OSIsoft.AF.Time import *  


import sys
sys.path.insert(0, 'C:\8157_PythonClone\8157UCF\P_Functions') #destination directory
import Pithon_functions #program to import
from Pithon_functions import connect_to_Server
from Pithon_functions import get_tag_snapshot
from Pithon_functions import get_tag_values
from Pithon_functions import get_tag_attribute_values

# call funtion from 'Pithon_functions' to connect to server
connect_to_Server('net1552.net.ucf.edu')  
piServer='net1552.net.ucf.edu'


# set IVTracer (Module) ID for the data you want to obtain
Module=792

# build Tag names based on Module ID and 
I_tag=['S2.A',Module,'.IV_I']
I_Tag=''.join(map(str,I_tag))

V_tag=['S2.A',Module,'.IV_V']
V_Tag=''.join(map(str,V_tag))

P_tag=['S2.A',Module,'.IV_P']
P_Tag=''.join(map(str,P_tag))

Isc_tag=['S2.A',Module,'.Isc']
Isc_Tag=''.join(map(str,Isc_tag))

Voc_tag=['S2.A',Module,'.Voc']
Voc_Tag=''.join(map(str,Voc_tag))

# create arrays of length 1000 to hold values
isc=np.zeros(shape=(1000,),dtype=float,order='F')
voc=np.zeros(shape=(1000,),dtype=float,order='F')
isc_corrected_base=np.zeros(shape=(1000,),dtype=float,order='F')
voc_corrected_base=np.zeros(shape=(1000,),dtype=float,order='F')

#Temperaturetag=['ModTemp',2,'_Avg']
# value, timestamp = get_tag_snapshot('Ground_Pyra2_mV_Avg')  
# print('Timestamp: {0} Value: {1}'.format(timestamp, value))  
timestart = '8/14/2016 11:30:00'
timeend = '8/14/2016 15:00:00'

# call function with values
#I_Values = get_tag_values(I_Tag,timestart,timeend)
#Isc_Values = get_tag_values(Isc_Tag,timestart,timeend)


# call function with value land time stamps
I_Values = get_tag_attribute_values(I_tag, timestart, timeend)
#Isc_Values = get_tag_attribute_values(Isc_tag, timestart, timeend)

# Find Maximum in object
I_Max_val = np.max(I_Values)
#Isc_Max_val = np.max(Isc_Values)

# Calculate standard mean, median and standard deviation for each object
# These values may indicate the smoothness of the dataset
I_mean = np.mean(I_Values)
#Isc_mean = np.mean(Isc_Values)

I_median =np.median(I_Values)
#Isc_median = np.median(Isc_Values)

I_std = np.std(I_Values)
#Isc_std = np.std(Isc_Values)

# print the output from above
print('I max = ',I_Max_val,'I mean = ',I_mean,'   I median = ', I_median,'  I stdev = ',I_std)
#print('Isc max = ',Isc_Max_val,'Isc mean = ',Isc_mean,'   Isc median = ', Isc_median,'  Isc stdev = ',Isc_std)


# create dataframe for each object
df_I=pd.DataFrame(I_Values)
#df_Isc=pd.DataFrame(Isc_Values)
# create an array of rolling averages and rolling standard deviations
I_mean_rolling_val = df_I.rolling(window=2).mean()
I_std_rolling_val = df_I.rolling(window=3).std()

#Isc_mean_rolling_val = df_Isc.rolling(window=2).mean()
#Isc_std_rolling_val = df_Isc.rolling(window=3).std()

##print('')
##print a specific index
#print(I_Values[20],I_Values[28])
#print('shape I_Values = ', I_Values.shape)
#

print(I_mean_rolling_val, I_std_rolling_val)

#
I_roll_max = np.max(I_mean_rolling_val)
print('max of I rolling ',I_roll_max)

# find the index of where the array has its maximum
I_max_index = np.where(I_mean_rolling_val == I_mean_rolling_val.max())
print('Index of max I rolling ', I_max_index)



    



TemperatureTag='Ground_RTD_C_Avg(1)'

Time1='8/13/2016 1:59:00 AM' # you must specify the starting time

#create an array to hold hours 1 to 18 and minutes 1 to 60
Day=13
hour=np.r_[1:18]
minute=np.r_[0:60]
# set initial values for sc and sc0
sc=0
sc0=0

k=0

#loop to find
#
#for i in hour:
# 
#
#    for j in np.arange(0, 60, 6):
#        
#        Time0=Time1;
#        if j<10:
#            time1=[Day,i,':0',j,':00']
#            time2=[Day,i,':0',j+6,':00']
#        else:
#            time1=[Day,i,':',j,':00']
#            time2=[Day,i,':',j+6,':00']
#
#        Time1=''.join(map(str,time1))
#        Time2=''.join(map(str,time2))
#        print(Time1)
#
##        Module_Temp=get_tag_value(TemperatureTag,Time1)
##        SC=get_tag_value(Isc_Tag,Time1) # get short-circuit current
##        sc=SC
##        OC=get_tag_value(Voc_Tag,Time1) # open-circuit voltage 
##        isc[k,]=SC
##        voc[k,]=OC
##        isc_corrected_base[k,]=SC-(Module_Temp-50)*0.0006
##        voc_corrected_base[k,]=(Module_Temp-50)*0.132+OC
#        if sc>sc0: # get the time when the module has maxinmum current
#            sc0=sc
#            Time0_select=Time0
#            Time1_select=Time1
#            Time2_select=Time2
#            Temp_IV=module_Temp
#
#       
#        k=k+1
#

## get the I-V curve and irradiance of the maximum current
##Current = get_tag_values(I_Tag,Time0_select,Time1_select) 
#Voltage_base = get_tag_values(V_Tag,Time0_select,Time1_select)
#Power_base=get_tag_values(P_Tag,Time0_select,Time1_select)
#Current_base=get_tag_values(I_Tag,Time0_select,Time1_select)
##Power1=Power[0:169,:]
##Current=Power/Voltage
##Voltage=Power1/Current
#Irradiance=get_tag_value('Ground_Pyra2_mV_Avg',Time1_select)
#irradiance=Irradiance
#Voltage_Correct_base=(Temp_IV-50)*0.132+Voltage_base # correct voltage and current according to module temperature
#Size=len(Current_base)
#Isc0=Current_base[Size-1,0]
#delta_Isc=Isc0/irradiance*10-Isc0
#Current_Correct_base=Current_base+delta_Isc              
# 
#
#           
#isc_corrected1_base=Isc0/irradiance*10-isc_corrected_base
#isc1=isc_corrected1_base=Isc0/irradiance*10-isc
#
##newList = list(dataObject)
##print 'time period is' , timeObject
#
##for i in newList:
# #   print(i)
#    
#I_base= Current_Correct_base[:,1]
#V_base= Voltage_Correct_base[:,1]
#
#
#plt.plot(V_base,I_base)
#
##plt.plot(Voc1,Isc1,'*')
#
#plt.plot(voc_corrected_base,isc_corrected1_base,'.')
#
#np.savetxt('IV_8_13_2016.txt',np.transpose([V_base,I_base]))
#
#np.savetxt('sunsvoc_8_13_2016.txt',np.transpose([voc_corrected_base,isc_corrected1_base]))
#
#x=voc_corrected_base #voltage
#y=isc_corrected1_base #current
#xx = np.linspace(0,x.max(), 1000) # do interpolation first
#itp = interp1d(x,y, kind='linear')
#window_size, poly_order = 101, 5
#yy_sg = savgol_filter(itp(xx), window_size, poly_order)
#plt.plot(x,y,'.')
#plt.plot(xx, yy_sg, 'k', label= "Smoothed curve")
#Isc_measured_base=yy_sg
#Voc_measured_base=xx
#
#
#
##print 'Number of data points is',len(newList)
## PSDK maximum/minimum-->time
#
