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


#### STEP 2: MOVE files into challenge directory
fs = os.listdir(f)
for fn in fs:
    shutil.copy(f + "/" + fn,d)


#### STEP 3: load catalog, create training / test sets
####         downsample light curves, , etc.
data = pd.read_table("catalog.txt",sep=" ")


######## obtain set of training rows
## divide data into training and test
## select 200 RRL and 500 quasars
to_use = data['cl'] == "QSO"


qsos = data[data['cl'] == "QSO"].index.tolist()
## maybe this function: scipy.stats.rv_discrete



np.arange(data.shape[0])*to_use


dim(data)
np.sum(to_use)




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


