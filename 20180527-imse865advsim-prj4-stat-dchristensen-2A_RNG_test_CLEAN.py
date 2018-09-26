        # -*- coding: utf-8 -*-
"""
Created on Wed Jun 06 15:21:44 2017

@author: Derek Christensen
"""

from __future__ import print_function
from __future__ import division
#import random
import math
#import scipy.stats as stats
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
#    arrfuncrand = -math.log(1.0 - arrlcg()) / arrlambda #convert Uni to Func
    
    arr364x2rand = 4 * (arrlcg())**(1/3)
    
    #---------------------------
#    print()
#    print('arr364x2rand = ', arr364x2rand)
#    print()
    #-----------------------------
    
    return (arr364x2rand) #returns time till next arr in additional hours

### Inter-arrival time dist Linear Congruential Generator (LCG) 
def arrlcg():
    a = 100801   #the multiplier
    c = 103319   #the increment
    m = 193723   #the modulus
    global curarrseed  #current Z value (seed)
    curarrseed = (a*curarrseed + c) % m  #calcualtion of next arr Z value
    arrlcgnum = curarrseed / m  #calculation of Uniform value
    
    #---------------------------------
#    print()
#    print('arrlcgnum = ', arrlcgnum)
#    print()
    #----------------------------------
    
    return(arrlcgnum)   #Uniform value returned to distribution converter

################################
### SERVICE TIME DIST. FUNCTIONS
################################

### service time determination 
def deptime(tnow):
    depmean = 2 #avg service time in hrs - i.e. 2 hrs to service = 120 min
    depsigma = 0.25
#    depmu = 1/depmean  #service RATE per hr
#                         # 1/2 of a unit will be served per hr
    depmu = depmean
    normrand = depgetrand(depmu, depsigma) #time for next serv in add hrs
    print('normrand = ', normrand)
    normrandmin = normrand * 60 #time for necxt service in additional min
    print('normrandmin = ', normrandmin)
    print('tnow = ', tnow)
    normrandmin_ar.append(normrandmin)
    nextdep = tnow + normrandmin #system clock time calc for next departure
    print('nextdep = ', nextdep)
    print()
    return(nextdep) #returns system clock time for next departure

### calculates time till next departure in hours
### random number convertor from Uniform into Normal
def depgetrand(depmu, depsigma):
#    depnormrand = -math.log(1.0 - deplcg()) / depmu #convert Uni to Norm
    u1 = 0
    u2 = 0
    w = 0
    
#    deplcg(u1, u2)
    u1, u2 = deplcg()
    v1 = (2*u1) - 1
    v2 = (2*u2) - 1
    w = v1**2 + v2**2
#    print('u1 = ', u1)
#    print('u2 = ', u2)
#    print('v1 = ', v1)
#    print('v2 = ', v2)
#    print('w = ', w)
    if w > 1:
#        print('bad w = ', w)
        return depgetrand(depmu, depsigma)  #recursive call
    Y = math.sqrt( (-2) * ( ( math.log(w) ) / w ) )
    X1 = v1*Y
#    X2 = v2*Y
    depnormrand1 = depmu + depsigma*X1
#    print('Y = ', Y)
#    print('X1 = ', X1)
#    print('depmu = ', depmu)
#    print('depsigma = ', depsigma)
#    print('depnormrand1 = ', depnormrand1)
#    print('depnormrand1 * 60 = ', depnormrand1*60)
#    print()
    
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
#    print('new curdepseed = ', curdepseed)
    origdepseed_ar.append(curdepseed)
    u2 = curdepseed / m  #calculation of Uniform value #2
    
    return(u1, u2)   #Uniform value returned to distribution converter

######
# main
######
if __name__ == '__main__':
#    print('line number ', lineno())
    
    global origarrseed
    global origdepseed
    
    origarrseed = 50001
    origdepseed = 94907
    
    origdepseed_ar = []
    origdepseed_ar.append(origdepseed)
#    print('origdepseed = ', origdepseed)
    
    global curarrseed  #current seed for inter-arrival dist.
    global curdepseed  #current seed for service time dist.
    
    curarrseed = origarrseed  #inital Z(0) seed for inter-arrival dist.
    curdepseed = origdepseed  #inital Z(0) seed for service time dist.
    
    #-------------------------
    nextarr_hr_ar = []
    #-------------------------
    
    #-------------------------
    nextdep_hr_ar = []
    #-------------------------
    normrandmin_ar = []
    
    ############
    # start reps
    ############
    
    numreps = 2
    for rep in range (0,numreps):
        print()
        print('(---------------rep = ', rep+1,'--------------)')
        hours = 20
        tmax = hours * 60 #max time to end program in minutes   #9600
        told = 0 #the most recent current time in minutes
        tnow = 0 #the current time in minutes
        
#        print('curarrseed = ', curarrseed)
#        print('curdepseed = ', curdepseed)
        
        #-------------------------
        nextarr_ar = []
        nextarr_ar.append(0)
        nextarr_sum = 0
        nextarr_avg = 0
        #-------------------------
        
        #-------------------------
        nextdep_ar = []
        nextdep_ar.append(0)
        nextdep_sum = 0
        nextdep_avg = 0
        #-------------------------
    
        nextdep = 1000000000 #set nextdep to a Big M time in minutes    
        nextarr = arrtime(tnow)
        
        #---------------------------
        nextarr_ar.append(nextarr)
        #---------------------------
        
    #    print('curarrseed = ', curarrseed)
        
        while tnow < tmax:   #while the current time < max time run while loop    
            if nextarr < nextdep:
                tnow = nextarr
#                if tnow == nextarr:
                nextdep = deptime(tnow) #put in serv -> now determine dep time
                
#                print('nextdep = ', nextdep)
#                print('tnow = ', tnow)
#                print()
#                print('tnow - nextdep = ', nextdep-tnow)
#                print()
                
                #---------------------------
                nextdep_ar.append(nextdep)
                #---------------------------
    
                nextarr = arrtime(tnow)
                #---------------------------
                nextarr_ar.append(nextarr)
                #---------------------------
    #            print('curarrseed = ', curarrseed)
                told = tnow
                
            else:
                tnow = nextdep
#                if tnow == nextarr:
                nextdep = deptime(tnow)
                #---------------------------
                nextdep_ar.append(nextdep)
                #---------------------------
    #            else:
                nextdep = 1000000000
                told = tnow
                
        #--------------------------------------------
#        print('tnow = ', tnow)
#        print('curarrseed = ', curarrseed)
#        print('curdepseed = ', curdepseed)
#        print()
        #-------------------------------------------- 
        
#        print('nextarr_ar = ', nextarr_ar)
#        print()
#        print('nextarr_ar length = ', (len(nextarr_ar)-1))
                
        #nextarr_sum = sum(i for i in nextarr_ar)
        nextarr_sum = sum([t - s for s, t in zip(nextarr_ar, nextarr_ar[1:])])
        nextarr_avg = nextarr_sum / (len(nextarr_ar)-1)
        nextarr_hr = 0        
        nextarr_hr = nextarr_avg / 60        
        nextarr_hr_ar.append(nextarr_hr)
        
#        print('nextarr_sum = ', nextarr_sum)
#        print('nextarr_avg = ', nextarr_avg)
#        print()
        #--------------------------------------------
        
        print('nextdep_ar = ', nextdep_ar)
        print()
        print(*nextdep_ar, sep = '\n')
        print()
        print('nextdep_ar length = ', (len(nextdep_ar)-1))
        
        #nextarr_sum = sum(i for i in nextarr_ar)
        nextdep_sum = sum([t - s for s, t in zip(nextdep_ar, nextdep_ar[1:])])
        
#        newsumnextdep_ar = 0
#        print('newsumnextdep_ar = ', newsumnextdep_ar)
#        for i in range(0,len(nextdep_ar)):
#            print('nextdep_ar[',i,'] = ', nextdep_ar[i])
#            newsumnextdep_ar += nextdep_ar[i]
#            print('newsumnextdep_ar = ', newsumnextdep_ar)
               
        nextdep_avg = nextdep_sum / (len(nextdep_ar)-1)
        nextdep_hr = 0
        nextdep_hr = nextdep_avg / 60
        nextdep_hr_ar.append(nextdep_hr)
        
        print('nextdep_sum = ', nextdep_sum)
        print('nextdep_avg = ', nextdep_avg)
        print('nextdep_hr = ', nextdep_hr)
        print()
        
        #-------------------------------------------
        
    nextarr_hr_ar_avg = sum(i for i in nextarr_hr_ar) / len(nextarr_hr_ar)
    #nextarr_sum = sum(i for i in nextarr_ar)
    
#    print('nextarr_hr_ar = ', nextarr_hr_ar)
##    print(nextarr_hr_ar)
#    print()
#    print('nextarr_hr_ar_avg = ', nextarr_hr_ar_avg)
#    print()
    #--------------------------------------------
    
    nextdep_hr_ar_avg = sum(i for i in nextdep_hr_ar) / len(nextdep_hr_ar)
    #nextarr_sum = sum(i for i in nextarr_ar)
    
    print('nextdep_hr_ar = ', nextdep_hr_ar)
#    print(nextdep_hr_ar)
    print()
    print('nextdep_hr_ar_avg = ', nextdep_hr_ar_avg)
    print()
#    print()
#    print('normrandmin_ar = ', normrandmin_ar)
#    print()
#    print(*normrandmin_ar, sep = '\n')
#    print()
    #--------------------------------------------
    
#    origdepseed_ar = [int(i) for i in origdepseed_ar]
#    print('origdepseed_ar = ', origdepseed_ar)
#    print()
#    print(*origdepseed_ar, sep = '\n')
    
    
    #print('########################')
    #print('###### END PROGRAM #####')
    #print('########################')
    #print()
    
