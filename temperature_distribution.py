# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 11:53:30 2018

@author: Siyu Guo
"""



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
#Temperaturetag=['ModTemp',2,'_Avg'], add any temperature tag you want to analysis
TemperatureTag1='Ground_RTD_C_Avg(4)'
TemperatureTag2='Ground_RTD_C_Avg(5)'
TemperatureTag3='Ground_RTD_C_Avg(6)'
TemperatureTag4='Ground_RTD_C_Avg(7)'

STD=np.zeros(shape=(10000,1),dtype=float,order='F')
Max=np.zeros(shape=(10000,1),dtype=float,order='F')
Min=np.zeros(shape=(10000,1),dtype=float,order='F')
Diff=np.zeros(shape=(10000,1),dtype=float,order='F')

T=np.zeros(shape=(10000,4),dtype=float,order='F')



M=[31,28,31,30,31,30,31,31,30,31,30,31] # define the numer of days for each month

Month=8
month=np.r_[Month]

p=0
k=0




for m in month:
    #date=np.r_[18]
    date=np.r_[1:M[m-1]]
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
                    

                    T[k,0]= get_tag_value(TemperatureTag1,Time0) # all tempearture values are stored in matrix T
                    T[k,1]= get_tag_value(TemperatureTag2,Time0)
                    T[k,2]= get_tag_value(TemperatureTag3,Time0)
                    T[k,3]= get_tag_value(TemperatureTag4,Time0)
                    
                    STD[k,0]=np.std(T[k,:]) # calculate the standard devitation of all the tmmperature values
                    Max[k,0]=np.amax(T[k,:]) # get the maximum value
                    Min[k,0]=np.amin(T[k,:]) # get the minimum value
                    Diff[k,0]=Max[k,0]-Min[k,0] # calculate the difference between max and min
                    



                    #Voltage = get_tag_values(V_Tag,Time0,Time1)

                    
                

                    k=k+1
 

        




# get the I-V curve and irradiance of the maximum current

#newList = list(dataObject)
#print 'time period is' , timeObject

#for i in newList:
 #   print(i)
    
        
        





