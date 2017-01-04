### input: data/stripe82candidateVar_v1.1.dat
### output: outfile, same as input but with extra column for classes
### by James Long

import numpy as np
import pandas as pd
import os
from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt

outfile = "catalog.txt"
try:
    os.remove(outfile)
except OSError:
    pass

## read in data
print "loading catalog . . ."
data = pd.read_table("data/stripe82candidateVar_v1.1.dat",header=None,sep=" ",
                     skiprows=42,skipinitialspace=True)
del data[17]
data.columns = ["ID","ra","dec","P","r","ug","gr","ri","iz","gN","gAmpl","rN","rAmpl","iN","iAmpl","zQSO","MiQSO"]
data['cl'] = "unknown"

## QSOs have redshift estimates > 0
print "QSO . . . "
data['cl'][data['zQSO'] > 0.0] = "QSO"

## merge RR Lyrae from sesar 2010
print "rrlyrae . . . "
rrlyrae = pd.read_table("data/rrlyrae.txt",header=None,sep=" ",
                     skiprows=42,skipinitialspace=True)
rrlyrae = rrlyrae[[0,1]]
rrlyrae.columns = ["ID","classrr"]
rrlyrae['classrr'] = ['rr_' + s for s in rrlyrae['classrr']]
data = pd.merge(data,rrlyrae,on='ID',how='left')
ix = np.invert(pd.isnull(data['classrr']))
data['cl'][ix] = data['classrr'][ix]
del data['classrr']

<<<<<<< HEAD
## merge high-amplitude delta scuti stars from Suveges et al. 2012
print "HADS . . . "
hads = pd.read_table("data/delta_scuti.txt",header=None,sep=" ",
                     skiprows=75,skipinitialspace=True)
hads = hads[[1]]
hads.columns = ["ID"]
hads['classdscu'] = pd.Series(['del_scu' for x in range(len(hads.index))])
data = pd.merge(data,hads,on='ID',how='left')
ix = np.invert(pd.isnull(data['classdscu']))
data['cl'][ix] = data['classdscu'][ix]
del data['classdscu']

## merge RR Lyr from Suveges et al. 2012
print "More RR lyrae . . . "
rr_suve = pd.read_table("data/more_rrlyrae_suveges.txt",header=None,sep=" ",
                     skiprows=77,skipinitialspace=True)
rr_suve = rr_suve[[2,5]]
rr_suve.columns = ["ID","classrrsuv"]
rr_suve["ID"] = pd.Series([int(x) for x in rr_suve["ID"]])
data = pd.merge(data,rr_suve,on='ID',how='left')
ix = np.invert(pd.isnull(data['classrrsuv']))
data['cl'][ix] = data['classrrsuv'][ix]
del data['classrrsuv']

## merge Double-mode RR Lyr, multiperiodic RR Lyrae candidates and multiperiodic HADS delta scuti stars from Suveges et al. 2012
print "More RR lyrae and HADS . . . "
rrhads = pd.read_table("data/rrlyrae_suveges.txt",header=None,sep=" ",
                     skiprows=73,skipinitialspace=True)
rrhads = rrhads[[1,4]]
rrhads.columns = ["ID","classrrhads"]
data = pd.merge(data,rrhads,on='ID',how='left')
ix = np.invert(pd.isnull(data['classrrhads']))
data['cl'][ix] = data['classrrhads'][ix]
del data['classrrhads']


## merge eclipsing binary sources
=======
>>>>>>> 6c3ed831966d047660cbd6f9dab613e3b23de32b
print "eclipsing binaries . . . "
eclipsing = pd.read_table("data/eclipsing_binary.txt",engine="python",
                          header=None,sep="\t",
                          skiprows=4,skipfooter=2,skipinitialspace=True)

ra = []
dec =[]
for i in np.arange(len(eclipsing[0])):
    coord = eclipsing[0][i][6:]
    h = coord[0:2]
    m = coord[2:4]
    s = coord[4:9]
    de = coord[9:12]
    mi = coord[12:14]
    se = coord[14:]
    coordi = h+" "+m+" "+s+" "+de+" "+mi+" "+se
    c = SkyCoord(coordi, unit=(u.hourangle, u.deg))
    #print c.ra.degree,c.dec.degree
    ra.append(c.ra.degree)
    dec.append(c.dec.degree)

c1 = SkyCoord(ra=ra*u.degree, dec=dec*u.degree)
catalog = SkyCoord(ra=np.array(data['ra'])*u.degree, dec=np.array(data['dec'])*u.degree)

idx, d2d, d3d = c1.match_to_catalog_sky(catalog)
idy =  np.where(np.log10(d2d.arcsec) < 0)

eclipsing_new = {'ra': np.array(data['ra'])[idx[idy]], 'dec': np.array(data['dec'])[idx[idy]], 'classecl':np.array(eclipsing[4])[idy]}
eclipsing_new = pd.DataFrame(data=eclipsing_new)

#print eclipsing_new
data = pd.merge(data,eclipsing_new,on=['ra','dec'],how='left')
ix = np.invert(pd.isnull(data['classecl']))
data['cl'][ix] = data['classecl'][ix]
del data['classecl']

## output catalog
print "writing catalog . . ."
data.to_csv(outfile,sep=" ",index=False)
