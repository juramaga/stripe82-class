## downloads all data necessary for creating catalog
## by James Long
import urllib
import os
import zipfile

d = "data" ## name of folder to store data files

#### STEP 1: REMOVE AND CREATE DATA FOLDER
if os.path.exists(d):
    shutil.rmtree(d)

os.makedirs(d)

#### STEP 2: DOWNLOAD SDSS STRIPE 82 CATALOG AND LIGHTCURVES
## only has quasar classifications
## lightcurves only necessary for visualizing data / checking classifications
## ::: usually hosted at :::
## http://www.astro.washington.edu/users/ivezic/sdss/catalogs/S82variables.html
## http://www.astro.washington.edu/users/ivezic/sdss/catalogs/stripe82candidateVar_v1.1.dat.gz
## ::: but currently these servers are down so downloading from james long's website :::
url = "http://www.stat.tamu.edu/~jlong/"
fnames = ["apj326724t2_mrt.zip","AllLCs.zip"]
for fname in fnames:
    print "downloading " + fname + ". . ."
    urllib.urlretrieve(url + fname, d + '/' + fname)
    zip_ref = zipfile.ZipFile(d + '/' + fname, 'r')
    zip_ref.extractall(d)
    zip_ref.close()

#### STEP 3: DOWNLOAD CLASSIFICATIONS ASSIGNED IN VARIOUS WORKS
## urls    : location of class files
## fnames  : list of files names to store different classifications
##
## we will extend these list as we collect classifications from more sources
fnames = ["rrlyrae.txt",
          "eclipsing_binary.txt"]
urls = ["http://iopscience.iop.org/0004-637X/708/1/717/suppdata/apj326724t2_mrt.txt",
        "http://iopscience.iop.org/0004-637X/731/1/17/suppdata/apj383813t2_ascii.txt"]
for ii in range(len(fnames)):
    url = urls[ii] + fnames[ii]
    fname = d + "/" + fnames[ii]
    print "downloading from: " + url + ",  storing in:" + fname
    urllib.urlretrieve(url,fname)
