# -*- coding: utf-8 -*-
"""
Created on Tue May 29 02:53:13 2018

@author: Derek Christensen
"""
from __future__ import print_function
from __future__ import division
#import random
import math

def arrgetrand(arrrate):
    arrexporand = -math.log(1.0 - arrlcg()) / arrrate
    return (arrexporand)

def arrlcg():
    a = 100801
    c = 103319
    m = 193723
    global curarrseed
    
    curarrseed = (a*curarrseed + c) % m
    
    arrlcgnum = curarrseed / m

    return(arrlcgnum)
    
def depgetrand(deprate):
    depexporand = -math.log(1.0 - deplcg()) / deprate
    return (depexporand)

def deplcg():
    a = 7000313
    c = 0
    m = 9004091
    global curdepseed
    
    curdepseed = (a*curdepseed + c) % m
    
    deplcgnum = curdepseed / m

    return(deplcgnum)
    
######
# main
######

arrtimes = []
deptimes = []

reparr = []
repdep = []

origarrseed = 50001
origdepseed = 94907

global curarrseed
global curdepseed

curarrseed = 50001
curdepseed = 94907

numreps = 3
for rep in range(0,numreps):
    
    sumarr = 0
    sumdep = 0
    avgarr = 0
    avgdep = 0
    
    arrmean = 3
    arrrate = 1/arrmean
    
    depmean = 2
    deprate = 1/depmean
    
    print('arrivals')
    arrnumreps = 10
    for i in range(arrnumreps):
        arrexporand = arrgetrand(arrrate)
        print(arrexporand)
        arrtimes.append(arrexporand)
        sumarr += arrexporand
    
    print('departures')
    depnumreps = 10
    for j in range(depnumreps):
        depexporand = depgetrand(deprate)
        print(depexporand)
        deptimes.append(depexporand)
        sumdep += depexporand
        
    avgarr = sumarr / arrnumreps
    avgdep = sumdep / depnumreps
    
    reparr.append(avgarr)
    repdep.append(avgdep)
    
    print()
    print('arrtimes =', arrtimes)
    print()
    
    print()
    print('deptimes =', deptimes)
    print()
    
    print()
    print('reparr =', reparr)
    print()
    
    print()
    print('repdep =', repdep)
    print() 
