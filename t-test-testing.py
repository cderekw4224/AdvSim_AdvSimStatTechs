# -*- coding: utf-8 -*-
"""
Created on Tue May 29 22:26:46 2018

@author: Derek Christensen
"""

from __future__ import print_function
from __future__ import division
import random
import math

#import numpy as np
#import pandas as pd
import scipy.stats as stats
#import matplotlib.pyplot as plt
#import random
#import math

arrmean = 3
arrlambda = 1/arrmean

depmean = 2 #avg service time in hrs - i.e. 2 hrs to service = 120 min
depmu = 1/depmean 

alpha = 0.10
tparam1 = 1 - (alpha/2)
conflvl = 1-alpha
#df = m+n-2

expecutil = arrlambda / depmu

expeclenq = (arrlambda/depmu)**2 / (1 - (arrlambda/depmu))

print('expecutil = ', expecutil)
print('expeclenq = ', expeclenq)



t_critical = stats.t.ppf(q = 0.95, df=29)  # Get the t-critical value*

print("t-critical value:")                  # Check the t-critical value
print(t_critical)                        

#sample_stdev = sample.std()    # Get the sample standard deviation
#
#sigma = sample_stdev/math.sqrt(sample_size)  # Standard deviation estimate
#margin_of_error = t_critical * sigma
#
#confidence_interval = (sample_mean - margin_of_error,
#                       sample_mean + margin_of_error)  
#
#print("Confidence interval:")
#print(confidence_interval)