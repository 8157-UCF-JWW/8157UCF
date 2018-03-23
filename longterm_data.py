

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 17:20:32 2017

@author: Siyu Guo


"""

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
Isc_tag=['S2.A',Module,'.Isc']
Isc_Tag=''.join(map(str,Isc_tag))
Voc_tag=['S2.A',Module,'.Voc']
Voc_Tag=''.join(map(str,Voc_tag))
Pm_tag=['S2.A',Module,'.Pmpp']
Pm_Tag=''.join(map(str,Pm_tag))

Isc_sweep=np.zeros(shape=(10000,1),dtype=float,order='F')
Isc_RDE=np.zeros(shape=(100000,1),dtype=float,order='F')
Voc_RDE=np.zeros(shape=(100000,1),dtype=float,order='F')
Temp_RDE=np.zeros(shape=(100000,1),dtype=float,order='F')
Pm_RDE=np.zeros(shape=(100000,1),dtype=float,order='F')
Irradiance_meas=np.zeros(shape=(100000,1),dtype=float,order='F')
Ist=np.zeros(shape=(100000,1),dtype=float,order='F')
Ts=np.zeros(shape=(100000,1),dtype=float,order='F')

M=[31,28,31,30,31,30,31,31,30,31,30,31] # define the numer of days for each month

Month=6
month=np.r_[Month]# [month1:monthN] define the months for analysis

p=0
k=0

for m in month:
    date=np.r_[18] #date=np.r_[1:M[m-1]]
    
    for d in date:
        
        Day_tag=[m,'/',d,'/2017 ']
        Day=''.join(map(str,Day_tag))

        hour=np.r_[4:18]
        minute=np.r_[0:60]
        sc=0
        sc0=0
        


  
        Time1='6/04/2017 3:59:00 AM'


#isc_corrected=np.ndarray(shape=(1,1000),dtype=float,order='F')
#voc_corrected=np.ndarray(shape=(1,1000),dtype=float,order='F')

    


        for i in hour:
            for j in np.arange(0, 60, 5):
                
                Time0=Time1;
                if j<10:
                    time1=[Day,i,':0',j,':00']
                    time2=[Day,i,':0',j,':01']
                else:
                    time1=[Day,i,':',j,':00']
                    time2=[Day,i,':',j,':01']
                    Time1=''.join(map(str,time1))
                    Time2=''.join(map(str,time2))
                    
                    print(Time1)
                    
                    Module_Temp=get_tag_value(TemperatureTag,Time0)
                    SC=get_tag_value(Isc_Tag,Time0)
                    Isc_RDE[k,0]=SC
                    OC=get_tag_value(Voc_Tag,Time0) # open-circuit voltage 
                    Voc_RDE[k,0]=OC
                    Temp_RDE[k,0]= Module_Temp
                    Pm=get_tag_value(Pm_Tag,Time0) 
                    Pm_RDE[k,0]=Pm


                    #Voltage = get_tag_values(V_Tag,Time0,Time1)

                    Irradiance_meas[k,0]=get_tag_value('Ground_Pyra2_mV_Avg',Time0)
                    
                

                    k=k+1
 

        




# get the I-V curve and irradiance of the maximum current

#newList = list(dataObject)
#print 'time period is' , timeObject

#for i in newList:
 #   print(i)
    
        
        






#plt.plot(Voc1,Isc1,'*')
plt.plot(Isc_sweep)
plt.scatter(Irradiance_meas,Isc_RDE)
plt.plot(Isc_RDE)
plt.plot(Irradiance_meas,Isc_sweep)

#systemdata={'Irradiance': Irradiance_meas[:,0:k], 'Temperature': Temp_RDE[:,0:k],'Isc':Isc_RDE[:,0:k],'Voc':Voc_RDE[:,0:k]}


#np.savetxt('IV.txt',np.transpose([V,I]))
#systemdata.to_csv('triansamples.csv')

#np.savetxt('sunsvoc.txt',np.transpose([voc_corrected,isc_corrected1]))

#print 'Number of data points is',len(newList)
# PSDK maximum/minimum-->time

System=[Irradiance_meas[:,0:k], Temp_RDE[:,0:k],Isc_RDE[:,0:k], Voc_RDE[:,0:k]]