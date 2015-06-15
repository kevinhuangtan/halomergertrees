import os
import numpy as np
import h5py
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline
DEPTH_ID_COL = 28
Z_COL = 0


def getTrunk(haloID, hdf5_file):
    """return list of id's of tree's trunk"""
    mask = []
    with h5py.File(hdf5_file, "r") as f:
        tree = f[str(haloID)]
        depth_id = tree[0][DEPTH_ID_COL] #first
        for i in range(0,len(tree)):
            if(tree[i][DEPTH_ID_COL] == (depth_id + 1)):# next in depth search
                mask.append(i)
                depth_id+=1
    return mask

def getTable(haloID, hdf5_file):
    with h5py.File(hdf5_file, "r") as f:
        table = f[str(haloID)][...]
    return table

def print_trunk_column(column, haloID, hdf5_file):
    """print values of a given column of a tree's trunk"""

    trunk_mask = getTrunk(haloID, hdf5_file) #get trunk

    table = getTable(haloID, hdf5_file) #get table

    masked_table = table[trunk_mask] #filter table with mask

    #print column
    for i in range(0, len(trunk_mask)):
        print masked_table[i][column]

#mass - (10)
def generalized_formation_time(column, input_value, fraction, haloID, hdf5_file):
    """inputs: colum, input value, fraction, haloId, hdf5_file"""

    trunk_mask = getTrunk(haloID, hdf5_file) #get trunk
    
    formation_time = input_value * fraction #formation time

    table = getTable(haloID, hdf5_file) #get table

    #filter table with mask
    masked_table = table[trunk_mask]

    # find when reaches formation time
    i = 0
    while(masked_table[i][column] > formation_time):
        i+=1

    print i
    print 'scale factor', masked_table[i][0]
    print 'id', masked_table[i][1]
    print 'formation time', masked_table[i][column]
    return

def generalized_property_derivative(column, z, dz, haloID, hdf5_file):
    """inputs: colum, input value, fraction, haloId, hdf5_file"""
   
    trunk_mask = getTrunk(haloID, hdf5_file) #get trunk

    table = getTable(haloID, hdf5_file) #get table

    masked_table = table[trunk_mask] #filter table with mask

    print masked_table[:, Z_COL]
    print masked_table[:, column]

    spline = InterpolatedUnivariateSpline(list(reversed(masked_table[:, Z_COL])), list(reversed(masked_table[:,column])))
    col_z = spline(z)
    col_dz = spline((z+dz))

    generalized_derivative = (col_dz - col_z)/(dz)
    return generalized_derivative





# def smooth_accretion(haloID, hdf5_file):
#     