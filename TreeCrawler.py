import os
import numpy as np
import h5py
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline
LAST_MAINLEAF_DEPTHFIRST_ID = 34
DEPTH_FIRST_ID = 28
SCALE = 0
NEXT_COPROGENITOR_DEPTHFIRST_ID = 32
MVIR = 10
ID = 1 


def plotArray(array1, array2):
    # print array1
    
    spline = InterpolatedUnivariateSpline(array1, array2)

    xs = np.linspace(0, 1.001, 1000)
    plt.plot(xs, spline(xs))
    plt.show()
    return


def getTrunkTable(haloID, hdf5_file):
    with h5py.File(hdf5_file, "r") as f:
        last_mainleaf = int(f[str(haloID)][0][LAST_MAINLEAF_DEPTHFIRST_ID])
        root = int(f[str(haloID)][0][DEPTH_FIRST_ID])
        length = last_mainleaf - root
        trunk = f[str(haloID)][0: (length + 1)]
    return trunk

#3061006267

def print_trunk_column(column, haloID, hdf5_file):
    """print values of a given column of a tree's trunk"""

    masked_table = getTrunkTable(haloID, hdf5_file)

    #print column
    for i in range(0, len(masked_table)): #O(1) for length function in any python object
        print masked_table[i][column]
    return masked_table[column]

#mass - (10)
def generalized_formation_time(column, input_value, fraction, haloID, hdf5_file):
    """inputs: colum, input value, fraction, haloId, hdf5_file"""

    masked_table = getTrunkTable(haloID, hdf5_file)
    formation_value = 2.7e13

    i = 0
    while(masked_table[i][column] > formation_value):
        i+=1
    return masked_table[i]

def generalized_property_derivative(column, z, dz, haloID, hdf5_file):
    """Solve for generalized property derivative at a given z

    Parameters 
    ----------
    column, z, dz, haloID, hdf5 filename

    Returns 
    -------
    Generalized Property Derivative (column(z1) - column(z0))/(z1-z0)
    """

    masked_table = getTrunkTable(haloID, hdf5_file)

    spline = InterpolatedUnivariateSpline(list(reversed(masked_table['scale'])), list(reversed(masked_table[column])))
    col_z = spline(z)
    col_dz = spline((z + dz)) #should dz go into future or past?

    generalized_derivative = (col_dz - col_z)/(dz)

    xs = np.linspace(0, 1.001, 1000)
    plt.plot(xs, spline(xs))
    plt.show()
    return generalized_derivative

def clumpy_accretion(haloID, hdf5_file):
    with h5py.File(hdf5_file, "r") as f:
        table = f[str(haloID)][...]
    trunk_table = getTrunkTable(haloID, hdf5_file)
    clumpy_array = []
    id_array = list(table['haloid_depth_first'])

    for i in range(0, len(trunk_table) - 1):
        clumpy = trunk_table[i + 1][MVIR]
        coprogenitor = table[i + 1][NEXT_COPROGENITOR_DEPTHFIRST_ID]
        while(coprogenitor != -1.0):
            index_coprogenitor = id_array.index(coprogenitor)
            clumpy += table[index_coprogenitor][MVIR]
            coprogenitor = table[index_coprogenitor][NEXT_COPROGENITOR_DEPTHFIRST_ID]
        clumpy_array.append(clumpy)


    #plot
    array_z = list(reversed(trunk_table['scale']))
    array_z = array_z[:(len(array_z) - 1)]
    plotArray(array_z, list(reversed(clumpy_array)))
    return clumpy_array


def smooth_accretion(haloID, hdf5_file):
    trunk_table = getTrunkTable(haloID, hdf5_file)
    M_0 = trunk_table[0][MVIR]
    smooth_array = []
    clumpy_array = clumpy_accretion(haloID, hdf5_file)

    for i in range(0, len(trunk_table) - 2):
        smooth = trunk_table[i][MVIR] - clumpy_array[i + 1]
        smooth_array.append(smooth) 

    z_array = list(reversed(trunk_table['scale']))
    z_array = z_array[:(len(z_array) - 2)]
    plotArray(z_array, list(reversed(smooth_array)))
    return smooth_array





    