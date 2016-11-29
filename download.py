## downloads all data necessary for creating catalog
## by James Long
## tested on python 2.7

import urllib
import shutil
import os
import gzip
import tarfile

d = "data" ## name of folder to store data files
LCfolder = "AllLCs" ## subfolder within d where lightcurves files stored

#### STEP 1: REMOVE AND CREATE DATA FOLDER
if os.path.exists(d):
    shutil.rmtree(d)

os.makedirs(d)



#### STEP 2: DOWNLOAD SDSS STRIPE 82 CATALOG AND LIGHTCURVES
## only has quasar classifications
## lightcurves only necessary for visualizing data / checking classifications
url = "http://www.astro.washington.edu/users/ivezic/sdss/catalogs/"
## url = "http://www.stat.tamu.edu/~jlong/"   ## mirrored here, can try if above link is not working
## download and extract catalog
fname = "stripe82candidateVar_v1.1.dat.gz"
print "downloading " + fname + " . . ."
urllib.urlretrieve(url + fname, d + '/' + fname)
inF = gzip.open(d + '/' + fname, 'rb')
outF = open(d + '/stripe82candidateVar_v1.1.dat','wb')
outF.write(inF.read())
inF.close()
outF.close()
## download and extract lightcurves
fname = "AllLCs.tar.gz"
print "downloading " + fname + " . . ."
urllib.urlretrieve(url + fname, d + '/' + fname)
tar = tarfile.open(d + '/' + fname)
os.makedirs(d + '/' + LCfolder)
tar.extractall(d + '/' + LCfolder)
tar.close()


    
#### STEP 3: DOWNLOAD CLASSIFICATIONS ASSIGNED IN VARIOUS WORKS
## urls    : location of class files
## fnames  : list of files names to store different classifications
##
## extend this list as gather more sources with classifications
fnames = ["rrlyrae.txt",
          "eclipsing_binary.txt"]
urls = ["http://iopscience.iop.org/0004-637X/708/1/717/suppdata/apj326724t2_mrt.txt",
        "http://iopscience.iop.org/0004-637X/731/1/17/suppdata/apj383813t2_ascii.txt"]
for ii in range(len(fnames)):
    url = urls[ii]
    fname = d + "/" + fnames[ii]
    print "downloading from: " + url + ",  storing in:" + fname
    urllib.urlretrieve(url,fname)

