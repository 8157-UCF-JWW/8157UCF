# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 13:40:41 2018

@author: jwalters
Learning base on 
Corey Schafer's You Tube videos.

"""
nums =[1,2,3,4,5]
print('simple loop')
for num in nums:
    print(num)
    
#using break and continue with the loop
print('break statement')    
for num in nums:
    if num == 3:
        print('Found num', num)
        break
    print(num)
 
#using break and continue with the loop
print('continue statement')    
for num in nums:
    if num == 3:
        print('Found num', num)
        continue
    print(num)

# loop in side a loop
print('loop inside loop')
for num in nums:
    for letter in 'abc':
        print(num,letter)
  
# going through a loop a certain number of times
print('using range')
for i in range(1,11):
    print(i)
    
# using the while loop
print('using while loop')
x = 0
while x <= 10:
    if x == 5:
        break
    print(x)
    x += 1
    