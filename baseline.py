# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 10:14:33 2017

@author: Siyu Guo
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter



# smooth the Isc-Voc curve



Voc_initial=Voc_measured_base
Isc_initial=Isc_measured_base

x=Voc_initial
y=Isc_initial

xx = np.linspace(0,x.max(), 1000) # do interpolation first
itp = interp1d(x,y, kind='linear',fill_value = "extrapolate")
window_size, poly_order = 101, 5
yy_sg = savgol_filter(itp(xx), window_size, poly_order)
plt.plot(x,y,'.')
plt.plot(xx, yy_sg, 'k', label= "Smoothed curve")
Voc_initial=xx
Isc_initial=yy_sg

Isc_measured=Isc_initial
Voc_measured=Voc_initial


xshunt=xx[0:49]
yshunt=yy_sg[0:49]

# fit the slope of the measured Isc-Voc curve, calcykate Rsh
k=np.r_[1:50]
for num in range(0,49):
    k[num]=1
A = np.c_[k, xshunt[:, np.newaxis]]
c, resid, rank, sigma = linalg.lstsq(A, yshunt)
Rshunt=-1.0/c[1]

plt.figure(1)


V_measured=V_base
I_measured=I_base

delta_Isc=Isc_initial[0]-Isc_measured[0]; # calculate difference on Isc
c2_I=Isc_initial-delta_Isc; # c2 incorporates influence from Isc
c2_V=Voc_initial;

c3_I=c2_I # c3 influence from shunt resistance
c3_V=Voc_initial;
plt.plot(Voc_initial,Isc_initial)
plt.plot(c2_V,c2_I)
plt.plot(c3_V,c3_I)

# calculate difference on Voc
itp=interp1d(c3_I,c3_V, kind='linear',fill_value = "extrapolate")
Voc_before=itp(0)
itp=interp1d(Isc_measured,Voc_measured,kind='linear',fill_value = "extrapolate")
Voc_after=itp(0)
delta_Voc=Voc_before-Voc_after


c4_I=c3_I # c4 influence from reverse saturation current
c4_V=c3_V-delta_Voc
plt.plot(c4_V,c4_I)
plt.plot(V_measured,I_measured)

length=len(I_measured)
I_Rs=I_measured[length-1]*1/4;
itp=interp1d(I_measured,V_measured, kind='linear',fill_value = "extrapolate")
V1_Rs=itp(I_Rs)
itp=interp1d(Isc_measured,Voc_measured, kind='linear',fill_value = "extrapolate")
V2_Rs=itp(I_Rs)
Rs=-(V1_Rs-V2_Rs)/I_Rs;

 #c5 influence from series resistance
c5_V=Voc_measured-Rs*Isc_measured
c5_I=Isc_measured
plt.plot(c5_V,c5_I)

# calculate power for each curve
P1=np.amax(Voc_initial*Isc_initial)
P2=np.amax(c2_V*c2_I)
P3=np.amax(c3_V*c3_I)
P4=np.amax(c4_V*c4_I)
P5=np.amax(Isc_measured*Voc_measured)
P6=np.amax(c5_I*c5_V)
P7=np.amax(I_measured*V_measured)
PL_Isc=P1-P2
PL_uRsh=P2-P3
PL_J0=P3-P4
PL_nuRsh=P4-P5
PL_Rs=P5-P6
PL_cm=P6-P7

# plot pie chart
labels = 'Isc', 'Rsh(uni)', 'J0', 'Rsh(non_uni)','Rs','Current_mismatch'
sizes = [PL_Isc, PL_uRsh, PL_J0, PL_nuRsh, PL_Rs, PL_cm ]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','red','orange']
explode = (0, 0, 0, 0, 0, 0)  # explode 1st slice
 
# Plot
plt.figure(2)
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
 
plt.axis('equal')
plt.show()

print(PL_Isc)

print(PL_uRsh)
print(PL_J0)
print(PL_nuRsh)
print(PL_Rs)
print(PL_cm)
print(P1)
print(P7)







