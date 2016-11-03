## downloads all data necessary for creating catalog
## by James Long

import urllib2
import os
import shutil

d = "data" ## name of folder to store data files


#### STEP 1: REMOVE AND CREATE DATA FOLDER

if os.path.exists(d):
    shutil.rmtree(d)

os.makedirs(d)


#### STEP 2: DOWNLOAD SDSS STRIPE 82 CATALOG AND LIGHTCURVES
## only has quasar classifications
## lightcurves only necessary for visualizing data / checking classifications

## http://www.astro.washington.edu/users/ivezic/sdss/catalogs/S82variables.html
##http://www.astro.washington.edu/users/ivezic/sdss/catalogs/stripe82candidateVar_v1.1.dat.gz


#### STEP 3: DOWNLOAD CLASSIFICATIONS ASSIGNED IN VARIOUS WORKS
## urls    : location of class files
## fnames  : list of files names to store different classifications
fnames = ["rrlyrae.txt",
          "eclipsing_binary.txt"]
urls = ["http://iopscience.iop.org/0004-637X/708/1/717/suppdata/apj326724t2_mrt.txt",
        "http://iopscience.iop.org/0004-637X/731/1/17/suppdata/apj383813t2_ascii.txt"]
for ii in range(len(fnames)):
    print "downloading from: " + urls[ii]
    print "storing in: " + d + "/" + fnames[ii]
    response = urllib2.urlopen(urls[ii])
    html = response.read()
    f = open(d + "/" + fnames[ii], 'w')
    f.write(html)
    f.close()


