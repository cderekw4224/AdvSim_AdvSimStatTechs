# AdvSimPrj4_AdvSimStatTechs

Projects

This  project  is  to  help  you  explore  various  advanced  aspects  of  simulation  and  output  analysis.    This  is  all  using  an  1  server  queue.  

For  any  arrival  create  a  linear  congruential  generator  for  your  random  number  generator.    Let  the  prime  numbers  a=100801,  c=103319  and  m=193723.    As  a  starting  seed,  use  50,001  for  the  arrivals.    All  simulations  should  start  this  way.  

For  any  service  time  create  a  congruential  generator  for  your  random  number  generator.    Let  the  prime  numbers  a=7,000,313  and  m=9,004,091.    As  a  starting  seed,  use  94,907.    All  simulations  should  start  this  way.  

1.  Create  an  M/M/1  with  a  arrival  rate  of  exponential  with  an  arrival  rate  of  1/3  per  hour  and  a  service  rate  of  ½  per  hour.  Run  this  for  30  replications  each  for  500  hours.    You  can  either  do  this  for  utilization  or  expected  number  of  people  in  line.    Your  choice.  
a. Perform  a  t-Test  to  determine  whether  or  not  there  is  a  statistical  difference  between  the  simulated  data  and  the  expected  value.    Also  find  the  confidence  interval.      
b. Repeat  this  entire  process  for  40  repetitions  (1200  runs)  and  find  all  95%  confidence  intervals.    Determine  how  many  of  these  95%  confidence  intervals  do  not  contain  the  theoretical  mean.    
c. Redo  part  a  and  b,  but  give  yourself  100  hours  of  warm  up.      
d. Run  a  batch  means  by  running  the  simulation  for  15,000  hours  and  divide  the  data  into  500  hours.    Compare  the  difference  between  a  and  d.  
e. Run  antithetic  pairing  on  part  a  and  compare  confidence  intervals  and  standard  deviation  to  determine  if  there  is  variance  reduction.  
f. Run  this  simulation  for  1000  regenerative  cycles  and  report  the  average  time  and  confidence  interval  of  the  length  of  the  regenerative  cycle.  

2. Create  a  G/G/1  queue  with  an  arrival  distribution  of  3/64  x2  between  0  and  4  and  0  else.  Run  this  for  30  replications  each  for  500  hours.    You  can  either  do  this  for  utilization  or  expected  number  of  people  in  line.    Note  it’s  mean  is  3.    Let  the  service  distribution  be  a  normal  (2,.25).    You  need  to  generate  these  and  cannot  have  software  generate  them  for  you.      
a. Use  seeds  50001  for  arrivals  and  94907  for  service  times.    Perform  a  t-Test  to  determine  whether  or  not  there  is  a  statistical  difference  between  the  simulated  data  and  1  a.    Also  find  the  confidence  interval.      
b. Repeat  this  entire  process  for  40  repetitions  and  find  all  95%  confidence  intervals.    Determine  how  many  of  these  95%  confidence  intervals  do  not  contain  the  theoretical  mean  from  part  1.      Observe  that  both  1  and  2  have  the  same  average  performance.  
c. Use  CRN  as  a  VRT  (revert  to  previous  seeds).    Compare  the  variances  between  1a  and  2a  to  determine  if  there  is  variance  reduction.  
d. Run  this  simulation  for  1000  regenerative  cycles  and  report  the  average  time  and  confidence  interval  of  the  regenerative  cycle.  

3. Compare  both  1  and  2  and  determine  the  variances  of  all  distributions.    Comment  on  the  importance  of  the  variance  in  the  simulations.  

Report  all  of  this  in  a  technical  report. 
