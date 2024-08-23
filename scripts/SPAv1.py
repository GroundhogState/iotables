# -*- coding: utf-8 -*-
"""
Created on Aug 12 2024
Last edit Aug 12 2024
@author: tim@footprintlab.io

Takes a single row of DIMS derived from a satellite account M, q
that may be expected to come from the method of IOanalysis.py:
ioanalysis(T,X,Y,M,phase='',loop='',year='',outputPath='').

This also returns A and TIMs. A and q may then be used in the 
following formula, which relates to paths in a structural path
analysis (SPA)

        q(I - A)^-1 = q + qA + qA^2 + qA^3

production layer ...  1 ...2  ...3  ...4

"""

import pandas as pd
import numpy as np
import os
import old.IOanalysis as IO
import csv



'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CONTENTS

* PATHS AND GLOBALS
* METHODS

'''



'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
PATHS AND GLOBALS
'''
print("")
print("Setting Paths and Globals")
print("")

# NB some of these path setting will become redundant or put into inputParams.csv
PATH = os.path.dirname(os.path.abspath(__file__))
DATAPATH = os.path.join(os.path.expanduser('~'),'Documents','FootPrintLab','IELab','Decomposition') + os.sep

'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
METHODS
'''

#### SINGLE SU I as in ECE  ###############################
#     IELAB Portal standard outputs with imports          #
#                                                         #
#                                                         #
# Single region SU table with TQ and imports treated as in
# ECE model: imports used to calculate total output, X but
# ROW not included as column, nor Imports as row, in L

def method_SingleSUI_NoImports(T, data_V, data_Y, data_TQ):
    print("Single Region SU IOA No Imports in Total Inputs, X")

    
    # create row vector of Primary Inputs
    V = data_V #[:,:industry_product_ext].sum(axis=0, keepdims=True)
    print("     Loaded Total V. Shape is: ", V.shape)   

    Y = data_Y #[:industry_product_ext,:].sum(axis=1, keepdims=True)    
    print("     Loaded Total Final Demand, Y. Shape is: ", Y.shape)

    print("     X. Shape is: ", X.shape)
    
    M = data_TQ #[:,:industry_product_ext]
    
    X = sum([np.sum(T, axis=0, keepdims=True), V]) #row vector

    print("     Loaded Satellite data for total GHG. Shape is:", M.shape)
    print("END of pre-processing")
    print("")
    
    return V, Y, X, M


def ioanalysis(transaction_table,X,final_demand,M):
    ''''
    expects numpy arrays: T with extents, (xt, xt)
    that is the same as vectors for Final Demand, Y (xt,1) and
    Primary inputs, V (1, xt) and also one dimenion of a table of
    direct material inputs, M (m, xt). X is assumed to be a row
    vector (1, xt)
    
    All inputs must be fully enumerated (no NaN or text)

    If a non-empty outputs path is specified, results are 
    exported as CSV files, otherwise numpy tables are returned.

    '''
    
    xt = X.shape[1]

    I = np.identity(xt)  
    technical_coefficient = transaction_table/X
    L = np.linalg.inv(I-technical_coefficient)  
    
    direct_intensity_multiplier = M/X
    total_intensity_multiplier = np.transpose(np.dot(direct_intensity_multiplier,L))

    #? name ? Need it for anything?
    FP = total_intensity_multiplier * final_demand
    
    return technical_coefficient,direct_intensity_multiplier,total_intensity_multiplier


inputPath = DATAPATH
Year = ""
filenameRoot =""

# labels aren't used other than to compute an extent
# which is the size of Y in the end
# Y is final demand so just the length of sectors
# so can just (temporarily) use Y as the source
labels = np.genfromtxt(DATAPATH + 'Labels.txt', dtype=str)
industry_product_ext = len(labels)
droot = 'data/gloria'
T  = np.genfromtxt(os.path.join(droot,'T.csv'), delimiter=",", dtype=float) # + str(Year) +'_' + str(Loop) + '_' + margin + '.csv'
print("     Loaded Table T data. Shape is: ", T.shape)
data_V  = np.genfromtxt(os.path.join(droot,'V.csv'), delimiter=",", dtype=float)  # + str(Year) +'_' + str(Loop) + '_' + margin + '.csv'
print("     Loaded Table V data. Shape is: ", data_V.shape)
data_Y = np.genfromtxt(os.path.join(droot,'Y.csv'), delimiter=",", dtype=float) # + str(Year) +'_' + str(Loop) + '_' + margin + '.csv'
# assert data_Y.shape[0] == industry_product_ext, "Y has wrong shape"   
print("     Loaded Table Y data. Shape is: ", data_Y.shape)
data_TQ = np.genfromtxt(os.path.join(droot,'TQ.csv'), delimiter=",", dtype=float) #  + str(Year) +'_' + str(Loop) + '_' + margin + '.csv'
print("     Loaded Satellite Data. Shape is:", data_TQ.shape)


# Prepare ingested single region SU format IELab data for input-output analysis 
V, Y, X, M = method_SingleSUI_NoImports(T, data_V, data_Y, data_TQ)
# run input-output analysis and export tables to csv files

A, DIMS, TIMS = ioanalysis(T,X,Y,M)


