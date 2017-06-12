## python wrapper for fit_template.R
## by james long
import numpy as np
import rpy2.robjects as robjects
from rpy2.robjects.vectors import IntVector, FloatVector, StrVector
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import itertools

## set up rpy2 so we can call R functions
r=robjects.r
r.source("fit_template.R")
r.load("template.RData") ## loads r.tem, see later code for usage
FitTemplate=robjects.r['FitTemplate']
ComputeCoeffs=robjects.r['ComputeCoeffs']

## load a light curve, put in nice format
fname="LC_999886.dat"
with open(fname) as csvf:
    f = csv.reader(csvf,delimiter=' ')
    time, band, mag, error = zip(*f)


no_pound = [not '#' in x for x in time]    
time = list(itertools.compress(time, no_pound))
band = list(itertools.compress(band, no_pound))
mag = list(itertools.compress(mag, no_pound))
error = list(itertools.compress(error, no_pound))





time = np.array(time,dtype='float64')
time = time - np.min(time) ## => time=0 is first observation
mag = np.array(mag,dtype='float64')
error = np.array(error,dtype='float64')


## create R dataframe using time,band,mag,error
lc = robjects.r['TBMEtoLC'](FloatVector(time),StrVector(band),FloatVector(mag),FloatVector(error))



# ###### fit model to lc
# ## choose frequency grid
# omegas=FloatVector(np.arange(start=1.0,stop=5.0,step=0.1/4000.0))
# ## compute rss (residual sum of squares) for each frequency, takes a minute
# rss=FitTemplate(lc,omegas,r.tem)
# ## select best fitting period, ie lowest rss
# omega = omegas[np.argmin(rss)] ## best fit frequency
# pest=1.0/omega ## best fit period
# coeffs=ComputeCoeffs(lc,omega,r.tem) ## parameter estimates of best fit frequency
# ## the output is [distance modulus (mu),amount of dust (E[B-V]),amplitude (a),phase (rho)]
# # >>> coeffs
# # R object with classes: ('numeric',) mapped to:
# # <FloatVector - Python:0x7fe29e3d4a08 / R:0x416c888>
# # [16.097936, 0.102392, 0.274502, 0.232388]

# ###### now plot results
# ## plot lightcurve folded on estimated period
# cols = {'g': 'green', 'i': 'red', 'r':'blue','u': 'orange', 'z': 'yellow'}
# pts=plt.scatter(np.mod(time,pest),mag,color=list(map(cols.get,band)))
# plt.gca().invert_yaxis()
# plt.xlim([0,pest])
# class_colours = list(map(cols.get,band))
# recs = []
# for i in range(0,len(class_colours)):
#     recs.append(mpatches.Rectangle((0,0),1,1,fc=class_colours[i]))

# plt.legend(recs,cols.keys(),loc=4)

# ### add template fits
# gamma = r.tem[2]
# gamma = np.resize(gamma,(5,100))
# t=(np.arange(100)/100.)*pest
# ords=np.argsort((t - coeffs[3]*pest) % pest)
# for ii in np.arange(gamma.shape[0]):
#     m=coeffs[0] + r.tem[0][ii] + r.tem[1][ii]*coeffs[1] + coeffs[2]*gamma[ii,:]
#     plt.plot(t,m[ords],'k',color=cols[r.tem[0].names[ii]])


# plt.show()










######## plot unfolded (raw light curve)


## plot lightcurve folded on estimated period
cols = {'g': 'green', 'i': 'red', 'r':'blue','u': 'orange', 'z': 'yellow'}
pts=plt.scatter(time,mag,color=list(map(cols.get,band)))
plt.gca().invert_yaxis()
plt.xlim([0,np.max(time)])
class_colours = list(map(cols.get,band))
recs = []
for i in range(0,len(class_colours)):
    recs.append(mpatches.Rectangle((0,0),1,1,fc=class_colours[i]))

plt.legend(recs,cols.keys(),loc=4)

#plt.show()


pylab.savefig('foo.pdf')
