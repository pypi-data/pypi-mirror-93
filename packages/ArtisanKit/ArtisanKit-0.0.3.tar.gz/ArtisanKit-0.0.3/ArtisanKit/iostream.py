# For data carpenting and gardening

# Importing dependencies

import os 
import dask.dataframe as dd
import pickle as pkl

# mypath = '/home/user/rundir/workdir/result'
# filepattern = '.dat'
# myfilepaths= survey(mypath, filepattern)

def survey(path,filepattern):
# Survey all files under path directory
    filepaths_ALL = []
    #Path = "/home/user/rundir/workdir"
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if filepattern in filename:
                filepath = "{}/{}".format(dirpath,filename)
                filepaths_ALL.append(filepath)
    print("A total of ",len(filepaths_ALL),filepattern," files are detected")
    return filepaths_ALL
