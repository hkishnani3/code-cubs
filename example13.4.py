"""
Created on Thu Jan 16 22:30:01 2020

@author: hkish
"""

""" this program aids the designer to find appropriate open type FLAT BELT 
for a particular application
given the relative parameters."""
# KEEP THE CAPS LOCK TURNED ON
import math
import random

n2 = int(input("Please enter the speed of driven pulley in rpm \n"))
n1 = int(input("Please enter the speed of driving pulley in rpm\n"))
kw_driving = float(input("now, enter the power of driving pulley in KW\n"))
C =  int(input("Please enter the distance b/w driven and driving pulley centres in meter\n"))

Application = input("Please enter the application: \n")

preffered_pulley_dia = [100,112,125,140,160,180,
                        200,224,250,280,315,355,
                        400,450,500,560,630,710,
                        800,900,1000]

F_a  = {'NORMAL LOAD':1.0,'STEADY LOAD':1.2 ,'INTERMITTENT LOAD':1.3 ,'SHOCK LOAD':1.5}

ACF = {120:1.33 ,130:1.26 ,140:1.19 ,150:1.13 ,160:1.08 ,170:1.04 ,180:1.00 ,190:0.97 ,200:0.94}

transmitting_capacity_KW = {'HI-SPEED':0.0118,'FORT':0.0147}

standard_widths = {3:[25,40,50,63,76],
                   4:[25,40,50,63,76,90,100,112,125,152],
                   5:[76,100,112,125,152],
                   6:[112,125,152,180,200]}

optimum_v = [velocity/10 for velocity in range(178,229)]

driving_pulley_dia = (60*1000*random.choice(optimum_v))//(math.pi*n1)
driving_pulley_dia = list(filter(lambda i: i > driving_pulley_dia, preffered_pulley_dia))[0]

driven_pulley_dia = int((n1/n2)*driving_pulley_dia)
driven_pulley_dia = list(filter(lambda i: i >= driven_pulley_dia, preffered_pulley_dia))[0]


d = driven_pulley_dia if driven_pulley_dia < driving_pulley_dia else driving_pulley_dia
D = driven_pulley_dia if driven_pulley_dia > driving_pulley_dia else driving_pulley_dia

max_power = F_a[Application]*kw_driving

alpha_s = 180 - (2*180*math.asin((D-d)/(2*C*1000)))/math.pi

x_0 = round(alpha_s//10) * 10
x_1 = x_0 + 10

F_d = ((alpha_s - x_1 )/(x_0 - x_1))*ACF[x_0] + ((alpha_s - x_0)/(x_1 - x_0))*ACF[x_1]

corrected_power = F_d * max_power
v = (math.pi * d *n1)/(60*1000)

corrected_belt_rating = (v * transmitting_capacity_KW[input("please enter the variety of dunlop transmission belt\n")])/5.08

for no_of_plies in standard_widths.keys():
    width = (corrected_power/corrected_belt_rating)/no_of_plies
    print(width)
    flag = 1
    try:
        W = list(filter(lambda i: i > width, standard_widths[no_of_plies]))[0]
    except IndexError:
        flag = 0
        continue
    if flag == 1:
        print(no_of_plies)
        break

L_belt = round(((2*C)+((math.pi*(D+d))/2)+(((D-d)**2)/(4*C)))/1000 , 2)

print("SPECIFICATION OF BELT ARE AS FOLLOWS: \n LENGTH:  ", L_belt," \n WIDTH:  ", W, " \n NO. OF PLIES:  ", no_of_plies," \n")