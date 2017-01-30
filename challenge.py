## makes the challenge
## tested on python 2.7

import shutil
import os
import numpy as np
import pandas as pd

np.random.seed(2017)

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
data = pd.read_table("catalog.txt",sep=" ")


## move all objects of class unknown to test
x = data[data['cl']=="unknown"]["ID"]
f = "data/AllLCs"
for ii in x:
    fname = "LC_" + str(ii) + ".dat"
    shutil.copy(f + "/" + fname,d + "/test")


## select p proportion of each class for training
## ids contains ids for training
p = 1.0/2.0
x = data[data['cl']!="unknown"]
classes = np.unique(x['cl'])
ids = np.array([],dtype="int64")
for ii in classes:
    n = np.sum(x['cl']==ii)
    num = np.random.binomial(n=n,p=p)
    ids = np.append(ids,x[x['cl']==ii]['ID'].sample(num))


## copy all training light curves into training folder
f = "data/AllLCs"
for ii in ids:
    fname = "LC_" + str(ii) + ".dat"
    shutil.copy(f + "/" + fname,d + "/train")

## copy all test light curves into test folder
x = data[data['cl']=="unknown"]["ID"]
test = np.setdiff1d(np.setdiff1d(data['ID'],ids),x) ## non-unknown, non-train
f = "data/AllLCs"
for ii in test:
    fname = "LC_" + str(ii) + ".dat"
    shutil.copy(f + "/" + fname,d + "/test")


## make train, test catalogs, output


data_train = data[np.in1d(data["ID"],ids)]
data_test = data[np.invert(np.in1d(data["ID"],ids))]

data_train.to_csv("challenge/train_classifications.txt",index=False)
data_test.to_csv("test_classifications.txt",index=False) ## not written to challenge folder



##shutil.make_archive(d,"gztar",d)
