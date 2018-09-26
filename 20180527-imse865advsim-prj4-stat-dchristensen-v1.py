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

#def getrand(lambdar):
#    exporand = -math.log(1.0 - random.random()) / lambdar
#    return (exporand)

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

#arrdistvals = []
#depdistvals = []

############
# start reps
############

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
 
for rep in range (0,30):
    
    hours = 500
    tmax = hours * 60 #max time to end program in minutes   #9600
    told = 0 #the most recent current time in minutes
    tnow = 0 #the current time in minutes
    
    #print()
    #print('tmax =', tmax)
    #print('told =', told)
    #print('initial tnow =', tnow)
    
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
    
    nextdep = 100000 #set nextdep to a Big M time in minutes
    
    #print('util =', util)
    #print('q =', q)
    #print('waittime =', waittime)
    #print('initial nextdep =', nextdep)
    
    nextarr = arrtime(tnow)
    
    #print()
    #    
    #print('#####################################')
    #print('#### BEGIN MAIN PART OF PROGRAM #####')
    #print('#####################################')
    #print()
    
    while tnow < tmax:   #while the current time < max time run while loop
    
    #    print('  #############################################################')
    #    print('  ### contunue to run while loop if current time < max time ###')
    #    print('  #############################################################')
    #    print()
    #    print(' tnow =', tnow)
    #    print(' tmax =', tmax)
    #    print()
    #
    #    print('##### if nextarr < nextdep run IF loop ######')
    #    print('nextarr =', nextarr)
    #    print('nextdep =', nextdep)
    #    print()
    
        if nextarr < nextdep:
    #        print('now running IF nextarr < nextdep')
    #        print()
            tnow = nextarr
    #        print('tnow has been assigned to nextarr ', tnow)
    #        print()
    #
    #        print('update stats')
            # update stats
    
            if util == 1:
                cumutil = cumutil + (tnow - told)
    #        else:
    #            cumutil = cumutil
    
            if q > 0:
                waittime = waittime + (q * (tnow - told))
    #        else:
    #            waittime = waittime
    
            if util == 1:
                cumsystime = cumsystime + ((util + q) * (tnow - told))
    #        else:
    #            cumsystime = cumsystime
    
            if tnow == nextarr:
                cumarr += 1
    #        else:
    #            cumarr = cumarr
    
    #        print('util =', util)
    
            if util == 0:          #i.e. - if no one is being serviced
    #            print('now running if util == 0')
    #            print('i.e. - if no one is being serviced')
    
                util = 1 #since no current service & 1 arr -> now service/util = 1
    #            print('since no current service & 1 arr -> now service/util = 1')
    #            print('util =', util)
    #            print('put in serv -> now determine new dep time')
    
                nextdep = deptime(tnow) #put in serv -> now determine dep time
    #            print()
    #            print('the nextdep has changed to', nextdep)
    #            print()
    
            else: #since util != 0/i.e. someone is being serv, must go into q
    #            print('since util != 0/i.e. someone is being serv, must go to q')
                q += 1
    #            print()
    #            print('q has increased by 1 to =', q)
    #            print()
    
            #now that the nextarr has either been put into serv or q,
            #we must now determine the nextarr
    #        print('now that the nextarr has either been put into serv or q,')
    #        print('we must now determine the nextarr')
    
            nextarr = arrtime(tnow)
    #        print('nextarr =', nextarr)
    
            told = tnow
    #        print('told is now changed to the current tnow =', told)
    #        print()
    
        else:   #since nextarr !< nextdep must run nextdep
    #        print()
    #        print('since nextarr !< nextdep must run nextdep')
    #        print('nextarr =', nextarr)
    #        print('nextdep =', nextdep)
    
            tnow = nextdep
    #        print()
    #        print('tnow is assigned to the value of nextdep =', tnow)
    
            # update stats
    
            if util == 1:
                cumutil = cumutil + (tnow - told)
    #        else:
    #            cumutil = cumutil
    
            if q > 0:
                waittime = waittime + (q * (tnow - told))
    #        else:
    #            waittime = waittime
    
            if util == 1:
                cumsystime = cumsystime + ((util + q) * (tnow - told))
    #        else:
    #            cumsystime = cumsystime
    
            if tnow == nextarr:
                cumarr += 1
    #        else:
    #            cumarr = cumarr
    
            if q >= 1:
                q -= 1
                nextdep = deptime(tnow)
    
            else:
                util = 0
                nextdep = 100000
    
    #        print('nextdep =', nextdep)
    
            told = tnow
    #        print('told is now changed to the current tnow =', told)
    #        print()
    #    print('end current while loop --> start new one')
    #    print()
    
    cumarr -= 1
    
#    print()
#    print('rep = ', rep+1)
#    
#    print('waittime =', waittime)
#    print('cumutil =', cumutil)
#    print('cumsystime = ', cumsystime)
#    print('cumarr = ', cumarr)
#    print()
    
    avgqtime = waittime / cumarr
    avgsystime = cumsystime / cumarr
    avgqlen = waittime / tnow
    avgutil = cumutil / tnow
    
#    print('The avg time in the q was ', avgqtime)
#    print('The avg time in the Sys was ', avgsystime)
#    print('The length of the q was ', avgqlen)
#    print('The avg utilization was ', avgutil)
    
    avgqtimeary.append(avgqtime)
    avgsystimeary.append(avgsystime)
    avgqlenary.append(avgqlen)
    avgutilary.append(avgutil)
    
#    print()

print()
print('avgqtimeary =', avgqtimeary)
print()
print('avgsystimeary =', avgsystimeary)
print()
print('avgqlenary =', avgqlenary)
print()
print('avgutilary =', avgutilary)
print()

sumq = 0
sumtime = 0
sumlen = 0
sumutil = 0

for rep in range (0,30):
    sumq += avgqtimeary[rep]
    sumtime += avgsystimeary[rep]
    sumlen += avgqlenary[rep]
    sumutil += avgutilary[rep]

avgqtimereps = sumq / 30
avgsystimereps = sumtime / 30
avgqlenreps = sumlen / 30
avgutilreps = sumutil / 30

print('avgqtimereps = ', avgqtimereps)
print('avgsystimereps = ', avgsystimereps)
print('avgqlenreps = ', avgqlenreps)
print('avgutilreps = ', avgutilreps)
print()

#a.	Perform a t-Test to determine whether or not there is a statistical 
# difference between the simulated data and the expected value
# You can either do this for utilization or expected number of people in line

# Utilization

# t test stat = xbar - mu / sqrt(s^2/m)
# xbar = avgutilreps
# mu = expected util

# expected util = lambda / mu = arrlambda / depmu
tstat = 0
m = 30
df = m-1
arrmean = 3  #avg time b/t arr in hrs - i.e. 3 hrs b/t arr = 180 min
arrlambda = 1/arrmean  #arr RATE per hr
                       # 1/3 of a unit will arrive per hr

depmean = 2 #avg service time in hrs - i.e. 2 hrs to service = 120 min
depmu = 1/depmean #service RATE per hr
                  # 1/2 of a unit will be served per hr

alpha = 0.10  # 1 - Confidence Level
q = 1 - alpha/2  #stats.t.ppf parameter
print('q = ', q)

expecutil = arrlambda / depmu #the expected utilization rate
expeclenq = (arrlambda/depmu)**2 / (1 - (arrlambda/depmu)) #E(x) Len Q

print('expecutil = ', expecutil)
print('expeclenq = ', expeclenq)

# s^2 = sum(mi - xbar)^2 / (m-1)
# s^2 = sum(avgutilary[i] - avgutilreps)^2 / (m-1)

ssqr = 0  #variable for s-squared
for i in range (0, 30):  #sum the sqared diff b/t each mi & xbar
    ssqr += (avgutilary[i] - avgutilreps)**2
    
ssqr /= (m-1)

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


#print('########################')
#print('###### END PROGRAM #####')
#print('########################')
#print()

