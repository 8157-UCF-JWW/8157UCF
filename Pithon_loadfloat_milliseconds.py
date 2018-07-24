# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 23:15:14 2017

@author: Revised version from Hubert Seigneur
"""

# This module imports libraries and such so python can call into the PI system
import numpy as np

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
    # piServer.Connect(False)
    credential1 = NetworkCredential("Hubert Seigneur", "temp123!@#");
    # credential1 = NetworkCredential("seigneur", "#14Zidane#14");
    piServer.Connect(credential1);
    return piServer.ConnectionInfo.IsConnected

# create the import function for tag call
def get_tag_snapshot(tagname):  
    tag = PIPoint.FindPIPoint(piServer, tagname)  
    lastData = tag.Snapshot()  
    return lastData.Value, lastData.Timestamp 

# create the import function for tag call
def get_tag_attribute_values(tagname, timestart, timeend):
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

#def get_tag_values(tagname,timestart,timeend):
#    start = AFTime.Parse('8/13/2016 1:55:00:123')
#    end = AFTime.Parse('8/13/2016 1:59:00:456')
#    print(start)
#    
##    start = datetime.now().isoformat(timespec='milliseconds')
##    end = datetime.now().isoformat(timespec='milliseconds')
##    print(start)
#    
##    start = start.ToPIPrecision()
##    end = end.ToPIPrecision()
#    
##    starttemp = AFTime.Parse(timestart)
##    endtemp = AFTime.Parse(timeend)
##    starttemp = AFTime(start.AddMilliseconds(1))
##    endtemp = AFTime(end.AddMilliseconds(1))
##    timeRange = AFTimeRange(start,end)
#    tag = PIPoint.FindPIPoint(piServer, tagname) 
#    timeRange = AFTimeRange(start,end)
#    boundary = AFBoundaryType.Inside
#    data = tag.RecordedValues(timeRange,boundary,'',False,0)
#    dataList = list(data)
#    #print len(dataList)
##    results = np.zeros((len(dataList), 3), dtype='object') #numpy array
##    for i, sample in enumerate(data):
##        results[i, 0] = i
##        results[i, 1] = float(sample.Value)
##        results[i, 2] = str(sample.Timestamp)
#    results = np.zeros((len(dataList), 2), dtype='object') #numpy array
#    for i, sample in enumerate(data):
#        results[i, 0] = float(sample.Value)
#        results[i, 1] = str(sample.Timestamp)
#    return results


def Update_Tag_Value(tagname, value, timestamp):
    tag_Value = clr.System.Object
    tag_AFTime = AFTime(timestamp)
#    tag_AFTime = AFTime.Parse(timestamp)
    tag_AFValue = AFValue(tag_Value, tag_AFTime)
    tag_AFValue.Value = value
    tag = PIPoint.FindPIPoint(piServer, tagname)
    tag_UpdateOption = AFUpdateOption.Replace #options: (Replace,Insert,NoReplace,ReplaceOnly,InsertNoCompression,Remove)
    tag_BufferOption = AFBufferOption.DoNotBuffer #options: (DoNotBuffer,BufferIfPossible,Buffer)
    tag.UpdateValue(tag_AFValue, tag_UpdateOption, tag_BufferOption)
    
# Disconnect server
def disconnect_Server(serverName):  
#    piServers = PIServers()  
    if (piServer == piServers[serverName]):
        piServer.Disconnect()
        return piServer.ConnectionInfo.IsConnected
    else:
        return 'Unknown'
