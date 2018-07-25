# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 16:25:58 2018

@author: Siyu Guo
"""# -*- coding: utf-8 -*-
"""

"""
Day='8/13/2016 '

from scipy.interpolate import interp1d
import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from scipy.interpolate import UnivariateSpline

from Pithon_loadfloat import * 
import matplotlib.pyplot as plt
connect_to_Server("net1552.net.ucf.edu")  
value, timestamp = get_tag_snapshot('Ground_Pyra2_mV_Avg')  
print('Timestamp: {0} Value: {1}'.format(timestamp, value))  

Module=792
#Temperaturetag=['ModTemp',2,'_Avg']
TemperatureTag='Ground_RTD_C_Avg(1)'
I_tag=['S2.A',Module,'.IV_I']
I_Tag=''.join(map(str,I_tag))

V_tag=['S2.A',Module,'.IV_V']
V_Tag=''.join(map(str,V_tag))
P_tag=['S2.A',Module,'.IV_P']
P_Tag=''.join(map(str,P_tag))

V_Tag=''.join(map(str,V_tag))
Isc_tag=['S2.A',Module,'.Isc']
Isc_Tag=''.join(map(str,Isc_tag))
Voc_tag=['S2.A',Module,'.Voc']
Voc_Tag=''.join(map(str,Voc_tag))



hour=np.r_[1:18]
minute=np.r_[0:60]
sc=0
sc0=0

isc=np.zeros(shape=(1000,),dtype=float,order='F')
voc=np.zeros(shape=(1000,),dtype=float,order='F')
isc_corrected_base=np.zeros(shape=(1000,),dtype=float,order='F')
voc_corrected_base=np.zeros(shape=(1000,),dtype=float,order='F')
Time1='8/13/2016 1:59:00 AM' # you must specify the starting time
#isc_corrected=np.ndarray(shape=(1,1000),dtype=float,order='F')
#voc_corrected=np.ndarray(shape=(1,1000),dtype=float,order='F')

k=0



for i in hour:
 

    for j in np.arange(0, 60, 6):
        
        Time0=Time1;
        if j<10:
            time1=[Day,i,':0',j,':00']
            time2=[Day,i,':0',j+6,':00']
        else:
            time1=[Day,i,':',j,':00']
            time2=[Day,i,':',j+6,':00']

        Time1=''.join(map(str,time1))
        Time2=''.join(map(str,time2))
        print(Time1)

        Module_Temp=get_tag_value(TemperatureTag,Time1)
        SC=get_tag_value(Isc_Tag,Time1) # get short-circuit current
        sc=SC
        OC=get_tag_value(Voc_Tag,Time1) # open-circuit voltage 
        isc[k,]=SC
        voc[k,]=OC
        isc_corrected_base[k,]=SC-(Module_Temp-50)*0.0006
        voc_corrected_base[k,]=(Module_Temp-50)*0.132+OC
        if sc>sc0: # get the time when the module has maxinmum current
            sc0=sc
            Time0_select=Time0
            Time1_select=Time1
            Time2_select=Time2
            Temp_IV=Module_Temp

       
        k=k+1


# get the I-V curve and irradiance of the maximum current
#Current = get_tag_values(I_Tag,Time0_select,Time1_select) 
Voltage_base = get_tag_values(V_Tag,Time0_select,Time1_select)
Power_base=get_tag_values(P_Tag,Time0_select,Time1_select)
Current_base=get_tag_values(I_Tag,Time0_select,Time1_select)
#Power1=Power[0:169,:]
#Current=Power/Voltage
#Voltage=Power1/Current
Irradiance=get_tag_value('Ground_Pyra2_mV_Avg',Time1_select)
irradiance=Irradiance
Voltage_Correct_base=(Temp_IV-50)*0.132+Voltage_base # correct voltage and current according to module temperature
Size=len(Current_base)
Isc0=Current_base[Size-1,0]
delta_Isc=Isc0/irradiance*10-Isc0
Current_Correct_base=Current_base+delta_Isc              
 

           
isc_corrected1_base=Isc0/irradiance*10-isc_corrected_base
isc1=isc_corrected1_base=Isc0/irradiance*10-isc

#newList = list(dataObject)
#print 'time period is' , timeObject

#for i in newList:
 #   print(i)
    
I_base= Current_Correct_base[:,1]
V_base= Voltage_Correct_base[:,1]


plt.plot(V_base,I_base)

#plt.plot(Voc1,Isc1,'*')

plt.plot(voc_corrected_base,isc_corrected1_base,'.')

np.savetxt('IV_8_13_2016.txt',np.transpose([V_base,I_base]))

np.savetxt('sunsvoc_8_13_2016.txt',np.transpose([voc_corrected_base,isc_corrected1_base]))

x=voc_corrected_base #voltage
y=isc_corrected1_base #current
xx = np.linspace(0,x.max(), 1000) # do interpolation first
itp = interp1d(x,y, kind='linear')
window_size, poly_order = 101, 5
yy_sg = savgol_filter(itp(xx), window_size, poly_order)
plt.plot(x,y,'.')
plt.plot(xx, yy_sg, 'k', label= "Smoothed curve")
Isc_measured_base=yy_sg
Voc_measured_base=xx



#print 'Number of data points is',len(newList)
# PSDK maximum/minimum-->time

