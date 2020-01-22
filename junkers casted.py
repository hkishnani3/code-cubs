
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 18:39:03 2020

@author: hkish
JUNKER'S
To study single cylinder, two-stroke opposed piston Junker's Diesel Engine. Conduct a  test to 
calculate Air-Fuel ratio and prepare a heat balance sheet
"""


from pandas import read_excel, to_numeric

from math import pi


heat_by_cooling_water = ['Kj/sec']
heat_by_exhaust_gases = ['Kj/sec']
heat_by_fuel          = ['Kj/sec']
m_a                   = ['Kg/sec']  
h_a                   = ['m']


excel_file = r'junkers.xlsx'

observation = read_excel(excel_file, skiprows = 2)

observation.dropna(axis = 1,inplace = True)

g           =       9.81        # in m/sec^2

m_w         =       3.6         # mass flow rate of water in kg/min

C_p_water   =       4.186       # in KJ/Kg.k

C_p_exhaust =       1.17        # in KJ/Kg.k

C_V_HSD     =       42.6*10**3  # in KJ/Kg

P_atm       =       101325      # in N/m^2

R_Ch        =       0.287       # in KJ/Kg

T_atm       =       273+20      # in K    

rho_water   =       1000        #in Kg/m^3

rho_HSD     =       840         #in Kg/m^3




Cd_orifice   =       {25:0.65, 30:0.66, 40:68}                                                           # dia in mm : C_d

Area_orifice =       [(((pi/4)*orifice_dia**2)/10**6) for orifice_dia in Cd_orifice.keys()]              # in m^2 

rho_air      =       P_atm/(R_Ch*T_atm*1000)                                                             # in Kg/m^3

hw1          =       list(to_numeric(observation["hw1"],errors= 'ignore' ,downcast='float'))          # in cm
 
hw2          =       list(to_numeric(observation["hw2"],errors= 'ignore' ,downcast='float'))          # in cm

Time         =       list(to_numeric(observation["Time"],errors= 'ignore',downcast='integer'))        # in sec

Fuel_used    =       list(to_numeric(observation["Fuel used"],errors= 'ignore',downcast='integer'))   # in cc

T_exit_water =       list(to_numeric(observation["Temperature of water at outlet"],errors= 'ignore',downcast='integer'))

T_exhaust_gases =    list(to_numeric(observation["Temperature of Exhaust air"],errors= 'ignore',downcast='integer'))

              
for i in range(1,len(hw1)):
    h_a.append((rho_water*((hw2[i]-hw1[i])/100))/rho_air)                                   # in m
    m_a.append(rho_air*Cd_orifice[30]*Area_orifice[1]*(2*g*h_a[i])**0.5)                    # in Kg/sec
    heat_by_fuel.append(C_V_HSD * ((Fuel_used[i]*10**-6)*(rho_HSD) / Time[i]))              # KJ/sec
    heat_by_cooling_water.append(C_p_water * (m_w/60) * ((273+T_exit_water[i]) - T_atm))    # KJ/sec
    heat_by_exhaust_gases.append(C_p_exhaust * (m_a[i]+((Fuel_used[i]*10**-6)*(rho_HSD) / Time[i])) * ((273+T_exhaust_gases[i]) - T_atm)) # KJ/sec


print(observation, sep = '\n')
