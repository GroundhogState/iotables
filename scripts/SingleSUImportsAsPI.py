
'''
Created on Dec 18 2023
@author: tim@footprintlab.io

Takes input on IELab SU formatted tables that
represent a single region, with imports considered
as Primary Inputs. Parameters assume IELab naming
conventions:

T, V, Y, TQ, Phase, Loop

and extent of sector list xt, imports and exports,
are assumed to have been obtained beforehand

Rows 6 to 8 inclusive of the Satellite data are taken for further
EEIO analysis

'''
import numpy as np
import pandas as pd

#### SINGLE SU I as in ECE  ###############################
#     IELAB Portal standard outputs with imports          #
#                                                         #
#                                                         #
# Single region SU table with TQ and imports treated as in
# ECE model: imports used to calculate total output, X but
# ROW not included as column, nor Imports as row, in L

def method_SingleSUImportsAsPI(T, imports, exports, data_V, data_Y, data_TQ, xt):
    print("Single Region SU IOA including Imports in Total Inputs, X")
    print("     Loaded Imports. Shape is: ", imports.shape)
    print("     Loaded Exports. Shape is: ", exports.shape)
    print("     Loaded T Table. Shape is: ", T.shape)

    importsTotal = imports[:,:(2*xt)].sum(axis=0, keepdims=True)
    print("     Total Imports. Shape is: ", importsTotal.shape)    

    
    # create row vector of Primary Inputs
    V = data_V[:,:(2*xt)].sum(axis=0, keepdims=True)
    print("     Loaded Total V. Shape is: ", V.shape)  
    

    Y = data_Y[:(2*xt),:].sum(axis=1, keepdims=True)    
    print("     Loaded Total Final Demand, Y. Shape is: ", Y.shape)

    X = sum([np.sum(T, axis=0, keepdims=True), V, importsTotal]) #row vector
    print("     X. Shape is: ", X.shape)
    
    M = data_TQ[:,:(2*xt)]
    print("     Loaded Satellite data for total GHG. Shape is:", M.shape)
    print("END of pre-processing")
    print("")
    
    return V, Y, X, M



