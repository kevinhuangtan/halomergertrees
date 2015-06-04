import os
import numpy as np
import h5py

a.f.close()

class RockstarReader(object):

    def __init__(self, filename):
        """
        RockstarReader(filename)
        """
        

        if not os.path.isfile(filename):
            raise IOError("Input filename %s is not a file" % filename)
        self.f = h5py.File('sample.hdf5', 'w')  
        self.fname = filename
        self._uncompress_ascii()
        self.get_header()
        self.forest = self.set_tree()

    def get_header(self):
        header = {}
        hd_header = self.f.create_group('header')
        with open(self.fname) as ascii_file:
            header['ascii_header'] = []
            for i, line in enumerate(ascii_file):
                header['ascii_header'].append(line)
                #create categories from first line
                if(i==0):
                    header['categories'] = line.split()
                if(line[0]!='#'):
                    hd_header.attrs['length'] = i
                    break
        hd_header['categories'] = np.asarray(header['categories'])
        hd_header['ascii_header'] = header['ascii_header']

    def set_tree(self):
        f = self.f
        with open(self.fname) as ascii_file:
            #skip header lines
            for x in xrange(f['header'].attrs['length']):
                next(ascii_file)

            forest = []
            tree = []
            #iterate through lines in file
            tree_root_ID = ""
            for line in ascii_file:
                if(line[0]=='#'): #new tree
                    forest.append(tree)
                    tree = []
                    tree_root_ID = line[6:]
                    curr_group = f.create_group("tree"+tree_root_ID)
                    curr_group.attrs['tree_root_ID'] = tree_root_ID
                tree.append(line)
                print line
            return forest
            # f['forest'] = forest

            
                
    def _uncompress_ascii(self):
        if self.fname[-3:]=='.gz':
            print("...uncompressing ASCII data")
            os.system("gunzip "+self.fname)
            self.fname = self.fname[:-3]
        else:
            pass
        return

a = RockstarReader('sample.txt')
