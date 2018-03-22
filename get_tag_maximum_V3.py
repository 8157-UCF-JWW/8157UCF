# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 15:27:37 2017

@author: Siyu Guo
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 17:20:32 2017

@author: Siyu Guo
"""
Day='8/9/2017 '

from Pithon_loadfloat import * 
import matplotlib.pyplot as plt
connect_to_Server("net1552.net.ucf.edu")  
value, timestamp = get_tag_snapshot('Ground_Pyra2_mV_Avg')  
print('Timestamp: {0} Value: {1}'.format(timestamp, value))  

Module=792# choose PV module for analysis
#Temperaturetag=['ModTemp',2,'_Avg']
TemperatureTag='Ground_RTD_C_Avg(1)' # get the module tempearture using temperature sensor tag
I_tag=['S2.A',Module,'.IV_I'] # construct the I-V parameters tag name for the selected module
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



hour=np.r_[1:18] # define the time range for a day eg.:1am to 18pm
minute=np.r_[0:60]
sc=0
sc0=0

isc=np.zeros(shape=(1000,),dtype=float,order='F') # define array to store each parameter
voc=np.zeros(shape=(1000,),dtype=float,order='F')
isc_corrected=np.zeros(shape=(1000,),dtype=float,order='F')
voc_corrected=np.zeros(shape=(1000,),dtype=float,order='F')
Time1='8/9/2017 0:59:00 AM' # you must specify the starting time


k=0



for i in hour:
 

    for j in np.arange(0, 60, 5): # set time to be from 0 to 60 minites with a step of 5 minutes
        
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
        isc_corrected[k,]=SC-(Module_Temp-50)*0.0006
        voc_corrected[k,]=(Module_Temp-50)*0.132+OC
        if sc>sc0: # get the time when the module has maxinmum current
            sc0=sc
            Time0_select=Time0
            Time1_select=Time1
            Time2_select=Time2
            Temp_IV=Module_Temp

       
        k=k+1


# get the I-V curve and irradiance of the maximum current

Voltage = get_tag_values(V_Tag,Time0_select,Time1_select)
Power=get_tag_values(P_Tag,Time0_select,Time1_select)
Current=get_tag_values(I_Tag,Time0_select,Time1_select)


Irradiance=get_tag_value('Ground_Pyra2_mV_Avg',Time1_select)
irradiance=Irradiance
Voltage_Correct=(Temp_IV-50)*0.132+Voltage # correct voltage and current according to module temperature
Size=len(Current)
Isc0=Current[Size-1,0]
delta_Isc=Isc0/irradiance*10-Isc0
Current_Correct=Current+delta_Isc              
 

           
isc_corrected1=Isc0/irradiance*10-isc_corrected
isc1=isc_corrected1=Isc0/irradiance*10-isc

#newList = list(dataObject)
#print 'time period is' , timeObject

#for i in newList:
 #   print(i)
    
I= Current_Correct[:,1]
V= Voltage_Correct[:,1]


plt.plot(V,I)

#plt.plot(Voc1,Isc1,'*')

plt.plot(voc_corrected,isc_corrected1,'.')

np.savetxt('IV_8_9_2017.txt',np.transpose([V,I]))

np.savetxt('sunsvoc_8_9_2017.txt',np.transpose([voc_corrected,isc_corrected1]))

#print 'Number of data points is',len(newList)
# PSDK maximum/minimum-->time