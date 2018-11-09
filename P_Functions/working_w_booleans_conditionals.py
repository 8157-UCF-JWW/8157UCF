# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 12:03:01 2018

@author: jwalters

Working with Booleans and conditionals
From Corey Schafer You Tube videos

"""

# Some conditionals to test for
# comparisons
# Equals        ==
# not equal     !=
# greater than  >
# less than     <
# greater than or equal     >=
# less than or equal        <=
# object identity   is  This checks that the objects are the same (the same ID)
# and
# or
# not   - Sets a boolean to the opposite (False to True or True to False)


# Simple IF-- Only runs if condition AFTER if is TRUE
language = 'Java'

if language == 'Python':
    print('language is Python')
# the elif allows for a second conditional check.  
# Multiple elifs can be used before the final Else
elif language == 'Java':
    print('language is Java')
else:
    print('No match')
    
user = 'Admin'
logged_in = True

if user == 'Admin' or logged_in:
    print('Admin Page')
else:
    print('Bad credentials')
    
if not logged_in:
    print('Please log in')
else:
    print('Welcome')
   
a = [1,2,3]
b =a

print(id(a))
print(id(b))

print(a is b)
     
#Pythons conditionals to False
# False
# None
# Zeros of any numberic type
# Any empty sequence. For example '', (), []
# Any empty mappiong. For example, {}

condition = 'Test'

if condition:
    print('Evaluated to True')
else:
    print('Evaluated to False')
    