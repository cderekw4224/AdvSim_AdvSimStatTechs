        # -*- coding: utf-8 -*-
"""
Created on Tue Jun 05 15:21:44 2017

@author: Derek Christensen
"""

from __future__ import print_function
from __future__ import division
#import random
import math
import scipy.stats as stats

######################################
### INTER-ARRIVAL TIME DIST. FUNCTIONS
######################################  

### inter-arriavel time determination 
def arrtime(tnow, rep):
    rep = rep
    arrmean = 3 #avg time b/t arr in hrs - i.e. 3 hrs b/t arr = 180 min
    arrlambda = 1/arrmean #arr RATE per hr
                        # 1/3 of a unit will arrive per hr
    exporand = arrgetrand(arrlambda, rep) #time till next arr in add hrs
    exporandmin = exporand * 60 #time till next arr in additional min
    nextarr = tnow + exporandmin #system clock time calc for next arrival
    return(nextarr) #returns system clock time for next arrival

### calculates time till next arrival in hours
### random number convertor from Uniform into Exponential
def arrgetrand(arrlambda, rep):
    arrexporand = -math.log(1.0 - arrlcg(rep)) / arrlambda #convert Uni to Expo
    return (arrexporand) #returns time till next arr in additional hours

### Inter-arrival time dist Linear Congruential Generator (LCG) 
def arrlcg(rep):
    a = 100801   #the multiplier
    c = 103319   #the increment
    m = 193723   #the modulus
    global curarrseed  #current Z value (seed)
    global aparrrepcnt
    global numreps
    
    if rep < (numreps/2):
        curarrseed = curarrseed
        zarrused.append(curarrseed)
    elif rep == (numreps/2) and aparrrepcnt == 0:
        curarrseed = 50001
        zarrused.append(curarrseed)
        aparrrepcnt += 1
    elif rep == (numreps/2) and aparrrepcnt > 0:
        curarrseed = curarrseed
        zarrused.append(curarrseed)
    elif rep > (numreps/2):
        curarrseed = curarrseed
        zarrused.append(curarrseed)
    curarrseed = (a*curarrseed + c) % m  #calcualtion of next arr Z value
    arrlcgnum = curarrseed / m  #calculation of Uniform value

    if rep < (numreps/2):
        arrlcgnum = arrlcgnum
        unifarrused.append(arrlcgnum)
    else:
        arrlcgnum = (1 - arrlcgnum)
        oneminunifarrused.append(arrlcgnum)
    return(arrlcgnum)   #Uniform value returned to distribution converter

################################
### SERVICE TIME DIST. FUNCTIONS
################################

### service time determination 
def deptime(tnow, rep):
    depmean = 2 #avg service time in hrs - i.e. 2 hrs to service = 120 min
    depmu = 1/depmean  #service RATE per hr
                         # 1/2 of a unit will be served per hr
    exporand = depgetrand(depmu, rep) #time for next service in addittional hrs
    exporandmin = exporand * 60 #time for necxt service in additional min
    nextdep = tnow + exporandmin #system clock time calc for next departure
    return(nextdep) #returns system clock time for next departure

### calculates time till next departure in hours
### random number convertor from Uniform into Exponential
def depgetrand(depmu, rep):
    depexporand = -math.log(1.0 - deplcg(rep)) / depmu #convert Uni to Expo
    return (depexporand) #returns time till next dep in additional hours

### Service time dist Linear Congruential Generator (LCG) 
def deplcg(rep):
    a = 7000313   #the multiplier
    c = 0         #the increment
    m = 9004091   #the modulus
    global curdepseed  #current Z value (seed)
    global apdeprepcnt
    global numreps
    
    if rep < (numreps/2):
        curdepseed = curdepseed
        zdepused.append(curdepseed)
    elif rep == (numreps/2) and apdeprepcnt == 0:
        curdepseed = 94907
        zdepused.append(curdepseed)
        apdeprepcnt += 1
    elif rep == (numreps/2) and apdeprepcnt > 0:
        curdepseed = curdepseed
        zdepused.append(curdepseed)
    elif rep > (numreps/2):
        curdepseed = curdepseed
        zdepused.append(curdepseed)
    
    curdepseed = (a*curdepseed + c) % m #calcualtion of next dep Z value
    deplcgnum = curdepseed / m  #calculation of Uniform value
    
    if rep < (numreps/2):
        deplcgnum = deplcgnum
        unifdepused.append(deplcgnum)
    else:
        deplcgnum = (1 - deplcgnum)
        oneminunifdepused.append(deplcgnum)
    return(deplcgnum)   #Uniform value returned to distribution converter
    

######
# main
######

#(------------TESTING ARRAYS---------------)#
repnum_ar = []
aparrrepcnt_ar = []
apdeprepcnt_ar = []

zarrused = []
unifarrused = []
oneminunifarrused = []
global aparrrepcnt 
aparrrepcnt = 0

zdepused = []
unifdepused = []
oneminunifdepused = []
global apdeprepcnt 
apdeprepcnt = 0

avgqtimeary = []
avgsystimeary = []
avgqlenary = []
avgutilary = []

origarrseed = 50001
origdepseed = 94907

global curarrseed  #current seed for inter-arrival dist.
global curdepseed  #current seed for service time dist.

curarrseed = 50001  #inital Z(0) seed for inter-arrival dist.
curdepseed = 94907  #inital Z(0) seed for service time dist.

global numreps
############
# start reps
############

numreps = 30
for rep in range (0,numreps):
#    print()
#    print('(---------------REP # ', rep+1,'---------------)')
#    print()
    
    repnum_ar.append(rep)
    
    hours = 500
    tmax = hours * 60 #max time to end program in minutes   #9600
    told = 0 #the most recent current time in minutes
    tnow = 0 #the current time in minutes
    
    util = 0
    q = 0
    waittime = 0
    cumutil = 0
    cumsystime = 0
    cumarr = 0
    
    avgqtime = 0
    avgsystime = 0
    avgqlen = 0
    avgutil = 0
    
    nextdep = 1000000000 #set nextdep to a Big M time in minutes
    nextarr = arrtime(tnow, rep)

    while tnow < tmax:   #while the current time < max time run while loop    
        if nextarr < nextdep:
            tnow = nextarr
            if util == 1:
                cumutil = cumutil + (tnow - told)
            if q > 0:
                waittime = waittime + (q * (tnow - told))
            if util == 1:
                cumsystime = cumsystime + ((util + q) * (tnow - told))
            if tnow == nextarr:
                cumarr += 1
            if util == 0:          #i.e. - if no one is being serviced
                util = 1 #since no cur service & 1 arr -> now service/util = 1
                nextdep = deptime(tnow, rep) #put in serv -> now calc dep time
            else: #since util != 0/i.e. someone is being serv, must go into q
                q += 1
            nextarr = arrtime(tnow, rep)
            told = tnow
        else:   #since nextarr !< nextdep must run nextdep
            tnow = nextdep
            if util == 1:
                cumutil = cumutil + (tnow - told)
            if q > 0:
                waittime = waittime + (q * (tnow - told))
            if util == 1:
                cumsystime = cumsystime + ((util + q) * (tnow - told))
            if tnow == nextarr:
                cumarr += 1
            if q >= 1:
                q -= 1
                nextdep = deptime(tnow, rep)
            else:
                util = 0
                nextdep = 1000000000
            told = tnow
            
    aparrrepcnt_ar.append(aparrrepcnt)
    apdeprepcnt_ar.append(apdeprepcnt)
    
    cumarr -= 1
    avgqtime = waittime / cumarr
    avgsystime = cumsystime / cumarr
    avgqlen = waittime / tnow
    avgutil = cumutil / tnow
    
    avgqtimeary.append(avgqtime)
    avgsystimeary.append(avgsystime)
    avgqlenary.append(avgqlen)
    avgutilary.append(avgutil)
    
    print()
    print('avgutilary = ', avgutilary)
    print()
    
print('final tnow = ', tnow)
sumq = 0
sumtime = 0
sumlen = 0
sumutil = 0

for rep in range (0,numreps):
    sumq += avgqtimeary[rep]
    sumtime += avgsystimeary[rep]
    sumlen += avgqlenary[rep]
    sumutil += avgutilary[rep]

avgqtimereps = sumq / numreps
avgsystimereps = sumtime / numreps
avgqlenreps = sumlen / numreps
avgutilreps = sumutil / numreps

print('avgutilreps = ', avgutilreps)

#a.	Perform a t-Test to determine whether or not there is a statistical 
# difference between the simulated data and the expected value
# You can either do this for utilization or expected number of people in line

# Utilization

# t test stat = xbar - mu / sqrt(s^2/m)
# xbar = avgutilreps
# mu = expected util

# expected util = lambda / mu = arrlambda / depmu
tstat = 0
m = numreps

df = m-1
arrmean = 3  #avg time b/t arr in hrs - i.e. 3 hrs b/t arr = 180 min
arrlambda = 1/arrmean  #arr RATE per hr
                       # 1/3 of a unit will arrive per hr

depmean = 2 #avg service time in hrs - i.e. 2 hrs to service = 120 min
depmu = 1/depmean #service RATE per hr
                  # 1/2 of a unit will be served per hr

alpha = 0.10  # 1 - Confidence Level
cl = 1 - alpha

q = 1 - alpha/2  #stats.t.ppf parameter
print('CL = ', cl,', ','alpha = ', alpha, ', CI = ', q)

expecutil = arrlambda / depmu #the expected utilization rate
expeclenq = (arrlambda/depmu)**2 / (1 - (arrlambda/depmu)) #E(x) Len Q

print('expecutil = ', expecutil)
#print('expeclenq = ', expeclenq)

# s^2 = sum(mi - xbar)^2 / (m-1)
# s^2 = sum(avgutilary[i] - avgutilreps)^2 / (m-1)

ssqr = 0  #variable for s-squared
for i in range (0, numreps):  #sum the sqared diff b/t each mi & xbar
    ssqr += (avgutilary[i] - avgutilreps)**2
#print('sssqr = ', ssqr)    
ssqr /= (m-1)
print()
print('sssqr = ', ssqr)
print()
print('m = ', m)
print('hours = ', hours)
tstat += abs((avgutilreps - expecutil) / (ssqr/m)**0.5) #Calculate T-Stat
print('tstat = ', tstat)

t_critical = stats.t.ppf(q = q, df=df)  # Get the t-critical value*

print('t-critical value:')                  # Check the t-critical value
print(t_critical) 
if tstat < t_critical:
    print('T-Stat < Critical Value, Fail to Reject Null Hypothesis')
elif t_critical < tstat:
    print('Critical Value < T-Stat, Reject Null Hypothesis')
else:
    print('T-Stat = Critical Value')
    
#####################
# CONFIDENCE INTERVAL
#####################

#CI: (xbarmod - xbarsys) +- (T(m-1,1 - alpha/2) *  SQRT(ssqr/m))
# xbarmod = avgutilreps
# xbarsys = expecutil
# T(m-1,1 - alpha/2) = t_critical
# SQRT(ssqr/m) = math.sqrt(ssrq/m)

LB = 0 #lower CI
UB = 0 #upper CI

LB = (avgutilreps - expecutil) - (t_critical * math.sqrt(ssqr/m))
UB = (avgutilreps - expecutil) + (t_critical * math.sqrt(ssqr/m))

print('CI LB = ', LB)
print('CI UB = ', UB)
print('CI = [',LB,', ',UB,']')
print()

print('repnum_ar = ', repnum_ar)
print('aparrrepcnt_ar = ', aparrrepcnt_ar)
print('apdeprepcnt_ar = ', apdeprepcnt_ar)
print()

#print('########################')
#print('###### END PROGRAM #####')
#print('########################')
#print()

