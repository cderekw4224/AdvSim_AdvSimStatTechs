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
    
#    global zarr
#    zarr = curarrseed
#    print('zarr = ', zarr)
    
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
    
#    global zdep
#    zdep = curdepseed
#    print('zdep = ', zdep)
    
    deplcgnum = curdepseed / m  #calculation of Uniform value
    return(deplcgnum)   #Uniform value returned to distribution converter


##################
# ----- MAIN -----
##################
    

#arrdistvals = []
#depdistvals = []

avgqtimeary = []
avgsystimeary = []
avgqlenary = []
avgutilary = []

cilbary = []
ciubary = []

origarrseed = 50001
origdepseed = 94907

global curarrseed  #current seed for inter-arrival dist.
global curdepseed  #current seed for service time dist.

curarrseed = 50001  #inital Z(0) seed for inter-arrival dist.
curdepseed = 94907  #inital Z(0) seed for service time dist.

global zarr
global zdep
zarr = curarrseed
zdep = curdepseed
#print('zarr = ', zarr)
#print('zdep = ', zdep)

############
# start reps
############

avgutilsreps_numci_ar = []
ssqr_numci_ar = []
tstat_numci_ar = []

numcireps = 40
for cirep in range (0,numcireps):
    
#    print()
#    print('cirep = ', cirep+1)
#    print()
    
    avgqtimeary = []
    avgsystimeary = []
    avgqlenary = []
    avgutilary = []
    
#    print()
#    print('avgqtimeary =', avgqtimeary)
#    print()
#    print('avgsystimeary =', avgsystimeary)
#    print()
#    print('avgqlenary =', avgqlenary)
#    print()
#    print('avgutilary =', avgutilary)
#    print()

    
    numreps = 30
    for rep in range (0,numreps):
#        print()
#        print('rep = ', rep+1)
        
        zarr = curarrseed
#        print('zarr = ', zarr)
        
        zdep = curdepseed
#        print('zdep = ', zdep)
        
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
        
        nextdep = 100000 #set nextdep to a Big M time in minutes        
        nextarr = arrtime(tnow)

        #####################################
        #### BEGIN MAIN PART OF ALGORITHM ###
        #####################################
        while tnow < tmax:   #while the current time < max time run while loop
        
        #############################################################
        ### contunue to run while loop if current time < max time ###
        #############################################################
            if nextarr < nextdep:
                tnow = nextarr  #tnow has been assigned to nextarr     
                if util == 1:
                    cumutil = cumutil + (tnow - told)        
                if q > 0:
                    waittime = waittime + (q * (tnow - told))
                if util == 1:
                    cumsystime = cumsystime + ((util + q) * (tnow - told))
                if tnow == nextarr:
                    cumarr += 1        
                if util == 0:   #now running if util == 0
                                #i.e. - if no one is being serviced       
                    util = 1 #since no current service & 1 arr -> 
                             #now service/util = 1
                    #put in serv -> now determine new dep time
                    nextdep = deptime(tnow)        
                else: #since util != 0/i.e. someone is being serv, 
                      #must go into q
                    q += 1
                #now that the nextarr has either been put into serv or q,
                #we must now determine the nextarr
                nextarr = arrtime(tnow)
                told = tnow
            else:   #since nextarr !< nextdep must run nextdep
                tnow = nextdep        
                # update stats        
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
            #told is now changed to the current tnow
        #end current while loop --> start new one
        cumarr -= 1
        
        avgqtime = waittime / cumarr
        avgsystime = cumsystime / cumarr
        avgqlen = waittime / tnow
        avgutil = cumutil / tnow
        
        avgqtimeary.append(avgqtime)
        avgsystimeary.append(avgsystime)
        avgqlenary.append(avgqlen)
        avgutilary.append(avgutil)
        
#        print()
#        print('avgqtimeary =', avgqtimeary)
#        print()
#        print('avgsystimeary =', avgsystimeary)
#        print()
#        print('avgqlenary =', avgqlenary)
#        print()
#        print('avgutilary =', avgutilary)
#        print()
    
#    print()
#    print('avgqtimeary =', avgqtimeary)
#    print()
#    print('avgsystimeary =', avgsystimeary)
#    print()
#    print('avgqlenary =', avgqlenary)
#    print()
#    print('avgutilary =', avgutilary)
#    print()
    
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
    
#    print('avgqtimereps = ', avgqtimereps)
#    print('avgsystimereps = ', avgsystimereps)
#    print('avgqlenreps = ', avgqlenreps)
#    print('avgutilreps = ', avgutilreps)
#    print()
    
    #a.    Perform a t-Test to determine whether or not there is a statistical 
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
    
    alpha = 0.05     # 1 - Confidence Level
    cl = 1 - alpha
    
    q = 1 - alpha/2  #stats.t.ppf parameter
#    print('q = ', q)
#    print('CL = ', cl,', ','alpha = ', alpha, ', CI = ', q)
    expecutil = arrlambda / depmu #the expected utilization rate
    expeclenq = (arrlambda/depmu)**2 / (1 - (arrlambda/depmu)) #E(x) Len Q
    
#    print('expecutil = ', expecutil)
#    print('expeclenq = ', expeclenq)
    
    # s^2 = sum(mi - xbar)^2 / (m-1)
    # s^2 = sum(avgutilary[i] - avgutilreps)^2 / (m-1)
    
    ssqr = 0  #variable for s-squared
    for i in range (0, numreps):  #sum the sqared diff b/t each mi & xbar
        ssqr += (avgutilary[i] - avgutilreps)**2
        
    ssqr /= (m-1)
    
    tstat += abs((avgutilreps - expecutil) / (ssqr/m)**0.5) #Calculate T-Stat
#    print('tstat = ', tstat)
    
    t_critical = stats.t.ppf(q = q, df=df)  # Get the t-critical value*
#    print('t-critical value = ', t_critical)                  
    
#    # Check the t-critical value
#    if tstat < t_critical:
#        print('T-Stat < Critical Value, Fail to Reject Null Hypothesis')
#    elif t_critical < tstat:
#        print('Critical Value < T-Stat, Reject Null Hypothesis')
#    else:
#        print('T-Stat = Critical Value')
        
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
    
#    LB = (avgutilreps - expecutil) - (t_critical * math.sqrt(ssqr/m))
#    UB = (avgutilreps - expecutil) + (t_critical * math.sqrt(ssqr/m))
    
    LB = (avgutilreps) - (t_critical * math.sqrt(ssqr/m))
    UB = (avgutilreps) + (t_critical * math.sqrt(ssqr/m))
    
#    print('CI LB = ', LB)
#    print('CI UB = ', UB)
    print('CI = [',LB,', ',UB,']')
    
    cilbary.append(LB)
    ciubary.append(UB)
    avgutilsreps_numci_ar.append(avgutilreps)
    ssqr_numci_ar.append(ssqr)
    tstat_numci_ar.append(tstat)
    
print()
print('cilbary = ', cilbary)
print('ciubary = ', ciubary)
print()

print('CL = ', cl,', ','alpha = ', alpha, ', CI = ', q)
print('m = ', m)
print('df = ', df)
print('arrmean = ', arrmean, ' depmean = ', depmean)
print('arrlanbda = ', arrlambda, ' depmu = ', depmu)
print('expecutil = ', expecutil)
print()
print('avgutilreps = ', avgutilreps)
print('ssqr = ', ssqr)
print('tstat = ', tstat)
print('t_critical = ', t_critical)
print()

avgutilsreps_numci_ar_avg = 0
ssqr_numci_ar_avg = 0
tstat_numci_ar_avg = 0

avgutilsreps_numci_ar_avg = ((sum(i for i in avgutilsreps_numci_ar)) / 
                             numcireps)
ssqr_numci_ar_avg = (sum(i for i in ssqr_numci_ar))/numcireps
tstat_numci_ar_avg = (sum(i for i in tstat_numci_ar))/numcireps

print('avgutilsreps_numci_ar_avg = ', avgutilsreps_numci_ar_avg)
print('ssqr_numci_ar_avg = ', ssqr_numci_ar_avg)
print('tstat_numci_ar_avg = ', tstat_numci_ar_avg)

###############################################################
# # of CI that contain theoretical mean (0.6667) of utilization
###############################################################
print('expecutil = ', expecutil)
print()
numcirepscontain = 0
numcirepscontainary = []

for i in range (0,numcireps):
    if (cilbary[i] <= expecutil) and (ciubary[i] >= expecutil):
        numcirepscontain +=1
        numcirepscontainary.append(i)
        
print('numcirepscontain = ', numcirepscontain)
print('numcirepscontainary = ', numcirepscontainary)

numcirepscontain_not = 0
numcirepscontainary_not = []

for i in range (0,numcireps):
    if (cilbary[i] >= expecutil) or (ciubary[i] <= expecutil):
        numcirepscontain_not +=1
        numcirepscontainary_not.append(i)
        
print('numcirepscontain_not = ', numcirepscontain_not)
print('numcirepscontainary_not = ', numcirepscontainary_not)

for i in range(0, numcirepscontain_not):
    arrayspot = numcirepscontainary_not[i]
    print('arrayspot = ', arrayspot)
    print('CI_NOT = [',cilbary[arrayspot],', ',ciubary[arrayspot],']')

#print('########################')
#print('###### END PROGRAM #####')
#print('########################')
#print()
