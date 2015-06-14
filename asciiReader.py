import os
import numpy as np
import h5py


class RockstarReader(object):

    def __init__(self, filename, hdf5_name):
        """
        RockstarReader(filename)
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
                            f[tree_id] = np.array(current_tree)
                            current_tree = []
                            tree_index += 1
                        else:
                            tree_index += 1
                        first_line = False
                        tree_id = line[6:].strip('\n')
                    else: #read in next tree element
                        current_tree.append(line.split())
                f[tree_id] = np.array(current_tree).astype('f8')
                
        return 
            
    def _uncompress_ascii(self):
        if self.fname[-3:]=='.gz':
            print("...uncompressing ASCII data")
            os.system("gunzip "+self.fname)
            self.fname = self.fname[:-3]
        else:
            pass
        return
