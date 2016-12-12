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

## TODO: merge eclipsing binary sources
print "eclipsing binaries . . . "
eclipsing = pd.read_table("data/eclipsing_binary.txt",header=None,sep="\t",
                     skiprows=4,skipinitialspace=True)

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
