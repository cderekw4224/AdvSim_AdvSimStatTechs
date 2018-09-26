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

############
# start reps
############
numreps = 30
for rep in range (0,numreps):
    
    hours = 15000
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
    
    #initialize data vars for sys prev data values
    sysprevtnow = 0
    sysprevwaittime = 0
    sysprevcumutil = 0
    sysprevcumsystime = 0
    sysprevcumarr = 0
    
    endprevreptnow = 0
    currepclocktime = 0
    
    nextdep = 1000000000 #set nextdep to a Big M time in minutes    
    nextarr = arrtime(tnow)
    
    #############
    #BATCH ARRAYS
    #############
    
    avgqtimeary_batch = []
    avgsystimeary_batch = []
    avgqlenary_batch = []
    avgutilary_batch = []
    tnow_batch = []
    cumarr_batch = []
    
    batchhours = 500
    #start tracking batch info for each rep
    batchmin = batchhours * 60
    batchtime = batchmin
    batchnum = -1
    
    #initialize batch current stats values
    batchtnow = 0
    batchwaittime = 0
    batchcumutil = 0
    batchcumsystime = 0
    batchcumarr = 0
    
#    print()
#    print('(--------------START WHILE--------------)')
#    print()
#            
    while tnow < tmax:   #while the current time < max time run while loop
        # tmax = 900,000
        
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
            if util == 0:  #i.e. - if no one is being serviced
                util = 1 #since no cur service & 1 arr -> now service/util = 1
                nextdep = deptime(tnow) #put in serv -> now determine dep time
            else: #since util != 0/i.e. someone is being serv, must go into q
                q += 1
            nextarr = arrtime(tnow)
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
            else:
                util = 0
                nextdep = 1000000000
            told = tnow
            
            
        #---END OF WHILE & tnow > batchtime --> ACCUMULATE STATS FOR BATCH----#
        
        #################################
        #-----BATCH PROCESSING CODE-----#
        #################################

        if tnow >= batchtime:
#            print()
#            print('(--------------BATCH CALCULATIONS-----------)')
#            print()

            batchnum += 1
            
            #assign data to batchcur = syscur - sysprev
            batchtnow = tnow - sysprevtnow
            batchwaittime = waittime - sysprevwaittime
            batchcumutil = cumutil - sysprevcumutil
            batchcumsystime = cumsystime - sysprevcumsystime
            batchcumarr = cumarr - sysprevcumarr
            
            #assign data to sysprev = syscur
            sysprevtnow = tnow
            sysprevwaittime = waittime
            sysprevcumutil = cumutil
            sysprevcumsystime = cumsystime
            sysprevcumarr = cumarr
            
            #calc metirccs of batchcur avg = data / measure
            batchcumarr -= 1
            batchavgqtime = batchwaittime / batchcumarr
            batchavgsystime = batchcumsystime / batchcumarr
            batchavgqlen = batchwaittime / batchtnow
            batchavgutil = batchcumutil / batchtnow
            
            #append batchcur metrics to batch array for cur rep
            tnow_batch.append(batchtnow)
            avgqtimeary_batch.append(batchavgqtime)
            avgsystimeary_batch.append(batchavgsystime)
            avgqlenary_batch.append(batchavgqlen)
            avgutilary_batch.append(batchavgutil)
            cumarr_batch.append(batchcumarr)
            
            #start tracking batch info for each rep
            batchtime += batchmin
            
    
    #-----END OF WHILE & REP --> ACCUMULATE STATS FOR REP-----#
    
    # REP AVG CALCULATIONS
    cumarr -= 1
    
    #calc metirccs of repcur avg = data / measure    
    sumq = 0
    sumtime = 0
    sumlen = 0
    sumutil = 0
    
    for batch in range (0,batchnum):
        sumq += avgqtimeary_batch[batch]
        sumtime += avgsystimeary_batch[batch]
        sumlen += avgqlenary_batch[batch]
        sumutil += avgutilary_batch[batch]
    
    #time divsor needs to be tnow(end of rep) - tnow(end of prev rep)
    #    tnow(end of rep) = tnow
    #    tnow(end of prev rep) = endprevreptnow
    currepclocktime = tnow - endprevreptnow
    
    avgqtimebatches = sumq / batchnum
    avgsystimebatches = sumtime / batchnum
    
    #-----which is correct?-----#
    
#    avgqlenbatches = sumlen / currepclocktime
#    avgutilbatches = sumutil / currepclocktime
    
    avgqlenbatches = sumlen / batchnum
    avgutilbatches = sumutil / batchnum
    
    # REP ARRAY STATS
    avgqtimeary.append(avgqtimebatches)
    avgsystimeary.append(avgsystimebatches)
    avgqlenary.append(avgqlenbatches)
    avgutilary.append(avgutilbatches)
    
    endprevreptnow = tnow
    
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
#print('sssqr = ', ssqr)
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


#print('########################')
#print('###### END PROGRAM #####')
#print('########################')
#print()

