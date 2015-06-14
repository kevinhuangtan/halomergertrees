import os
import numpy as np
import h5py
DEPTH_ID_COL = 28
Z_COL = 19


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

#Z - 19
def generalized_property_derivative(column, z, dz, haloID, hdf5_file):
    """inputs: colum, input value, fraction, haloId, hdf5_file"""
   
    trunk_mask = getTrunk(haloID, hdf5_file) #get trunk

    table = getTable(haloID, hdf5_file) #get table

    masked_table = table[trunk_mask] #filter table with mask

    # find z
    i = 0
    found_z = False
    while(i < len(trunk_mask) - 1):
        if (abs(masked_table[i][Z_COL] - z) <= .01 ):
            found_z = True
            break
        i+=1
    z_index = i
    z_value = masked_table[i][Z_COL]


    #find index at dz
    found_dz = False
    if (found_z):
        while(i > 0):
            i-=1
            delta_z = abs(masked_table[i][Z_COL] - z_value) 
            if (abs(delta_z - dz) <= .01 ):
                found_dz = True
                break
        dz_index = i
        dz_value = masked_table[i][Z_COL]

    if(found_z and found_dz):
        print 'z index', z_index
        print 'dz index', dz_index
        # print 'scale factor', masked_table[i][0]
        # print 'id', masked_table[i][1]
        print 'z value', masked_table[z_index][Z_COL]
        print 'dz value', masked_table[dz_indexge][Z_COL]
    else:
        if(not found_z):
            print 'did not find z'
        else:
            print 'did not find dz'
    



# def smooth_accretion(haloID, hdf5_file):
#     