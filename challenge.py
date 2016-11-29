## makes the challenge
## by James Long
## tested on python 2.7

import shutil
import os

d = "challenge" ## name of folder to put challenge files
f = "challenge-docs" ## name of folder with challenge readme, example, etc


#### STEP 1: REMOVE AND CREATE d
if os.path.exists(d):
    shutil.rmtree(d)

os.makedirs(d)

## copy these files to d
os.listdir(f)
