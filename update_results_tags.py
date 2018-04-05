

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 17:20:32 2017

@author: Hubert Seigneur


"""

from Pithon_loadfloat1 import *


##### test Connect() ---------- PI Server

status = connect_to_Server("net1552.net.ucf.edu")
print('\nConnection status is',status)


##### test get_tag_snapshot() ---------- PI Server



Update_Tag_Value(''.join(map(str,['S2.A', Module,'.PL_cm'])), float(PL_cm), Time1) # Restore original value of tag at same timestamp
value = get_tag_value(''.join(map(str,['S2.A', Module,'.PL_cm'])),Time1) # verify that the original value has been restored
print('The current mismatch loss is {} at {}'.format(value,Time1))

Update_Tag_Value('S2.A792.PL_uni_Rsh', float(PL_uRsh), Time1) # Restore original value of tag at same timestamp
value = get_tag_value('S2.A792.PL_uni_Rsh',Time1) # verify that the original value has been restored
print('The uniform shunting loss is {} at {}'.format(value,Time1))

Update_Tag_Value('S2.A792.PL_Isc',float(PL_Isc), Time1) # Restore original value of tag at same timestamp
value = get_tag_value('S2.A792.PL_Isc',Time1) # verify that the original value has been restored
print('The Isc loss is {} at {}'.format(value,Time1))

Update_Tag_Value('S2.A792.PL_J0', float(PL_J0), Time1) # Restore original value of tag at same timestamp
value = get_tag_value('S2.A792.PL_J0',Time1) # verify that the original value has been restored
print('The J0 loss is {} at {}'.format(value,Time1))

Update_Tag_Value('S2.A792.PL_non_uni_Rsh', float(PL_nuRsh), Time1) # Restore original value of tag at same timestamp
value = get_tag_value('S2.A792.PL_non_uni_Rsh',Time1) # verify that the original value has been restored
print('The non uniform shunting loss is  {} at {}'.format(value,Time1))

Update_Tag_Value('S2.A792.PL_Rs', float(PL_Rs), Time1) # Restore original value of tag at same timestamp
value = get_tag_value('S2.A792.PL_Rs',Time1) # verify that the original value has been restored
print('The series resistance loss is {} at {}'.format(value,Time1))

#### Disconnect() ---------- PI Server

Update_Tag_Value('S2.A792.PL_cm_Percent', float(PLP_cm), Time1) # Restore original value of tag at same timestamp
value = get_tag_value('S2.A792.PL_cm_Percent',Time1) # verify that the original value has been restored
print('The current mismatch loss percentage is {} at {}'.format(value,Time1))

Update_Tag_Value('S2.A792.PL_uni_Rsh_Percent', float(PLP_uRsh), Time1) # Restore original value of tag at same timestamp
value = get_tag_value('S2.A792.PL_uni_Rsh_Percent',Time1) # verify that the original value has been restored
print('The uniform shunting loss percentage is {} at {}'.format(value,Time1))

Update_Tag_Value('S2.A792.PL_Isc_Percent',float(PLP_Isc), Time1) # Restore original value of tag at same timestamp
value = get_tag_value('S2.A792.PL_Isc_Percent',Time1) # verify that the original value has been restored
print('The Isc loss percentage is {} at {}'.format(value,Time1))

Update_Tag_Value('S2.A792.PL_J0_Percent', float(PLP_J0), Time1) # Restore original value of tag at same timestamp
value = get_tag_value('S2.A792.PL_J0_Percent',Time1) # verify that the original value has been restored
print('The J0 loss percentage is {} at {}'.format(value,Time1))

Update_Tag_Value('S2.A792.PL_non_uni_Rsh_Percent', float(PLP_nuRsh), Time1) # Restore original value of tag at same timestamp
value = get_tag_value('S2.A792.PL_non_uni_Rsh_Percent',Time1) # verify that the original value has been restored
print('The non uniform shunting loss percentage is  {} at {}'.format(value,Time1))

Update_Tag_Value('S2.A792.PL_Rs_Percent', float(PLP_Rs), Time1) # Restore original value of tag at same timestamp
value = get_tag_value('S2.A792.PL_Rs_Percent',Time1) # verify that the original value has been restored
print('The series resistance loss percentage is {} at {}'.format(value,Time1))


status = disconnect_Server("net1552.net.ucf.edu")
print('\nConnection status is',status)


