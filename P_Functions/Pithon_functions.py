# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 23:15:14 2017

@author: Revised version from Hubert Seigneur

Modifed by Joe Walters 8/4/2018

"""

# This module imports libraries and such so python can call into the PI system
import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta

import sys
sys.path.append('C:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\')

import clr #requires pythonnet
clr.AddReference('OSIsoft.AFSDK')
clr.AddReference('System.Collections')
from System import Object
from System.Collections import *
from System.Net import *

# This imports the different AF classes
from OSIsoft.AF.PI import *  
from OSIsoft.AF.Search import *  
from OSIsoft.AF.Asset import *  
from OSIsoft.AF.Data import *  
from OSIsoft.AF.Time import * 
from OSIsoft.AF.Time import * 
from datetime import datetime


# create the import function for server connection
def connect_to_Server(serverName):  
    global piServers, piServer
    piServers = PIServers()  
    piServer = piServers[serverName]
    piServer.Connect(False)
    return piServer.ConnectionInfo.IsConnected

# Disconnect server
def disconnect_Server(serverName):  
#    piServers = PIServers()  
    if (piServer == piServers[serverName]):
        piServer.Disconnect()
        return piServer.ConnectionInfo.IsConnected
    else:
        return 'Unknown'

# create the import function for tag call
def get_tag_snapshot(tagname):  
    tag = PIPoint.FindPIPoint(piServer, tagname)  
    lastData = tag.Snapshot()  
    return lastData.Value, lastData.Timestamp 

# create the import function for tag call
def get_tag_attribute_values(tagname, timestart, timeend):
    #print('This is value of passed tagname :', tagname)  # temporary line for TShoot
    tag = PIPoint.FindPIPoint(piServer, tagname)
    start = AFTime.Parse(timestart)
    end = AFTime.Parse(timeend)
#    print(timestart)
#    print(timeend)
    #    tag = PIPoint.FindPIPoint(piServer, tagname)  
#    lastData = tag.Snapshot()  
#    return lastData.Value, lastData.Timestamp
    timeRange = AFTimeRange.Parse(timestart,timeend)
#    timeRange = AFTimeRange.Parse(timestart,timeend)
#   print(timeRange)
    boundary = AFBoundaryType.Inside
    data = tag.RecordedValues(timeRange,boundary,'',False,0)
    dataList = list(data)
    #print len(dataList)
#    results = np.zeros((len(dataList), 3), dtype='object') #numpy array
#    for i, sample in enumerate(data):
#        results[i, 0] = i
#        results[i, 1] = float(sample.Value)
#        results[i, 2] = str(sample.Timestamp)
    results = np.zeros((len(dataList), 2), dtype='object') #numpy array
    for i, sample in enumerate(data):
        results[i, 0] = str(sample.Value)
        results[i, 1] = str(sample.Timestamp.ToString("MM/dd/yyyy HH:mm:ss.fff"))
    return results

# create the import function for tag call
def get_tag_attribute_values2(tagname, timestart, timeend):
    tag = PIPoint.FindPIPoint(piServer, tagname)
    start = AFTime.Parse(timestart)
    end = AFTime.Parse(timeend)
    print(timestart)
    print(timeend)
    #    tag = PIPoint.FindPIPoint(piServer, tagname)  
#    lastData = tag.Snapshot()  
#    return lastData.Value, lastData.Timestamp
    timeRange = AFTimeRange.Parse(timestart,timeend)
#    timeRange = AFTimeRange.Parse(timestart,timeend)
    print(timeRange)
    boundary = AFBoundaryType.Inside
#    data = tag.RecordedValues(timeRange,boundary,'',False,0)
    data = tag.PISampDat()
    dataList = list(data)
    #print len(dataList)
#    results = np.zeros((len(dataList), 3), dtype='object') #numpy array
#    for i, sample in enumerate(data):
#        results[i, 0] = i
#        results[i, 1] = float(sample.Value)
#        results[i, 2] = str(sample.Timestamp)
    results = np.zeros((len(dataList), 2), dtype='object') #numpy array
    for i, sample in enumerate(data):
        results[i, 0] = str(sample.Value)
        results[i, 1] = str(sample.Timestamp.ToString("MM/dd/yyyy HH:mm:ss.fff"))
    return results

def get_tag_type(tagname):
    tag = PIPoint.FindPIPoint(piServer, tagname)  
    typeData = tag.GetType()
    return typeData
    
def get_tag_value(tagname,timestart):
    tag = PIPoint.FindPIPoint(piServer, tagname) 
    # print(timestart) # print for TShoot
    timeValue = AFTime.Parse(timestart)
    newData = tag.RecordedValue(timeValue,0)
    return newData.Value
    
def get_tag_values(tagname,timestart,timeend):
    tag = PIPoint.FindPIPoint(piServer, tagname) 
    timeRange = AFTimeRange(timestart,timeend)
    boundary = AFBoundaryType.Inside
    data = tag.RecordedValues(timeRange,boundary,'',False,0)
    dataList = list(data)
    #print len(dataList)
    results = np.zeros((len(dataList), 2), dtype='object') #numpy array
    for i, sample in enumerate(data):
        results[i, :] = float(sample.Value)
    return results


def addSecs(tm, secs):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()

def get_time_at_MaxIsc(Isc_Tag,timestart,timeend):    
    # call function for tag values in the time range.  Returns an array[x,2] of values. [0 -value, 1=time]
    Isc_Values = get_tag_attribute_values(Isc_Tag, timestart, timeend)
    ## Find Maximum value in object
    Isc_Max_val = np.max(Isc_Values)
    # find the index of where the array has its maximum
    Isc_Max_index = np.where(Isc_Values == Isc_Values.max())
    # get the time stamp where the maximum value was found.  Need to specify the index positionsd to specify the index positions 
    Time_Max = Isc_Values[Isc_Max_index[0],1]
    return Time_Max

def get_IV_at_Time(I_Tag, V_Tag,timestart):
    # Get the IV data set for that time stamp
    Time_Max= timestart
    I_Tag = I_Tag
    V_tag = V_Tag
    print(' Time @ ',Time_Max)
    # Need the start time and end time of the IV curve trace
    #   need to convert time as objects to time as datetime so you can add 1 minute
    IV_start=pd.to_datetime(Time_Max[0], dayfirst =True, format='%m/%d/%Y %H:%M:%S.%f')
    # add 1 minute to that time to provide time span
    IV_end = IV_start + timedelta(seconds=60)
    print('start IV @',IV_start, ' end IV @ ',IV_end)
    # Need to convert time back to type and format the function will accept
    T_format_pd = '%Y-%m-%d %H:%M:%S'
    T_format_PI = '%m/%d/%Y %H:%M:%S.%f'
    #  make strings
    IV_start_date_pd = datetime.strftime(IV_start, T_format_pd )
    IV_end_date_pd = datetime.strftime(IV_end, T_format_pd )
    print('srt pd ', IV_start_date_pd,'   end pd ', IV_end_date_pd)
    #  make datetimes
    new_IV_start = datetime.strptime(IV_start_date_pd, T_format_pd)
    new_IV_end = datetime.strptime(IV_end_date_pd, T_format_pd)

    print(' new IV ', new_IV_end)
    # make string with proper format to pass to PI functions
    IV_start = new_IV_start.strftime(T_format_PI)
    IV_end = new_IV_end.strftime(T_format_PI)
    print('start IV @', IV_start,'  end IV @ ',IV_end)
    # call function to get IV 
    I_Values =get_tag_values(I_Tag,IV_start, IV_end)
    V_Values =get_tag_values(V_Tag,IV_start, IV_end)
    return I_Values, V_Values

def Update_Tag_Value(tagname, value, timestamp):
    tag_Value = clr.System.Object
    tag_AFTime = AFTime(timestamp)
    tag_AFValue = AFValue(tag_Value, tag_AFTime)
    tag_AFValue.Value = value
    tag = PIPoint.FindPIPoint(piServer, tagname)
    tag_UpdateOption = AFUpdateOption.Replace #options: (Replace,Insert,NoReplace,ReplaceOnly,InsertNoCompression,Remove)
    tag_BufferOption = AFBufferOption.DoNotBuffer #options: (DoNotBuffer,BufferIfPossible,Buffer)
    tag.UpdateValue(tag_AFValue, tag_UpdateOption, tag_BufferOption)
  

def Update_Tag_Value2(tagname, value, timestamp):
    tag_Value = clr.System.Object
    tag_AFTime = AFTime(timestamp)
#    tag_AFTime = AFTime.Parse(timestamp)
    tag_AFValue = AFValue(tag_Value, tag_AFTime)
    tag_AFValue.Value = value
    tag = PIPoint.FindPIPoint(piServer, tagname)
    tag_UpdateOption = AFUpdateOption.Replace #options: (Replace,Insert,NoReplace,ReplaceOnly,InsertNoCompression,Remove)
    tag_BufferOption = AFBufferOption.DoNotBuffer #options: (DoNotBuffer,BufferIfPossible,Buffer)
    tag.UpdateValue(tag_AFValue, tag_UpdateOption, tag_BufferOption)
    
