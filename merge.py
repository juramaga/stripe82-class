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
data['Cat_P'] = 'n/a' #Catalina Period
data['Cat_mag'] = 'n/a' #Catalina V magnitude

############################BEGINNING OF CATALINA MERGER##########################################
# merge catalina catalog 
print "merging catalina catalog . . . "
#creates a nice data array
catalina = pd.read_table("data-controlled/catalina-catalog-converted.txt",
                       header=1,delim_whitespace=True,
                       skipinitialspace=True,comment="#",names=['Catalina_Surveys_ID','Numerical_ID','ra',
                             'dec','V_(mag)','Period_(days)','Amplitude','Number_Obs','Var_Type','ra_deg','dec_deg'])

#create the catalina coordinate list
c1 = SkyCoord(ra = catalina['ra_deg'], dec=catalina['dec_deg'], unit=(u.degree,u.degree))

#create the stripe-82 coordinate list
catalog = SkyCoord(ra=np.array(data['ra'])*u.degree, dec=np.array(data['dec'])*u.degree)

data['g'] = data['gr'] + data['r'] 
data['v'] = data['g'] - 0.5784*data['gr'] - 0.0038

#compare the two
idx, d2d, d3d = c1.match_to_catalog_sky(catalog)
#eliminates all matches that have too big of a separation
idy =  np.where((d2d.arcsec) < 1.5) ####make error check####

#this was included in the code
#I merely modified it for the catalina catalog
catalina_new = {'ra': np.array(data['ra'])[idx[idy]], 'dec': np.array(data['dec'])[idx[idy]], 
                'classecl':np.array(catalina['Var_Type'])[idy], 'cat_p':np.array(catalina['Period_(days)'])[idy],
                'v_mag':np.array(catalina['V_(mag)'])[idy]}
catalina_new = pd.DataFrame(data=catalina_new)

#add the new data to the old catalog
data = pd.merge(data,catalina_new,on=['ra','dec'],how='left')
ix = np.invert(pd.isnull(data['classecl']))
data['cl'][ix] = data['classecl'][ix]
data['Cat_P'][ix] = data['cat_p'][ix]
data['Cat_mag'][ix] = data['v_mag'][ix]
del data['classecl']
del data['cat_p']
del data['v_mag']

###Most types found in https://www.aavso.org/vsx/index.php?view=about.vartypes
data['temp_cl'] = ''
data['temp_cl'].loc[data['cl']=='unknown']='unknown'
data['temp_cl'].loc[data['cl']==1]='ew' #W Ursae Majoris-type eclipsing variables
data['temp_cl'].loc[data['cl']==2]='ea' #beta Persei-type (Algol) eclipsing systems
data['temp_cl'].loc[data['cl']==3]='eb' #beta Lyrae-type eclipsing systems
data['temp_cl'].loc[data['cl']==4]='rr_ab' #RR Lyrae variables with asymmetric light curves
data['temp_cl'].loc[data['cl']==5]='rr_c' #RR Lyrae variables with nearly symmetric
data['temp_cl'].loc[data['cl']==6]='rr_d' #Double-mode RR Lyrae stars which pulsate...
data['temp_cl'].loc[data['cl']==7]='bl' #RR Lyrae stars showing the Blazhko effect.
data['temp_cl'].loc[data['cl']==8]='rs' #non-eclipsing RS CVn stars
data['temp_cl'].loc[data['cl']==9]='acep' #Anomalous Cepheids
data['temp_cl'].loc[data['cl']==10]='cep-ii' ####need to confirm which star this is...
data['temp_cl'].loc[data['cl']==11]='hads' #High Amplitude delta Scuti stars
data['temp_cl'].loc[data['cl']==12]='lads'
data['temp_cl'].loc[data['cl']==13]='lpv' #Long Period Variables 
data['temp_cl'].loc[data['cl']==14]='ell' #ellipsoidal binary system
data['temp_cl'].loc[data['cl']==15]='hump' ####????
data['temp_cl'].loc[data['cl']==16]='pceb' #post common envelope binary planetary system
data['temp_cl'].loc[data['cl']==17]='ea_up' ####????

data['cl'] = data['temp_cl']
del data['temp_cl']

#######################################END OF CATALINA MERGER#####################################

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

## merge high-amplitude delta scuti stars from Suveges et al. 2012
print "HADS . . . "
hads = pd.read_table("data-controlled/delta_scuti.txt",header=None,delim_whitespace=True,
                     skipinitialspace=True,comment="#")
#hads = pd.read_table("data-controlled/delta_scuti.txt",header=None,sep=" ",skiprows=75,skipinitialspace=True)
hads = hads[[1]]
hads.columns = ["ID"]
hads['classdscu'] = pd.Series(['del_scu' for x in range(len(hads.index))])
data = pd.merge(data,hads,on='ID',how='left')
ix = np.invert(pd.isnull(data['classdscu']))
data['cl'][ix] = data['classdscu'][ix]
del data['classdscu']

## merge RR Lyr from Suveges et al. 2012
print "More RR lyrae . . . "
rr_suve = pd.read_table("data-controlled/more_rrlyrae_suveges.txt",
                        header=None,delim_whitespace=True,
                        skipinitialspace=True,comment="#")
rr_suve = rr_suve[[2,5]]
rr_suve.columns = ["ID","classrrsuv"]
rr_suve["ID"] = pd.Series([int(x) for x in rr_suve["ID"]])
data = pd.merge(data,rr_suve,on='ID',how='left')
ix = np.invert(pd.isnull(data['classrrsuv']))
data['cl'][ix] = data['classrrsuv'][ix]
del data['classrrsuv']

## merge Double-mode RR Lyr, multiperiodic RR Lyrae candidates and multiperiodic HADS delta scuti stars from Suveges et al. 2012
print "More RR lyrae and HADS . . . "
rrhads = pd.read_table("data-controlled/rrlyrae_suveges.txt",
                       header=None,delim_whitespace=True,
                       skipinitialspace=True,comment="#")
rrhads = rrhads[[1,4]]
rrhads.columns = ["ID","classrrhads"]
data = pd.merge(data,rrhads,on='ID',how='left')
ix = np.invert(pd.isnull(data['classrrhads']))
data['cl'][ix] = data['classrrhads'][ix]
del data['classrrhads']


## merge eclipsing binary sources
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

############Standardizing naming###############
print "standardizing classification names . . ."
#if you want to rename anything, just write what it's called and what you want to replace it with

#eg.
#data['temp_cl'].loc[data['cl']=='what it is called']='what you want to call it'

data['temp_cl'] = ''
data['temp_cl'].loc[data['cl']=='unknown']='unknown'
data['temp_cl'].loc[data['cl']=='QSO']='QSO' #variable quasars
data['temp_cl'].loc[data['cl']=='del_scu']='del_scu' #delta scuti variables
data['temp_cl'].loc[data['cl']=='EC']='EC' #Contact binaries in ASAS-3
data['temp_cl'].loc[data['cl']=='ED']='ED' #Detached eclipsing binaries
data['temp_cl'].loc[data['cl']=='ESD']='ESD' #Semi-detached eclipsing binaries
data['temp_cl'].loc[data['cl']=='EC/ESD']='EC/ESD'
data['temp_cl'].loc[data['cl']=='ESD/ED']='ESD/ED'
data['temp_cl'].loc[data['cl']=='EC*']='EC*'
data['temp_cl'].loc[data['cl']=='ED*']='ED*'
data['temp_cl'].loc[data['cl']=='mult']='mult'
data['temp_cl'].loc[data['cl']=='ew']='ew' #W Ursae Majoris-type eclipsing variables
data['temp_cl'].loc[data['cl']=='ea']='ea' #beta Persei-type (Algol) eclipsing systems
data['temp_cl'].loc[data['cl']=='eb']='eb' #beta Lyrae-type eclipsing systems
data['temp_cl'].loc[data['cl']=='rr_ab']='rr_ab' #RR Lyrae variables with asymmetric light curves
data['temp_cl'].loc[data['cl']=='rr_c']='rr_c' #RR Lyrae variables with nearly symmetric
data['temp_cl'].loc[data['cl']=='rr_d']='rr_d' #Double-mode RR Lyrae stars which pulsate...
data['temp_cl'].loc[data['cl']=='bl']='bl' #RR Lyrae stars showing the Blazhko effect.
data['temp_cl'].loc[data['cl']=='rs']='rs' #non-eclipsing RS CVn stars
data['temp_cl'].loc[data['cl']=='acep']='acep' #Anomalous Cepheids
data['temp_cl'].loc[data['cl']=='cep-ii']='cep-ii' ####need to confirm which star this is...
data['temp_cl'].loc[data['cl']=='hads']='hads' #High Amplitude delta Scuti stars
data['temp_cl'].loc[data['cl']=='lads']='lads' #low-amplitude delta Scuti stars
data['temp_cl'].loc[data['cl']=='lpv']='lpv' #Long Period Variables 
data['temp_cl'].loc[data['cl']=='ell']='ell' #ellipsoidal binary system
data['temp_cl'].loc[data['cl']=='hump']='hump' #LPV Humps
data['temp_cl'].loc[data['cl']=='pceb']='pceb' #post common envelope binary planetary system
data['temp_cl'].loc[data['cl']=='ea_up']='ea_up' 
data['temp_cl'].loc[data['cl']=='RRAB']='rr_ab' #RR Lyrae variables with asymmetric light curves
data['temp_cl'].loc[data['cl']=='RRmf']='rr_mf'
data['temp_cl'].loc[data['cl']=='RRC']='rr_c' #RR Lyrae variables with nearly symmetric
data['temp_cl'].loc[data['cl']=='RRdm']='rr_dm' #Detached main-sequence systems?
data['temp_cl'].loc[data['cl']=='RRu']='rr_u'

data['cl'] = data['temp_cl']
del data['temp_cl']

## output catalog
print "writing catalog . . ."
data.to_csv(outfile,sep=" ",index=False)
