# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 16:25:58 2018

@author: Hubert Seigneur
"""

#from IPython import get_ipython
#get_ipython().magic('reset -sf') # Erase all variables

from RUNFILE import String
from RUNFILE import Module
from RUNFILE import Day_Start
from RUNFILE import Day_End
from RUNFILE import Day_Noon

from scipy.interpolate import interp1d
import numpy as np
from numpy import array
from scipy import linalg
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from scipy.interpolate import UnivariateSpline

from Pithon_loadfloat_milliseconds import * 
import matplotlib.pyplot as plt



# ******** TO DO: write a script that automatically get tag names

connect_to_Server("net1552.net.ucf.edu")  
value, timestamp = get_tag_snapshot('Ground_Pyra2_mV_Avg')  
print('Timestamp: {0} Value: {1}'.format(timestamp, value))  


#Day='8/13/2016 '
#Day ='8/9/2017' # TEST: module with missing data at 14ms and 70ms


#Module=792
#Module=584 # TEST: module with missing data at 14ms and 70ms

#Temperaturetag=['ModTemp',2,'_Avg']
#TemperatureTag='Ground_RTD_C_Avg(1)'
TemperatureTag='Module_Temperatures.Median_Mod_Temp.fef629b9-de32-49c8-b171-a672c4f21fc3'

#I_tag=['S2.A',Module,'.IV_I']
#I_Tag=''.join(map(str,I_tag))
#
#V_tag=['S2.A',Module,'.IV_V']
#V_Tag=''.join(map(str,V_tag))
#
#P_tag=['S2.A',Module,'.IV_P']
#P_Tag=''.join(map(str,P_tag))
#
#Isc_tag=['S2.A',Module,'.Isc']
#Isc_Tag=''.join(map(str,Isc_tag))
#
#Voc_tag=['S2.A',Module,'.Voc']
#Voc_Tag=''.join(map(str,Voc_tag))

I_tag=[String,'.A',Module,'.IV_I']
I_Tag=''.join(map(str,I_tag))

V_tag=[String,'.A',Module,'.IV_V']
V_Tag=''.join(map(str,V_tag))

P_tag=[String,'.A',Module,'.IV_P']
P_Tag=''.join(map(str,P_tag))

Isc_tag=[String,'.A',Module,'.Isc']
Isc_Tag=''.join(map(str,Isc_tag))

Voc_tag=[String,'.A',Module,'.Voc']
Voc_Tag=''.join(map(str,Voc_tag))

Flag_tag=[String,'.A',Module,'.IV_Flag']
Flag_tag=''.join(map(str,Flag_tag))

# Specify date anf time
#Day_Start='8/9/2017 4:00:00.000'
#Day_End='8/9/2017 21:00:00.000'
#Day_Noon = '8/9/2017 12:00:00'

#Day_Start='8/9/2017 8:00:00.000' #TEST: module with missing data at 8:07:55 AM and 14ms and 70ms
#Day_End='8/9/2017 8:10:00.000' #TEST: module with missing data at 8:07:55 AM and 14ms and 70ms
#Day_Start='8/9/2017 5:00:00.000' #TEST: module with missing data at 8:07:55 AM and 14ms and 70ms
#Day_End='8/9/2017 20:00:00.000' #TEST: module with missing data at 8:07:55 AM and 14ms and 70ms

# Find times when IV Flags are true
iv_flag = get_tag_attribute_values(Flag_tag, Day_Start, Day_End) #TEST: module with missing data at 14ms and 70ms
#iv_flag = get_tag_attribute_values('S2.A584.IV_Flag', Day_Start, Day_End) #TEST: module with missing data at 14ms and 70ms#iv_flag_test = [[0 for j in range(2)] for i in range(len(iv_flag))]
iv_flag_true = []
ISC = []
VOC = []
ISC_corrected = []
VOC_corrected = []
ISC_max = 0
Temp_IV = 0

for index in range(len(iv_flag)):
#    iv_flag_test[index]=iv_flag[index,0],iv_flag[index,1]
#    print('index is', index)
        
    if iv_flag[index,0] == 'True':
        iv_flag_true.append([iv_flag[index,0],iv_flag[index,1]])

#for i, sample in enumerate(iv_flag_true):
    
#        ISC_base = []
#        VOC_base = []
#        ISC_corrected_base = []
#        VOC_corrected_base = []
        TEMP_ISC = []
#        index2 = i
        index2 = index
#        print('index when true is', index, iv_flag[index,1])

        while iv_flag[index2,1][1:19] == iv_flag[index,1][1:19]:       
            Module_Temp=get_tag_value(TemperatureTag,iv_flag[index2,1])
            SC=get_tag_value(Isc_Tag,iv_flag[index2,1]) # get short-circuit current
            sc=SC
            OC=get_tag_value(Voc_Tag,iv_flag[index2,1]) # open-circuit voltage 
            TEMP_ISC.append(SC)
            ISC.append(SC)
            VOC.append(OC)
            ISC_corrected.append(SC-(Module_Temp-50)*0.0006) # T coeff Isc = +0.0053 %/C
            VOC_corrected.append((Module_Temp-50)*0.132+OC)  # T coeff Voc = -0.351 %/C
#            print(ISC_base, VOC, len(ISC), len(VOC), index2)
#            print(index, index2)
            if index2+1 <= len(iv_flag)-1:
                index2 = index2 + 1
            else:
                break
                    
        
        if ISC_max < max(TEMP_ISC):
            ISC_size = len(TEMP_ISC)
            ISC_max = max(TEMP_ISC)
            ISC_max_index = TEMP_ISC.index(ISC_max)
            ISC_max_index_start = index
            ISC_max_index_end = index+ISC_size-1
            ISC_max_timestamp = iv_flag[index+ISC_max_index,1]
            ISC_max_start_time = iv_flag[index,1]
            ISC_max_end_time = iv_flag[index+ISC_size-1,1]
            Temp_IV=Module_Temp
#            print(ISC_max,ISC_max_index,ISC_max_timestamp,ISC_max_start_time,ISC_max_end_time,Temp_IV)
#        else:
#            print('No new ISC max')

#        break


# get the I-V curve and irradiance of the maximum current
            

#Voltage = get_tag_attribute_values(V_Tag,ISC_max_start_time,ISC_max_end_time)
#Power = get_tag_attribute_values(P_Tag,ISC_max_start_time,ISC_max_end_time)
#Current = get_tag_attribute_values(I_Tag,ISC_max_start_time,ISC_max_end_time)

Voltage = []
Power = []
Current = []


for index3 in range(0, ISC_size):
    voltage = get_tag_value(V_Tag,iv_flag[ISC_max_index_start+index3,1])
    power = get_tag_value(P_Tag,iv_flag[ISC_max_index_start+index3,1])
    current = get_tag_value(I_Tag,iv_flag[ISC_max_index_start+index3,1])
    
    Voltage.append(voltage)
    Power.append(power)
    Current.append(current)
    
#    print(ISC_size,ISC_size-index3,ISC_max_start_time,ISC_max_end_time)


Voltage_temp = array(Voltage)
    
#Voltage_temp = tuple(map(float, Voltage[:,0]))
#for i, sample in enumerate(Voltage):
#    Voltage[i,0] = float(Voltage[i,0])
    

Irradiance = get_tag_value('Ground_Pyra2_mV_Avg',ISC_max_timestamp)
irradiance = Irradiance


#Voltage_Correct_base = (Temp_IV-50)*0.132 + Voltage_base[:,0] # correct voltage and current according to module temperature
Voltage_Correct = (Temp_IV-50)*0.132 + array(Voltage) 

#for i, sample in enumerate(Current):
#    Current[i,0] = float(Current[i,0])
    
Size = len(Current)
Isc0 = Current[-1]
delta_Isc = (Isc0 / irradiance * 10) - Isc0
#Current_Correct = Current[:,0] + delta_Isc  
Current_Correct = array(Current) + delta_Isc              
 
     
ISC_corrected1 = (Isc0 / irradiance * 10) - array(ISC_corrected)
ISC1 = ISC_corrected1 = (Isc0 / irradiance * 10) - array(ISC)


#newList = list(dataObject)
#print 'time period is' , timeObject

#for i in newList:
 #   print(i)
    
I = Current_Correct
V = Voltage_Correct

plt.figure(3)
plt.rc('ytick',labelsize=16)
plt.rc('xtick',labelsize=16)
plt.xlabel('Voltage (V)',fontsize=20)
plt.ylabel('Current (A)',fontsize=20)


plt.plot(V,I)

# print plotted data to file
np.savetxt('S5.A832_IV_8_20_2017IV_corrected.txt',np.transpose([V,I]))

#plt.plot(Voc1,Isc1,'*')

VOC_corrected.append(0)

if I[-1] >= ISC_corrected1[-1]:
    ISC_corrected1 = np.append(ISC_corrected1,I[-1])
else:
    ISC_corrected1 = np.append(ISC_corrected1,ISC_corrected1[-1])

    
plt.rc('ytick',labelsize=16)
plt.rc('xtick',labelsize=16)
plt.xlabel('Voltage (V)',fontsize=20)
plt.ylabel('Current (A)',fontsize=20)

plt.plot(VOC_corrected,ISC_corrected1,'g.')
# plt.save('corrrected IV next year')
# plt.savefig('corrected IV in next year')
# np.savetxt('S5.A832_Aug2017.txt',np.transpose([V,I]))

#filename_temp_1 = 'IV_' + str(Module) + '_' + str(Day_Start)-
#filename_temp_1 = filename_temp_1.replace('/', '-')
#filename_temp_1 = filename_temp_1.replace(':', '-')
#filename_temp_1 = filename_temp_1.replace('.', '-')
#filename_temp_1 = filename_temp_1.replace(' ', '_') + '.txt'
#np.savetxt(filename_temp_1, np.transpose([V,I]))


np.savetxt('S5.A832_8_20_2017_ISC_VOC_corrected.txt',np.transpose([VOC_corrected,ISC_corrected1]))

#filename_temp_2 = 'sunsvoc_' + str(Module) + '_' + str(Day_Start)
#filename_temp_2 = filename_temp_2.replace('/', '-')
#filename_temp_2 = filename_temp_2.replace(':', '-')
#filename_temp_2 = filename_temp_2.replace('.', '-')
#filename_temp_2 = filename_temp_2.replace(' ', '_') + '.txt'
#np.savetxt(filename_temp_2,np.transpose([VOC_corrected,ISC_corrected1]))

#x=VOC_corrected_base #voltage
#y=ISC_corrected1_base #current
#xx = np.linspace(0,max(x),1000) # do interpolation first
#itp = interp1d(x,y, kind='linear',fill_value="extrapolate")
#window_size, poly_order = 101, 5
#yy_sg = savgol_filter(itp(xx), window_size, poly_order)
#plt.plot(x,y,'.')
#plt.plot(xx, yy_sg, 'k', label= "Smoothed curve")
#Isc_measured_base=yy_sg
#Voc_measured_base=xx

#print 'Number of data points is',len(newList)
# PSDK maximum/minimum-->time

