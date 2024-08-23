# -*- coding: utf-8 -*-
"""
Created on June 7 2024
Last edit 16 Aug 2024
@author: tim@footprintlab.io

Takes Supply Use (SU) formatted input-output tables:
T - Transaction
V - Primary inputs
Y - Final demand
TQ - Satellite data under the T table

returns 'symmetric' (IOT) formatted input-output tables
for an IO analysis or SPA on IOT tables

Assumes that these are MRIO without imports

TODO
Set up a boolean import_table = TRUE that specifies what to do
with a Single Region SU set of base tables with a block of import data

"""

import numpy as np
import os

'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
PATHS AND GLOBALS
'''
print("Setting Paths and Globals")
print("")


DATAPATH = 'data'

# Define regional and sectoral extents
# a 'sector' here is a member of a list used to describe both industries and products
# which is generally how it's done in IELab data though not in the SPA toy example ...
# so, there's a need to generalise the following to allow for SU formatted tables with
# quadrants of different extents as in the example from Wiedmann (2017)

countries = 2
sectors = 4

#e.g. for GLORIA
#countries = 164
#sectors = 120

# May be needed later for sourcing/ using IELab files
#Phase = '002'
#Loop = '059'


'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DATA
'''
print("Reading in Base Tables")
print("")


# NOTE the code that follows works with 2D V and Y files that are the usual
# dimensions of raw data from IELab, but erroneous results transpire when
# the V and Y data is 1D as in the tutorial example. Similarly for TQ
# An additional zero row was added to V and TQ, and additional zero column to Y files


# e.g. of input base tables from GLORIA
# T = np.genfromtxt(DATAPATH + '20240110_120secMother_AllCountries_002_T-Results_2022_059_Markup001(full).csv', delimiter=",", dtype=float)
# V = np.genfromtxt(DATAPATH + '20240110_120secMother_AllCountries_002_V-Results_2022_059_Markup001(full).csv', delimiter=",", dtype=float)
# Y = np.genfromtxt(DATAPATH + '20240110_120secMother_AllCountries_002_Y-Results_2022_059_Markup001(full).csv', delimiter=",", dtype=float)
# TQ = np.genfromtxt(DATAPATH + '20231117_120secMother_AllCountries_002_TQ-Results_2022_059_Markup001(full).csv', delimiter=",", dtype=float)





def make_iot_tables(transaction_table,V,Y,TQ):

    total_output = np.sum(transaction_table, axis=0, keepdims=True) + np.sum(V, axis=0, keepdims=True)
    technical_coefficient = transaction_table/total_output

    #select only Commodity block rows and colunms
    commodity_rows = [(c * 2 + 1) * sectors + sr for sr in list(range(sectors)) for c in list(range(countries))]
    commodity_rows.sort()

    commodity_columns = [c * 2 * sectors + sr for sr in list(range(sectors)) for c in list(range(countries))]
    commodity_columns.sort()

    B = technical_coefficient.take(commodity_rows, axis=0)

    supply_rows = [c * 2 * sectors + sr for sr in list(range(0,sectors)) for c in list(range(0,countries))]
    supply_rows.sort()

    supply_columns = [(c * 2 +1) * sectors + sr for sr in list(range(0,sectors)) for c in list(range(0,countries))]
    supply_columns.sort()

    D = technical_coefficient.take(supply_rows, axis=0)
    
    Aq = np.dot(B,D)

    xt = Aq.shape[1]
    identity = np.identity(xt) 
    L = np.linalg.inv(identity-Aq)
    DL =  np.dot(D,L)


    Xr = total_output.take(commodity_columns) # for industry output X.take(supply_columns)),axis=0)
    Yr = Y.take(commodity_rows, axis=0)
    TQr = TQ.take(commodity_columns, axis=1)
    # TQr=TQr[[3168,5943]] .. for GLORIA this further selects the two impact rows with total CO2-eq emissions (from EDGAR and OECD respectively)
    Ar = I - np.linalg.inv(DL)
    Tr = Ar * Xr
    
    return Tr,Yr,TQr








print("Made DL")
print()

print(Tr)


print("Made T IOT")

print()
print ("----Finished ----")