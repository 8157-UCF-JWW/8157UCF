# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 14:13:15 2017

@author: Siyu Guo
"""

import os
from scipy import interp, arange, exp,interpolate
import pandas as pd
import numpy as np

# define the path where you store the original files
path = 'C:/Users/Siyu Guo/Dropbox/UCF/projects/PVRD2-2/NIST/Data_for_FSEC20180109171252/Set_2/IV_Traces_Strata-4/'
dir_list = os.listdir(path)

for root,dirs,files in os.walk(path):
    for file in files:
       if file.endswith(".csv"): # get all the csv files in that directory
           t=float(file[11:13])
           if t>=5 and t<=21:
           
             ID=899 # this ID is not required 
             A=pd.read_csv(os.path.join(root,file),skiprows=1) # load all information in one original file into dataframe A
             A.columns=['IV_I','IV_V'] # define column name in A
             data= A.as_matrix()
             IV_I=data[:,0] # extract I-V data
             IV_V=data[:,1]
             Meas=len(IV_I) # get the total number of current, voltage pairs
             Power=list(range(Meas))  # define list to store power, length should be the same as I-V
             rowindex2=list(range(Meas))
             rowindex1=list(range(Meas))
             fv = interpolate.interp1d(IV_I, IV_V, fill_value='extrapolate') # extrapolate voltage at open circuit
             Voc=fv(0)
             fI=interpolate.interp1d( IV_V,IV_I, fill_value='extrapolate') # extrapolate current at short circuit
             Isc=fI(0) 
             sizeI=len(IV_I)
             
             
             if np.isinf(Isc) == True:  # check whether there are infinity numbers from extrapolation, if there is, just feed the Isc/Voc with the maximum ones from the measurement
               Isc=IV_I[sizeI-3]

             if np.isinf(Voc) == True: 
               Voc=IV_V[0]
             Mpp=0
             Time=[file[5:7],'/',file[8:10],'/',file[0:4],' ',file[11:13],':',file[14:16],':',file[17:19]] # get the time from the original file name
             time=''.join(map(str,Time))
             for i in range(Meas+1):
                 Power[i-1]=IV_V[i-1]*IV_I[i-1] # calculate power from I-V and construct a new column
                 time_mili=(time,'.',str(i).zfill(3) ) # construct another column to store the milisecond time stamp


                 rowindex2[i-1]=''.join(map(str,time_mili))
                 rowindex1[i-1]='D' # construct another culumn
 
                 if Power[i-1]>Mpp: # get the maximum power from the power values
                     Mpp=Power[i-1]
                     Impp=IV_I[i-1]
                     Vmpp=IV_V[i-1]

# insert all the extra columns into dataframe A
             A.insert(0, 'H', rowindex1) 
             A.insert(1, 'TimeStamp_milli', rowindex2)
             A['IV_P'] = pd.Series(Power, index=A.index)
             P=pd.DataFrame({'Parameters': ['Values'], 'Timestamp': [time],'Tracer_ID':[ID],'Voc':[Voc]})
             P.insert(4, 'Isc', [Isc])
             P.insert(5, 'Impp', [Impp])
             P.insert(6, 'Vmpp', [Vmpp])
             P.insert(7, 'Pmpp', [Mpp])
           


           
             Fileout=[file[0:47],'-out.csv'] # define the output file name, which is based on the input file name
             fileout=''.join(map(str,Fileout))
           
           
           
           
             with open(fileout, 'w') as handle: # save the data to output file

               P.to_csv(handle, index=False)

               A.to_csv(handle, index=False)

   