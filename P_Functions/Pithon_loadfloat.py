# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 23:15:14 2017

@author: Siyu Guo
"""

# This module imports libraries and such so python can call into the PI system
import sys
sys.path.append('C:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\')
import clr
clr.AddReference('OSIsoft.AFSDK')
import numpy as np

# This imports the difference classes
from OSIsoft.AF.PI import *  
from OSIsoft.AF.Search import *  
from OSIsoft.AF.Asset import *  
from OSIsoft.AF.Data import *  
from OSIsoft.AF.Time import *  

# create the import function for server connection
def connect_to_Server(serverName):  
    piServers = PIServers()  
    global piServer  
    piServer = piServers[serverName]  
    piServer.Connect(False)  

# create the import function for tag call
def get_tag_snapshot(tagname):  
    tag = PIPoint.FindPIPoint(piServer, tagname)  
    lastData = tag.Snapshot()  
    return lastData.Value, lastData.Timestamp 

def get_tag_type(tagname):
    tag = PIPoint.FindPIPoint(piServer, tagname)  
    typeData = tag.GetType()
    return typeData
    
def get_tag_value(tagname,timestart):
    tag = PIPoint.FindPIPoint(piServer, tagname) 
    timeValue = AFTime(timestart)
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

def Update_Tag_Value(tagname, value, timestamp):
    tag_Value = clr.System.Object
    tag_AFTime = AFTime(timestamp)
    tag_AFValue = AFValue(tag_Value, tag_AFTime)
    tag_AFValue.Value = value
    tag = PIPoint.FindPIPoint(piServer, tagname)
    tag_UpdateOption = AFUpdateOption.Replace #options: (Replace,Insert,NoReplace,ReplaceOnly,InsertNoCompression,Remove)
    tag_BufferOption = AFBufferOption.DoNotBuffer #options: (DoNotBuffer,BufferIfPossible,Buffer)
    tag.UpdateValue(tag_AFValue, tag_UpdateOption, tag_BufferOption)
    
