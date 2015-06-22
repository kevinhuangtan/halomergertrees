import os
import numpy as np
import h5py
DEPTH_FIRST_ID = 28
LAST_MAINLEAF_DEPTHFIRST_ID = 34

dt = np.dtype([
    ('scale', 'f4'), 
    ('haloid', 'i8'), 
    ('scale_desc', 'f4'), 
    ('haloid_desc', 'i8'), 
    ('num_prog', 'i4'), 
    ('pid', 'i8'), 
    ('upid', 'i8'), 
    ('pid_desc', 'i8'), 
    ('phantom', 'i4'), 
    ('mvir_sam', 'f4'), 
    ('mvir', 'f4'), 
    ('rvir', 'f4'), 
    ('rs', 'f4'), 
    ('vrms', 'f4'), 
    ('mmp', 'i4'), 
    ('scale_lastmm', 'f4'), 
    ('vmax', 'f4'), 
    ('x', 'f4'), 
    ('y', 'f4'), 
    ('z', 'f4'), 
    ('vx', 'f4'), 
    ('vy', 'f4'), 
    ('vz', 'f4'), 
    ('jx', 'f4'), 
    ('jy', 'f4'), 
    ('jz', 'f4'), 
    ('spin', 'f4'), 
    ('haloid_breadth_first', 'i8'), 
    ('haloid_depth_first', 'i8'), 
    ('haloid_tree_root', 'i8'), 
    ('haloid_orig', 'i8'), 
    ('snap_num', 'i4'), 
    ('haloid_next_coprog_depthfirst', 'i8'), 
    ('haloid_last_prog_depthfirst', 'i8'), 
    ('haloid_last_mainleaf_depthfirst', 'i8'), 
    ('rs_klypin', 'f4'), 
    ('mvir_all', 'f4'), 
    ('m200b', 'f4'), 
    ('m200c', 'f4'), 
    ('m500c', 'f4'), 
    ('m2500c', 'f4'), 
    ('xoff', 'f4'), 
    ('voff', 'f4'), 
    ('spin_bullock', 'f4'), 
    ('b_to_a', 'f4'), 
    ('c_to_a', 'f4'), 
    ('axisA_x', 'f4'), 
    ('axisA_y', 'f4'), 
    ('axisA_z', 'f4'), 
    ('b_to_a_500c', 'f4'), 
    ('c_to_a_500c', 'f4'), 
    ('axisA_x_500c', 'f4'), 
    ('axisA_y_500c', 'f4'), 
    ('axisA_z_500c', 'f4'), 
    ('t_by_u', 'f4'), 
    ('mass_pe_behroozi', 'f4'), 
    ('mass_pe_diemer', 'f4')
    ])

class RockstarReader(object):

    def __init__(self, filename, hdf5_name):
        """A class that reads an ASCII merger tree and stores its header and tree data. Writes data to hdf5 file. 

        Parameters 
        ----------
        ASCII file name, hdf5 file name

        Returns 
        -------
        writes to hdf5 file
        """
        if not os.path.isfile(filename):
            raise IOError("Input filename %s is not a file" % filename)
        # self.f = h5py.File('myReaderAppend.hdf5', 'w')  
        self.fname = filename
        self.hdf5_name = hdf5_name + '.hdf5'
        self._uncompress_ascii()
        self.get_header()
        self.read_in_trees()

    def get_header(self):
        """ Finds header rows in ASCII File and stores them in hdf5 group "ascii_header"
        """
        with h5py.File(self.hdf5_name,"w") as f: #write new hdf5
            header = {}
            h5_header = f.create_group('ascii_header')
            with open(self.fname) as ascii_file:
                header['comments'] = []
                for i, line in enumerate(ascii_file):
                    header['comments'].append(line)
                    #create categories from first line
                    if(i==0):
                        header['columns'] = line.split()
                    if(line[0]!='#'):
                        h5_header.attrs['length'] = i
                        break
            h5_header['columns'] = np.asarray(header['columns'])
            h5_header['comments'] = header['comments']
        return

    def read_in_trees(self):
        """Store each tree in its own hdf5 dataset. Tree is sorted by Depth First ID for fast access to trunk
        """
        with h5py.File(self.hdf5_name,"r+") as f:
            tree_id = ""
            with open(self.fname) as ascii_file:
                 #skip header lines
                for _ in xrange(f['ascii_header'].attrs['length']):
                    next(ascii_file)    

                f['ascii_header/numtrees'] = next(ascii_file)
                tree_index = 0
                first_line = True
                current_tree = []
                for line in ascii_file:
                    if(line[0]=='#'): #new tree
                        if(not first_line): #not first tree
                            arr = np.array(current_tree, dtype = dt)
                            depth_sort =  arr['haloid_depth_first'].argsort() #sort by depthid
                            f[tree_id] = arr[depth_sort] 
                            current_tree = []
                            tree_index += 1
                        else:
                            tree_index += 1
                        first_line = False
                        tree_id = line[6:].strip('\n')
                    else: #read in next tree element
                        current_tree.append(tuple(line.split()))
                arr = np.array(current_tree, dtype = dt)
                depth_sort =  arr['haloid_depth_first'].argsort()
                f[tree_id] = arr[depth_sort]

        return 
            
    def _uncompress_ascii(self):
        if self.fname[-3:]=='.gz':
            print("...uncompressing ASCII data")
            os.system("gunzip "+self.fname)
            self.fname = self.fname[:-3]
        else:
            pass
        return
