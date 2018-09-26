# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 15:21:44 2017

@author: Derek
"""

from __future__ import print_function
from __future__ import division
import random
import math

def getrand(lambdar):
    exporand = -math.log(1.0 - random.random()) / lambdar
    return (exporand)

def arrtime(tnow):
    mean = 0.25 #avg time b/t arr in hrs - i.e. .25 hrs b/t arr = 15 min
    lambdar = 1/mean #arr RATE per hr -> 1/.25 = 4 - i.e. 4 per hr
    exporand = getrand(lambdar) #time till next arr in addittional hrs
    exporandmin = exporand * 60 #time till next arr in additional min
#    print('arr exporandmin =', exporandmin)
    nextarr = tnow + exporandmin
#    print('nextarr =', nextarr)
#    print()
    return(nextarr)

def deptime(tnow):
    mean = 0.2
    lambdar = 1/mean
    exporand = getrand(lambdar)
    exporandmin = exporand * 60
#    print('dept exporandmin =', exporandmin)
    nextdep = tnow + exporandmin
#    print('nextdep =', nextdep)
#    print()
    return(nextdep)

######
# main
######

tmax = 9600 #max time to end program in minutes   #9600
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
        else:
            cumutil = cumutil
        if q > 0:
            waittime = waittime + (q * (tnow - told))
        else:
            waittime = waittime
        if util == 1:
            cumsystime = cumsystime + ((util + q) * (tnow - told))
        else:
            cumsystime = cumsystime
        if tnow == nextarr:
            cumarr += 1
        else:
            cumarr = cumarr

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
        else:
            cumutil = cumutil
        if q > 0:
            waittime = waittime + (q * (tnow - told))
        else:
            waittime = waittime
        if util == 1:
            cumsystime = cumsystime + ((util + q) * (tnow - told))
        else:
            cumsystime = cumsystime
        if tnow == nextarr:
            cumarr += 1
        else:
            cumarr = cumarr
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

print('waittime =', waittime)
print('cumutil =', cumutil)
print('cumsystime = ', cumsystime)
print('cumarr = ', cumarr)
print()

avgqtime = waittime / cumarr
avgsystime = cumsystime / cumarr
avgqlen = waittime / tnow
avgutil = cumutil / tnow

print('The avg time in the q was ', avgqtime)
print('The avg time in the Sys was ', avgsystime)
print('The length of the q was ', avgqlen)
print('The avg utilization was ', avgutil)


#print('########################')
#print('###### END PROGRAM #####')
#print('########################')
#print()

