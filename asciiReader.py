import os
import numpy as np
import h5py
DEPTH_FIRST_ID = 28
LAST_MAINLEAF_DEPTHFIRST_ID = 34

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
                            arr = np.array(current_tree).astype('f8')
                            f[tree_id] = arr[arr[:, DEPTH_FIRST_ID].argsort()] #sort by depthid
                            f[tree_id].attrs['last_mainleaf'] = int(f[tree_id][0][LAST_MAINLEAF_DEPTHFIRST_ID]) #set last_mainleaf
                            current_tree = []
                            tree_index += 1
                        else:
                            tree_index += 1
                        first_line = False
                        tree_id = line[6:].strip('\n')
                    else: #read in next tree element
                        current_tree.append(line.split())
                arr = np.array(current_tree).astype('f8')
                f[tree_id] = arr[arr[:, DEPTH_FIRST_ID].argsort()]
                f[tree_id].attrs['last_mainleaf'] = int(f[tree_id][0][LAST_MAINLEAF_DEPTHFIRST_ID])

        return 
            
    def _uncompress_ascii(self):
        if self.fname[-3:]=='.gz':
            print("...uncompressing ASCII data")
            os.system("gunzip "+self.fname)
            self.fname = self.fname[:-3]
        else:
            pass
        return
