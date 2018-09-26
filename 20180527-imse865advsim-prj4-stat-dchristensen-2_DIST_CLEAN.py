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
import inspect

def lineno():
    """Returns the current line number in our program."""
    return(inspect.currentframe().f_back.f_lineno)
    
######################################
### INTER-ARRIVAL TIME DIST. FUNCTIONS
######################################  

### inter-arriavel time determination 
def arrtime(tnow):
    arrmean = 3 #avg time b/t arr in hrs - i.e. 3 hrs b/t arr = 180 min
    arrlambda = 1/arrmean #arr RATE per hr
                        # 1/3 of a unit will arrive per hr
    funcrand = arrgetrand(arrlambda) #time till next arr in addittional hrs
    funcrandmin = funcrand * 60 #time till next arr in additional min
    nextarr = tnow + funcrandmin #system clock time calc for next arrival
    return(nextarr) #returns system clock time for next arrival

### calculates time till next arrival in hours
### random number convertor from Uniform into Function
def arrgetrand(arrlambda):
    arr364x2rand = 4 * (arrlcg())**(1/3) #convert Uni to 364x2
    return (arr364x2rand) #returns time till next arr in additional hours

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
    depsigma = 0.25
    depmu = depmean
    normrand = depgetrand(depmu, depsigma) #time for next serv in add hrs
    normrandmin = normrand * 60 #time for necxt service in additional min
    normrandmin_ar.append(normrandmin)
    nextdep = tnow + normrandmin #system clock time calc for next departure
    return(nextdep) #returns system clock time for next departure

### calculates time till next departure in hours
### random number convertor from Uniform into Normal
def depgetrand(depmu, depsigma):
#    depnormrand = -math.log(1.0 - deplcg()) / depmu #convert Uni to Norm
    u1 = 0
    u2 = 0
    w = 0
    u1, u2 = deplcg()
    v1 = (2*u1) - 1
    v2 = (2*u2) - 1
    w = v1**2 + v2**2
    if w > 1:
        return depgetrand(depmu, depsigma)  #recursive call
    Y = math.sqrt( (-2) * ( ( math.log(w) ) / w ) )
    X1 = v1*Y
#    X2 = v2*Y
    depnormrand1 = depmu + depsigma*X1
#    depnormrand2 = depmu + depsigma*X2
    return (depnormrand1) #returns time till next dep in additional hours

### Service time dist Linear Congruential Generator (LCG) 
#def deplcg(u1, u2):
def deplcg():
    global curdepseed  #current Z value (seed)
    a = 7000313   #the multiplier
    c = 0         #the increment
    m = 9004091   #the modulus
    u1 = curdepseed / m  #calculation of Uniform value #1
    curdepseed = (a*curdepseed + c) % m #calcualtion of next dep Z value
    origdepseed_ar.append(curdepseed)
    u2 = curdepseed / m  #calculation of Uniform value #2
    return(u1, u2)   #Uniform value returned to distribution converter

######
# main
######
if __name__ == '__main__':
    
    avgqtimeary = []
    avgsystimeary = []
    avgqlenary = []
    avgutilary = []
    
    global origarrseed
    global origdepseed
    
    origarrseed = 50001
    origdepseed = 94907
    
    origdepseed_ar = []
    origdepseed_ar.append(origdepseed)
        
    global curarrseed  #current seed for inter-arrival dist.
    global curdepseed  #current seed for service time dist.
    
    curarrseed = 50001  #inital Z(0) seed for inter-arrival dist.
    curdepseed = 94907  #inital Z(0) seed for service time dist.
    
    #-------------------------
    nextarr_hr_ar = []
    #-------------------------
    
    #-------------------------
    nextdepmin_hr_ar = []
    #-------------------------
    
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
        #-------------------------
        nextarr_ar = []  #array for next arrivals
        nextarr_ar.append(0)  #start of replication
        nextarr_sum = 0  #sum of next arrival times
        nextarr_avg = 0  #average of next arrival times
        #-------------------------
        #-------------------------
        normrandmin_ar = []  #array for service times
        nextdepmin_sum = 0  #sum of service times
        nextdepmin_avg = 0  #avg of service times
        #-------------------------
        nextdep = 1000000000 #set nextdep to a Big M time in minutes    
        nextarr = arrtime(tnow)
        #---------------------------
        nextarr_ar.append(nextarr)
        #---------------------------
        
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
                    util = 1 #since no cur serv & 1 arr -> now serv/util = 1
                    nextdep = deptime(tnow) #put in serv -> now determine dep
                else: #since util != 0/i.e. someone is in serv, must go into q
                    q += 1
                nextarr = arrtime(tnow)
                #---------------------------
                nextarr_ar.append(nextarr)
                #---------------------------
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
        #------------------------------------------
        cumarr -= 1
        avgqtime = waittime / cumarr
        avgsystime = cumsystime / cumarr
        avgqlen = waittime / tnow
        avgutil = cumutil / tnow
        
        avgqtimeary.append(avgqtime)
        avgsystimeary.append(avgsystime)
        avgqlenary.append(avgqlen)
        avgutilary.append(avgutil)
        #-------------------------------------------
        #--------------------------------------------------
        nextarr_sum = sum([t - s for s, t in zip(nextarr_ar, nextarr_ar[1:])])
        nextarr_avg = nextarr_sum / (len(nextarr_ar)-1)
        nextarr_hr = 0
        nextarr_hr = nextarr_avg / 60
        nextarr_hr_ar.append(nextarr_hr)
        #---------------------------------------------------
        #--------------------------------------------------
        nextdepmin_sum = sum(i for i in normrandmin_ar)
        nextdepmin_avg = nextdepmin_sum / len(normrandmin_ar)
        nextdepmin_hr = 0
        nextdepmin_hr = nextdepmin_avg / 60
        nextdepmin_hr_ar.append(nextdepmin_hr)
        #------------------------------------------------------
        
    #---------------------------------------------
    print('#--------------------------------------------')
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
    print(*avgutilary, sep = '\n')
    print()
    #---------------------------------------------
    #--------------------------------------------------------------------
    #a.	Perform a t-Test to determine whether or not there is a statistical 
    # difference between the simulated data and the expected value
    # You can either do this for util or expected number of people in line
    
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
    #--------------------------------------------------------------------
    
    #--------------------------------------------------------------------
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
    print('#-------------------------------------------------')
    print()
    #----------------------------------------------------------------------
    
    #----------------------------------------------------------------------
    #####################################
    # SUMMARY STATS FOR FUNC & NORM DISTS
    #####################################
    #---------------------------------------------------
    nextarr_hr_ar_avg = sum(i for i in nextarr_hr_ar) / len(nextarr_hr_ar)
#    print('nextarr_hr_ar = ', nextarr_hr_ar)
#    print('nextarr_hr_ar_avg = ', nextarr_hr_ar_avg)
#    print()
    #---------------------------------------------------
    #------------------------------------------------------------
    nextdepmin_hr_ar_avg = (sum(i for i in nextdepmin_hr_ar) 
                                / len(nextdepmin_hr_ar))
#    print('nextdepmin_hr_ar = ', nextdepmin_hr_ar)
#    print('nextdepmin_hr_ar_avg = ', nextdepmin_hr_ar_avg)
#    print()
    #--------------------------------------------------------------
#print('########################')
#print('###### END PROGRAM #####')
#print('########################')
#print()
