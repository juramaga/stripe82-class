import numpy as np
import pandas as pd
import os

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


## output catalog
print "writing catalog . . ."
data.to_csv(outfile,sep=" ",index=False)
