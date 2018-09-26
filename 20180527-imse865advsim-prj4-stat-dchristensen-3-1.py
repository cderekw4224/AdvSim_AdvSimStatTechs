        # -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 15:21:44 2017

@author: Derek
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
def arrtime(tnow):
    arrmean = 3 #avg time b/t arr in hrs - i.e. 3 hrs b/t arr = 180 min
    arrlambda = 1/arrmean #arr RATE per hr
                        # 1/3 of a unit will arrive per hr
    exporand = arrgetrand(arrlambda) #time till next arr in addittional hrs
    exporandmin = exporand * 60 #time till next arr in additional min
#    print('arr exporandmin =', exporandmin)
    nextarr = tnow + exporandmin #system clock time calc for next arrival
#    print('nextarr =', nextarr)
#    print()
    return(nextarr) #returns system clock time for next arrival

### calculates time till next arrival in hours
### random number convertor from Uniform into Exponential
def arrgetrand(arrlambda):
    arrexporand = -math.log(1.0 - arrlcg()) / arrlambda #convert Uni to Expo
    return (arrexporand) #returns time till next arr in additional hours

### Inter-arrival time dist Linear Congruential Generator (LCG) 
def arrlcg():
    a = 100801   #the multiplier
    c = 103319   #the increment
    m = 193723   #the modulus
    global curarrseed  #current Z value (seed)
    curarrseed = (a*curarrseed + c) % m  #calcualtion of next arr Z value
    arrlcgnum = curarrseed / m  #calculation of Uniform value
    return(arrlcgnum)   #Uniform value returned to distribution converter

################################
### SERVICE TIME DIST. FUNCTIONS
################################

### service time determination 
def deptime(tnow):
    depmean = 2 #avg service time in hrs - i.e. 2 hrs to service = 120 min
    depmu = 1/depmean  #service RATE per hr
                         # 1/2 of a unit will be served per hr
    exporand = depgetrand(depmu) #time for next service in addittional hrs
    exporandmin = exporand * 60 #time for necxt service in additional min
#    print('dept exporandmin =', exporandmin)
    nextdep = tnow + exporandmin #system clock time calc for next departure
#    print('nextdep =', nextdep)
#    print()
    return(nextdep) #returns system clock time for next departure

### calculates time till next departure in hours
### random number convertor from Uniform into Exponential
def depgetrand(depmu):
    depexporand = -math.log(1.0 - deplcg()) / depmu #convert Uni to Expo
    return (depexporand) #returns time till next dep in additional hours

### Service time dist Linear Congruential Generator (LCG) 
def deplcg():
    a = 7000313   #the multiplier
    c = 0         #the increment
    m = 9004091   #the modulus
    global curdepseed  #current Z value (seed)
    curdepseed = (a*curdepseed + c) % m #calcualtion of next dep Z value
    deplcgnum = curdepseed / m  #calculation of Uniform value
    return(deplcgnum)   #Uniform value returned to distribution converter

######
# main
######

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

#33333333333333333333333333333333333
nextarr_ar = []
nextdep_ar = []
nextarr_ar.append(0)
first_tnow_rep_ar = []

nextarr_dif_ar = []
nextdep_dif_ar = []

#33333333333333333333333333333333333

############
# start reps
############

numreps = 30
for rep in range (0,numreps):
    
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
    nextarr = arrtime(tnow)
    
    #33333333333333333333333333333333333
    nextarr_ar.append(nextarr)
#    print('nextarr_ar = ', nextarr)
    
    first_tnow_rep = 0
    cnt = 0    
    
    #33333333333333333333333333333333333
    
    while tnow < tmax:   #while the current time < max time run while loop    
        if nextarr < nextdep:
            tnow = nextarr
#            print('tnow = ', tnow)
            if util == 1:
                cumutil = cumutil + (tnow - told)
            if q > 0:
                waittime = waittime + (q * (tnow - told))
            if util == 1:
                cumsystime = cumsystime + ((util + q) * (tnow - told))
            if tnow == nextarr:
                cumarr += 1
            if util == 0:          #i.e. - if no one is being serviced
                util = 1 #since no curr serv & 1 arr -> now service/util = 1
                nextdep = deptime(tnow) #put in serv -> now determine dep time
                
                #33333333333333333333333333333333333
                if cnt == 0:
                    first_tnow_rep = tnow
                    first_tnow_rep_ar.append(first_tnow_rep)
#                    print()
#                    print('tnow = ', tnow)
#                    print('first_tnow_rep = ', first_tnow_rep)
#                    print('first_tnow_rep_ar = ', first_tnow_rep_ar)
#                    print()
                nextdep_ar.append(nextdep)
#                print('nextdep_ar = ', nextdep)
                cnt += 1
                #33333333333333333333333333333333333
                
            else: #since util != 0/i.e. someone is being serv, must go into q
                q += 1
            nextarr = arrtime(tnow)
            
            #33333333333333333333333333333333333
            nextarr_ar.append(nextarr)
#            print('nextarr_ar = ', nextarr)
            #33333333333333333333333333333333333
            
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
                nextdep = deptime(tnow)
                
                #33333333333333333333333333333333333
                if cnt == 0:
                    first_tnow_rep = tnow
                    first_tnow_rep_ar.append(first_tnow_rep)
#                    print()
#                    print('tnow = ', tnow)
#                    print('first_tnow_rep = ', first_tnow_rep)
#                    print('first_tnow_rep_ar = ', first_tnow_rep_ar)
#                    print()
                nextdep_ar.append(nextdep)
#                print('nextdep_ar = ', nextdep)
                cnt += 1
                #33333333333333333333333333333333333
                
            else:
                util = 0
                nextdep = 1000000000
            told = tnow
            
    cumarr -= 1
    avgqtime = waittime / cumarr
    avgsystime = cumsystime / cumarr
    avgqlen = waittime / tnow
    avgutil = cumutil / tnow
    
    avgqtimeary.append(avgqtime)
    avgsystimeary.append(avgsystime)
    avgqlenary.append(avgqlen)
    avgutilary.append(avgutil)
    
#print('final tnow = ', tnow)
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
print()
print('avgutilreps = ', avgutilreps)
print()
#print(*avgutilary, sep = '\n')
#print()
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
#print()
print('sssqr = ', ssqr)
#print()
print('m = ', m)
print('hours = ', hours)
tstat += abs((avgutilreps - expecutil) / (ssqr/m)**0.5) #Calculate T-Stat
print('tstat = ', tstat)

t_critical = stats.t.ppf(q = q, df=df)  # Get the t-critical value*

print('t-critical value:')                  # Check the t-critical value
print(t_critical) 
#if tstat < t_critical:
#    print('T-Stat < Critical Value, Fail to Reject Null Hypothesis')
#elif t_critical < tstat:
#    print('Critical Value < T-Stat, Reject Null Hypothesis')
#else:
#    print('T-Stat = Critical Value')
    
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


#333333333333333333333333333333333333333333333333333333333333333333
nextarr_dif = 0
nextdep_dif = 0

nextarr_ar_sum = 0
nextarr_ar_len = len(nextarr_ar)
#print('nextarr_sum_len = ', nextarr_ar_len)

for i in range (1, nextarr_ar_len):
    if nextarr_ar[i] > nextarr_ar[i-1]:
        nextarr_dif = nextarr_ar[i] - nextarr_ar[i-1]
        nextarr_ar_sum += nextarr_dif
        nextarr_dif_ar.append(nextarr_dif)
#        print('nextarr_ar_sum = ', nextarr_ar_sum)
    elif nextarr_ar[i] < nextarr_ar[i-1]:
        nextarr_dif = nextarr_ar[i] - 0
        nextarr_ar_sum += nextarr_dif
        nextarr_dif_ar.append(nextarr_dif)
#        print('(-----------NEXT REP---------------)')
#        print('nextarr_ar_sum = ', nextarr_ar_sum)
#        print()
    else:
        nextarr_dif = 0
        nextarr_ar_sum += nextarr_dif
        nextarr_dif_ar.append(nextarr_dif)
#        print('nextarr_ar_sum = ', nextarr_ar_sum)

#print()
#print('nextarr_ar_sum = ', nextarr_ar_sum)
#print()

nextdep_ar_sum = 0
nextdep_ar_len = len(nextdep_ar)
#print('nextdep_ar_len = ', nextdep_ar_len)

#print()
#print('first_tnow_rep_ar = ', first_tnow_rep_ar)
#print()
#333333333333333333333333333333333333333333333333333333333333333333

#333333333333333333333333333333333333333333333333333333333333333333
jcnt = 0
for i in range (0, nextdep_ar_len):
    if i == 0:
        nextdep_dif = nextdep_ar[i] - first_tnow_rep_ar[jcnt]
        nextdep_ar_sum += nextdep_ar[i] - first_tnow_rep_ar[jcnt]
        nextdep_dif_ar.append(nextdep_dif)
#        print('nextdep_ar_sum = ', nextdep_ar_sum)
        jcnt += 1
    elif nextdep_ar[i] > nextdep_ar[i-1]:
        nextdep_dif = nextdep_ar[i] - nextdep_ar[i-1]
        nextdep_ar_sum += nextdep_dif
        nextdep_dif_ar.append(nextdep_dif)
#        print('nextdep_ar_sum = ', nextdep_ar_sum)
    elif nextdep_ar[i] < nextdep_ar[i-1]:
#        print()
#        print('jcnt = ', jcnt)
#        print('first_tnow_rep_ar[jcnt] = ', first_tnow_rep_ar[jcnt])
        nextdep_dif = nextdep_ar[i] - first_tnow_rep_ar[jcnt]
        nextdep_ar_sum += nextdep_dif
        nextdep_dif_ar.append(nextdep_dif)
#        print('nextdep_ar_sum = ', nextdep_ar_sum)
        jcnt += 1
    else:
        nextdep_dif = 0
        nextdep_ar_sum += nextdep_dif
        nextdep_dif_ar.append(nextdep_dif)
#        print('nextdep_ar_sum = ', nextdep_ar_sum)
#333333333333333333333333333333333333333333333333333333333333333333

#333333333333333333333333333333333333333333333333333333333333333333
#print('nextdep_ar_sum = ', nextdep_ar_sum)
#print()

#print('nextarr_ar = ', nextarr_ar)
#print()
#print(*nextarr_ar, sep = '\n')
#print()
#
#print('nextdep_ar = ', nextdep_ar)
#print()
#print(*nextdep_ar, sep = '\n')
#print()

#print('nextarr_dif_ar = ', nextarr_dif_ar)
#print()
#print('nextdep_dif_ar = ', nextdep_dif_ar)
#print()

nextarr_dif_ar_len = len(nextarr_dif_ar)
print('nextarr_dif_ar_len = ', nextarr_dif_ar_len)
#print()

nextdep_dif_ar_len = len(nextdep_dif_ar)
print('nextdep_dif_ar_len = ', nextdep_dif_ar_len)
print()

nextarr_dif_ar_sum = sum(i for i in nextarr_dif_ar)
nextdep_dif_ar_sum = sum(i for i in nextdep_dif_ar)
print('nextarr_dif_ar_sum = ', nextarr_dif_ar_sum)
print('nextdep_dif_ar_sum = ', nextdep_dif_ar_sum)
print()

nextarr_dif_ar_avg = nextarr_dif_ar_sum / nextarr_dif_ar_len
nextdep_dif_ar_avg = nextdep_dif_ar_sum / nextdep_dif_ar_len
print('nextarr_dif_ar_avg = ', nextarr_dif_ar_avg)
print('nextdep_dif_ar_avg = ', nextdep_dif_ar_avg)
print()
#333333333333333333333333333333333333333333333333333333333333333333

#333333333333333333333333333333333333333333333333333333333333333333
nextarr_dif_ar_diffsq_ar = []
nextdep_dif_ar_diffsq_ar = []

for i in range(0, nextarr_dif_ar_len):
    nextarr_dif_ar_diffsq = (nextarr_dif_ar[i] - nextarr_dif_ar_avg)**2
    nextarr_dif_ar_diffsq_ar.append(nextarr_dif_ar_diffsq)
    
for i in range(0, nextdep_dif_ar_len):
    nextdep_dif_ar_diffsq = (nextdep_dif_ar[i] - nextdep_dif_ar_avg)**2
    nextdep_dif_ar_diffsq_ar.append(nextdep_dif_ar_diffsq)
    
nextarr_dif_ar_diffsq_ar_sum = sum(i for i in nextarr_dif_ar_diffsq_ar)
nextdep_dif_ar_diffsq_ar_sum = sum(i for i in nextdep_dif_ar_diffsq_ar)
print('nextarr_dif_ar_diffsq_ar_sum = ', nextarr_dif_ar_diffsq_ar_sum)
print('nextdep_dif_ar_diffsq_ar_sum = ', nextdep_dif_ar_diffsq_ar_sum)
print()

vararr = nextarr_dif_ar_diffsq_ar_sum / (len(nextarr_dif_ar_diffsq_ar)-1)
vardep = nextdep_dif_ar_diffsq_ar_sum / (len(nextdep_dif_ar_diffsq_ar)-1)
print('vararr = ', vararr)
print('vardep = ', vardep)
print()
#333333333333333333333333333333333333333333333333333333333333333333

#print('########################')
#print('###### END PROGRAM #####')
#print('########################')
#print()
