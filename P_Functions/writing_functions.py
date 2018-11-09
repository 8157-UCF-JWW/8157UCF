# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 14:02:39 2018

@author: jwalters
Writing functions
based on you tube videos from
Corey Schafer

"""
#define the function
def hello_func():
    return 'Hello Function-'

# passing an arguemnt in 
def hi_func(greeting, name = 'You'):
    return '{}, {}' .format(greeting, name)
    
 # using args and kwargs
def student_info(*args, **kwargs):
    print(args)
    print(kwargs)
       
# leap year function
month_days = [0,31,28,31,30,31,30,31,31,30,31,30,31]

def is_leap(year):
   # """ triple quote is comment line identifier for code
   #     Returns True for leap years, False for non-leap years """
     return year % 4 == 0 and (year % 100 != 0 or year % 400 ==0)   

def days_in_month(year,month):
    """ Returns number of days in that month in that year """

    #year = 2017
    #month= 2
    if not 1 <= month <=12:
        return 'Invalid Month'

    if month == 2 and is_leap(year):
        return 29
    return month_days[month]

#call the function
print(hello_func())
    
#call the function
print(hi_func('Hi', name = 'Joe'))


#call function

courses =['Math','Art']
info = {'name': 'John', 'age': 22}

student_info(*courses, **info)

#call function for leap year
print(days_in_month(2020,2))