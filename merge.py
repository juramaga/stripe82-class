import numpy as np
import pandas as pd

## read in data
data = pd.read_table("data/stripe82candidateVar_v1.1.dat",header=None,sep=" ",
                     skiprows=42,skipinitialspace=True)
del data[17]
data.columns = ["ID","ra","dec","P","r","ug","gr","ri","iz","gN","gAmpl","rN","rAmpl","iN","iAmpl","zQSO","MiQSO"]
data['cl'] = "unknown"

## QSOs have redshift estimates > 0
data['cl'][data['zQSO'] > 0.0] = "QSO"

## merge RR Lyrae from sesar 2010
rrlyrae = pd.read_table("data/rrlyrae.txt",header=None,sep=" ",
                     skiprows=42,skipinitialspace=True)
rrlyrae = rrlyrae[[0,1]]
rrlyrae.columns = ["ID","classrr"]
rrlyrae['classrr'] = ['rr_' + s for s in rrlyrae['classrr']]
data = pd.merge(data,rrlyrae,on='ID',how='left')
ix = np.invert(pd.isnull(data['classrr']))
data['cl'][ix] = data['classrr'][ix]
data['cl'][data['classrr']!=NA] <- dat$classrr[!is.na(dat$classrr)]
del data['classrr']

## TODO: merge eclipsing binary sources


## output catalog
data.to_csv("catalog.txt",sep=" ",index=False)
