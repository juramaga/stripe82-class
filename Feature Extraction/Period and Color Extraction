import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gatspy import periodic

#Converting to csv format
a = 'folder' #folder containing lightcurve data in '.dat' format
for filename in os.listdir(a):
       infilename = os.path.join(a,filename)
       if not os.path.isfile(infilename): continue
       oldbase = os.path.splitext(filename)
       newname = infilename.replace('.dat', '.csv')
       output = os.rename(infilename, newname)


df = pd.read_csv('LC_13350.csv',  header=None,sep=' ') #Load your light curve file as a csv
#Cleaning the data
df = df[df.ix[:,2] >= 0] 
df = df[~df.ix[:,0].str.contains("#")]
df.columns = ['Time','Band','Magnitude','Error'] #Adding column names
df.head()

#Color Extraction
grouped = df.groupby('Band')
grouped.size()
df2 = grouped.mean() #mean values of band magnitudes and their errors
df2


# ### Method-1: Calculating u-g,g-r,r-i,i-z as colors
# #### Reference: http://cas.sdss.org/dr2/en/proj/basic/color/definition.asp

ug = df2.ix[3].subtract(df2.ix[0])
gr = df2.ix[0].subtract(df2.ix[2])
ri = df2.ix[2].subtract(df2.ix[1])
iz = df2.ix[1].subtract(df2.ix[4])
print ug,gr,ri,iz


# ### Method-2: The band with lowest mean magnitude (highest brightness)
# #### Reference: http://skyserver.sdss.org/dr1/en/proj/advanced/color/sdssfilters.asp

df2['Wavelength in Angstroms'] = ['4770','7625','6231','3543','9134']
df2['Magnitude'].argmin() 

fig = plt.figure(figsize=(14, 5))
gs = plt.GridSpec(4, 3, left=0.10, right=0.95, bottom=0.15,
                  wspace=0.3, hspace=0.6)
ax = [fig.add_subplot(gs[:, 0])]

ax[0].errorbar(df2.ix[:,2], df2.ix[:,0], yerr=df2.ix[:,1],fmt='.')
ax[0].set_ylim(19.5, 17.6)
ax[0].set_xlabel('Band Wavelength')
ax[0].set_ylabel('Band Magnitude')
plt.show()


#Period estimation for a single lightcurve file 
time = map(float,df.ix[:,0].values) 
mags = map(float,df.ix[:,2].values)
dmags = map(float,df.ix[:,3].values)
filters = df.ix[:,1].values


#sys.stdout = open(os.devnull,"w") #To prevent printing intermediate results by in-built functions
ls = periodic.LombScargleMultiband(fit_period=True); #For finding periodicity in irregularly sampled multiband data
ls.optimizer.period_range = (0.2, 1.0)
ls.fit(time,mags,dmags,filters)
period = ls.best_period
#sys.stdout = sys.__stdout__
print period 

#Plotting the folded light curves for each band
fig = plt.figure(figsize=(14, 5))
gs = plt.GridSpec(5, 2, left=0.10, right=0.95, bottom=0.15,
                  wspace=0.3, hspace=0.6)
ax = [fig.add_subplot(gs[:, 0])]

for band, mask in zip('ugriz', masks):
    ax[0].errorbar(foldTimes[mask], mags[mask], yerr=dmags[mask],fmt='.',label=band)

ax[0].set_ylim(20, 17)
ax[0].legend(loc='lower right', fontsize=8, ncol=3)
ax[0].set_title('Folded Data', fontsize=12)
ax[0].set_xlabel('phase')
ax[0].set_ylabel('magnitude')
plt.show()
