
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 17:20:32 2017

@author: Hubert Seigneur


"""

from Pithon_loadfloat import *


##### test Connect() function ---------- PI Server #####

status = connect_to_Server("Server Address")
print('\nConnection status is',status)



##### test get_tag_snapshot() function ---------- PI Server #####

value, timestamp = get_tag_snapshot('PT0024')  
print('\nCurrent Timestamp: {0} and Current Value: {1}'.format(timestamp, value))



##### test get_tag_type() function ---------- PI Server #####

TypeData = get_tag_type('PT0024')
print('\nThe data type is {}',TypeData)



##### test get_tag_value() function ---------- PI Server #####

time='1/25/2018 5:00:00 AM'   
Value = get_tag_value('PT0024',time)
print('\nGet a single data point - Timestamp: {} and Value: {}'.format(time,Value))



##### test get_tag_values() function ---------- PI Server #####

timestart='1/25/2018 6:00:00 AM'
timeend='1/25/2018 6:10:00 AM'   
values = get_tag_values('PT0024',timestart,timeend)
Arraysize = len(values)
print ('\nGet multiple data points - The array size is',Arraysize)
print (values)



##### Update_Tag_Value() function ---------- PI Server #####

time='1/25/2018 7:00:00 AM'   
originalValue = get_tag_value('PT0024',time) # get value at desired timestamp
print('\nTimestamp: {} and the original Value: {}'.format(time, originalValue))

newValue = originalValue + 10 # get new value
Update_Tag_Value('PT0024', newValue, time) # upload new value of tag at same timestamp
value = get_tag_value('PT0024',time) # verify that tag value has been updated
print('Timestamp: {} and new Value: {}'.format(time, value))

Update_Tag_Value('PT0024', originalValue, time) # Restore original value of tag at same timestamp
value = get_tag_value('PT0024',time) # verify that the original value has been restored
print('The original Value {} was restored at {}'.format(value,time))



#### Disconnect() function ---------- PI Server #####

status = disconnect_Server("Server Address")
print('\nConnection status is',status)


