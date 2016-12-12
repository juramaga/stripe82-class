## makes the challenge
## tested on python 2.7

import shutil
import os
import numpy as np
import pandas as pd


d = "challenge" ## name of folder to put challenge files
f = "challenge-docs" ## name of folder with challenge readme, example, etc


#### STEP 1: REMOVE AND CREATE directory for challenge
if os.path.exists(d):
    shutil.rmtree(d)

os.makedirs(d)
os.makedirs(d + "/train")
os.makedirs(d + "/test")


#### STEP 2: MOVE files into challenge directory
fs = os.listdir(f)
for fn in fs:
    shutil.copy(f + "/" + fn,d)


#### STEP 3: load catalog, create training / test sets
####         downsample light curves, , etc.
data = pd.read_table("catalog.txt",sep=" ")


######## obtain set of training rows
## divide data into training and test
## select Nrr RRL and Nq quasars
Nrr = 200
Nq = 500
qso = np.random.permutation(data[data['cl'] == "QSO"].index.tolist())
qso_train = qso[:Nq] ## random select Nq qsos for training
qso_test = qso[Nq:] ## rest are test
rr = np.random.permutation(data[data['cl'].str.contains("rr")].index.tolist())
rr_train = rr[:Nrr] ## random select Nrr rr for training
rr_test = rr[Nrr:] ## rest are test
unknown_test = data[data['cl'] == "unknown"].index.tolist() ## all unknowns are test
train = data.loc[np.concatenate((qso_train,rr_train)),["ID","cl"]]
test = data.loc[np.concatenate((qso_test,rr_test,unknown_test)),["ID","cl"]]


## load, downsample, and move all lcs in train, test
## write train, test data frames out
## should probably compute features in a different file


#### files and folders in challenge/
### train/
###  - light curves for training data
### test/
###  - light curves for test data
### train.txt
###  - matrix with column for ids (match to train files) classifications, and maybe features
### test.txt
###  - matrix with column for ids (match to test files) and features
### test_classes.txt
###  - matrix with column for ids (match to test files) and test classes
### all other files from challenge-doc


